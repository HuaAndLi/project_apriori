import json
import requests
from lxml import etree

# 获取网页
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
data = requests.get('http://zhongyaofangji.com/zhuzhi/buxu.html', headers=headers)
html_str = data.content.decode('utf-8')

# print(html_str)

# 转为element对象
element = etree.HTML(html_str)

# 获取所有li
a_list = element.xpath("//ul[@class='uzyc']/li/a")

# 药方列表
tcm_list = []
for a_element in a_list:
    # print(a_element.xpath('./text()')[0])
    tcm_dict = {}  # 每个药方信息
    tcm_dict["title"] = a_element.xpath('./text()')[0]
    tcm_dict["href"] = "http://zhongyaofangji.com/" + a_element.xpath("./@href")[0]
    tcm_list.append(tcm_dict)
# 保存
with open('./data/tcm.json', 'w', encoding='utf-8') as f:
    json.dump(tcm_list, f, ensure_ascii=False, indent=2)
