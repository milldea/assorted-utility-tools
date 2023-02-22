# 概要
テキスト内のBacklogチケットの課題番号がリンク化されます。   
RedmineモードではBacklogと同じ課題番号のissueがプロジェクト内にある場合、Redmineリンクも挿入できます。   
指定するBacklogチケットのプレフィックス文字列が入っていない行はそのまま出力されます。

## 注意事項
リポジトリはpublicです。   
実際に使用されているRedmine, BacklogのURLおよびAPI Keyなどのプロジェクト情報は絶対にコミットしないでください。   
事故防止のため、プロジェクト情報はスクリプト上部に用意した定数以外に入れての使用は非推奨とします。

## 構造
```
.
├── README.md               => 本ページ
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
4. `add_ticket_link.py` の上部の変数に必要な情報を入れる

## 実行
1. ディレクトリ直下で `$python3 add_ticket_link.py {元ファイルのパス}` を実行
2. `output/` ディレクトリ内に`{元ファイル名}_added.md`として整形後のファイルがmarkdown形式で出力される

#### オプション
* `-redmine`   
  RedmineとBacklogを併用している場合に使える機能です。   
  `REDMINE_PROJECT_ID`で指定したプロジェクト上にBacklogチケットの課題番号が含まれるissueがある場合、Redmine記法のRedmineチケットリンク(`#{チケット番号}`)が合わせて挿入されます。   
  ない場合、`#TODO`として挿入されます。   
  ex. `python3 add_ticket_link.py original/example.txt -redmine`

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