import requests
from lxml import etree
import os

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

def get_page_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    return response.text

def get_links(page_text):
    tree = etree.HTML(page_text)
    links = tree.xpath('/html/body/div[1]/div[2]/ul[2]/li/a/@href')
    return links

def get_title(page_text):
    tree = etree.HTML(page_text)
    title = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/h1/text()')
    return title[0]

def download_photo(photo_url, folder_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    response = requests.get(url=photo_url, headers=headers)
    photo = response.content
    file_name = photo_url.split('/')[-1]
    with open(os.path.join(folder_path, file_name), 'wb') as fp:
        fp.write(photo)

def crawl_photos():
    base_url = 'https://www.win3000.com/tags/nmxtp/'
    folder_path = './Pictures'
    create_folder(folder_path)
    li_all = []

    for i in range(1, 6):
        url = base_url + 'p' + str(i) + '/'
        page_text = get_page_text(url)
        li_list = get_links(page_text)
        li_all += li_list

    for li in li_all:
        url = li
        page_text = get_page_text(url)
        dir_name = get_title(page_text)
        dir_path = os.path.join(folder_path, dir_name)
        create_folder(dir_path)

        for i in range(1, 20):
            picture_url = str(li).rstrip('.html') + '_' + str(i) + '.html'
            picture_detail_text = get_page_text(picture_url)
            tree = etree.HTML(picture_detail_text)
            picture_detail_url = tree.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/p/img/@src')
            
            if not picture_detail_url:
                print(dir_name, " is ok.")
                break
            else:
                download_photo(picture_detail_url[0], dir_path)
                print(dir_name, "'s ", i, ' is ok.')

    print("Everything is ok!")

crawl_photos()
