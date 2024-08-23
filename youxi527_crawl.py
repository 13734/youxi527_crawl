import requests
from bs4 import BeautifulSoup  # 网页解析，获取数据
import json
import os
import time
import re  # 正则表达式，进行文字匹配`

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
all_end = 20001  # 起始id
all_start = 10001  # 结束id
save_html = True # 是否保持html文件
def GetOnePage(url,name_title,tf_save):
    print(url)
    data_dict = dict()
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    soup_page = BeautifulSoup(page_text, "html.parser")


    data_name = soup_page.find(class_ = "gamecname").getText()
    data_dict['name'] = data_name

    data_size = soup_page.find(class_="gamesize").find('span').getText()
    data_dict['size_str'] = data_size
    try:
        size_num  = float(data_size[:-1])
        size_big = data_size[-1].lower()
        if size_big == 'm':
            pass
        elif size_big == 'g':
            size_num *= 1000
        elif size_big == 'k':
            size_num /= 1000
        elif size_big == 't':
            size_num *= 1000000
        data_dict['size'] = size_num
    except:
        data_dict['size'] = 0



    if ( len(data_name) < 3)  or (data_name == name_title):
        return 0, data_dict




    xl_html = soup_page.find(class_="xunleibox")

    try:
        xl_url = xl_html.find(class_="a-right-title").find('a')['href']
        data_dict['have_xl'] = True
        data_dict['url_xl'] = xl_url
    except:
        data_dict['have_xl'] = False


    try:
        quark_html = soup_page.find(class_="quarkbox")
        quark_url = quark_html.find(class_="a-right-title").find('a')['href']
        data_dict['have_quark'] = True
        data_dict['url_quark'] = quark_url
    except:
        data_dict['have_quark'] = False


    try:
        al_html = soup_page.find(class_="alypbox")
        al_url = al_html.find(class_="down_xl")['href']
        data_dict['have_al'] = True
        data_dict['url_al'] = al_url
    except:
        data_dict['have_al'] = False

    try:
        baidu_html = soup_page.find(class_="newhzbdd")
        baidu_url = baidu_html.find(class_='down_bdd')['data-src']
        try:
            baidu_url_password = baidu_html.find(class_='down_bdd').find(class_='a-right-title').find('p').getText()
            data_dict['have_bd_password'] = True
            data_dict['bd_password'] = baidu_url_password
        except:
            data_dict['have_bd_password'] = False
        data_dict['have_bd'] = True
        data_dict['url_bd'] = baidu_url
    except:
        data_dict['have_bd'] = False


    try:
        bt_html = soup_page.find(id='btbtn')
        bt_url = bt_html['href']
        data_dict['have_bt'] = True
        data_dict['bt_url'] = bt_url
    except:
        data_dict['have_bt'] = False
    if tf_save:
        html_file_name = url.split('/')[-1]
        html_path = os.path.join('./htmls',html_file_name)
        with open(html_path, 'w', encoding='utf-8') as fp:
            fp.write(page_text)

    return 1,data_dict

if __name__ == '__main__':


    list_all = []

    if save_html:
        if not os.path.exists("./htmls"):
            os.mkdir("./htmls")

    for num_front in range(all_start,all_end):
        num_end = 1
        ret_end = 1
        name_title = ''
        while ret_end:
            url = 'https://www.youxi527.com/down/{}-{}.html'.format(num_front,num_end)
            ret_end,dict_single = GetOnePage(url, name_title, save_html )

            if ret_end ==1: #判断此id内容是否全部获取
                list_all.append(dict_single)
                if not(ret_end-1):
                    name_title= dict_single['name']
            num_end +=1

    #print(list_all)
        if num_front%500 == 0:
            i = 0
            while True:

                filename = 'data_all_po{num_front}.json'.format(i)
                if not os.path.exists(filename):
                    break
                i += 1
            with open(filename,'w',encoding='utf-8') as f:
                f.write(json.dumps(list_all))