"""
目标视频: https://www.bilibili.com/video/BV1Lm421L7Tk/
数据：用户名 评论内容 性别 IP属地
可以使用评论内容定位数据包的内容和地址
数据包地址: https://api.bilibili.com/x/v2/reply/wbi/main
"""
import requests
import csv

# 单页采集数据

# 保存数据
f = open('2406BComments/data.csv', mode='w', encoding='utf-8', newline='')
# 字典写入
csv_writer = csv.DictWriter(f, fieldnames=['NickName', 'Sex', 'Time', 'Message'])

# 模拟浏览器发送请求

headers = {
    "Cookie": "cookie",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
}

# url地址, 查询参数使用字典去接收
url = 'https://api.bilibili.com/x/v2/reply/wbi/main'
# 查询参数
data = {
    "oid" : '1605540456',
    "type" : '1',
    "mode" : '2',
    "pagination_str" : '{"offset":""}',
    "plat" : '1',
    "seek_rpid" :"",
    "web_location" : '1315875',
    "w_rid" : "975b0f0106b89fe64060f2648a4ee6c9",
    "wts" : '1718678392'
}

res = requests.get(url = url, params=data, headers=headers)

# res.text() 获取响应文本数据
# res.json() 获取响应的json数据
# res.content() 获取二进制数据 (图片、音频等)

json_data = res.json()
# print(json_data)

# 提取评论信息所在的列表
# 字典取值：键值对取值（分层提取内容），提取评论内容
replies = json_data['data']['replies']
# print(replies)
# 循环遍历提取列表中的每一个元素
for reply in replies:
    message = reply['content']['message'] # 提取评论内容
    name = reply['member']['uname'] # 用户名
    sex = reply['member']['sex'] # 性别
    tm = reply['reply_control']['time_desc'] # 发布时间
    
    # 信息封装为字典
    _dict = {
        'NickName' : name,
        'Sex' : sex,
        'Time': tm,
        'Message': message
    }

    # print(_dict)

    csv_writer.writerow(_dict)

"""
多页处理
pagination_str
w_rid: 加密参数, 需要进行逆向分析
wts 时间戳
time.time() 获取当前时间戳
"""

# 提取下一页参数
next_offset = json_data['data']['cursor']['pagination_reply']['next_offset']
print(next_offset)


