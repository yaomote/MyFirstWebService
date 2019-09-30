# -*- coding: utf-8 -*-

import urllib.request, urllib.error                         # urlアクセス
import requests                                             # urlアクセス
from bs4 import BeautifulSoup                               # web scraping用
from selenium import webdriver                              # 動的ページに対するscraping用
from selenium.webdriver.chrome.options import Options       # webdriverの設定用
import time                                                 # scrapingの時間制御用
import mysql.connector                                      # データベース操作用

import nlpSelbo                                             # 自然言語処理

from scrapySelboLocal import *                              # ローカル設定

# 本の感情辞書を作成
#emotions = {
#    '喜び': ['嬉し', '楽し', '幸せ', '気持ちい', 'ハッピーエンド', '気持ちよ', 'スッキリ', '笑い', '笑え', '満足', '爽快', '感動', '関心', '和む', '癒される', '落ち着く', 'ワクワク', '興奮', '高ぶる', '懐かし', '優し'],
#    '好き': ['愛する', '恋する', '憧れる', '欲する', '好み', '思いやり', '尊敬する', '気遣う', '同情', '尊敬', '大切な', 'あげたい', '素敵', '優し', '思いやり'],
#    '悲しみ': ['かわいそう', '寂し', '淋し', '悲し', '孤独', '困る', '憐れ', '嘆き', '気分が晴れない', '哀れ', '戸惑う', '辛い', '萎える', '心が痛む', '憂鬱', '失望', 'ため息', '虚しい', '情けない', '喪失感', '惨め', 'へこむ', 'がっかり', '屈辱', '切ない', '泣ける', '落胆', '重い', '死', '罪', '苦し', '残酷'],
#    '恐怖': ['怖い', '不気味', '躊躇', '不安', '心配', '青ざめる', '震える', '絶望', '息苦しい', '心細い', '鳥肌が立つ', '恐ろしい', '戦慄', '焦る'],
#    '不安・驚き': ['慌てる', '予想外', '悩む', '落ち込む', '悩ましい'],
#    '嫌い': ['嫌い', '馬鹿にする', '見下す', '憎む', '嫉妬', '困る', '戸惑う', '恨む', '苦笑する'],
#    '怒り': ['不愉快', '不機嫌', '我慢できない', '叱る', '文句を言う', '怒鳴る', 'イライラ', '呆れる'],
#    '力強い': ['我慢', '諦め', '辛抱', '耐える', '諦念', 'じれった'],
#    '悔やむ': ['後悔', '悔しい', '負い目を感じる', '罪悪感', '後ろめたい', '恨む', '惜しむ', '悔やむ', '負い目', 'モヤモヤ'],
#    '心が傷つく': ['つらく', '苦しい', 'せつない', '恥ずかしい', '心苦しい'],
#    '感動': ['感銘を受ける', '心打たれる', '胸に響く', '印象に残る', 'ウルウル', 'ほっこり'],
#    '興奮・緊張・気持ちが高ぶる・心が乱れる': ['気が急く', '強張る', '泣けてくる', '頑張る', '感動', '関心する', '興奮', '欲しい', 'ドキドキ', '萎縮する', '強張る', '強張る', '乱心', '苛立ち', '焦る', 'じれったい', '理性を失う', '赤面'],
#    '安心': ['安心する', 'スッキリする', '和む', '落ち着く', '自信がある', '温か', '温もり']
#}
emotions = {
    '思わず恋をしたくなる': ['キュン', 'きゅん', '心理描写', '恋愛', '胸に響', 'ウルウル', 'うるうる', 'ほっこり', '泣', '涙', '和ん', '和む', '落ち着', '暖か', '温か', '温もり', '感動', '恋', '愛', '愛する', '愛し', '恋する', '恋し', '憧れ', '好み', '好き', '思いやり', '尊敬', '大切', 'あげたい', '素敵', '優し', '自然な', '自然に', 'ふわっ', 'ふわふわ', 'キラキラ', '無邪気', '可愛', 'せつない', '切ない', '片思い', '成就', '病', '甘', 'ヒロイン', '幸', '手紙', '一途', 'ドキドキ', 'キス', '悲し', '報われ', '純粋', '想い', '羨まし', '初恋', '美し', 'じれった'],
    '心がすっと軽くなる': ['綺麗', '繊細', '心理描写', '心打たれ', '胸に響', 'ウルウル', 'ほっこり', '泣', '涙', '家族愛', '親子愛', '兄妹愛', '兄弟愛', '姉弟愛', '姉妹愛', '安心', 'スッキリ', '和ん', '和む', '落ち着', '温か', '温もり', '感動', '愛する', '愛し', '恋', '憧れ', '好み', '好き', '思いやり', '尊敬', '気遣う', '同情', '大切', 'あげたい', '素敵', '優し', '笑', '嬉し', '楽し', '幸', '気持ちい', '気持ちよ', 'ハッピーエンド', '満足', '爽快', '関心', '癒され', '癒し', 'ワクワク', '青春', '高ぶる', '懐かし', '優し', '透き通', '透明', '清々し'],
    #'爽やかで晴れやかな気分になる': [''],
    #'思わず余韻に浸ってしまう': [''],
    'ずっしりと重く残る': ['綺麗', '繊細', '心理描写', '感情移入', '罪', '死', '殺', '苦し', '悲し', '絶望', '断絶', '悲壮', '怖い', '不気味', '躊躇', '不安', '心配', '青ざめる', '震える', '息苦しい', '心細い', '鳥肌が立つ', '恐ろしい', '戦慄', '焦る', '感銘を受ける', '心打たれる', '胸に響く', '印象に残る', '切ない', 'せつない', '後悔', '悔しい', '負い目を感じる', '罪悪感', '後ろめたい', '恨む', '惜しむ', '悔やむ', '負い目', 'モヤモヤ', '馬鹿にする', '見下す', '憎', '嫉妬', '恨', 'かわいそう', '寂し', '淋し', '孤独', '憐れ', '嘆き', '気分が晴れない', '哀れ', '辛い', '心が痛', '憂鬱', '失望', 'ため息', '虚し', '情けない', '喪失感', '惨め', '屈辱', '泣ける', '重い', '残酷']
}

# Web Scraping
def main():
    # データベースの接続
    connectDB = ConnectDB()
    conn = connectDB.connect()
    # 接続が切れたときに再接続できるように、定期的にpingを送る。
    conn.ping(reconnect=True)

    if (conn.is_connected() == True): # 接続 正常
        print('\n-------------MYSQL 接続完了-------------\n')
        # カーソルオブジェクトを作成。これでexecuteメソッドを使ってクエリを実行できる。
        cur = conn.cursor()

        for i in range(1449, 10000):
            #本IDを格納
            id = i
            # アクセスするURL
            #url = f"https://bookmeter.com/books/{i}"
            # URLにアクセスする htmlが帰ってくる → <html><head><title>例例例</title></head><body....
            #html = urllib.request.urlopen(url=url)
            # ブラウザのオプションを格納する変数をもらってくる。
            options = Options()
            # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がる）
            options.set_headless(True)
            # ブラウザを起動
            driver = webdriver.Chrome(chrome_options=options, executable_path='C:\\chromedriver.exe')
            #スクレイピングの間隔を開ける
            time.sleep(3)
            # ブラウザでアクセスする
            driver.get(f"https://bookmeter.com/books/{i}")
            # HTMLを文字コードをUTF-8に変換してから取得します。
            html = driver.page_source.encode('utf-8')
            # htmlをBeautifulSoupで扱う
            soup = BeautifulSoup(html, "html.parser")

            #--------タイトル---------#
            # タイトル要素を取得する → <〇〇 class="inner__title">例例例例例例<〇〇>
            title_tag = soup.find(class_='inner__title')
            # 要素の文字列を取得する → 例例例例例例
            title = title_tag.string
            title = str(title)

            #--------著者---------#
            # 著者要素を取得する → <〇〇 class="header__authors">例例例例例例<〇〇>
            author_tag = soup.find(class_='header__authors')
            # 要素の文字列を取得する → 例例例例例例
            author = author_tag.string
            author = str(author)

            #--------本画像---------#
            # 画像要素を取得する → <〇〇 class="header__authors">例例例例例例<〇〇>
            image_tag = soup.select_one('div.group__image > a > img')
            image_src = image_tag.get('src')
            # 画像保存
            re = requests.get(image_src)
            image_path = f'{MEDIA_URL}' + image_src.split('/')[-1]
            with open(image_path, 'wb') as f:
                f.write(re.content)
            image = 'selbo/' + image_src.split('/')[-1]
            # 要素の文字列を取得する → 例例例例例例
            print(f'\nimage_tag = {image_tag}\nimage_src = {image_src}\n{type(image_tag)}\nimage = {image}\n')

            print(f'\n-------------title = {title}, author = {author}-------------\n')

            #--------感情属性決定---------#
            # content要素を取得する → <div>例例例</div>
            j = 1
            pagenationFlag = True
            emotionCountTmp = 0
            emotionListNum = 0
            emotionNum = 0
            maxEmotionCount = 0
            maxEmotion = ''
            maxEmotionList = ''
            corpus = ''

            while pagenationFlag == True:
                if j != 1:
                    # page=1のアクセスを切る
                    driver.quit()
                    # ブラウザのオプションを格納する変数をもらってくる。
                    options = Options()
                    # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がる）
                    options.set_headless(True)
                    # ブラウザを起動
                    driver = webdriver.Chrome(chrome_options=options, executable_path='C:\\chromedriver.exe')
                    # スクレイピングの間隔を開ける
                    time.sleep(5)
                    # ブラウザでアクセスする
                    driver.get(f"https://bookmeter.com/books/{i}?page={j}")
                    print(f"\n-------------https://bookmeter.com/books/{i}?page={j}-------------\n")
                else:
                    print(f"\n-------------https://bookmeter.com/books/{i}-------------\n")
                # HTMLを文字コードをUTF-8に変換してから取得します。
                html = driver.page_source.encode('utf-8')
                # htmlをBeautifulSoupで扱う
                soup = BeautifulSoup(html, "html.parser")

                content_elements = soup.select('.frame__content__text')
                for content_element in content_elements:
                    print(f"\n-------------content_element.text-------------\n{content_element.text}")
                    for emotionList in emotions:
                        for emotion in emotions[emotionList]:
                            emotionCount = content_element.text.count(f'{emotion}')
                            emotionCountDict[f'{emotionListNum}'][emotionNum] = int(emotionCountDict[f'{emotionListNum}'][emotionNum]) + emotionCount
                            emotionNum += 1
                        emotionNum = 0
                        emotionListNum += 1
                    emotionListNum = 0
                    corpus += f'{content_element.text}\n'

                for emotionList in emotions:
                    for emotion in emotions[emotionList]:
                        if maxEmotionCount < int(emotionCountDict[f'{emotionListNum}'][emotionNum]):
                            maxEmotionCount = int(emotionCountDict[f'{emotionListNum}'][emotionNum])
                            maxEmotion = emotion
                            maxEmotionList = emotionList
                        emotionNum += 1
                    emotionNum = 0
                    emotionListNum += 1
                emotionListNum = 0
                driver.quit()

                # レビューが複数ページにわたる場合
                for pagenation in soup.select('.bm-pagination__link'):
                    if pagenation.text == f'{j+1}':
                        j += 1
                        pagenationFlag = True
                        break
                    else:
                        pagenationFlag = False
                        driver.quit()

            print(f'\n-------------emotionCountDict-------------\n{emotionCountDict}')
            print(f'\n-------------corpus-------------\n{corpus}')

            nlpSelbo.main(corpus)

            # emotionCountDictの初期化
            emotionCountDict.clear()
            for emotionList in emotions:
                for emotion in emotions[emotionList]:
                    emotionCountDict.setdefault(f'{emotionListNum}', []).append('0')
                emotionListNum += 1
            emotionListNum = 0

            # データベース更新
            try:
                sql = """
                INSERT INTO selbo_book (
                    book_id,
                    book_title,
                    author_name,
                    book_attribute,
                    book_image
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON DUPLICATE KEY UPDATE
                    book_id = VALUES (book_id),
                    book_title = VALUES (book_title),
                    author_name = VALUES (author_name),
                    book_attribute = VALUES (book_attribute),
                    book_image = VALUES (book_image)
                """
                cur.execute(sql, (id, title, author, maxEmotionList, image))
                conn.commit()
            except:
                conn.rollback()
                raise

            print(f'\n-----------{i}冊目 完了----------\n')

            #cur.execute('SELECT book_title FROM selbo_book')
            #result = cur.fetchall()
            #print(result)

        print('\n-----------scraping 完了----------\n')

        return
    else:
        return

if __name__ == '__main__':
    # 画像保存パス
    MEDIA_URL = 'media/selbo/'
    # 感情属性のカウント用初期設定
    emotionListNum = 0
    emotionNum = 0
    emotionCountDict = {}
    emotionTotalCount = []

    # 初期化処理
    for emotionList in emotions:
        for emotion in emotions[emotionList]:
            emotionCountDict.setdefault(f'{emotionListNum}', []).append('0')
        emotionListNum += 1

    # メイン関数
    main()
