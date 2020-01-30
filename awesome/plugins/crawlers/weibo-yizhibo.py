# Get the real streaming media url from yizhibo

# NOTICE:
# Time: 2020-1-29 23:11:27 (Beijing)
# Now, it can work well to get the real url of the live-stream. But it can't send message to my qq because I don't know the ID of kasuga nozomi.
# And she hasn't activated broadcast service. If she does do it, I will implement this module.


import requests
import re


def get_real_url(room_url):
    try:
        scid = re.findall(r'/l/([\-\w]*)\.html', room_url)[0]
        flvurl = 'http://alcdn.f01.xiaoka.tv/live/{}.flv'.format(scid)
        m3u8url = 'http://al01.alcdn.hls.xiaoka.tv/live/{}.m3u8'.format(scid)   # Just keep it now. Not use it.
        rtmpurl = 'rtmp://alcdn.r01.xiaoka.tv/live/live/{}'.format(scid)        # Use this url we can watch the live-video by our PotPlayer.
        '''
        real_url = {
            'flvurl': flvurl,
            'm3u8url': m3u8url,
            'rtmpurl': rtmpurl
        }
        '''
        real_url = flvurl
    except:
        real_url = 'wrong url!'
    return real_url


def get_status(room_url):
    try:
        scid = re.findall(r'/l/([\-\w]*)\.html', room_url)[0]
        response = requests.get(
            url='https://m.yizhibo.com/www/live/get_live_video?scid=' + str(scid)).json()
        status_code = response.get('data').get('info').get('status')
        status = 'Broadcast live right now!' if status_code == 10 else 'Not broadcast'
    except:
        status = 'wrong url!'
    return status


def weibo_yizhibo_main():
    rid = input('Please input the room url：\n')
    status = get_status(rid.strip())
    print('The status of the room is: ', status)
    real_url = get_real_url(rid.strip())
    print('The url of the room live is: ')
    print(real_url)

    '''
    After that, all we need to handle is:
    How to download it online:
    We use aria2 tool to download it.
    Open your command window, and operate the command:
    aria2c real_url --dir "E:/IDM-Download/Video/weibo_test"
    *The real_url parameter is the value that the code above get finally. Remember to replace it with your own url get.*
    
    The --dir option determines the directory to store the downloaded file.
    By the way, we can know more options through command:
    aria2c -h
    '''
