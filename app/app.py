from flask import Flask,render_template
from routes.modify import register_routes as register_modify
from routes.dashboard import register_routes as register_dashboard
from routes.login import register_routes as register_login
from routes.register import register_routes as register_register

app = Flask(__name__)
register_modify(app)
register_dashboard(app)
register_login(app)
register_register(app)

app.secret_key = 'your-secret-key' 

@app.route('/')
def home():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
