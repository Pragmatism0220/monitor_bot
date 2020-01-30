import os
import time
import csv
import json
import datetime
import pandas as pd
import numpy as np
from func_timeout import FunctionTimedOut, func_set_timeout
from retrying import retry


ins_username = 'nozomi_ka'
Save_Location = os.path.join('E:/IDM-Download/Video/crawler/ins_crawler/', ins_username)
dic = {'image': 'Post', 'story': 'Story'}
loginUserName = 'dl_test004'
loginPassword = 'zaq1xsw2'
SEND_MSG = []


def getText(df_all):    # get post's text. return a list
    lst = []
    for i in range(len(df_all)):
        lst.append(df_all.iloc[i]['edge_media_to_caption'])
    ans = []
    if len(lst) > 1:  # if there're a lot of posts
        for l in lst:
            try:
                ans.append(l['edges'][0]['node']['text'].replace(u'\ufeff', '').strip())
            except:
                pass
    elif len(lst) == 1:  # only one post
        try:
            ans.append(lst[0]['edges'][0]['node']['text'].replace(u'\ufeff', '').strip())  ## type : string
        except:
            pass
    return ans


def getTime(df_all):    # get post's time. NOT TEST STORY'S TIME FORMAT!! NOTICE!!!!!
    lst = []
    for i in range(len(df_all)):
        lst.append(df_all.iloc[i]['taken_at_timestamp'])
    ans = []
    if len(lst) > 1:  # if there're a lot of posts
        for l in lst:
            try:
                ans.append(str(datetime.datetime.fromtimestamp(l)))
            except:
                pass
    elif len(lst) == 1:  # only one post
        try:
            ans.append(str(datetime.datetime.fromtimestamp(lst[0])))   ## type: switch to string
        except:
            pass
    return ans


def getLikeNum(df_all):
    lst = []
    for i in range(len(df_all)):
        lst.append(df_all.iloc[i]['edge_media_preview_like'])
    ans = []
    if len(lst) > 1:  # if there're a lot of posts
        for l in lst:
            try:
                ans.append(l['count'])   ## type: int
            except:
                pass
    elif len(lst) == 1:  # only one post
        try:
            ans.append(lst[0]['count'])
        except:
            pass
    return ans


def getCommentNum(df_all):
    lst = []
    for i in range(len(df_all)):
        lst.append(df_all.iloc[i]['edge_media_to_comment'])
    ans = []
    if len(lst) > 1:  # if there're a lot of posts
        for l in lst:
            try:
                ans.append(l['count'])   ## type: int
            except:
                pass
    elif len(lst) == 1:  # only one post
        try:
            ans.append(lst[0]['count'])
        except:
            pass
    return ans


def getPicURLs(df_all):
    lst = []
    for i in range(len(df_all)):
        lst.append(df_all.iloc[i]['urls'])
    ans = []
    if len(lst) > 1:  # if there're a lot of posts
        for l in lst:
            try:
                ans.append(l)  ## type: int
            except:
                pass
    elif len(lst) == 1:  # only one post
        try:
            ans.append(lst[0])
        except:
            pass
    return ans


def getPostContent(df_all):  # contains two return values.
    # a return text contains: Time; Text; Pics; Likes_num; Comments_num;
    # The other return value contains a list of picture's name which were downloaded just now.
    Time = getTime(df_all)
    Text = getText(df_all)
    Pics = getPicURLs(df_all)
    Likes_num = getLikeNum(df_all)
    Comments_num = getCommentNum(df_all)
    tot = len(Time)
    ans = []
    Pic_name = []
    result_headers = [u'发帖时间', u'帖子内容', u'帖子配图及视频', u'点赞数', u'评论数']
    postFile = os.path.join(Save_Location, ins_username + '_帖子内容.csv')
    for i in range(tot):
        pic_name = []
        result_data = []
        Txt = u'【Instagram】\n你的老婆春日望のんちゃん发新ins啦！！\n发帖时间：%s\n帖子内容：\n%s\n\n帖子配图及视频：\n' % (Time[i] if i < len(Time) else '', Text[i] if i < len(Text) else '')
        result_data.append(Time[i] if i < len(Time) else '')
        result_data.append(Text[i] if i < len(Text) else '')
        for url in Pics[i]:
            try:
                pic_name.append(url.split('?')[0].split('/')[-1])
                Txt += url + '\n'  # append pic url to the text
            except:
                pass
        result_data.append(pic_name)
        Txt += u'图片及视频已上传至服务器储存！\n已有%d人点赞；已有%d人评论！\n快去看看吧！！！' % (Likes_num[i] if i < len(Likes_num) else 0, Comments_num[i] if i < len(Comments_num) else 0)
#        print(Txt)
        result_data.append(Likes_num[i] if i < len(Likes_num) else 0)
        result_data.append(Comments_num[i] if i < len(Comments_num) else 0)
        ans.append(Txt)
        Pic_name.append(pic_name)
        # 把帖子信息写入csv文件
        if not os.path.isfile(postFile):  # 如果个人信息的csv文件不存在则先创建，并写入表头
            with open(postFile, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(result_headers)
        with open(postFile, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result_data)
    return ans, Pic_name


def getProPicURL(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[9]['info']


def getPostsCount(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[8]['info']


def getID(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[4]['info']


def getFullName(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[3]['info']


def getFollowingCount(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[2]['info']


def getFollowersCount(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[1]['info']


def getProBiography(df):
    df_all = pd.DataFrame(df['GraphProfileInfo'])  # change to dataframe
    return df_all.iloc[0]['info']


def delJsonFile(path):
    f_list = os.listdir(path)
    for i in f_list:
        if os.path.splitext(i)[1] == '.json':
            os.remove(os.path.join(path, i))


def retry_if_error(exception):
    flag = isinstance(exception, FunctionTimedOut)
    if flag:
        print(u'-----Instagram爬取超时！准备重试！-----')
    return flag


@retry(retry_on_exception=retry_if_error, stop_max_attempt_number=3)
@func_set_timeout(120)
def os_system(s):
    os.system(s)


def instagram_main():
    global SEND_MSG
    if os.path.exists(os.path.join(Save_Location, 'Post')):
        delJsonFile(os.path.join(Save_Location, 'Post'))
    if os.path.exists(os.path.join(Save_Location, 'Story')):
        delJsonFile(os.path.join(Save_Location, 'Story'))
    hasPersonalInfo = hasPosts = hasProPic = hasStories = False
    SEND_MSG = []
    for tag in ['image', 'story']:
        save_location = os.path.join(Save_Location, dic[tag])
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        totFileNum = len([lists for lists in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, lists))])
        currentFileList = os.listdir(save_location)     # without counting username.json file in it.
        try:
            s = ('instagram-scraper ' + ins_username + ' -u ' + loginUserName + ' -p ' + loginPassword + ' -d ' + '\"' + save_location + '\"' + ' --media-types ' + tag + (' --profile-metadata' if tag == 'image' else '') + ' --comments --latest --retry-forever')
            os_system(s)
        except FunctionTimedOut:
            print(u'-----爬取Instagram超时！-----')
        jsonFile = os.path.join(save_location, ins_username + '.json')
        if tag == 'image':  # check whether the user posted new posts(including profile picture!).
            try:
                s = ('instagram-scraper ' + ins_username + ' -u ' + loginUserName + ' -p ' + loginPassword + ' -d ' + '\"' + save_location + '\"' + ' --media-types video --profile-metadata --comments --latest --retry-forever')
                os_system(s)
            except FunctionTimedOut:
                print(u'-----爬取Instagram超时！-----')
            if os.path.isfile(jsonFile):
                df = json.load(open(jsonFile, encoding='utf-8'))
            else:
                print(u'【Instagram】\n找不到json文件，可能哪里出问题了！')
                continue
            bioFile = os.path.join(Save_Location, ins_username + '_个人信息.csv')
            result_headers = [u'日期', u'用户id', u'用户昵称', u'发帖数', u'粉丝数', u'关注数', u'简介', u'高清头像地址']
            result_data = [time.strftime('%Y-%m-%d', time.localtime())]
            result_data.append(getID(df))
            result_data.append(getFullName(df))
            result_data.append(getPostsCount(df))
            result_data.append(getFollowersCount(df))
            result_data.append(getFollowingCount(df))
            result_data.append(getProBiography(df))
            result_data.append(getProPicURL(df))
            if not os.path.isdir(Save_Location):  # 先创建用户目录文件夹
                os.makedirs(Save_Location)
            if not os.path.isfile(bioFile):  # 如果个人信息的csv文件不存在则先创建，并写入表头
                with open(bioFile, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(result_headers)
            reader = pd.read_csv(bioFile)
            if reader.shape[0] > 0:  # 说明之前已经生成了csv文件且有个人信息的记录
                change_tag = []  # reader.shape[0] - 1表示最后一行数据
                if str(reader.iloc[reader.shape[0] - 1][u'用户id']) != result_data[1]:
                    change_tag.append(u'用户id')
                if reader.iloc[reader.shape[0] - 1][u'用户昵称'] != result_data[2]:
                    change_tag.append(u'用户昵称')
                if str(reader.iloc[reader.shape[0] - 1][u'发帖数']) != str(result_data[3]):    # 因为这个数字到了“万”的时候就变成带汉字的字符串了。为了兼容统一str
                    change_tag.append(u'发帖数')
                if str(reader.iloc[reader.shape[0] - 1][u'关注数']) != str(result_data[5]):
                    change_tag.append(u'关注数')
                try:
                    if ('' if np.isnan(reader.iloc[reader.shape[0] - 1][u'简介']) else str(reader.iloc[reader.shape[0] - 1][u'简介']).strip()) != str(result_data[6]).strip():
                        change_tag.append(u'简介')
                except:
                    if str(reader.iloc[reader.shape[0] - 1][u'简介']).strip() != str(result_data[6]).strip():
                        change_tag.append(u'简介')
                tot = len(change_tag)
                if tot == 0:  # 第一种情况，仅仅写入即可，粉丝数的改变不至于发消息
                    if str(reader.iloc[reader.shape[0] - 1][u'粉丝数']) != str(result_data[4]):  # 只有粉丝数有改动时，才写入csv文件
                        with open(bioFile, 'a', encoding='utf-8-sig', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(result_data)
                else:  # 第二种情况，要发消息的，同时写入csv文件
                    hasPersonalInfo = True
                    msg = u'【Instagram】\n你的老婆春日望のんちゃん的个人信息：\n'
                    for i in range(tot):
                        msg += change_tag[i] + (u'、' if i < tot - 1 else '')
                    msg += u'\n更新啦！现在的信息：\n'
                    for i in range(1, len(result_headers)):
                        msg += result_headers[i] + u'：' + str(result_data[i]) + '\n'
                    msg += u'信息已上传至服务器储存！\n赶快去看看吧~'
                    SEND_MSG.append(msg)
                    #print(msg)
                    with open(bioFile, 'a', encoding='utf-8-sig', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(result_data)
            else:  # 否则说明之前还没有个人信息的记录，需要写入第一条
                with open(bioFile, 'a', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(result_data)
            all_pic_file_name = []

            if 'GraphImages' in df.keys():  # if there has new posts
                df_all = pd.DataFrame(df['GraphImages'])  # change to dataframe
                ans, pic_file_name = getPostContent(df_all)  # two return value means text and picture's filename respectively.
                addNum = 0
                for i in range(len(ans)):
                    #print(ans[i])
                    SEND_MSG.append(ans[i])
                    #print('Pic-file name:')
                    #print(pic_file_name[i])
                    all_pic_file_name += pic_file_name[i]
                    addNum += len(pic_file_name[i])
                    #print('****************************************************************************************************')
                totFileNum += addNum
                hasPosts = True

            totNum = len([lists for lists in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, lists))]) - 1 # remove the username.json file

            # check whether there has new profile pictures
            if totNum != totFileNum:  # Yes she is.
                file_lists = os.listdir(save_location)
                if ins_username + '.json' in file_lists:
                    file_lists.remove(ins_username + '.json')
                file_lists = list(set(file_lists) - set(currentFileList))
                newProPic = list(set(file_lists) - set(all_pic_file_name))  # 新头像的文件名，存在列表里
                msg = u'【Instagram】\n你的老婆春日望のんちゃん换新头像啦！！\n头像图片地址：%s\n图片已上传至服务器储存！\n赶快去看看吧~' % getProPicURL(df)
                SEND_MSG.append(msg)
                #print(msg)
                #print(newProPic)
                hasProPic = True
            if not hasPersonalInfo and not hasPosts and not hasProPic:
                #print('のんちゃん还没有发新的帖子哦~')
                pass
            os.remove(jsonFile)
        else:   # check whether the user has posted new stories.
            totNum = len([lists for lists in os.listdir(save_location) if os.path.isfile(os.path.join(save_location, lists))])
            if totNum != totFileNum: # Yes she is.
                file_lists = os.listdir(save_location)
                newStories = list(set(file_lists) - set(currentFileList))   # 新的快拍的文件名，存在列表里
                msg = u'【Instagram】\n你的老婆春日望のんちゃん发新的story啦！！\n图片及视频已上传至服务器储存！\n赶快去看看吧~'
                SEND_MSG.append(msg)
                #print(msg)
                #print(newStories)
                hasStories = True
            else:
                #print('のんちゃん还没有发新的快拍哦~')
                pass
    if not hasPersonalInfo and not hasProPic and not hasPosts and not hasStories:
        print(u'你的老婆春日望のんちゃん还没有发新的ins哦~')
    return SEND_MSG
