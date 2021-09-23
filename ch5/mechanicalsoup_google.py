import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()
browser.open('')

browser.select_from('form[action="/search"]')
browser['q'] = 'Python'
browser.submit_selected()

page = browser.get_current_page()
for a in page.select('h3 > a'):
    print(a.text)
    print(browser.absolute_url(a.get('href')))
