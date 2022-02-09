import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

urls = ["https://m.jinhak.com/MyInfo/SATAysComPerc.aspx?Idx=0&Sigi=&Part=2&CID=11F120",
        "https://m.jinhak.com/MyInfo/SATAysComPerc.aspx?Idx=0&Sigi=&Part=1&CID=11F120"
]   # 자, 인
length = [65, 78]  # 자, 인
line = ['자연', '인문']
d=pd.DataFrame()
count = 0

for url, l, line in zip(urls, length, line):
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    dom = etree.HTML(str(soup))


    '''
    LEGACY -
    print(dom.xpath('/html/body/div[4]/div/div[2]/form/table/tbody/tr[1]/td[1]')[0].text)
    print(dom.xpath('/html/body/div[4]/div/div[2]/form/table/tbody/tr[1]/td[2]')[0].text)
    print(dom.xpath('/html/body/div[4]/div/div[2]/form/table/tbody/tr[1]/td[3]')[0].text)
    print(dom.xpath('/html/body/div[4]/div/div[2]/form/table/tbody/tr[1]/td[4]')[0].text)
    
    print(dom.xpath('/html/body/div[4]/div/div[2]/form/table/tbody/tr[1]/td[6]/a')[0].attrib.get('onclick'))
    print(dom.xpath('/html/body/div[4]/div/div[2]/form/table/tbody/tr[5]/td[6]/a')[0].attrib.get('onclick'))
    
    
    '''


    def refine_univ(u: str):
        u = u.replace('showUnivs', '')
        u = u.strip("('")
        u = u.strip("')")
        list = [i.strip()[5:] for i in u.split(',')]
        return list

    placeholder = '/html/body/div[4]/div/div[2]/form/table/tbody/tr[{0}]/td[{1}]'
    ph_univ = '/html/body/div[4]/div/div[2]/form/table/tbody/tr[{0}]/td[6]/a'

    subject = ['대학', '계열', '국어', '수학', '영어', '탐구']
    df = pd.DataFrame(columns=subject)


    for i in range(1, l):
        freq = []
        for k in range(1, 5):
            freq.append(dom.xpath(placeholder.format(i, k))[0].text)
        univ = dom.xpath(ph_univ.format(i, 6))[0].attrib.get('onclick')
        univ = refine_univ(univ)
        for u in univ:
            f = [u] + [line] + freq
            dict = {key: [n] for key, n in zip(subject, f)}
            df = pd.concat([df, pd.DataFrame(dict)])
    if count: d = pd.concat([d, df])
    else: d = df;
    count = 1

d.to_json('freq_score.json', orient='records')
