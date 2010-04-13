#!/usr/bin/python
from urllib import *
import re, os , sys

ego = 'http://ego.globo.com'

def getContent(url):
	html = urlopen(url , proxies={})
	return html.read().strip()

def saveContent(diretorio,url,file1):
	html = urlopen(url + file1 , proxies={})

	if not os.path.exists(diretorio) :
		os.mkdir(diretorio)
	f = open(diretorio + "/" + file1.replace("/","_"),"w");

	f.write(html.read())
	f.close


def main():
	if len(sys.argv) == 3:
		name = sys.argv[2]
	elif len(sys.argv) == 2:
	 name = 'default'
	else:
		sys.exit(1)
	print name
	url = sys.argv[1]

	p = re.compile("function ppzFotoPrincipalLink\(\){\s+window\.open\(\'(.*\.html)\'.*\)")

	m = p.search(getContent(url))

	p2 = re.compile("var urlXML =\'(.*)\'")

	m2 = p2.search(getContent(ego + m.group(1)))

	p3 = re.compile(".* fg=\"(.*.jpg)\" ")

	m3 = p3.findall(getContent(ego + m2.group(1)))


	for figure in m3:
		print figure
		saveContent(name,ego,figure)

if __name__ == "__main__":
	main()
