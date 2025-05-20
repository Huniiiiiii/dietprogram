from flask import request, jsonify
import pymysql
import calendar
from datetime import datetime

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='0000',
        db='test',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

def register_routes(app):
    @app.route('/dashboard/<int:user_id>', endpoint='dashboard_view')
    def dashboard(user_id):
        # ✅ 연도와 월 GET 파라미터 받아오기 (기본값은 현재)
        year = int(request.args.get("year", datetime.now().year))
        month = int(request.args.get("month", datetime.now().month))

        print(f"[DEBUG] 사용자 요청: user_id={user_id}, year={year}, month={month}")

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # 1. 기록 현황
                cur.execute("""
                    SELECT COUNT(DISTINCT date) AS recorded_days
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                """, (user_id, year, month))
                recorded_days = cur.fetchone()['recorded_days']
                total_days = calendar.monthrange(year, month)[1]

                # 2. 끼니별 비율
                cur.execute("""
                    SELECT time, COUNT(*) AS count
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                    GROUP BY time
                """, (user_id, year, month))
                meal_distribution = cur.fetchall()

                # 3. 자주 먹은 음식 TOP 3
                cur.execute("""
                    SELECT menu, COUNT(*) AS count
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                    GROUP BY menu
                    ORDER BY count DESC
                    LIMIT 3
                """, (user_id, year, month))
                top_foods = cur.fetchall()

                # 4. 일별 기록 여부
                cur.execute("""
                    SELECT DATE(date) AS record_date, COUNT(*) AS count
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                    GROUP BY record_date
                """, (user_id, year, month))
                daily_records = cur.fetchall()

                print(f"[DEBUG] recorded_days={recorded_days}, meals={len(meal_distribution)}, top3={len(top_foods)}")

                return jsonify({
                    'monthly_progress': {
                        'year': year,
                        'month': month,
                        'total_days': total_days,
                        'recorded_days': recorded_days
                    },
                    'meal_time_distribution': meal_distribution,
                    'top_foods': top_foods,
                    'daily_records': daily_records
                })

        finally:
            conn.close()
