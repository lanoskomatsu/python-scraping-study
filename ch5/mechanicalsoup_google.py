import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')
browser.open('')

browser.select_form('form[action="/search"]')
browser['q'] = 'Python'
browser.submit_selected()

page = browser.get_current_page()
for a in page.select('a > h3'):
    print(a.text)
    print(browser.absolute_url(a.get('href')))
