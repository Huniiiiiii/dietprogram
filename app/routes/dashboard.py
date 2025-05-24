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
        year = int(request.args.get("year", datetime.now().year))
        month = int(request.args.get("month", datetime.now().month))

        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # 기능 1. 월간 기록 현황 (총 일수 대비 며칠 기록했는지)
                cur.execute("""
                    SELECT COUNT(DISTINCT date) AS recorded_days
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                """, (user_id, year, month))
                recorded_days = cur.fetchone()['recorded_days']
                total_days = calendar.monthrange(year, month)[1]

                # 기능 2. 끼니별 기록 분포 (아침/점심/저녁 비율)
                cur.execute("""
                    SELECT time, COUNT(*) AS count
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                    GROUP BY time
                """, (user_id, year, month))
                meal_distribution = cur.fetchall()

                # 기능 3. 자주 먹은 음식 TOP 3
                cur.execute("""
                    SELECT menu, COUNT(*) AS count
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                    GROUP BY menu
                    ORDER BY count DESC
                    LIMIT 3
                """, (user_id, year, month))
                top_foods = cur.fetchall()

                # 기능 4. 일별 식사 기록 여부 (아침/점심/저녁 중 무엇을 기록했는지)
                cur.execute("""
                    SELECT DATE(date) AS record_date, time
                    FROM diets
                    WHERE user_id = %s AND YEAR(date) = %s AND MONTH(date) = %s
                """, (user_id, year, month))
                meal_records = cur.fetchall()

                daily_meals = {}
                for record in meal_records:
                    date_str = record['record_date'].strftime('%Y-%m-%d')
                    time_mapping = {'아침': 'breakfast', '점심': 'lunch', '저녁': 'dinner'}
                    time = time_mapping.get(record['time'])

                    if time:  # 매핑된 값이 있을 경우만 처리
                        if date_str not in daily_meals:
                            daily_meals[date_str] = {'breakfast': 0, 'lunch': 0, 'dinner': 0}
                        daily_meals[date_str][time] = 1

                # 전체 데이터 반환
                return jsonify({
                    'monthly_progress': {
                        'year': year,
                        'month': month,
                        'total_days': total_days,
                        'recorded_days': recorded_days
                    },
                    'meal_time_distribution': meal_distribution,
                    'top_foods': top_foods,
                    'daily_meals': daily_meals  # → JS로 달력에 표시할 기록 여부
                })
        finally:
            conn.close()