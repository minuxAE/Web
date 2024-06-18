"""
音乐下载
目标网站：www.gequbao.com
"""

import requests
import parsel
from prettytable import PrettyTable

# 采集目标歌曲：离别开出花
def MusicDownload():
    # 在媒体中确定链接地址：https://lx-sycdn.kuwo.cn/d494190caefdbd767871728c64faa4d6/665d3549/resource/n2/82/74/4006202814.mp3?from=vip
    # 确定链接来源（数据包的地址）：https://www.gequbao.com/api/play_url?id=8236063&json=1

    def getResponse(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
        }

        res = requests.get(url=url, headers=headers)
        return res
    
    def getMusicInfo(url):
        res = getResponse(url)
        json_data = res.json()
        song_url = json_data['data']['url']

        # print(json_data)
        return song_url
    
    def saveMusic(title, url):
        song_url = getMusicInfo(url)
        song_content = getResponse(url=song_url).content

        with open('2406MusicDownload/'+title+'.mp3', mode='wb') as f:
            f.write(song_content)
        print(f'{title}下载完成...')


    # url = 'https://www.gequbao.com/api/play_url?id=8236063&json=1'
    # saveMusic('离别开出花', url)
    # return

    # 搜索并下载
    def search_download(word):
        # 搜索关键词‘凤凰传奇’
        # 点击第一首歌，并点击播放，在媒体中找到GET请求：https://sz-sycdn.kuwo.cn/258da538513f07c80e049e1888fdda6c/665d6231/resource/n3/55/26/3773591637.mp3?from=vip
        # 定位出数据包：https://www.gequbao.com/api/play_url?id=62797&json=1
        # 点击第二首歌，定位数据包：https://www.gequbao.com/api/play_url?id=121981&json=1
        # 变化的是id
        # search_url = 'https://www.gequbao.com/s/%E5%87%A4%E5%87%B0%E4%BC%A0%E5%A5%87'
        search_url = f'https://www.gequbao.com/s/{word}'
        # print(search_url)
        html = getResponse(url=search_url).text
        """
        <a href="/music/62797" class="text-primary font-weight-bold" target="_blank">奢香夫人</a>
        """
        selector = parsel.Selector(html)
        # 使用css选择器，根据标签属性选取内容
        # 所有歌曲的标签
        rows = selector.css('.row')[2:-1] # 开头和末尾不是歌曲信息
        info_list = []
        tb = PrettyTable()
        tb.field_names = ['序号', '歌名', '演唱者']
        idx = 0
        for row in rows:
            title = row.css('.text-primary::text').get().strip()
            song_id = row.css('.text-primary::attr(href)').get().split('/')[-1]
            songer = row.css('.text-success::text').get().strip()
            # print(title, song_id, songer)

            dict = {
                'Title': title,
                'Songer': songer,
                'SongId': song_id
            }

            tb.add_row([idx, title, songer])
            idx += 1
            info_list.append(dict)
        print(tb)
        return info_list
    

    word = input('请输入你搜索的关键词：')
    info_list = search_download(word)
    # print(info_list)
    while True:
        sid = input('请输入歌曲序号进行下载(X退出 A全部下载)：')
        if sid == 'x' or sid == 'X':
            break
        elif sid == 'a' or sid == 'A':
            for info in info_list:
                music_id = info['SongId']
                music_title = info['Title']
                url = f'https://www.gequbao.com/api/play_url?id={music_id}&json=1'
                try:
                    saveMusic(title=music_title, url=url)
                except:
                    print(f'{music_title}存在下载问题，请重试')
        else:
            music_id = info_list[int(sid)]['SongId']
            music_title = info_list[int(sid)]['Title']
            url = f'https://www.gequbao.com/api/play_url?id={music_id}&json=1'
            try:
                saveMusic(title=music_title, url=url)
            except:
                print(f'{music_title}存在下载问题，请重试')


if __name__ == '__main__':
    MusicDownload()