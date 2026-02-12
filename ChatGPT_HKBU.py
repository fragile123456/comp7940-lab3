import requests
import configparser
import sys
import traceback  # 新增：导入错误追踪模块


class ChatGPT:
    def __init__(self, config):
        api_key = config['CHATGPT']['API_KEY']
        base_url = config['CHATGPT']['BASE_URL']
        model = config['CHATGPT']['MODEL']
        api_ver = config['CHATGPT']['API_VER']

        self.url = f'{base_url}/deployments/{model}/chat/completions?api-version={api_ver}'

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "api-key": api_key,
        }

        self.system_message = (
            'You are a helper! Your users are university students. '
            'Your replies should be conversational, informative, use simple words, and be straightforward.'
        )

    def submit(self, user_message: str):
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": user_message},
        ]

        payload = {
            "messages": messages,
            "temperature": 1,
            "max_tokens": 150,
            "top_p": 1,
            "stream": False
        }

        try:  # 新增：捕获请求环节的错误
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return "Error: " + response.text
        except Exception as e:
            return f"Request error: {str(e)}\n{traceback.format_exc()}"  # 打印请求错误栈


if __name__ == '__main__':
    # 强制设置标准输出编码（增强版）
    try:
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    except Exception:
        pass

    # 读取配置文件
    config = configparser.ConfigParser()
    try:  # 新增：捕获配置文件读取错误
        config.read('config.ini', encoding='utf-8')
    except Exception as e:
        print(f"Config read error: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1)

    chatGPT = ChatGPT(config)

    # 主循环：添加完整的异常捕获
    while True:
        try:
            print('Input your query: ', end='')
            user_input = input().strip()
            if not user_input:
                continue
            response = chatGPT.submit(user_input)

            # 尝试打印，若失败则写入文件
            try:
                print("Reply: ", response)
            except UnicodeEncodeError:
                # 打印失败时，写入文件验证内容
                with open('chat_reply.txt', 'w', encoding='utf-8') as f:
                    f.write(response)
                print("Failed to print reply (encoding error), saved to chat_reply.txt")
        except Exception as e:
            print(f"Runtime error: {str(e)}\n{traceback.format_exc()}")