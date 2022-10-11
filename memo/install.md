SQLite3が使えるようPython3.10.5をビルドする

　30分くらいかかる。

<!-- more -->

# 目次

1. Pythonをインストールする
	1. Python依存ライブラリ
	1. anyenv
	1. pyenv
	1. Python 3.10.5
	1. 使用するpythonのバージョンを指定する
2. SQLite3をインストールする
	1. ソースコードをダウンロードする（SQLite 3.39.4）
	1. コンフィグを確認＆セットする
	1. ビルドする
	1. 配置する
	1. パスを通す
3. PythonでSQLite3を使う
	1. ソースコードを書く
	1. 実行する

# 1. Pythonをインストールする

## 依存ライブラリをインストールする

　まずはPythonで使う依存ライブラリをインストールしておく。ここ大事。`libsqlite3-dev`を入れてから後述するPythonビルドをしないと`import sqlite3`が使えない。Pythonをビルドし直すハメになる。

```sh
sudo apt install -y libsqlite3-dev libbz2-dev libncurses5-dev libgdbm-dev liblzma-dev libssl-dev tcl-dev tk-dev libreadline-dev
```

## anyenvをインストールする

```sh
git clone https://github.com/anyenv/anyenv ~/.anyenv
echo 'export PATH="$HOME/.anyenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(anyenv init -)"' >> ~/.bash_profile
anyenv install --init
```

　以下のように出るので`y`を入力しEnterキーを押す。

```sh
Manifest directory doesn't exist: /home/pi/.config/anyenv/anyenv-install
Do you want to checkout https://github.com/anyenv/anyenv-install.git? [y/N]: 
```

　ログが出て最後は以下のようになる。

```sh
...
Completed!
```

## pyenvをインストールする

```sh
anyenv install pyenv
exec $SHELL -l
```

## pythonをインストールする

　まずはバージョンを確認する。

```sh
pyenv install --list
```

　一覧から好きなのを選ぶ。今回は`3.10.5`。

```sh
pyenv install 3.10.5
```

　ちなみに既存のときは上書き確認が出るので`y`で実行すればビルドし直してくれる。所要時間10分位。

## 使用するpythonのバージョンを指定する

```sh
pyenv global 3.10.5
```

　以下で確認する。

```sh
pyenv version
```

# 2. SQLite3をインストールする

## ソースコードをダウンロードする（SQLite 3.39.4）

　[download][]から最新かつ自分の環境にあったコードを取得する。

[download]:https://www.sqlite.org/download.html

```sh
YEAR="$(date +%Y)"
NAME=sqlite-autoconf-3390400
ZIP=${NAME}.tar.gz
wget https://www.sqlite.org/$YEAR/$ZIP
tar -zxvf $ZIP
cd $NAME
```

## コンフィグを確認＆セットする

## 確認

```sh
./configure --help
```

## セット

```sh
./configure --enable-readline
```

## ビルドする

```sh
time make
```

　所要時間10分位。

## 配置する

　ディレクトリ一式をすべて任意パスに配置する。

　異なるバージョンをインストールするかもしれないので`sudo make install`はしない。

## パスを通す

```sh
export PATH=任意パス:$PATH
```

　`任意パス`は`sqlite3`コマンドが存在するディレクトリパス。

　Pythonで参照するライブラリに`SQLite3パス/.libs`をセットする。

```sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:SQLite3パス/.libs
```

# 3. PythonでSQLite3を使う

## ソースコードを書く

```sh
vim hello.py
```

### hello.py

```python
#!/usr/bin/env python3
# coding: utf8
import sqlite3
con = sqlite3.connect(':memory:')
cur = con.cursor()
for row in cur.execute("select 'Hello SQLite3 !!';"):
	print(row[0])

```

　SQLite3のAPIは[sqlite3.html][]参照。

[sqlite3.html]:https://docs.python.org/ja/3/library/sqlite3.html

## 実行する

```sh
python hello.py
```
```sh
Hello SQLite3 !!
```

　OK！　動作した。お疲れ様でした。

　

