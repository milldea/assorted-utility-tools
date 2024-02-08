# README
## 概要

このリポジトリはAsciiDocを生成するためのRuby環境を整えたDockerコンテナの素を管理しています。

## 生成されるコンテナについて

以下の3つのgemを含む、Ruby2.7の実行環境です。

```
asciidoctor
asciidoctor-diagram
asciidoctor-pdf
```

Docker version 20.10.17にて動作確認済みです。(2024/02)

## 準備

以下のコマンドでコンテナを立ち上げ、コンテナに入ります。

```
$ cd asciidoc-container
$ docker compose up -d
$ docker compose exec app bash
```

## 生成

コンテナに入った状態で生成するコマンドを使用します。   
コマンドは[asciidoctorのリファレンス](https://github.com/asciidoctor/asciidoctor/blob/main/README-jp.adoc#%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%83%A9%E3%82%A4%E3%83%B3%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%95%E3%82%A7%E3%83%BC%E3%82%B9-cli)などを参照ください。