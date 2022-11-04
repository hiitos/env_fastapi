# fastAPI

## poetry 環境の整備初回コマンド
```
docker-compose build
```

```
docker-compose run \
  --entrypoint "poetry init \
    --name app \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  app
```
Dockerコンテナ（app）の中で、 poetry init コマンドを実行。  
引数として、 fastapi と、ASGIサーバーである uvicorn をインストールする依存パッケージとして指定。

このコマンドにより、インタラクティブなダイアログが始まる。  
Authorのパートのみ n の入力が必要ですが、それ以外はすべてEnterで進めていけば問題ない  
FastAPIを依存パッケージに含む、poetryの定義ファイルを作成ができた(pyproject.toml ファイルの作成)  

```
docker-compose run --entrypoint "poetry install" app
```
poetry.lock ファイルの作成

新しいPythonパッケージを追加した場合などは以下のようにイメージを再ビルドするだけで、 pyproject.toml に含まれている全てのパッケージをインストールすることができる
```
docker-compose build --no-cache
```

## 起動
```
docker-compose up
```

## db確認
```
docker-compose exec db mysql demo
```

## パッケージインストール
```
docker-compose up
```
```
# "demo-app" コンテナの中で "poetry add sqlalchemy aiomysql" を実行
docker-compose exec app poetry add sqlalchemy aiomysql
```

## db作成
```
# api モジュールの migrate_db スクリプトを実行する
docker-compose exec app poetry run python -m api.migrate_db
```


# ユニットテスト
```
docker-compose exec app poetry add -D pytest-asyncio aiosqlite httpx
```
-D はpoetryの「開発用モード」を指定するオプションです。開発用モードでは、production用のデプロイではスキップされる、テストや開発時のローカル環境のみで使用するライブラリをインストールします。これによって本番環境では不要なライブラリをインストールせずに済み、コンテナでインストールする場合も結果的にコンテナのイメージサイズを減らしたり、ビルド時間を短縮することが可能

pyproject.toml と poetry.lock が更新されます。

[tool.poetry.dev-dependencies] にライブラリが新たに追加されているはず

#### テストの実行
```
docker-compose run --entrypoint "poetry run pytest --asyncio-mode=auto" app
```