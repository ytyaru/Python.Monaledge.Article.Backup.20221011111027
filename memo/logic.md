# 記事バックアップのビジネスロジック

　WebAPIで最新順に10件ずつ取得される。日をまたいで不定期に取得するとき、できるだけ少ないリクエストで全記事をバックアップしたい。

* myArticles APIで自分の記事データを全件取得する
    * DBのデータと比較する
        * レコードが存在しない
            * article APIで記事の本文を取得する
            * レコードを挿入する
        * レコードが存在する
            * 更新日時が古くなっていたら
                * article APIで記事の本文を取得する
                * myArticlesのレコードを更新する

　もしarticle APIで記事本文を常に取得するのであれば、UPSERTが使えた。

```sql
insert into articles(article_id,created,updated,title,sent_mona,access,ogp_path,category,content) 
values (...)
on conflict(id, updated) 
do update set 
    updated = updated, 
    title = title,
    sent_mona = sent_mona,
    access = access,
    ogp_path = ogp_path,
    category = category,
    content = content 
```

　ただ、レコードが既存で更新日時が同じなら本文を取得する必要がない。本文の取得は別のarticle APIなので、条件次第では発行しない。

* 何もしない条件
    * レコードが既存である: `article_id`
    * 更新日時が同一である
* UPSERTする条件（上記以外）

　気になるのは、`access`や`sent_mona`などのデータ。更新日時が変更される条件がわからない。もしタイトルや本文を修正したときなら、今回の想定でよい。でも、`access`や`sent_mona`は変更されても更新日時が変わらないことがあるかもしれない。どうせmyArticlesは必ず取得するのだから、毎回上書きでいいかもしれない。でもそうなると書き込み回数や量がムダに増えるのでやはり避けたい。

---------------------------------------

* DBに指定した記事が
	* 存在しない
		* APIで本文を取得し挿入する
	* 存在する
		* 更新日時が古い：APIで本文を取得し更新する
		* 更新日時が同じ：何もしない
			* 念の為すべての値が同じであることを確認する
				* もし違えば本文以外を更新する
					* ただし`access`や`sent_mona`など本文やコメント以外のものの変更まで更新すべきか疑問

　パターンは3通り。とりあえず記事が既存のときは更新日時のみで判定する。

* insert
* update
* 何もしない

```sql
select exists(select * from articles id = id);
```

```sql
select count(*) from  articles id = id;
```

```sql
insert into user values (2, 'hoge', 'hogefuga') on conflict(id) do update set description = 'fugafuga';
```

　[UPSERT][]によると`excluded`修飾子を使えば、挿入されるときの新しい値が参照できる。これを使って更新日時が新しいか否かを判定する。

[UPSERT]:https://www.sqlite.org/lang_UPSERT.html

```sql
insert into articles(id,created,updated,title,sent_mona,access,ogp_path,category,content) 
values (...)
on conflict(id) 
do update set 
    updated = updated, 
    title = title,
    sent_mona = sent_mona,
    access = access,
    ogp_path = ogp_path,
    category = category,
    content = content 
   where updated < excluded.updated
```

　ただ、article APIで記事の本文を取得するか否かを判定せねばならない。事前に取得すればいいのだが、もし更新日時が同じだったら記事を取得する必要がない。ムダな処理をしたくないので、更新日時が同じときは本文を取得しないようにしたい。そのときは更新処理もしないようにしたい。となるとUPSERT文は使えない。プログラミングによってルーティングするしかない。

```python
myArticles = Api.myArtiles()
for article of myArticles:
    id = article['id']
    method = Db.insert_article
    if Db.exists_article(id):
        if article['updatedAt'] <= Db.get_article(id)['updated']: continue
        else: method = update_article
    content = Api.article(article['id'])
    method(article, content)
Db.commit()
```

