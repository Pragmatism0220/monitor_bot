import sys
import os
import csv
import datetime
import pandas as pd
import requests
from func_timeout import FunctionTimedOut, func_set_timeout
from retrying import retry


tweets_username = 'kasuga_nozomi'
save_location = 'E:/IDM-Download/Video/crawler/tweets_crawler/'
save_location = os.path.join(save_location, tweets_username)
result_headers = ['has_media', 'hashtags', 'img_urls', 'is_replied', 'is_reply_to', 'likes',
                  'links', 'parent_tweet_id', 'replies', 'reply_to_users', 'retweets', 'screen_name',
                  'text', 'text_html', 'timestamp', 'timestamp_epochs', 'tweet_id', 'tweet_url',
                  'user_id', 'username', 'video_url']
SEND_MSG = []


def add2CSVFile(file_path, result_data):
    data = csv.reader(open(file_path, 'r', encoding='utf-8-sig', newline=''))
    lst = list(data)[1:]  # 这是个巨坑。csv.reader只是提供了一个句柄，换句话说，data的值会随着你csv文件被写了而改变。你需要额外用一个list将原来的值储存。用切片去掉标题头
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        fileWriter = csv.writer(f)
        fileWriter.writerow(result_headers)
        for i in range(len(result_data)):
            fileWriter.writerow(result_data.iloc[i].tolist())
        for row in lst:
            fileWriter.writerow(row)


def is_less_or_equal(time1, time2):
    d1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
    return d1.__le__(d2)


def retry_if_error(exception):
    print(u'-----Twitter爬取超时！准备重试！-----')
    return isinstance(exception, FunctionTimedOut)


@retry(retry_on_exception=retry_if_error, stop_max_attempt_number=3)
@func_set_timeout(120)
def os_system(s):
    os.system(s)


def save_img(img_url, file_path, file_name=''):
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    html = requests.get(img_url)
    if file_name == '':
        file_name = img_url.split('/')[-1]
    with open(os.path.join(file_path, file_name), 'wb') as f:
        f.write(html.content)


def twitter_main():
    global SEND_MSG
    SEND_MSG = []
    if not os.path.isdir(save_location):
        os.makedirs(save_location)
    target_csv = os.path.join(save_location, tweets_username + '.csv')
    if os.path.isfile(target_csv):
        reader = pd.read_csv(target_csv)
        if reader.shape[0] > 0:  # 说明之前已经生成了csv文件且有推文的记录
            latest_tweet_timestamp = reader.loc[0, 'timestamp']
        else:  # 否则说明之前还没有推文的记录
            latest_tweet_timestamp = '1970-01-01 00:00:00'
        retry_time = 5
        hasOld = False
        least_num = 10
        while True:
            try:
                s = ('twitterscraper ' + tweets_username + ' --limit ' + str(least_num) + ' --user -o ' + save_location + tweets_username + '.json')
                os_system(s)
            except FunctionTimedOut:
                print(u'-----爬取Twitter超时！-----')
            jsonFile = save_location + tweets_username + '.json'
            if os.path.exists(jsonFile):
                '''
                Demo:
                twitterscraper Trump --limit 1000 --output=tweets.json  #Number of minimum tweets to gather.
                twitterscraper Trump -l 1000 -o tweets.json
                twitterscraper Trump -l 1000 -bd 2017-01-01 -ed 2017-06-01 -o tweets.json # -bd means begindate and -ed means enddate.

                twitterscraper realDonaldTrump --user -o tweets_username.json # Including retweets, and this does not work in combination with -p, -bd, or -ed.
                '''
                df = pd.read_json(jsonFile, encoding='utf-8-sig')
                result = pd.DataFrame(columns=result_headers)
                '''
                pd.set_option('display.max_columns', 1000)
                pd.set_option('display.width', 1000)
                pd.set_option('display.max_colwidth', 1000)
                '''
                for i in range(len(df)):
                    if is_less_or_equal(str(df.iloc[i]['timestamp']), latest_tweet_timestamp):
                        hasOld = True
                        break
                    else:
                        result.loc[i] = df.iloc[i]
                os.remove(jsonFile)
                # 如果出现旧的推文，就break掉
                if hasOld:
                    if not result.empty:  # 如果有要写的内容
                        for i in range(len(result)):
                            if str(result.iloc[i]['user_id']) == '1079279736214282240':
                                msg = u'【Twitter】\n你的老婆春日望のんちゃん发了一条新的推特！\n'
                            else:
                                msg = u'你的老婆春日望のんちゃん转发了一条推特！\n'
                            msg += u'发表时间：%s\n' % str(result.iloc[i]['timestamp'])
                            msg += u'推文内容：\n%s\n\n' % result.iloc[i]['text']
                            msg += u'推文链接：https://twitter.com%s\n' % result.iloc[i]['tweet_url']
                            if len(result.iloc[i]['hashtags']):
                                msg += u'推文标签：%s\n' % str(result.iloc[i]['hashtags'])
                            if result.iloc[i]['has_media']:
                                msg += u'图片地址：%s\n' % str(result.iloc[i]['img_urls'])
                                # save the images
                                for img_url in list(result.iloc[i]['img_urls']):
                                    save_img(img_url, os.path.join(save_location, tweets_username))
                            msg += u'已有%d人喜欢；已有%d人评论；已有%d人转发\n赶快去看看吧~' % (int(result.iloc[i]['likes']),
                                                                          int(result.iloc[i]['replies']),
                                                                          int(result.iloc[i]['retweets']))
                            SEND_MSG.append(msg)
                            #print(msg)
                            #print('*' * 100)
                        add2CSVFile(target_csv, result)
                    else:
                        print(u'你的老婆春日望のんちゃん还没有发新的推特哦~')
                    # print(result)
                    break
                else:
                    least_num += 20
                    if least_num > 200:  # 一个人连发200条推特，实在是不大可能；所以用200作为防止异常死循环的条件，强制退出
                        sys.stderr.write(u'死循环异常！！强行退出！！\n')
                        break
                    print(u'我草竟然不够？！')  # 滑稽.jpg
                    continue
            else:
                print('Can not get json file! Maybe crawler has something wrong...')
                retry_time -= 1
                if retry_time == 0:
                    break
    else:
        try:
            s = ('twitterscraper ' + tweets_username + ' --user -o ' + save_location + tweets_username + '.json')
            os_system(s)
        except FunctionTimedOut:
            print(u'-----爬取Twitter超时！-----')
        jsonFile = save_location + tweets_username + '.json'
        if os.path.exists(jsonFile):
            df = pd.read_json(jsonFile, encoding='utf-8')
            os.remove(jsonFile)
            df.to_csv(target_csv, index=False, encoding='utf-8-sig')
        else:
            print('Can not get json file! Maybe crawler has something wrong...')
    return SEND_MSG
