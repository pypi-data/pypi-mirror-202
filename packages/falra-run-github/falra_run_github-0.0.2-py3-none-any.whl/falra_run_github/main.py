import argparse
import os
import shutil
import subprocess
import requests
import sys
import ast


def download_github_repo(repo_url, access_token, repo_name="repo"):
    # 解析出 repo 的 owner 和 name
    _, owner, name = repo_url.rstrip('/').rsplit('/', 2)

    # 設置 API 請求頭部，添加授權欄位
    headers = {
        'Authorization': f'Token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # 請求 repo 的內容
    repo_url = f'https://api.github.com/repos/{owner}/{name}/contents/'
    response = requests.get(repo_url, headers=headers)

    # 將內容轉換為 JSON 格式
    repo_contents = response.json()

    # 創建新目錄來存儲 repo 的內容
    if not os.path.exists("user-repo"):
        os.mkdir("user-repo")
    repo_name = os.path.join("user-repo", repo_name)
    if not os.path.exists(repo_name):
        os.mkdir(repo_name)

    # 下載每個文件並存儲到本地
    try:
        for file in repo_contents:
            if file['type'] == 'file':
                file_url = file['download_url']
                response = requests.get(file_url, headers=headers)
                with open(os.path.join(repo_name, file['path']), 'wb') as f:
                    f.write(response.content)
    except Exception as e:
        # 如果 下載 產生錯誤，將錯誤訊息寫到檔案中
        print(f"""[Github download ERROR!!] repo_url:  {repo_url}. ERROR_msg：{e}""")


def run_main_py(repo_name, output_file="falra_output.txt", py_name="main.py", arg=[]):
    # 獲取 main.py 的路徑
    repo_name = os.path.join("user-repo", repo_name)
    main_path = os.path.join(repo_name, py_name)

    # 檢查 main.py 是否存在
    if not os.path.exists(main_path):
        print("Error: main.py not found")
        return

    # 清除上一次的 falra_output.txt
    output_file = f"""{repo_name}/falra_output.txt"""
    if os.path.exists(output_file):
        os.remove(output_file)

    # 執行 main.py
    python_command = ["python3", main_path]
    python_command = python_command + arg
    try:
        print(f"""============ python_command==========  {python_command}""")
        output = subprocess.check_output(python_command, universal_newlines=True)

        # 將輸出寫入檔案
        with open(output_file, "a") as f:
            f.write(output)

    except Exception as e:
        # 如果 subprocess 產生錯誤，將錯誤訊息寫到檔案中
        print(f"""=[python command ERROR!!] python_command:  {python_command}""")
        error_msg = f"ERROR while running '{py_name}', python_command:  {python_command}. ERROR_msg：{e}"
        print(error_msg)
        with open(output_file, "a") as f:
            f.write(error_msg)


def query_output(repo_name, output_file="falra_output.txt"):
    repo_name = os.path.join("user-repo", repo_name)
    #print(f"""result_file = {repo_name}/{output_file}""")
    # 讀取檔案內容
    output_file_path = f"""{repo_name}/{output_file}"""
    with open(output_file_path, 'r') as f:
        contents = f.read()
        print(contents)
        # 返回結果
        return contents


def clean_user_repo():
    folder_path = 'user-repo'

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def main_run_github(repo_url, access_token, repo_name, py_name, arg_str):

    #repo_url = sys.argv[1] # "https://github.com/my-account/my-repo"
    #access_token = sys.argv[2] # "access_token
    #repo_name = sys.argv[3] # 'my-repo'
    #py_name = sys.argv[4] # 'main.py'

    # read parameters
    arg = []
    #arg_str = sys.argv[5] # "['argument']"
    # 將字符串轉換為 list
    arg = ast.literal_eval(arg_str)

    # Download GitHub repo and save to local directory user-repo
    print("002 download_github_repo..")
    download_github_repo(repo_url, access_token, repo_name)

    # 創建 output 目錄來存儲執行結果
    #if not os.path.exists(repo_name):
    #    os.mkdir(repo_name)
    # 創建 output 目錄來存儲執行結果
    #output_dir = f"""{repo_name}/output"""
    #if not os.path.exists(output_dir):
    #    os.mkdir(output_dir)

    # 運行 main.py 並將輸出結果記錄到 repo 下的 falra_output.txt 檔案
    print("003 run_main_py..")
    output_file= f"""falra_output.txt"""
    run_main_py(repo_name=repo_name, output_file=output_file, py_name=py_name, arg=arg)

    # Query output
    execution_result = query_output(repo_name=repo_name)
    print(execution_result)
    print("004 run_main_py done.")


def main():
    parser = argparse.ArgumentParser(description='GitHub Executor')
    parser.add_argument('--action', type=str, required=True, choices=['start', 'output', 'clean'], help="The actions to execute")
    parser.add_argument('--repo_url', metavar='repo_url', type=str, help='URL of the GitHub repository')
    parser.add_argument('--access_token', metavar='access_token', type=str, help='Access token for the GitHub API')
    parser.add_argument('--repo_name', metavar='repo_name', type=str, help='Name of the repository')
    parser.add_argument('--py_name', metavar='py_name', type=str, help='Name of the Python file to execute')
    parser.add_argument('--argument', metavar='argument', type=str, help='Arguments of the Python to execute as string')

    args = parser.parse_args()

    print(f"""Action = {args.action}""")

    if args.action == "start":
        if not args.repo_url:
            parser.error("Executing run_github requires --repo_url parameter")
        print(f"""001 start falra_run_github..""")
        main_run_github(repo_url=args.repo_url,
                        access_token=args.access_token,
                        repo_name=args.repo_name,
                        py_name=args.py_name,
                        arg_str=args.argument,
                        )
    elif args.action == "output":
        if not args.repo_name:
            parser.error("Executing output query requires --repo_name parameter")
        query_output(args.repo_name)

    elif args.action == "clean":
        clean_user_repo()

if __name__ == "__main__":
    main()
