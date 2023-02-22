import re
import sys

import requests

# Backlog情報(必須)
# プロジェクトのURL
BACKLOG_URL_BASE = "https://hogefuga123.backlog.jp/view"
# 課題番号のプレフィックスをハイフンまで指定
BACKLOG_PREFIX = "HOGE-"
# Redmine情報(使用しない場合は入力不要)
# RedmineのURL
REDMINE_BASE_URL = "https://www.hogefuga123.com/redmine/issues"
# RedmineのプロジェクトID
REDMINE_PROJECT_ID = "project-hoge"
# Redmineの個人設定から取得可能
REDMINE_API_KEY = "abcdefghijklmnopqrstuvwxyz"

redmine_mode: bool = False
issue_number_converter: dict = {}


"""
実行方法:
    $ python3 add_ticket_link.py {元のチケットのテキストファイル}
オプション:
    -redmine : Redmineモード
"""


def handler(original_path: str) -> None:
    # Redmineモードの場合issue取得と対応表生成をする
    if redmine_mode:
        # Redmineプロジェクトからissueのリストを取得
        redmine_issues = _get_redmine_issues()
        # RedmineとBacklogの課題番号対応表を生成
        _generate_issue_number_converter(redmine_issues)
    file_name = original_path.split("/")[-1].split(".")[0]

    with open(original_path, mode="r") as f:
        with open(f"output/{file_name}_added.md", mode="w") as new:
            for line in f.readlines():
                # チケットタイトル行の場合処理する
                if BACKLOG_PREFIX in line:
                    number = _get_ticket_number(line)
                    # 各チケットリンクを含めた文字列を生成、書き込み
                    new_line = _generate_link_added_line(line, number)
                    new.write(new_line)
                    continue
                # チケットタイトル以外の行はそのまま書き込み
                new.write(line)
    print("complete.")
    return


def _get_redmine_issues() -> list:
    get_url = f"{REDMINE_BASE_URL}.json"
    params = {
        "project_id": REDMINE_PROJECT_ID,
        "key": REDMINE_API_KEY,
        "limit": 500,
    }
    res = requests.get(get_url, params).json()
    if res["total_count"] > res["limit"]:
        # TODO このメッセージが出ていたら取り切れていないチケットがある
        # limitを見直す, ページング処理を入れるなどの対応が必要
        print("Warn: TotalCount > Limit.")
    return res["issues"]


def _generate_issue_number_converter(redmine_issues: list) -> None:
    # issue_number_converter = {
    #     {backlog課題番号}:{redmine課題番号},
    # }
    for issue in redmine_issues:
        subject = issue["subject"]
        if BACKLOG_PREFIX in subject:
            backlog_number = subject.split(BACKLOG_PREFIX)[1].split(" ")[0]
            issue_number_converter.update({backlog_number: issue["id"]})
    return


def _generate_link_added_line(line: str, number: str) -> str:
    # Backlogチケットのリンクを生成
    backlog_url = f"[{BACKLOG_PREFIX}{number}]({BACKLOG_URL_BASE}/{BACKLOG_PREFIX}{number})"  # noqa:E501
    if redmine_mode:
        # Redmineのチケット番号を取得
        try:
            redmine_number = issue_number_converter[number]
        except KeyError:
            # BacklogチケットがあってRedmineチケットがない場合
            # エラーを吐いてファイル内ではTODOとする
            redmine_number = "TODO"
            print(
                f"Redmine Issue NotFound in {REDMINE_PROJECT_ID}, "
                f"{BACKLOG_PREFIX}{number}."
            )
        new_line = line.replace(
            BACKLOG_PREFIX + number,
            f"{backlog_url} #{redmine_number}",
        )
    else:
        new_line = line.replace(
            BACKLOG_PREFIX + number,
            f"{backlog_url}",
        )
    return new_line


def _get_ticket_number(line: str) -> str:
    # TODO チケット番号の取り方悩む
    number = re.findall("[-]([0-9]*)", line)[0]
    return number


class FileNotSpecifiedError(Exception):
    """ファイル未指定エラー"""


if __name__ == "__main__":
    args = sys.argv
    try:
        try:
            original_path = args[1]
        except Exception:
            raise FileNotSpecifiedError
        for arg in args[1:]:
            if arg.startswith("-redmine"):
                redmine_mode = True
        handler(original_path)
    except FileNotSpecifiedError:
        print("Source file is not specified.")
        print("  ex. $python3 add_ticket_link.py {original.txt}")
    except Exception:
        raise
