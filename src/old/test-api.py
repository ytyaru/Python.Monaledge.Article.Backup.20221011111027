#!/usr/bin/env python3
# coding: utf8
import importlib
MonaledgeApi = importlib.import_module("monaledge-api")
print(MonaledgeApi)
api = MonaledgeApi.MonaledgeApi()
address = 'MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu'
user = api.my_info(address)
print(user)
print()
articles = api.my_articles(user['id'], 1)
print(articles)
print()
print(articles['articles'][0]['id'])
article = api.article(articles['articles'][0]['id'])
print(article)
print()

