from flask import request, render_template, redirect, session, url_for, flash
import pymysql

def get_db_connection():
    return pymysql.connect(host='localhost', user='root',
                           password='0000', db='test', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

def register_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(
                  "SELECT id FROM users WHERE name=%s AND password=%s",
                  (username, password)
                )
                user = cur.fetchone()
            conn.close()
            if user:
                session['user_id'] = user['id']
                return redirect(url_for('modify_meal'))
            else:
                flash('잘못된 아이디 또는 비밀번호입니다.', 'error')
                return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
