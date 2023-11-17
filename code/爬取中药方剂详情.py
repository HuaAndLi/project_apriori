import json
import requests
from lxml import etree
import time

def spider(url, tcm_dict):
    # 获取网页
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    data = requests.get(url, headers=headers)
    code = data.apparent_encoding
    html_str = data.content.decode(data.apparent_encoding)

    # print(html_str)

    # 转为element对象
    element = etree.HTML(html_str)

    # 获取所有p
    p1 = element.xpath("//div[@class='spider']//p[contains(text(), '【处方】')]")
    p2 = element.xpath("//div[@class='spider']//p[contains(text(), '【制法】')]")
    p3 = element.xpath("//div[@class='spider']//p[contains(text(), '【功能主治】')]")
    p4 = element.xpath("//div[@class='spider']//p[contains(text(), '【用法用量】')]")
    p5 = element.xpath("//div[@class='spider']//p[contains(text(), '【摘录】')]")

    if p1:
        p1 = p1[0]
        tcm_dict['medical_prescription'] = ' '.join(p1.xpath('.//text()'))
        tcm_dict['prescription_list'] = p1.xpath('.//a/text()')

    if p2:
        p2 = p2[0]
        tcm_dict['method_of_making'] = ' '.join(p2.xpath('.//text()'))
    if p3:
        p3 = p3[0]
        tcm_dict['diagnosis_and_treatment_of_a_disease'] = ' '.join(p3.xpath('.//text()'))
    if p4:
        p4 = p4[0]
        tcm_dict['usage_and_dosage'] = ' '.join(p4.xpath('.//text()'))
    if p5:
        p5 = p5[0]
        tcm_dict['excerpt'] = ' '.join(p5.xpath('.//text()'))



tcm_list = None
with open('./data/tcm.json', encoding='utf-8') as f:
    tcm_list = json.load(f)

for tcm in tcm_list:
    time.sleep(0.8)
    tcm_url = tcm['href']
    spider(tcm_url, tcm)
    print(tcm)

# 保存
with open('./data/tcm_detail.json', 'w', encoding='utf-8') as f:
    json.dump(tcm_list, f, ensure_ascii=False, indent=2)