import os
from db import Db
class MonaledgeDb(Db):
    def __init__(self):
        super().__init__('monaledge.db')
        self.create_table()
        print('MonaledgeDb()')
    def __del__(self): super().__del__()
    def create_table(self):
        print('create_table')
        if self._exists_table(): return
        for name in ['users', 'categories', 'articles', 'comments']:
            self._exec_create_table(os.path.join('sql', name + '.sql'))
        print('create_table 2')
    def _exists_table(self): return 0 < self.exec("select count(*) from sqlite_master where type='table'").fetchone()[0]
    def _exec_create_table(self, path):
        with open(path, 'r', encoding='UTF-8') as f:
            self.execs(f.read())
    def _exiest_record(self, table, id): return 0 < self.exec(f"select count(*) from {table} where id = {id}").fetchone()[0]
    def exists_user(self, id): return self._exiest_record('users', id)
    def insert_user(self, user): #user:myInfo API JSON結果
        self.execm("insert into users values(?,?,?,?,?,?);", [(user['id'], user['address'], user['created'], user['updated'], user['name'], user['icon_image_path'])])
    def update_user(self, user):
        self.execm("update users set address=?, created=?, updated=?, name=?, icon_image_path=? where id = ?;", [(user['address'], user['createdAt'], user['updatedAt'], user['name'], user['icon_image_path'], user['id'])])
    def upsert_user(self, user):
        self.exec(
            "insert into users values(?,?,?,?,?,?) on conflict(id) do update set address=?, created=?, updated=?, name=?, icon_image_path=? where updated < excluded.updated;", 
            (user['id'], user['address'], user['createdAt'], user['updatedAt'], user['name'], user['icon_image_path'], 
                          user['address'], user['createdAt'], user['updatedAt'], user['name'], user['icon_image_path']))
    def exists_article(self, id): return self._exiest_record('articles', id)
    def get_article(self, id): return self.exec("select * from articles where id = ?", (id, )).fetchone()
    def get_article_updated(self, id): return self.get_article(id)[2]
    def insert_article(self, article, content):
        self.exec("insert into articles values(?,?,?,?,?,?,?,?,?);", (article['id'], article['createdAt'], article['updatedAt'], article['title'], article['sent_mona'], article['access'], article['ogp_path'], article['category_id'], content))
    def update_article(self, article, content):
        self.exec("update articles created=?, updated=?, title=?, sent_mona=?, access=?, ogp_path=?, category_id=? content=? where id = ?;", (article['createdAt'], article['updatedAt'], article['title'], article['sent_mona'], article['access'], article['ogp_path'], article['category_id'], content, article['id']))
    def upsert_article(self, article, content):
        self.exec("insert into articles values(?,?,?,?,?,?,?,?,?) on conflict(id) do update set created=?, updated=?, title=?, sent_mona=?, access=?, ogp_path=?, category_id=?, content=? where updated < excluded.updated;", 
            (
                article['id'], article['createdAt'], article['updatedAt'], article['title'], article['sent_mona'], article['access'], article['ogp_path'], article['category'], content,
                               article['createdAt'], article['updatedAt'], article['title'], article['sent_mona'], article['access'], article['ogp_path'], article['category'], content
            ))
    def exists_comment(self, id): return self._exiest_record('comments', id)
    def upsert_comments(self, comments):
        self.execm("insert or ignore into comments values(?,?,?,?,?,?);", list(map(lambda c: (c['id'], c['article_id'], c['createdAt'], c['updatedAt'], c['user']['id'], c['comment']), comments)))

