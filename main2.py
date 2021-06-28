from flask import Flask, request, make_response, render_template
import redis
from time import strftime


app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True, db=0)

@app.route("/", methods=['post', 'get'])
def login():
    day = strftime("%Y-%m-%d")
    if not request.cookies.get("username"):
        message = ''
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if (username == 'root' and password == 'pass') or (username == 'root1' and password == 'pass1'):
                res = make_response(render_template("index.html", username=username))
                res.set_cookie("username", username)
                r.sadd(f'day:{day}', username)
                return res
            else:
                message = "Wrong username or password"
        return render_template('login.html', message=message)
    else:
        user_exists = r.sismember(f'day:{day}', request.cookies.get("username"))
        if not user_exists:
            r.sadd(f'day:{day}', request.cookies.get("username"))
        return render_template("index.html", username=request.cookies.get("username"))

@app.route("/admin/")
def index():
    days = r.keys('day:*')
    statistic = {day:r.smembers(day) for day in days}
    return render_template("index.html", statistic=statistic)


if __name__ == '__main__':
    app.run(debug=True)
