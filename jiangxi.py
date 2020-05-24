# 目标爬取欣欣旅游网中江西的图片

import requests
from lxml import etree
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}

url = "https://jxyichun.cncn.com/photo/"

page_text = requests.get(url=url, headers=headers).text
tree = etree.HTML(page_text)
li_list = tree.xpath('//*[@id="wrapper"]/div[2]/div[1]/div[2]/ul/li')
for li in li_list:
    title = li.xpath('./a/img/@alt')[0] + '.jpg'
    # print(title)
    #   https://beijing.cncn.com/photo/185370/
    detail_url = "https://jxyichun.cncn.com" + li.xpath('./a/@href')[0]
    # print(detail_url)
    response = requests.get(url=detail_url, headers=headers)
    response.encoding = "utf-8"
    detail_page = response.text
    detail_tree = etree.HTML(detail_page)
    # https://c.cncnimg.cn/046/913/50c9_b.jpg
    pic_url = "https:" + detail_tree.xpath('//*[@id="wrapper"]//div[@class="pic"]//img/@src')[0]
    # print(pic_url)

    img_data = requests.get(pic_url, headers=headers).content

    path = './江西图片/' + title
    try:
        if not os.path.exists(path):  # 判断文件是否存在

            with open(path, 'wb')as f:
                f.write(img_data)
                f.close()
                print(title, "文件保存成功")

        else:
            print("文件已存在")
    except:
        print("爬取失败")