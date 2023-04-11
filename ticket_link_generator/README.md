# 概要
テキスト内のBacklogチケットの課題番号がリンク化されます。   
RedmineモードではBacklogと同じ課題番号のissueがプロジェクト内にある場合、Redmineリンクも挿入できます。   
指定するBacklogチケットのプレフィックス文字列が入っていない行はそのまま出力されます。

## 注意事項
リポジトリはpublicです。   
実際に使用されているRedmine, BacklogのURLおよびAPI Keyなどのプロジェクト情報は絶対にコミットしないでください。   
事故防止のため、.gitignoreファイルによって以下のファイルをGitの追跡対象から除外しています。

* originalおよびoutputディレクトリのexampleから始まるファイルを除く全てのファイル・ディレクトリ
* config.json

## 構造
```
.
├── README.md               => 本ページ
├── .gitignore              => Git追跡除外設定ファイル
├── config_sample.json      => config.json生成用のサンプルファイル
├── add_ticket_link.py      => メインスクリプト
├── original
│   └── example.txt         => 元ファイルサンプル
├── output                  => 作成したファイルの出力先
│   └── example_added.md    => 出力ファイルサンプル
└── requirements.txt        => pip installに使用する必要モジュールリスト
```

# 使用方法
## 準備
1. `assorted_utility_tools` リポジトリをcloneする
2. `$cd ticket_link_generator` で本ディレクトリに移動する
3. 環境準備
   1. Python3系が入っている状態にする
   2. 本ディレクトリ直下で`$pip install -r requirements.txt` を実行する
4. `config.json` ファイルを作成し、必要な情報を入れる
   1. `config_sample.json` をコピーし、以下の情報を自身の使用環境に合わせて埋めてください。   
   ただし、REDMINE_から始まるキーについてはRedmineモードを使用しない場合はダミーの値で構いません。
      * "BACKLOG_URL_BASE": BacklogプロジェクトのURL
      * "BACKLOG_PREFIX": 課題番号のプレフィックスをハイフンまで
      * "REDMINE_BASE_URL": RedmineのURL
      * "REDMINE_PROJECT_ID": RedmineのプロジェクトID
      * "REDMINE_API_KEY": Redmine APIのキー

## 実行
1. ディレクトリ直下で `$python3 add_ticket_link.py {元ファイルのパス}` を実行
2. `output/` ディレクトリ内に`{元ファイル名}_added.md`として整形後のファイルがmarkdown形式で出力される

#### オプション
* `-redmine` (Redmineモード)   
  RedmineとBacklogを併用している場合に使える機能です。   
  `REDMINE_PROJECT_ID`で指定したプロジェクト上にBacklogチケットの課題番号が含まれるissueがある場合、Redmine記法のRedmineチケットリンク(`#{チケット番号}`)が合わせて挿入されます。   
  指定のプロジェクトに該当のチケットがない場合、`#TODO`として挿入されます。   
  ex. `python3 add_ticket_link.py original/example.txt -redmine`
* `-P` (プレーンモード)   
  -redmineオプション使用時のみ有効なオプションです。   
  Redmineチケットのリンクが通常のマークダウン形式のリンクとなります。   
  ex. `python3 add_ticket_link.py original/example.txt -redmine -P`

#### メッセージ出力
* `Source file is not specified.` => 元ファイルが指定されていない
* `Redmine Issue NotFound in {RedmineプロジェクトID}, {Backlog課題}.` => Backlogの課題番号を含むissueがRedmineにない
* `complete.` => 処理完了

# 使用例
## オプションなし
`$python3 add_ticket_link.py original/example.md`
### before
```
メモ
* HOGE-1 hogeAPIの改修
    * xxを改修して動作確認する
* HOGE-2 API仕様書の修正
    * HOGE-1 が終わったら作業する
* Aさんにお願いすること
    * HOGE-3 fugaサーバ証明書の更新
```
### after
```
メモ
* [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) hogeAPIの改修
    * xxを改修して動作確認する
* [HOGE-2](https://hogefuga123.backlog.jp/view/HOGE-2) API仕様書の修正
    * [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) が終わったら作業する
* Aさんにお願いすること
    * [HOGE-3](https://hogefuga123.backlog.jp/view/HOGE-3) fugaサーバ証明書の更新
```
↓ markdownプレビュー   
メモ
* [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) hogeAPIの改修
    * xxを改修して動作確認する
* [HOGE-2](https://hogefuga123.backlog.jp/view/HOGE-2) API仕様書の修正
    * [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) が終わったら作業する
* Aさんにお願いすること
    * [HOGE-3](https://hogefuga123.backlog.jp/view/HOGE-3) fugaサーバ証明書の更新
### コンソール出力
```
complete.
```
## オプションあり(Redmineモード)
* Redmine の状態
  * HOGE-1 hogeAPIの改修, (急) HOGE-2 API仕様書の修正 というチケットあり
  * HOGE-3はRedmineチケットなし
`$python3 add_ticket_link.py original/example.md -redmine`
### before
```
メモ
* HOGE-1 hogeAPIの改修
    * xxを改修して動作確認する
* HOGE-2 API仕様書の修正
    * HOGE-1 が終わったら作業する
* Aさんにお願いすること
    * HOGE-3 fugaサーバ証明書の更新
```
### after
```
メモ
* [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) #12345 hogeAPIの改修
    * xxを改修して動作確認する
* [HOGE-2](https://hogefuga123.backlog.jp/view/HOGE-2) #12346 API仕様書の修正
    * [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) #12345 が終わったら作業する
* Aさんにお願いすること
    * [HOGE-3](https://hogefuga123.backlog.jp/view/HOGE-3) #TODO fugaサーバ証明書の更新
```
↓ markdownプレビュー   
メモ
* [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) #12345 hogeAPIの改修
    * xxを改修して動作確認する
* [HOGE-2](https://hogefuga123.backlog.jp/view/HOGE-2) #12346 API仕様書の修正
    * [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) #12345 が終わったら作業する
* Aさんにお願いすること
    * [HOGE-3](https://hogefuga123.backlog.jp/view/HOGE-3) #TODO fugaサーバ証明書の更新
### コンソール出力
```
Redmine Issue NotFound in project-hoge, HOGE-3.
complete.
```

## オプションあり(Redmineモード・プレーンモード併用)
* Redmine の状態
  * HOGE-1 hogeAPIの改修, (急) HOGE-2 API仕様書の修正 というチケットあり
  * HOGE-3はRedmineチケットなし
`$python3 add_ticket_link.py original/example.md -redmine -P`
### before
```
メモ
* HOGE-1 hogeAPIの改修
    * xxを改修して動作確認する
* HOGE-2 API仕様書の修正
    * HOGE-1 が終わったら作業する
* Aさんにお願いすること
    * HOGE-3 fugaサーバ証明書の更新
```
### after
```
メモ
* [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) [#12345](https://www.hogefuga123.com/redmine/issues/12345) hogeAPIの改修
    * xxを改修して動作確認する
* [HOGE-2](https://hogefuga123.backlog.jp/view/HOGE-2) [#12346](https://www.hogefuga123.com/redmine/issues/12346) API仕様書の修正
    * [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) [#12345](https://www.hogefuga123.com/redmine/issues/12345) が終わったら作業する
* Aさんにお願いすること
    * [HOGE-3](https://hogefuga123.backlog.jp/view/HOGE-3) [#TODO](https://www.hogefuga123.com/redmine/issues/TODO) fugaサーバ証明書の更新
```
↓ markdownプレビュー   
メモ
* [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) [#12345](https://www.hogefuga123.com/redmine/issues/12345) hogeAPIの改修
    * xxを改修して動作確認する
* [HOGE-2](https://hogefuga123.backlog.jp/view/HOGE-2) [#12346](https://www.hogefuga123.com/redmine/issues/12346) API仕様書の修正
    * [HOGE-1](https://hogefuga123.backlog.jp/view/HOGE-1) [#12345](https://www.hogefuga123.com/redmine/issues/12345) が終わったら作業する
* Aさんにお願いすること
    * [HOGE-3](https://hogefuga123.backlog.jp/view/HOGE-3) [#TODO](https://www.hogefuga123.com/redmine/issues/TODO) fugaサーバ証明書の更新
### コンソール出力
```
Redmine Issue NotFound in project-hoge, HOGE-3.
complete.
```