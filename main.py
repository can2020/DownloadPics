__author__ = 'can.zeng <can.zeng@hotmail.com>'

import requests
import bs4
import os
import urllib


def get_all_links_in_album(url, work_dir):
    for index in xrange(1,100):
        if index != 1:
            one_album_url = url.replace(".html", "_"+ str(index) +'.html')
        else:
            one_album_url = url
        print 'From : ' + one_album_url
        response = requests.get(one_album_url)
        if not response or not response.text:
            break
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        for item in soup.find_all("img"):
            if -1 != item.get('src').find('thumb'):
                continue
            if -1 != item.get('src').find('uploadfile'):
                print 'Download ' + item.get('src')
                download_picture(item.get('src'), work_dir)


def download_picture(url, save_to_dir):
    name_from_url = url[url.rfind('/') +1:]
    save_to_path = os.path.join(save_to_dir, name_from_url)
    urllib.urlretrieve (url, save_to_path)
    pass


def get_all_album_in_catalogue(catalogue_url):
    album = list()
    for index in xrange(1, 100):
        url = catalogue_url
        if index != 1:
            url = catalogue_url + str(index) + '.html'
        print url
        response = requests.get(url)
        if not response or not response.text:
            break

        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        for item in soup.find_all("a", target='_blank'):
            if item.img and item.get('href'):
                album.append({'name': item.img['alt'], 'url': item['href']})
    return album


def main():
    album = get_all_album_in_catalogue('http://www.abumei.com/sex/')
    for item in album:
        #target_dir = os.path.join('/Users/zcan/git/DownloadPics/pic', bs4.UnicodeDammit(item['name']).unicode_markup)
        #if os.path.exists(target_dir):
         #   os.mkdir(target_dir)
        #get_all_links_in_album(item['url'], target_dir)
        pass
    pass


if __name__ == '__main__':
    main()