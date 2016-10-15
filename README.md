# Omni Weekly - Weekly Generator for Lazybones

After working as a software developer for two years, I find writing weekly report a really tough experience.

I spent lots of time doing trivial daily works and finally I can't recall them when I need to write the fucking report.

I have to spend time writing what I did this week instead of creating useful code pieces or having some fun. 

Now with Omni Weekly, I can log what I did, what I am doing, what I plan to do into a fucking expensive GTD software
called OmniFocus on the weekdays, and than generate a well formatted report when I need to.

It was first implement with Apple's ScriptBridge, but I rewrote it and it's base on OmniFocus's SQLite database
now!

## Installation

```
pip install git+https://github.com/JamesPan/py-omni-weekly.git
```

Maybe `sudo` is needed for privilege issue.

## Usage

After install, `weekly` command is in your path. See what we can do with `weekly`.

```
usage: weekly [-h] [-t TEMPLATE] [-d DEADLINE] [-p PERIOD] [-tz TIMEZONE]
              [-db DATABASE]

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        absolute path of template file
  -d DEADLINE, --deadline-date DEADLINE
  -p PERIOD, --period-days PERIOD
  -tz TIMEZONE, --timezone TIMEZONE
  -db DATABASE, --database DATABASE
```

Every argument has default value. Of cause the default template is for myself, I just need to type `weekly` and my
report for this week up to today will be print to stdout. You can use `-t` or `--template` to pass the absolute path
of a customize jinja2 template file to Omni Weekly, and pray for rendering properly.

```
$ weekly
1. 已经完成：

2. 仍在进行：
   + 到了北京我干了这十几年我也没有什么别的
     - 颐养天年  
       [估计进度 ??%]

3. 下周计划：
   + 到了北京我干了这十几年我也没有什么别的
     - 颐养天年
```

It seems I did nothing this week. With `-d` or `--deadline` we can reproduce weekly earlier or even later.

```
$ weekly -d 2016-10-07
1. 已经完成：
   + 到了北京我干了这十几年我也没有什么别的
     - 确立社会主义市场经济
     - 把邓小平的理论列入了党章
     - 三个代表  
       [[过程记录](http://www.baidu.com)]
   + 还有一点什么成绩
     - 军队一律不得经商：这个对军队的命运有很大的关系
     - 军委主席：后来又干了一年零八个月，等于我在部队干了15年军委主席
     - 抗洪：九八年的抗洪也是很大的

2. 仍在进行：
   + 到了北京我干了这十几年我也没有什么别的
     - 颐养天年  
       [估计进度 ??%]

3. 下周计划：
   + 到了北京我干了这十几年我也没有什么别的
     - 颐养天年
```

Excited.

On my Macbook, OmniFocus place it's SQLite database on
`~/Library/Containers/com.omnigroup.OmniFocus2/Data/Library/Caches/com.omnigroup.OmniFocus2/OmniFocusDatabase2`, but
this path may be different on your Mac, it depends on the App version. So, `-db` and `--database` can help passing the
right path of database to Omni Weekly.

Other arguments like `-tz` is for timezone, default is 'Asia/Shanghai'，'-p' is for reporting period, 7 for weekly, 1
for daily, 30 for monthly, etc.

Happy Hacking!
