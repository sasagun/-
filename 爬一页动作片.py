#coding:utf-8
import re, json, sys
reload(sys)
sys.setdefaultencoding("utf-8")
from urllib import urlopen
from collections import OrderedDict

count = 1     #电影序号

def get_link_list(url):			#爬取一页中的正文链接
    text = urlopen(url).read().decode('gbk').encode('utf-8')
    patt = re.compile('<b>.*?<a href="(.*?)".*?</b>', re.S)
    tail = re.findall(patt,text)
    front = 'http://www.dy2018.com'
    target_links = [(front + tail[i]) for i in range (len(tail))]
    return target_links
	
def get_one_page(target_links):			#进入到每个链接爬取电影信息	
    global count
    for target_link in  target_links:
        text = urlopen(target_link).read().decode('gbk').encode('utf-8')
        patt = re.compile('<p>.*?名　(.*?)</p>.*?[家|地]　(.*?)</p>.*?[别|型]　(.*?)</p>.*?文件大小　(.*?)</p>.*?长　(.*?)</p>.*?<td.*?<a href="(.*?)">.*?</a></td>', re.S)
        try:
            item = re.search(patt,text)
            dict = OrderedDict([('片名',item.group(1)),
							    ('产地',item.group(2)),
							    ('类型',item.group(3)),
							    ('大小',item.group(4)),
							    ('片长',item.group(5)),
							    ('下载',item.group(6))])
        except AttributeError:
            print '>>>>>>>>>>>>>>>原网页第' + str(count) + '部信息有误<<<<<<<<<<<<<<<'
            count += 1
            continue
        print str(count) + ('-'*240)      #用多个减号做分隔
        count += 1
        for i in dict.keys():
            print i, json.dumps(dict[i], encoding="UTF-8", ensure_ascii=False)
			
def main():
    url = 'http://www.dy2018.com/2'			#动作片分类首页
    target_links = get_link_list(url)
    get_one_page(target_links)

if __name__ == '__main__':
    main()
