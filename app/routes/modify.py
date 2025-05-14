from flask import request, render_template,jsonify
import pymysql

#데이터 베이스 연결
#데이터베이스 host, user, pswd, db명이 상이하면 연결 불가 -> 추후 맞출 것
def get_db_connection():
    return pymysql.connect(host='localhost',user='root',
                           password='0000',db='test',charset='utf8')
# register_routes()가 없으면 app에서 에러 발생하여 register_routes() 함수 안에 각 라우팅 함수 작성

def register_routes(app):
    # 기본 페이지 로드 
    @app.route('/modify',methods=['GET'])
    def modify_meal():
        return render_template("modify.html")
    
    # 로드 후 사용자의 최근 식단 기본으로 조회
    @app.route('/modify/list', methods = ['POST'])
    def get_meal():
        if request.cookies:
            user_id = int(request.cookies.get('user_id',0))
        else:
            data = request.get_json()
            user_id = data['user_id']
        # if user_id == 0:
        #     return jsonify({'error': 'Invalid user ID'}), 400
        # 지금은 에러 처리 말고 그냥 user id 1로 
        if (not user_id) or user_id == '0':
            user_id = '1'
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

        result = [{"id": row[0], "menu": row[1],"date":row[2], "time":row[3]} for row in rows]
        
        conn.close()
        return jsonify(result)
    
    # 조회 버튼 클릭 시 호출 함수 (식단 조회)
    @app.route('/modify/search',methods=['POST'])
    def search_meal():
        data = request.get_json()
        year = data['year']; month = data['month']; day = data['day']
        time = data["time"]
        if request.cookies:
            user_id = int(request.cookies.get('user_id',0))
        else:
            user_id = data['user_id']
        # 나중에 합칠 때 삭제해야 하는 문
        if user_id == 0: 
            user_id = '1'
            
        if year and month and day:
            date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            date = None 
        
        conn = get_db_connection()
        cur= conn.cursor()
        cur.execute('''
                    SELECT id, menu, date, time
                    FROM diets
                    WHERE date = %s AND time = %s AND user_id = %s
                    ''', (date,time,user_id))
        row = cur.fetchone()
        result = []
        if row:
            result.append({'id':row[0],'menu':row[1],'date':row[2], 'time':row[3]})
        else: 
            result=[]
            
        cur.close()
        conn.close()
        return jsonify(result)
    
    # 조회 후 수정 버튼 클릭 시 호출 함수 (메뉴 변경)
    @app.route('/modify/update', methods=['POST'])
    def update_meal():
        data = request.get_json()
        id= data['id']
        menu = data['menu']
        year = data['year']
        month = data['month']
        day = data['day']
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        time = data['time']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE diets SET menu = %s, date = %s, time = %s WHERE id = %s",
            (menu, date, time, id)
        )
        conn.commit()
        
        cur.close()
        conn.close()
        return jsonify({'status': 'success'})
    
    # 조회 후 삭제 버튼 클릭 시 호출 함수 (메뉴 삭제)
    @app.route('/modify/delete', methods = ['POST'])
    def delete_meal():
        data = request.get_json()
        id = data['id']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM diets WHERE id = %s", (id))
        conn.commit()
        
        cur.close()
        conn.close()
        return jsonify({'status': 'success'})
    
    # +버튼 클릭 시 호출 함수 (식단 추가)
    @app.route('/modify/add', methods=['POST'])
    def add_meal():
        data = request.get_json()
        menu = data['menu']
        user_id = data['user_id']
        
        year = data['year']
        month = data['month']
        day = data['day']
        date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        time = data['time']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO diets 
                    (user_id, menu, date, time)
                    VALUES (%s,%s,%s,%s)
                    ''', (user_id,menu,date,time))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'success'})
        
    # 임시 html 라우팅
    @app.route('/mypage',methods = ['GET'])
    def mypage():
        return render_template("info.html")
    
    @app.route('/dashboard',methods = ['GET'])
    def dashboard():
        return render_template("dashboard.html")
    
    @app.route('/info',methods = ['GET'])
    def info():
        return render_template("info.html")
