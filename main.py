from myflask import myflask

app = myflask("0.0.0.0", 8002)

@app.route("/")
def index():
    return "welcome to the class"

@app.route("/hello")
def hello():
    return "world"

@app.route("/login", methods=["GET"])
def login():
    return '<form method="post" url="/login"><input name="username" /><input type="submit"/></form>'

@app.route("/login", methods=["POST"])
def login():
    return 'you have submited some thing'

app.run()
