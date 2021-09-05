from pyquery import PyQuery as pq

d = pq(filename='dp.html')
d.make_links_absolute('https://gihyo.jp/dp')

for a in d('#listBook > li > a[itemprop="url"]'):
    url = d(a).attr('href')

    p = d(a).find('p[itemprop="name"]').eq(0)
    title = p.text()

    print(url, title)