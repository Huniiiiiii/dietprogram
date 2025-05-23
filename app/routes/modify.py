from flask import request, render_template,jsonify
import pymysql
#데이터 베이스 연결 부분
#데이터베이스 host, user, pswd, db명이 상이하면 연결 불가 -> 나중에 맞출 것
def get_db_connection():
    return pymysql.connect(host='localhost',user='root',
                           password='0000',db='test',charset='utf8')

#app에서 자꾸 에러가 나 register_routes() 함수 안에 작성 (추후 수정 가능하면 할 것)

def register_routes(app):

    @app.route('/modify',methods=['GET'])
    def modify_meal():
        return render_template("modify.html")
    
    @app.route('/modify/search',methods=['POST'])
    def search_meal():
        data = request.get_json()
        year = data['year']; month = data['month']; day = data['day']
        time = data["time"]
        if year and month and day:
            date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            date = None 
        
        conn = get_db_connection()
        cur= conn.cursor()
        cur.execute('''
                    SELECT id, menu, date, time
                    FROM diets
                    WHERE date = %s AND time = %s
                    ''', (date,time))
        row = cur.fetchone()
        result = []
        if row:
            result.append({'id':row[0],'menu':row[1],'date':row[2], 'time':row[3]})
        else: 
            result=[]
            
        cur.close()
        conn.close()
        return jsonify(result)
    
    @app.route('/modify/update', methods=['POST'])
    def update_meal():
        data = request.get_json()
        id= data['id']
        menu = data['menu']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE diets SET menu = %s WHERE id = %s", (menu,id))
        conn.commit()
        
        cur.close()
        conn.close()
        return jsonify({'status': 'success'})
    
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