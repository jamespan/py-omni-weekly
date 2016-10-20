# coding=utf-8
from __future__ import print_function

from jinja2 import Undefined


def is_project(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: x.parent is None, iterable)


def is_task_of(iterable, project):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: x.parent == project.persistentIdentifier, iterable)


def project_with_completed_tasks(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: len(
        filter(lambda y: y.parent == x.persistentIdentifier and y.dateCompleted is not None, iterable)) > 0,
                  is_project(iterable))


def project_with_incomplete_tasks(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: len(
        filter(lambda y: y.parent == x.persistentIdentifier and y.dateCompleted is None, iterable)) > 0,
                  is_project(iterable))


def project_with_processing_tasks(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: len(
        filter(lambda y: y.parent == x.persistentIdentifier and y.dateCompleted is None and 'progress' in y.note.metadata, iterable)) > 0,
                  is_project(iterable))


def is_complete(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: x.dateCompleted is not None, iterable)


def is_incomplete(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: x.dateCompleted is None, iterable)


def is_processing(iterable):
    if iterable is None or isinstance(iterable, Undefined):
        return iterable
    return filter(lambda x: 'progress' in x.note.metadata, is_incomplete(iterable))
