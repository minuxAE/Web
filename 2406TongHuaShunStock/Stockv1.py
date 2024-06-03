"""
编写爬虫获取同花顺股票数据
目标网站地址：https://q.10jqka.com.cn
"""
# 模拟浏览器向url发送请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0'
}

cookie = {
    'v': 'AzH75iak852ZTF-JqAZESD13QLzOHqU3T5BJpBNGKKIWlV8oW261YN_iWVCg'
}

# 设置目标url
url = 'https://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/2/ajax/1/'

import requests
import parsel
import csv

f = open('2406TongHuaShunStock/data.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    'Code',
    'Name',
    'Price',
    'Price Range(%)',
    'Price Range',
    'Speed(%)',
    'Turnover(%)',
    'Volume Ratio',
    'Volatility(%)',
    'Turn Volume',
    'Floating Stock',
    'Market Value',
    'PE Ratio'
])

csv_writer.writeheader() # 写入表头

res = requests.get(url=url, headers=headers, cookies=cookie)
# res = requests.get(url=url, headers=headers)

# 响应数据
## response.text 获取响应文本数据
## response.json 获取响应json数据
## response.content 获取响应二进制数据

html = res.text
# print(html) # 内容不一致，可能存在反爬
# 尝试加入cookie

# 提取数据内容
## re正则
## xpath
## css选择器
## json解析
## 直接处理
"""
<tr>
    <td>33</td>
    <td><a href="http://stockpage.10jqka.com.cn/300502/" target="_blank">300502</a></td>
    <td><a href="http://stockpage.10jqka.com.cn/300502/" target="_blank">新易盛</a></td>
    <td class="c-rise">92.00</td>
    <td class="c-rise">5.96</td>
    <td class="c-rise">5.17</td>
    <td class="c-rise">1.55</td>
    <td>1.44</td>
    <td class="c-rise">9.17</td>
    <td class="c-rise">5.07</td>
    <td>8.01亿</td>
    <td>6.18亿</td>
    <td>568.21亿</td>
    <td>50.31</td>
    <td><a class="j_addStock" title="加自选" href="javascript:void(0);"><img src="http://i.thsi.cn/images/q/plus_logo.png" alt=""></a></td>
</tr>
"""
# print(html)
selector = parsel.Selector(html)
# 从class="m-table"的table中提取tr标签
trs = selector.css('.m-table tr')[1:] # 标题行舍弃
for tr in trs:
    stock_info = tr.css('td a::text').getall() # 股票信息
    trade_info = tr.css('td::text').getall() # 交易信息
    # print(stock_info)
    # print(trade_info)

    # 数据保存
    dict = {
        'Code': stock_info[0],
        'Name': stock_info[1],
        'Price': trade_info[1],
        'Price Range(%)': trade_info[2],
        'Price Range': trade_info[3],
        'Speed(%)': trade_info[4],
        'Turnover(%)': trade_info[5],
        'Volume Ratio': trade_info[6],
        'Volatility(%)': trade_info[7],
        'Turn Volume': trade_info[8],
        'Floating Stock': trade_info[9],
        'Market Value': trade_info[10],
        'PE Ratio': trade_info[11]
    }

    csv_writer.writerow(dict)

    print(dict)
