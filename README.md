# sakura-twitter-api

## 開発環境構築

```sh
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ npm install serverless-python-requirements
```

## ローカルで実行

```sh
(venv) $ sls invoke local --function <<function名>>
```

## AWS へのデプロイ

docker を起動しておく

```sh
(venv) $ sls deploy
```

## venv から抜け出す

```sh
(venv) $ deactivate
```
