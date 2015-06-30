#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'can.zeng <can.zeng@hotmail.com>'

import bs4
import os
import urllib
import urllib2
import optparse


def GetAllPicturesInAlbum(url, work_dir):
    for index in xrange(1, 100):
        if index != 1:
            one_album_url = url.replace(".html", "_"+ str(index) +'.html')
        else:
            one_album_url = url
        print 'From : ' + one_album_url
        soup = bs4.BeautifulSoup(urllib2.urlopen(one_album_url).read(), 'html.parser')
        if soup is None:
            break

        for item in soup.find_all("img"):
            if -1 != item.get('src').find('thumb'):
                continue
            if -1 != item.get('src').find('uploadfile'):
                print 'Download ' + item.get('src')
                DownloadFile(item.get('src'), work_dir)


def DownloadFile(url, save_to_dir):
    name_from_url = url[url.rfind('/') +1:]
    save_to_path = os.path.join(save_to_dir, name_from_url)
    #urllib.urlretrieve(url, save_to_path)
    print 'Fack download ' + save_to_path

def GetResourceContent(url):
    response = urllib2.urlopen(url)
    return response.read()


def GetAllAlbumInCatalogue(catalogue_url):
    album = list()
    for index in xrange(1, 100):
        url = catalogue_url
        if index != 1:
            url = catalogue_url + str(index) + '.html'
        print url
        html = GetResourceContent(catalogue_url)
        if not html:
            break
        soup = bs4.BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        for item in soup.find_all("a", target='_blank'):
            if item.img and item.get('href'):
                album.append({'name': item.img['alt'], 'url': item['href']})
    return album


def main():
    option_parser = optparse.OptionParser()
    option_parser.add_option('--host-name', type='string',
                             help='The website which pictures download from')
    option_parser.add_option('--save-to-dir', type='string',
                             help='Directory which the pictures save to')
    options = option_parser.parse_args()[0]
    if not options.host_name or not options.save_to_dir:
        raise Exception('Should run with --host-name=http://www.example.com')

    album = GetAllAlbumInCatalogue(options.host_name)
    for item in album:
        target_dir = os.path.join(options.save_to_dir, item['name'])
        target_dir = os.path.normpath(target_dir)
        if os.path.exists(target_dir):
            os.mkdir(target_dir)
        GetAllPicturesInAlbum(item['url'], target_dir)


if __name__ == '__main__':
    main()