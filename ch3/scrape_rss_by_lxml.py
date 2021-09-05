import lxml.etree

tree = lxml.etree.parse('rss2.xml')
root = tree.getroot()

for item in root.xpath('channel/item'):
    titele = item.xpath('title')[0].text
    url = item.xpath('link')[0].text
    
    print (url, titele)