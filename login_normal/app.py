from flask import Flask, render_template, request, redirect, session, jsonify

import sqlite3  # SQLiteデータベース操作用の標準ライブラリをインポート

import bcrypt  # パスワードのハッシュ化・検証のためのbcryptライブラリをインポート

app = Flask(__name__)  # Flaskアプリケーションのインスタンスを生成

app.secret_key = 'your_secret_key'  # セッションの暗号化に必要な秘密鍵を設定

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    if 'username' in session:
        return f"ようこそ、{session['username']}さん！ <a href=/logout>ログアウト</a>"
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['username'] = username
            return redirect('/')
        else:
            return "ログイン失敗"

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        name = request.form.get('name') or username
        bio = request.form.get('bio') or ''
        ico = request.form.get('ico') or '/favicon.ico'

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, name, bio, ico) VALUES (?, ?, ?, ?, ?)",
                           (username, password.decode('utf-8'), name, bio, ico))
            conn.commit()
        except sqlite3.IntegrityError:
            return "ユーザー名が既に使われています"
        finally:
            conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


# API: get user profile by username
@app.route('/api/user')
def api_get_user():
    username = request.args.get('name')
    if not username:
        return jsonify({'error': 'name parameter required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, name, bio, ico FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'user not found'}), 404

    # UserGetData shape: map to expected keys
    user = {
        'id': row['id'],
        'username': row['username'],
        'name': row['name'],
        'bio': row['bio'],
        'ico': row['ico'],
    }
    return jsonify(user)


# API: get posts by username
@app.route('/api/post/user')
def api_get_posts_by_user():
    username = request.args.get('name')
    if not username:
        return jsonify({'error': 'name parameter required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return jsonify({'d': []})

    user_id = user['id']
    cursor.execute("SELECT text, good, heart, createAt FROM posts WHERE user_id=? ORDER BY id DESC", (user_id,))
    posts = cursor.fetchall()
    conn.close()

    d = []
    for p in posts:
        d.append({
            'text': p['text'],
            'user': {'id': user_id, 'name': username, 'ico': ''},
            'good': p['good'],
            'heart': p['heart'],
            'createAt': p['createAt'],
        })

    return jsonify({'d': d})


# API: get latest posts
@app.route('/api/post/latest')
def api_get_latest_posts():
    limit = int(request.args.get('limit') or 20)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT p.text, p.good, p.heart, p.createAt, u.id as user_id, u.username as username, u.ico as ico FROM posts p JOIN users u ON p.user_id = u.id ORDER BY p.id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()

    d = []
    for r in rows:
        d.append({
            'text': r['text'],
            'user': {'id': r['user_id'], 'name': r['username'], 'ico': r['ico']},
            'good': r['good'],
            'heart': r['heart'],
            'createAt': r['createAt'],
        })

    return jsonify({'d': d})


# API: create new post
@app.route('/api/post/make', methods=['POST'])
def api_make_post():
    data = request.get_json() or request.form
    # expected LabelType: text, user (with id/name/ico), good, heart, createAt
    text = data.get('text')
    user = data.get('user')
    good = int(data.get('good') or 0)
    heart = int(data.get('heart') or 0)
    createAt = data.get('createAt') or ''

    if not text or not user:
        return jsonify({'error': 'text and user required'}), 400

    user_id = user.get('id')
    # if user_id is not provided, try to find by username
    if not user_id:
        username = user.get('name')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        u = cursor.fetchone()
        if not u:
            conn.close()
            return jsonify({'error': 'user not found'}), 404
        user_id = u['id']
        conn.close()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (text, user_id, good, heart, createAt) VALUES (?, ?, ?, ?, ?)", (text, user_id, good, heart, createAt))
    conn.commit()
    conn.close()

    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(debug=True)
    