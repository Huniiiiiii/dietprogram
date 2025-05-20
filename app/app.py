from flask import Flask, render_template
from routes.modify import register_routes as register_modify
from routes.dashboard import register_routes as register_dashboard

app = Flask(__name__)

# 각 라우터 등록
register_modify(app)
register_dashboard(app)

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
