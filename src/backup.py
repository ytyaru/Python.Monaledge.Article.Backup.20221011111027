from db import Db
import importlib
MonaledgeApi = importlib.import_module("monaledge-api")
MonaledgeDb = importlib.import_module("monaledge-db")
import os
# ビジネスロジック。モナレッジAPIから最新取得しDB挿入・更新する。
class Backup:
    def __init__(self):
        self._api = MonaledgeApi.MonaledgeApi()
        self._db = MonaledgeDb.MonaledgeDb()
        self._article_count = -1
        print('Backup()')
    #def __del__(self): self._db.__del__()
    def run(self, address='MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu'):
        user = self._api.my_info(address)
        self._db.upsert_user(user)
        self.paginate(user['id'])
    def paginate(self, author_id, page=1):
        articles = self._api.my_articles(author_id, page)
        for article in articles['articles']:
            print(f"---- {article['id']} -----")
            print(article)
            print(article['id'])
            self.upsert_article(article)
        if 1 == page: self._article_count = articles['articlesCount']
        self._article_count -= len(articles['articles'])
        if 0 < self._article_count: self.paginate(author_id, page+1)
        self._db.commit()
    #def is_changed(self, id, updated): return not self._db.exists_article(id) or self._db.get_article_updated(id) < updated
    def is_changed(self, id, updated):
        print('----- is_changed -----')
        print(id)
        print(self._db.exists_article(id))
        print(self._db.get_article_updated(id) < updated)
        print(self._db.get_article_updated(id))
        print(updated)
        return not self._db.exists_article(id) or self._db.get_article_updated(id) < updated
    def upsert_article(self, article):
        id = article['id']
        if not self.is_changed(id, article['updatedAt']): return
        a = self._api.article(id)
        self._db.upsert_article(article, a['content'])
        self._db.upsert_comments(a['comments'])

