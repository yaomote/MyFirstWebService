import urllib.request, urllib.error
from bs4 import BeautifulSoup
import time
import mysql.connector

from scrapySelboLocal import *
import logging

# Web Scraping
def scraping():
    # データベースの接続
    connectDB = ConnectDB()
    conn = connectDB.connect()
    # 接続が切れたときに再接続できるように、定期的にpingを送る。
    conn.ping(reconnect=True)

    if (conn.is_connected() == True): # 接続 正常
        print('\n-------------MYSQL 接続完了-------------\n')
        # カーソルオブジェクトを作成。これでexecuteメソッドを使ってクエリを実行できる。
        cur = conn.cursor()

        for i in range(20):
            # アクセスするURL
            url = f"https://bookmeter.com/books/{i+1}"
            #url = "https://bookmeter.com/books/13963455"
            # URLにアクセスする htmlが帰ってくる → <html><head><title>例例例</title></head><body....
            html = urllib.request.urlopen(url=url)
            # htmlをBeautifulSoupで扱う
            soup = BeautifulSoup(html, "html.parser")
            # タイトル要素を取得する → <title>例例例例例例</title>
            title_tag = soup.find(class_='inner__title')
            #title_tag = soup.title
            # 要素の文字列を取得する → 例例例例例例
            title = title_tag.string
            title = str(title)

            # データベース更新
            try:
                sql = """
                    INSERT INTO selbo_book (book_title, author_name, book_attribute)
                    VALUES (%s, 'test', 'test')
                    ON DUPLICATE KEY UPDATE book_title = VALUES (book_title)
                    """
                cur.execute(sql, (title, ))
                conn.commit()
            except:
                conn.rollback()
                raise

            #cur.execute('SELECT book_title FROM selbo_book')
            #result = cur.fetchall()
            #print(result)

            #スクレイピングの間隔を開ける
            time.sleep(5)

        print('\n-----------scraping完了----------\n')
        return
    else:
        return

scraping()
