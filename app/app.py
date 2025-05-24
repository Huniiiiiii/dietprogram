from flask import Flask,render_template
from routes.modify import register_routes

app = Flask(__name__)
register_routes(app)
app.secret_key = 'your-secret-key' 
@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
