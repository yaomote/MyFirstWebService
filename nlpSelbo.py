# -*- coding: utf-8 -*-

import CaboCha
import MeCab
import gc


def main(text):
    wakati_data = []
    dependency_data = []
    dependency_data_seirigo = []

    #形態素解析
    mecab = MeCab.Tagger()
    print(mecab.parse(text))
    wakati_data.extend(mecab.parse(text).split("\n"))
    del mecab
    del wakati_data
    del text
    gc.collect()

    #かかり受け解析
    #cabocha = CaboCha.Parser()
    #print(cabocha.parseToString(text))
    #dependency_data.extend(cabocha.parseToString(text).split("\n"))
    #for i in dependency_data:
    #    j = i.maketrans({' ': '', '　':''})
    #    dependency_data_seirigo.append(i.translate(j))
