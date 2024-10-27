# Zaim SDK

## 概要
Zaimの公式APIを利用するためのPythonのSDKです。

## インストール
```bash
pip install zaim-sdk
```

## 使い方
1. アクセストークンを取得する
    ```python
    from zaim_sdk import get_access_token

    CONSUMER_ID = "xxxxxxxxxx"
    CONSUMER_SECRET = "xxxxxxxxxx"
    get_access_token(consumer_id, consumer_secret)
    ```
    これを、ブラウザが開かれ、Zaimの認証画面が表示されます。  
    認証後、表示されるアクセストークンとアクセストークンシークレットを控えておいてください。

1. 先ほど取得したアクセストークンを使って、ZaimのAPIを利用する。
    ```python
    from zaim_sdk import ZaimSDK, get_access_token

    CONSUMER_ID = "xxxxxxxxxx"
    CONSUMER_SECRET = "xxxxxxxxxx"
    ACCESS_TOKEN = "xxxxxxxxxx"
    ACCESS_TOKEN_SECRET = "xxxxxxxxxx"
    zaim = ZaimSDK(CONSUMER_ID, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

## Requirements
```
Flask==2.3.3
requests-oauthlib==2.0.0
Werkzeug==2.3.7
```