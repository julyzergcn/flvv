#coding=utf-8
# need curl: http://curl.haxx.se/

new_folder = True
#~ new_folder = False

URLS = '''

http://v.youku.com/v_show/id_XNjYwODgxMjA0.html

'''

import os
import re
import sys
import subprocess


def get_title_urls(url):
    print url
    url = 'http://www.flvcd.com/parse.php?kw='+url
    a= subprocess.check_output(['curl', url])

    re_td = re.compile(u'下载地址.*?</td>'.encode('cp936'), re.I+re.U+re.S)
    re_a = re.compile('<a .*?href="(.*?)"', re.I+re.U+re.S)
    re_title = re.compile(u'当前解析视频.*?>(.*?)<'.encode('cp936'), re.I+re.S+re.U)

    title = ''
    urls = []

    if re_title.search(a):
        title = re_title.search(a).groups()[0].strip().decode('cp936')
    if re_td.search(a):
        urls = re_a.findall(re_td.search(a).group())
    return title, urls


def download(url):
    title, urls = get_title_urls(url)
    for i,url in enumerate(urls):
        if len(urls) > 1:
            fname = u'%s_%s_%s.flv' % (title, len(urls), '%02d'%(i+1) if len(urls)>9 else i+1)
        else:
            fname = u'%s.flv' % title

        if new_folder:
            if not os.path.exists(title):
                os.mkdir(title)
            fname = u'%s/%s' % (title, fname)

        fname = fname.encode('cp936')

        print
        print '---', fname
        print
        subprocess.call('curl -L -o "%s" %s' % (fname, url))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for url in sys.argv[1:]:
            download(url)
    else:
        for line in URLS.split('\n'):
            url = line.strip()
            if url:
                download(url)
