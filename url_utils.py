from asyncore import write
from tkinter import E
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def get_content_(url):
    """
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding:gzip, deflate, sdch
    Accept-Language:en-US,en;q=0.8,vi;q=0.6
    Connection:keep-alive
    Cookie:__ltmc=225808911; __ltmb=225808911.202893004; __ltma=225808911.202893004.204252493; _gat=1; __RC=4; __R=1; _ga=GA1.3.938565844.1476219934; __IP=20217561; __UF=-1; __uif=__ui%3A-1%7C__uid%3A877575904920217840%7C__create%3A1475759049; __tb=0; _a3rd1467367343=0-9
    Host:dantri.com.vn
    Referer:http://dantri.com.vn/su-kien.htm
    Upgrade-Insecure-Requests:1
    User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
    """
    domain = None
    domains = url.split('/')
    if (domains.__len__() >= 3):
        domain = domains[2]

    headers = dict()
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = domain
    headers['Referer'] = url
    headers['Upgrade-Insecure-Requests'] = '1'
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

    r = requests.get(url, headers=headers, timeout=100)
    r.encoding = 'utf-8'
    r.close()
    return str(r.text)

def get_link_from_webpage(url):
    link = ""
    raw_content = get_content_(url)
    soup = BeautifulSoup(raw_content, 'html.parser')
    try:
        body = soup.find('body')
        div = body.find('div', id="wrapper")
        div2 = div.find('div', id='root', class_='redesign')
        div3 = div2.find("div", id="pagecontent", class_='pagecontent')
        div4 = div3.find("div", id="content-2-wide")
        div5 = div4.find("div", id="main")
        div6 = div5.find("div", class_="article")
        div7 = div6.find("div", class_="findSection")
        table = div7.find("table", class_="findList")
        body = table.find("tr",class_='findResult odd')
        result = body.find('td', class_="result_text")
        p = result.find('a', href=True)
        movie_url = "https://www.imdb.com" + p['href']
        link += movie_url

    except Exception:
        pass


    return link

def get_data_from_webpage(url):
    data = dict({"movie_brief": "", "director": "", "writers": [], "casts": []})
    raw_content = get_content_(url)
    soup = BeautifulSoup(raw_content, 'html.parser')
    try:
        body = soup.find("body")
        div = body.find("div", id="__next")
        m = div.find("main", role="main", class_="ipc-page-wrapper ipc-page-wrapper--base")
        div2 = m.find('div', class_="ipc-page-content-container ipc-page-content-container--full sc-b1984961-0 kXDasd", role="presentation")
        section = div2.find("section", class_="ipc-page-background ipc-page-background--base sc-c7f03a63-0 kUbSjY")
        section2 = section.find("section", "ipc-page-background ipc-page-background--baseAlt sc-6120f884-0 ezIlqu")
        div3 = section2.findAll("div", class_="ipc-page-content-container ipc-page-content-container--center", role="presentation")[2]
        section3 = div3.find("section", class_="ipc-page-background ipc-page-background--baseAlt sc-910a7330-0 iZtLgL")
        section4 = section3.find("section", class_="ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-910a7330-1 iPKxCm")
        div4 = section4.findChildren("div", recursive=False)[-1]
        div5 = div4.findChildren("div",recursive=False)[1]
        div6 = div5.findChild("div", recursive=False)
        all_div = div6.findChildren("div", recursive=False)

        ## Get data for brief
        try:
            brief_div = all_div[0]
    
            brief_div2 = brief_div.findChild("p", recursive=False)
            if brief_div2:
                brief_span = brief_div2.findChild("span", recursive=False)
                data["movie_brief"] += brief_span.text
            else:
                brief_div3 = brief_div.findChildren("div", recursive=False)[1]
                brief_span = brief_div3.find("span")
                data["movie_brief"] += brief_span.text
        except Exception:
            pass
        ## Get data for credits
        try:
            credits_div = all_div[3]
            credits_div2 = credits_div.findChild("div", recursive=False)
            credits_div3 = credits_div2.findChild("div", recursive=False)
            credits_ul = credits_div3.findChild("ul", recursive=False)
            credits_li = credits_ul.findChildren("li", recursive=False)##class_="ipc-metadata-list__item")
        except Exception:
            pass
        ## get director
        try:
            director = credits_li[0].find("a")

            data["director"] += director.text
        except Exception:
            pass

        ## get Writter
        try:
            writer_div = credits_li[1].findChild("div", recursive=False)
            writer_ul = writer_div.findChild("ul", recursive=False)
            writer_li = writer_ul.findChildren("li", recursive=False)
            for li in writer_li:
                writer = li.find("a").text
                data["writers"].append(writer)
        except Exception:
            pass
        ## get list cast
        try:
            casts = credits_li[2].findAll("li", class_="ipc-inline-list__item", role="presentation")
 
            for cast in casts:
                data["casts"].append(cast.find("a").text)
            print(data["casts"])
        except Exception:
            pass
    except Exception:
        pass

    if not data["movie_brief"]:
        data["movie_brief"] += "Unknown"
    if not data["director"]:
        data["director"] += "Unknown"
    if not data["writers"]:
        data["writers"].append("Unknown")
    if not data["casts"]:
        data["casts"].append("Unknown")
    return data