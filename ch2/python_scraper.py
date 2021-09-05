import csv
from os import write
from typing import List

import requests
import lxml.html

def main():
    """
    メインの処理。fetch(), scrape(), save()の3つの関数を呼び出す。
    """

    url = 'https://gihyo.jp/dp'
    html = fetch(url)
    books = scrape(html, url)
    save('books.csv', books)

def fetch(url: str) -> str:
    """
    引数urlで与えられたURLのwebページを取得する。
    webページのエンコーディングはContent-Typeヘッダーから取得する。
    戻り値: str型のHTML
    """
    r = requests.get(url)
    return r.text # HTTPヘッダーから取得したエンコーディングでデコードした文字列を返す

def scrape(html: str, base_url: str) -> List[dict]:
    """
    引数htmlで与えられたHTMLから正規表現で書籍の情報を抜き出す。
    引数base_urlは絶対URLに変換する際の基準となるURLを指定する。
    戻り値: 書籍(dict)のリスト
    """

    books = []
    html = lxml.html.fromstring(html)
    html.make_links_absolute(base_url)

    # cssselect()メソッドで、セレクタに該当するa要素のリストを取得して、個々のa要素に対して処理を行う。
    # セレクタの意味： id="listBook"である要素の直接の子であるli要素の直接の子であるitemprop="url"という属性を持つa要素
    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        p = a.cssselect('p[itemprop="name"]')[0]
        title = p.text_content()

        books.append({'url': url, 'title': title})
    
    return books

def save(file_path: str, books: List[dict]):
    """
    引数booksで与えられた書籍のリストをCSV形式のファイルに保存する。
    ファイルのパスは引数file_pathで与えられる。
    戻り値: なし
    """
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader()
        writer.writerows(books)

if __name__ == '__main__':
    main()
