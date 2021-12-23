from flask import Flask
from flask import session
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for

import pymysql
import OpenSSL

app = Flask(__name__)

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='mysql1234!@',
    db='flask_post_db',
    charset='utf8',
    port=2003
)

curs = conn.cursor()

# 페이지 템플릿
pagination = {
}

# mysql> CREATE TABLE posts(
#     -> title VARCHAR(100) DEFAULT '',
#     -> author VARCHAR(20) DEFAULT '',
#     -> content VARCHAR(100) DEFAULT '');
# Query OK, 0 rows affected (0.03 sec)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        if title != '' and author != '' and content != '':
            sql = "INSERT INTO posts VALUES ('%s', '%s', '%s')" % (title, author, content)
            curs.execute(sql)
            data = curs.fetchall()
            curs.close()
            conn.close()
            if not data:
                conn.commit()
                print('게시글 업로드 완료!')
                return ''
            else:
                conn.rollback()
                return "알 수 없는 작업입니다."
    elif request.method == 'GET':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        content = request.args.get('content', '')
        if title != '' and author != '' and content != '':
            sql = "INSERT INTO posts VALUES ('%s', '%s', '%s')" % (title, author, content)
            curs.execute(sql)
            data = curs.fetchall()
            curs.close()
            conn.close()
            if not data:
                conn.commit()
                print('게시글 업로드 완료!')
                return ''
            else:
                conn.rollback()
                return "알 수 없는 작업입니다."

        return render_template('main.html')
    else:
        return "GET 또는 POST 접근만 허용"


@app.route('/list/', methods=['GET', 'POST'])
def listFun():
    # 게시글 목록으로 이동
    # TODO.. obj 안에 모든 게시글 담기

    curs.execute("SELECT title, author, content FROM posts")
    data = curs.fetchall()

    data_list = []

    for obj in data:
        mapping = {
            'title': obj[0],
            'author': obj[1],
            'content': obj[2]
        }
        data_list.append(mapping)

    return render_template('list.html', data_list=data_list)
