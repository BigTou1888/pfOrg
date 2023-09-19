from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('./JavBus - AV磁力連結分享 - 日本成人影片資料庫.html')

if __name__ == "__main__":
    app.run()