from flask import request, render_template,jsonify, session, redirect, url_for, flash
import pymysql

#데이터 베이스 연결
#데이터베이스 host, user, pswd, db명이 상이하면 연결 불가 -> 추후 맞출 것
def get_db_connection():
    return pymysql.connect(host='localhost',user='root',
                           password='0000',db='test',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
# register_routes()가 없으면 app에서 에러 발생하여 register_routes() 함수 안에 각 라우팅 함수 작성
def get_user_info(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, fullname FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user if user else {'name': 'Unknown', 'fullname': 'Unknown'}

def register_routes(app):
    # 기본 페이지 로드 
    @app.route('/modify',methods=['GET'])
    def modify_meal():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        return render_template("modify.html",user_id=user_id)
    
    # 로드 후 사용자의 최근 식단 기본으로 조회
    @app.route('/modify/list', methods = ['POST'])
    def get_meal():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400
        # if (not user_id) or user_id == '0':
        #     user_id = '1'
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
        SELECT id, menu,date,time
        FROM diets
        WHERE user_id = %s
        ORDER BY 
            date DESC,
            CASE time
                WHEN '저녁' THEN 1
                WHEN '점심' THEN 2
                WHEN '아침' THEN 3
            END ASC
        LIMIT 10
        """
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()

        result = [
        {
            "id": row['id'],
            "menu": row['menu'],
            "date": row['date'],
            "time": row['time']
        }
            for row in rows
        ]
        
        conn.close()
        return jsonify(result)
    
    # 조회 버튼 클릭 시 호출 함수 (식단 조회)
    @app.route('/modify/search', methods=['POST'])
    def search_meal():
        data = request.get_json()
        year = data['year']
        month = data['month']
        day = data['day']
        time = data['time']
        
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400
            
        # if user_id == 0:
        #     user_id = '1'

        # 조건 조립
        conditions = ["user_id = %s"]
        values = [user_id]

        if year and month:
            if day:
                date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                conditions.append("date = %s")
                values.append(date)
            else:
                date_prefix = f"{year}-{month.zfill(2)}"
                conditions.append("DATE_FORMAT(date, '%%Y-%%m') = %s")
                values.append(date_prefix)
        
        if time:
            conditions.append("time = %s")
            values.append(time)

        where_clause = " AND ".join(conditions)

        sql = f'''
            SELECT id, menu, date, time
            FROM diets
            WHERE {where_clause}
            ORDER BY 
                date DESC,
                CASE time
                    WHEN '저녁' THEN 1
                    WHEN '점심' THEN 2
                    WHEN '아침' THEN 3
                END ASC
            LIMIT 100
        '''

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, tuple(values))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = [{'id': row['id'], 'menu': row['menu'], 'date': row['date'], 'time': row['time']} for row in rows]

        return jsonify(result)

    # +버튼 클릭 시 호출 함수 (식단 추가)
    @app.route('/modify/add', methods=['POST'])
    def add_meal():
        data = request.get_json()
        menu = data['menu']
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400
        
        year = data['year']
        month = data['month']
        day = data['day']
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        time = data['time']
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
        SELECT COUNT(*) FROM diets 
        WHERE user_id = %s AND date = %s AND time = %s
        ''', (user_id, date, time))
        row = cur.fetchone()
        count = row['COUNT(*)']

        if count > 0:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'reason': '해당 날짜와 시간에 식단이 존재합니다.'}), 400
        
        cur.execute('''INSERT INTO diets 
                    (user_id, menu, date, time)
                    VALUES (%s,%s,%s,%s)
                    ''', (user_id,menu,date,time))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'success'})

    @app.route('/modify/update', methods=['POST'])
    def update_meal():
        data = request.get_json()
        meal_id = data.get('id')
        menu = data.get('menu')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        time = data.get('time')

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400

        date = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"

        conn = get_db_connection()
        cur = conn.cursor()

        # 해당 식단 존재 여부 확인
        cur.execute('''
            SELECT COUNT(*) AS cnt FROM diets
            WHERE id = %s AND user_id = %s
        ''', (meal_id, user_id))
        row = cur.fetchone()
        if row['cnt'] == 0:
            cur.close()
            conn.close()
            return jsonify({'error': '해당 식단이 존재하지 않습니다.'}), 404

        # 식단 수정 쿼리
        cur.execute('''
            UPDATE diets
            SET menu = %s, date = %s, time = %s
            WHERE id = %s AND user_id = %s
        ''', (menu, date, time, meal_id, user_id))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'status': 'success'})
    
    @app.route('/modify/delete', methods=['POST'])
    def delete_meal():
        data = request.get_json()
        meal_id = data.get('id')

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Invalid user ID'}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # 해당 식단이 존재하고, 본인의 것인지 확인
        cur.execute('SELECT COUNT(*) AS cnt FROM diets WHERE id = %s AND user_id = %s', (meal_id, user_id))
        row = cur.fetchone()
        if row['cnt'] == 0:
            cur.close()
            conn.close()
            return jsonify({'error': '해당 식단이 존재하지 않거나 권한이 없습니다.'}), 403

        # 삭제 쿼리
        cur.execute('DELETE FROM diets WHERE id = %s AND user_id = %s', (meal_id, user_id))
        conn.commit()

        cur.close()
        conn.close()
        return jsonify({'status': 'success'})

    # 임시 html 라우팅
    @app.route('/mypage')
    def mypage():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = get_user_info(session['user_id'])  # 사용자 정보 가져오기
        return render_template('mypage.html', user_name=user['name'], user_fullname=user['fullname'])

    
    @app.route('/dashboard',methods = ['GET'])
    def dashboard():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        return render_template("dashboard.html",user_id=user_id)
    
    @app.route('/info',methods = ['GET'])
    def info():
        return render_template("info.html")
    
    @app.route('/login', methods=['GET','POST'])
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
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/home')
    def home_page():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('home.html')
