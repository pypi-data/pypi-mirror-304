import logging
import threading
import webbrowser
from urllib.parse import urlparse

from flask import Flask, render_template, request
from requests_oauthlib import OAuth1Session
from werkzeug.serving import make_server

REQUEST_TOKEN_URL = "https://api.zaim.net/v2/auth/request"
AUTHORIZE_URL = "https://auth.zaim.net/users/auth"
ACCESS_TOKEN_URL = "https://api.zaim.net/v2/auth/access"
CALLBACK_URI = "http://127.0.0.1:5000/"

# Flaskから不要なログを出させない
logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(__name__)

oauth_verifier = None
oauth_verifier_event = threading.Event()

server = None


@app.route("/", methods=["GET"])
def callback():
    global oauth_verifier
    oauth_verifier = request.args.get("oauth_verifier")
    oauth_verifier_event.set()
    return render_template("callback.html")


@app.route("/access-token", methods=["GET"])
def access_token():
    access_token = request.args.get("access_token")
    access_token_secret = request.args.get("access_token_secret")
    return render_template("access_token.html", access_token=access_token, access_token_secret=access_token_secret)


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        parsed_uri = urlparse(CALLBACK_URI)
        host = parsed_uri.hostname
        port = parsed_uri.port
        if host is None or port is None:
            raise ValueError("CALLBACK_URIが不正です。")
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


def get_access_token(consumer_id: str, consumer_secret: str):
    server_thread = ServerThread(app)
    server_thread.start()

    auth = OAuth1Session(client_key=consumer_id, client_secret=consumer_secret, callback_uri=CALLBACK_URI)
    auth.fetch_request_token(REQUEST_TOKEN_URL)

    # ユーザーを認証URLにリダイレクト
    authorization_url = auth.authorization_url(AUTHORIZE_URL)
    webbrowser.open(authorization_url)

    # oauth_verifierの取得を待機
    oauth_verifier_event.wait()
    if oauth_verifier is None:
        raise ValueError("oauth_verifierの取得に失敗しました。")

    access_token_res = auth.fetch_access_token(url=ACCESS_TOKEN_URL, verifier=oauth_verifier)
    access_token = access_token_res.get("oauth_token")
    access_token_secret = access_token_res.get("oauth_token_secret")
    webbrowser.open(f"{CALLBACK_URI}access-token?access_token={access_token}&access_token_secret={access_token_secret}")

    # サーバーをシャットダウン
    server_thread.shutdown()
    server_thread.join()
