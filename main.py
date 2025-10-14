from http import *

app = MiniApp()

@app.route("/hello")
def hello(request):
  name = request.args.get("name", "Flask")
  return f"Hello, {escape(name)}!"

@app.route("/")
def index(request):
  return "<h1>Welcome to MiniApp</h1><p>Try /hello?name=World</p>"
 
app.run("0.0.0.0", 8000)