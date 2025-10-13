#　環境構築
```zsh
cd login_normal
python3 -m venv .venv
source .venv/bin/activate
pip install flask bcrypt
```
## アカウント新規作成
```zsh
curl -v -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
--data "username=testuser&password=secret123" \
-L http://127.0.0.1:5000/register
```
## ログイン
```zsh
curl -v -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
--data "username=testuser&password=secret123" \
-c cookies.txt \
-L http://127.0.0.1:5000/login
```
## クッキーで保護ページにアクセス
```zsh
curl -v -b cookies.txt http://127.0.0.1:5000/
```
## プロフィール取得（存在するユーザー名で）
```zsh
curl 'http://127.0.0.1:5000/api/user?name=testuser'
```
## ユーザー投稿一覧
```zsh
curl 'http://127.0.0.1:5000/api/post/user?name=testuser'
```
## 最新投稿
```zsh
curl 'http://127.0.0.1:5000/api/post/latest?limit=10'
```
## 投稿作成（JSON）
```zsh
curl -X POST 'http://127.0.0.1:5000/api/post/make' \
-H 'Content-Type: application/json' \
-d '{"text":"テスト投稿","user":{"name":"testuser"},"good":0,"heart":0,"createAt":"2025-10-13T00:00:00Z"}'
```

仕様変更：変更箇所

バックエンドの設計を変えてください。

ユーザの投稿 テーブルを追加してください
ログイン情報のテーブルの設計を変更してください
今作っているアプリは
ログイン、およびサインアップ（/register）を作ることでログイン機能を作りますがユーザの情報などを保管する機能がありません。
getリクエスト

自己紹介 などプロフィールを取得できる/user?name="[username]"、types/user.tsのUserGetDataを参照してそこに当てはまる結果をjsonで返してください
ユーザの投稿/post/user?name="[username]"、types/labelのLabelTypesを参照してそこに当てはまる値をjsonで返してください
最新の投稿を取得/post/latest、types/labelのLabelTypesを参照してそこに当てはまる値をjsonで返してください
postリクエスト

新しい投稿を作成 /post/make
bodyにtypes/labelのLabelTypeのjsonが与えられます
