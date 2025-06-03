from flask import request, render_template, redirect, url_for, flash, session
import pymysql

def get_db_connection():
    return pymysql.connect(host='localhost', user='root',
                           password='0000', db='test', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

def register_routes(app):
    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            fullname = request.form['fullname']
            password = request.form['password']
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE name=%s", (username,))
                if cur.fetchone():
                    flash('이미 존재하는 아이디입니다.', 'error')
                    return redirect(url_for('register'))
                cur.execute(
                  "INSERT INTO users (name,password,fullname) VALUES (%s,%s,%s)",
                  (username, password,fullname)
                )
                conn.commit()
            conn.close()
            flash('회원가입이 완료되었습니다. 로그인 해주세요.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')
