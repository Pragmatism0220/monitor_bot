# monitor_bot
A monitor bot works on Instagram, Twitter and Weibo.

## Statement
This project is just a practice for me. I write this project just out of my interest.
This project is just used for me to follow my idol(laugh). I am sorry if it troubles you.

## What's it?
It's a monitor bot works on Instagram, Twitter and Weibo. In other words, it's a **crawler**.
Every 10 minutes, as a interval, this program will do the work to look for whether the target user has send new posts or retweeted. If the user did do it, the program will send message to your QQ to remind you by CoolQ.

**Thanks for the CoolQ project and nonebot module.**


## Environment
These project uses Python3 and works on Windows operating system.
If you use Python2, it may cause some problems.
If you use Linux operating system, I am sorry to tell you that CoolQ cannot works on Linux. Therefore, you may use Docker if you insist on using it on Linux.

In addition, there are a lot of modules I have used. Thanks for these projects.

### Send Message to QQ
1. [CoolQ](https://cqp.cc/)

Documents(API): https://cqhttp.cc/docs/4.13/#/

2. [NoneBot](https://github.com/richardchien/nonebot)

Documents: https://nonebot.cqp.moe/guide/scheduler.html

### Craw Instagram
1. [instagram-scraper](https://github.com/rarcega/instagram-scraper)

### Craw Twitter
1. [twitterscraper](https://github.com/taspinar/twitterscraper)
2. [requests](https://github.com/psf/requests)

### Craw Weibo
1. [weibo-crawler(without cookie version)](https://github.com/dataabc/weibo-crawler)
2. [real-url](https://github.com/wbt5/real-url)

### Others modules
1. [pandas](https://github.com/pandas-dev/pandas)
2. [numpy](https://github.com/numpy/numpy)
3. [func_timeout](https://github.com/kata198/func_timeout)
4. [retrying](https://github.com/rholder/retrying)
5. [fake_useragent](https://github.com/hellysmile/fake-useragent)

And so on, THANK YOU for all of the works you have done!!
Thank you very much!

## How to use
Just clone this project, and enter this directory in cmd after installing related requirements.
Use the command:
```
python3 bot.py
```
At the same time, run the CoolQ(exe) and login it.
And that's it. It will run once every 10 minutes.

If there are some problem, please fix it yourself.(smile)

I'm tired.

## Structure
bot.py is the communication interface which help us establish the connection with CoolQ client.
config.py is the config file to initialize some config about bot.py file.
Besides, there's a directory called awesome. The name is a joke, just ignore it.
In the awesome directory, there's a directory called plugins which is used to store some CoolQ-plugins written in Python. Open it, and we will find that there's a file called top.py. It's the top file to control the plugins. I store the crawlers in the crawlers directory. Or more exactly, crawlers package. There are a lot of plugins written in Python.

The structure can be shown in this way:
``` graph
CoolQ
 |_ bot.py        # communicate with CoolQ
 |_ config.py     # config file
 |_ awesome
     |_ plugins
         |_ top.py      # top file
         |_ Test.py     # It's empty file. Just use for test and it's useless now.
         |_ crawlers
             |_ __init__.py
             |_ config.json         # weibo.py's config json file
             |_ instagram.py
             |_ twitter.py
             |_ weibo.py
             |_ weibo-yizhibo.py    # weibo has broadcast live service. This file can get the real stream url.
```

## How it works
Magic.

I just use the open-source tools to get the data, and store them into a file for the first time to run it.(I use csv file)
Next time, the program will compare the latest message in the csv-file to the data when the crawler finished its work. Once it finds the old message in the data crawed, it will stop compare work and write the new message to the csv file on its top. At the same time, it will return the message to the top file, which will send these message to QQ then.

That's this project's principle(magic).

There are a hundred of exception handling. I even use time-out handling and retrying handling for some tools.
All the file and directory operation is strong enough(maybe).

Just one thing. There're a lot of traps and bugs in some module I use. I find them and I fix them. I really learn a lot from it.
And, it really takes me a lot of time.

~~S.H.I.T~~

## Postscript
The code I wrote sucks.
