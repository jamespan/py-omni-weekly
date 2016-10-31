# coding=utf-8
from __future__ import print_function

import os
import sys
import time
from six.moves import configparser
import argparse
import datetime
import pytz
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
import frontmatter
import re

config = configparser.ConfigParser()

config_file = os.environ.get('OMNI_WEEKLY_CONFIG_FILE', False)
if config_file == os.devnull:
    config_file = False
if not config_file:
    user_dir = os.path.expanduser('~')
    if sys.platform.startswith('win') or (sys.platform == 'cli' and os.name == 'nt'):
        config_basename = 'omni-weekly.ini'
    else:
        config_basename = 'omni-weekly.conf'
    config_dir = os.path.join(user_dir, '.omni-weekly')
    config_file = os.path.join(config_dir, config_basename)
if os.path.exists(config_file) and os.path.isfile(config_file):
    with open(config_file, 'r') as f:
        config.readfp(f)

DEFAULT_DATABASE = '~/Library/Containers/com.omnigroup.OmniFocus2' \
                   '/Data/Library/Caches/com.omnigroup.OmniFocus2/OmniFocusDatabase2'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template', dest='template',
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template.jinja'),
                        help='absolute path of template file')
    parser.add_argument('-d', '--deadline-date', dest='deadline',
                        default=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
    parser.add_argument('-p', '--period-days', dest='period', default=7)
    parser.add_argument('-tz', '--timezone', default='Asia/Shanghai', dest='timezone')
    parser.add_argument('-db', '--database', dest='database', default=DEFAULT_DATABASE)
    args = parser.parse_args()

    args.template = os.path.expanduser(args.template)
    args.database = os.path.expanduser(args.database)

    if not os.path.exists(args.database):
        print('%s not exist, please check again' % args.database, file=sys.stderr)
        exit(1)
    if not os.path.isfile(args.database):
        print('%s is not a file, please check again' % args.database, file=sys.stderr)
        exit(1)
    with open(args.database, 'rx') as f:
        ima = f.read(16).encode('hex')
        if ima != '53514c69746520666f726d6174203300':
            print('%s is not a sqlite3 database, please check again' % args.database, file=sys.stderr)
            exit(1)

    Base = declarative_base()
    engine = create_engine('sqlite:///%s' % args.database)
    metadata = MetaData(bind=engine)

    class FloatDateTime(sqlalchemy.types.TypeDecorator):

        def __init__(self, timezone, *args, **kwargs):
            super(FloatDateTime, self).__init__(*args, **kwargs)
            self.timezone = timezone
            time.mktime(pytz.utc.localize(datetime.datetime(2001, 1, 1)).timetuple())
            self.osx_epoch_offset = int((pytz.utc.localize(datetime.datetime(2001, 1, 1))
                                         - datetime.datetime.fromtimestamp(0, tz=pytz.utc)).total_seconds())

        impl = sqlalchemy.types.Float

        def process_bind_param(self, value, dialect):
            return int(
                (value - datetime.datetime.fromtimestamp(0, tz=pytz.utc)).total_seconds()) - self.osx_epoch_offset

        def process_result_value(self, value, dialect):
            if value is not None:
                value = datetime.datetime.fromtimestamp(int(value) + self.osx_epoch_offset,
                                                        pytz.timezone(self.timezone))
            return value

    class Task(Base):
        __table__ = Table('Task', metadata,
                          Column('dateModified', FloatDateTime(args.timezone)),
                          Column('dateAdded', FloatDateTime(args.timezone)),
                          Column('dateCompleted', FloatDateTime(args.timezone)),
                          Column('effectiveDateToStart', FloatDateTime(args.timezone)),
                          Column('dateToStart', FloatDateTime(args.timezone)),
                          Column('effectiveDateDue', FloatDateTime(args.timezone)),
                          Column('dateDue', FloatDateTime(args.timezone)),
                          autoload=True)

    session = create_session(bind=engine)

    deadline = pytz.timezone(args.timezone).localize(
        datetime.datetime.strptime(args.deadline, '%Y-%m-%d')) + datetime.timedelta(days=1)

    tasks = session.query(Task).filter(
        or_(and_(Task.dateCompleted >= deadline - datetime.timedelta(days=args.period),
                 Task.dateCompleted < deadline),
            Task.dateCompleted.is_(None),
            Task.parent.is_(None))
    ).all()

    for task in tasks:
        if task.plainTextNote:
            post = frontmatter.loads(re.sub(u"—{1,3}", "---", task.plainTextNote))
            if 'issue' in post.metadata and post.metadata['issue'] is not None:
                issue = post.metadata['issue']
                post.metadata['issue'] = re.sub(r"\s+<.+>$", "", issue)
        else:
            post = frontmatter.loads("")
        # exclude content lines import from OmniPlan
        post.content = '\n'.join(filter(lambda x: not x.startswith('Metadata:'), post.content.splitlines()))
        setattr(task, 'note', post)

    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.path.dirname(args.template)))

    import filters
    for _ in filters.__all__:
        env.filters[_.__name__] = _

    rendered = env.get_template(os.path.basename(args.template)).render(tasks=tasks, deadline=deadline)
    print(rendered.encode('utf-8'))

if __name__ == '__main__':
    main()
