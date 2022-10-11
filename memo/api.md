# モナレッジから自分の記事のマークダウンをすべて取得したい２
# モナレッジAPIを検索する

　モナレッジAPIがあると教えてもらったのでコードから検索してみた。

<!-- more -->

* [モナレッジから自分の記事のマークダウンをすべて取得したい][]

[モナレッジから自分の記事のマークダウンをすべて取得したい]:https://monaledge.com/article/459

> 今更ではあるんですけど、モナレッジのフロントではこんな感じで自分の記事を取ってきてるのでAPIの叩き方の参考にしていただければ　https://github.com/Raiu1210/omaemona_front/blob/master/pages/mypage/_page.vue#L63

* [_page.vue#L63][]:

[_page.vue#L63]:https://github.com/Raiu1210/omaemona_front/blob/master/pages/mypage/_page.vue#L63

## コードからAPIなどを検索する

* [search Api.get][]
* [search Api.post][]
* [search categories][]

[search Api.get]:https://github.com/Raiu1210/omaemona_front/search?q=Api.get
[search Api.post]:https://github.com/Raiu1210/omaemona_front/search?q=Api.post
[search categories]:https://github.com/Raiu1210/omaemona_front/search?q=categories

## API要点

* BASE_URL: `https://monaledge.com:8443`

API Endpoint|HTTP Method|data or query|result
------------|-----------|-------------|------
`/myInfo`|`POST`|`{address:モナコイン用アドレス}`|ユーザID等
`/myArticles`|`POST`|`{page:1, author_id:myInfo.id}`|所有記事ID等
`/article`|`GET`|`?id=記事ID`|記事(Markdownテキスト)

　おおむね以下の３ステップで全件取得する。

1. `myInfo`で指定したアドレスのユーザID等を返す
2. `myArticles`で指定したユーザIDが所有する記事ID等を返す（最新順に1ページ10件ずつ）
3. `article`で指定した記事IDのMarkdownテキスト等を返す

## 1. `myInfo`で指定したアドレスのユーザID等を返す

```sh
ADDRESS=MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu
URL=https://monaledge.com:8443
API_MYINFO=$URL/myInfo
DATA_MYINFO='{"address":"'$ADDRESS'"}'
HEADER='Content-Type:application/json'

API=$API_MYINFO
DATA=$DATA_MYINFO
curl -X POST -H $HEADER -d "$DATA" $API
```

```javascript
{"id":92,"name":"ytyaru","icon_image_path":"https://monaledge.com:8443/articleImages/1652177650934ytyaru.png","address":"MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu","createdAt":"2022-05-02T10:03:17.751Z","updatedAt":"2022-05-10T10:14:11.115Z"}
```

## 2. `myArticles`で指定したユーザIDが所有する記事ID等を返す（最新順に1ページ10件ずつ）

```sh
AUTHOR_ID=92
PAGE=1

URL=https://monaledge.com:8443
API_MYARTICLES=$URL/myArticles
DATA_MYARTICLES='{"page":'$PAGE',"author_id":'$ID'}'
HEADER='Content-Type:application/json'

API=$API_MYARTICLES
DATA=$DATA_MYARTICLES
curl -X POST -H $HEADER -d "$DATA" $API
```

```javascript
{"articlesCount":169,"articles":[{"id":558,"author_id":92,"title":"Electronでつぶやきを保存する20","sent_mona":0,"access":null,"ogp_path":"https://monaledge.com/1665103807918.png","category":8,"createdAt":"2022-10-07T00:50:08.011Z","updatedAt":"2022-10-07T00:50:08.011Z"},{"id":557,"author_id":92,"title":"Electronでつぶやきを保存する19","sent_mona":0,"access":13,"ogp_path":"https://monaledge.com/1665016960493.png","category":8,"createdAt":"2022-10-06T00:42:40.685Z","updatedAt":"2022-10-07T00:19:16.601Z"},{"id":556,"author_id":92,"title":"coininfoでアドレスを作成するCUIを作った 改","sent_mona":0,"access":27,"ogp_path":"https://monaledge.com/1664929087109.png","category":8,"createdAt":"2022-10-05T00:18:07.298Z","updatedAt":"2022-10-06T23:54:00.857Z"},{"id":555,"author_id":92,"title":"coininfoの全コイン種別を調べる【24種】改","sent_mona":0,"access":39,"ogp_path":"https://monaledge.com/1664840694443.png","category":8,"createdAt":"2022-10-03T23:44:54.602Z","updatedAt":"2022-10-06T20:53:14.493Z"},{"id":553,"author_id":92,"title":"coininfoでライトコイン用アドレスを作った","sent_mona":0.114114,"access":36,"ogp_path":"https://monaledge.com/1664754967119.png","category":8,"createdAt":"2022-10-02T23:56:07.225Z","updatedAt":"2022-10-06T13:58:02.322Z"},{"id":552,"author_id":92,"title":"electrum-clientを試したがエラーになった","sent_mona":0,"access":23,"ogp_path":"https://monaledge.com/1664675017696.png","category":8,"createdAt":"2022-10-02T01:43:38.031Z","updatedAt":"2022-10-06T14:14:09.425Z"},{"id":551,"author_id":92,"title":"coininfoでモナコイン用アドレスを作った","sent_mona":0,"access":41,"ogp_path":"https://monaledge.com/1664583692086.png","category":3,"createdAt":"2022-10-01T00:21:32.266Z","updatedAt":"2022-10-06T21:47:52.448Z"},{"id":550,"author_id":92,"title":"ビットコインのアドレスを作成した（bitcoinjs-lib, ecpair, tiny-secp256k1）","sent_mona":0,"access":48,"ogp_path":"https://monaledge.com/1664498328630.png","category":8,"createdAt":"2022-09-30T00:38:48.777Z","updatedAt":"2022-10-05T23:56:22.096Z"},{"id":549,"author_id":92,"title":"bitcoinjs-libを触ってみた","sent_mona":0,"access":38,"ogp_path":"https://monaledge.com/1664411638798.png","category":8,"createdAt":"2022-09-29T00:33:58.947Z","updatedAt":"2022-10-05T05:59:09.364Z"},{"id":548,"author_id":92,"title":"bitcoinjs-lib等を使ったコード例を読む（Node.jsでモナコイン送金できるか調査）","sent_mona":0,"access":75,"ogp_path":"https://monaledge.com/1664326129822.png","category":8,"createdAt":"2022-09-28T00:48:50.033Z","updatedAt":"2022-10-06T12:50:07.640Z"}]}
```

## 3. `article`で指定した記事IDのMarkdownテキスト等を返す

```sh
ARTICLE_ID=454

URL=https://monaledge.com:8443
API_ARTICLE=$URL/article?id=ARTICLE_ID
HEADER='Content-Type:application/json'

API=$API_ARTICLE
curl  -H $HEADER $API
```

```javascript
{"id":454,"author_id":92,"title":"モナコインを送金する方法を調べた","content":"　[mpurse][], [mpchain][], [counterParty][], [counterBlock][] APIを使えば送金できるはず。その方法を調査してみる。\n\n[mpurse]:https://github.com/tadajam/mpurse\n[mpchain]:https://mpchain.info/doc\n[counterBlock]:https://counterparty.io/docs/counterblock_api/\n[counterParty]:https://counterparty.io/docs/api/\n\n<!-- more -->\n\n# 結論\n\n...無謀な挑戦だったか。","sent_mona":0,"access":211,"ogp_path":"https://monaledge.com/1658283590367.png","category":3,"createdAt":"2022-07-20T02:19:50.531Z","updatedAt":"2022-10-07T07:27:34.037Z","user":{"id":92,"name":"ytyaru","icon_image_path":"https://monaledge.com:8443/articleImages/1652177650934ytyaru.png","address":"MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu","createdAt":"2022-05-02T10:03:17.751Z","updatedAt":"2022-05-10T10:14:11.115Z"},"comments":[{"id":211,"from":52,"article_id":454,"comment":"フルノードを立てずにでしたらこのあたりでしょうか\nhttps://qiita.com/cryptcoin-junkey/items/fc6d62c22d4444d98c45\n\nあとは各ウォレット（Monapaletteやもにゃ等）のソース等も大変参考になります。","createdAt":"2022-07-21T03:03:00.378Z","updatedAt":"2022-07-21T03:03:00.378Z","user":{"id":52,"name":"コタロ@駆け出し100兆MONAほしい侍","icon_image_path":"https://monaledge.com:8443/articleImages/1619234990674EL-n3CLUcAUoxrc.jpg","address":"MSgQuJGBkbnnV9i6ZozUfaRNmkq9j5tL3W","createdAt":"2021-04-24T03:29:02.181Z","updatedAt":"2021-11-21T04:46:08.779Z"}},{"id":212,"from":92,"article_id":454,"comment":"情報ありがとうございます！　色々な方法があるのですね。\nもっと単純にWebAPI一発でいけるかと思ってたのですが甘かったようです。\nソースコードは見つけましたが使ったことがないアプリな上にmpurseより複雑そう。私にはまだ難しそうな予感。いつか読み解きたいところです。\nhttps://bitbucket.org/anipopina/monapalette/commits/\nhttps://github.com/monya-wallet/monya","createdAt":"2022-07-25T00:58:49.006Z","updatedAt":"2022-07-25T00:58:49.006Z","user":{"id":92,"name":"ytyaru","icon_image_path":"https://monaledge.com:8443/articleImages/1652177650934ytyaru.png","address":"MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu","createdAt":"2022-05-02T10:03:17.751Z","updatedAt":"2022-05-10T10:14:11.115Z"}},{"id":210,"from":92,"article_id":454,"comment":"情報ありがとうございます！\n\nテスト環境あったのですね。testnet, mainnetというキーワードを教えていただけたので調べられそうです。少し調べた限り今の私には難しそうですが。\n\nトランザクション作成までならMONA消費なしでできるのですね。そうおっしゃっていただけると安心して試せます。そのうちまたAPIをいじってみようと思います。","createdAt":"2022-07-21T00:50:39.680Z","updatedAt":"2022-07-21T00:50:39.680Z","user":{"id":92,"name":"ytyaru","icon_image_path":"https://monaledge.com:8443/articleImages/1652177650934ytyaru.png","address":"MEHCqJbgiNERCH3bRAtNSSD9uxPViEX1nu","createdAt":"2022-05-02T10:03:17.751Z","updatedAt":"2022-05-10T10:14:11.115Z"}},{"id":209,"from":93,"article_id":454,"comment":"トランザクションを作成する機能は counterparty-server 側の API にあります。counterblock にはありません。\nAPI で無事トランザクションが生成されても無署名なのでブロックチェーンに投げ込んでも、無効扱いされ、手持ちの MONA は消えません。秘密鍵による署名が完了するまでは気軽に試しても問題ありません。testnet の API は存在しますが、testnet の MONA の入手は難しく、mainnet で試したほうが手間が少ないと思います。","createdAt":"2022-07-20T07:13:23.039Z","updatedAt":"2022-07-20T07:13:23.039Z","user":{"id":93,"name":"anonymous","icon_image_path":null,"address":"MUqM2tDnZXtJ4h87W2g8fFz9nW3GsYhMfu","createdAt":"2022-05-19T00:31:30.719Z","updatedAt":"2022-05-19T00:31:30.719Z"}}]}
```

```javascript
{
    id:
    author_id:
    title:
    content:
    sent_mona:
    access:
    ogp_path:
    category
    createdAt:
    updatedAt:
    user:{
        id:
        name:
        icon_image_path:
        address:
        createdAt:
        updatedAt:
    }
    comments:[
        {
            id:
            from:
            article_id:
            comment:
            user:{
                id:
                name:
                icon_image_path:
                address:
                createdAt:
                updatedAt:
            }
        },
        ...
    ]
}
```

