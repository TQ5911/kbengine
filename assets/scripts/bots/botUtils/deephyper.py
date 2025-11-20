import requests
import json
import os


class DeepSeekDialogue:
    api_url = "https://api.deepseek.com/chat/completions"
    def __init__(self):
        # self.api_url = api_url
        # self.auth_token = auth_token
        self.messages = []
        self.model = "deepseek-chat"  # 默认使用deepseek-chat模型
        self.auth_token = None
        with open(os.path.join(os.path.dirname(__file__), '.deepseek_config'), 'r') as f:
            self.auth_token = f.read().strip()
            print(self.auth_token)

    def send_message(self, message, role="user"):
        # 添加用户消息到对话历史
        self.messages.append({"content": message, "role": role})

        # 构建请求数据
        payload = {
            "messages": self.messages,
            "model": self.model,
            "frequency_penalty": 0,
            "max_tokens": 2048,
            "presence_penalty": 0,
            "stop": None,
            "stream": False,
            "temperature": 1,
            "top_p": 1,
            "logprobs": False,
            "top_logprobs": None
        }

        # 发送POST请求
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))

        _ret = '请求失败'
        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应数据
            response_data = response.json()
            # 打印AI的回复
            print("AI回复:", response_data['choices'][0]['message']['content'])
            # 将AI的回复添加到对话历史中
            self.messages.append(response_data['choices'][0]['message'])
            _ret = response_data['choices'][0]['message']['content']
        else:
            print("请求失败，状态码：", response.status_code)

        return _ret

    def change_model(self, model_id):
        # 更换使用的模型
        self.model = model_id

# 使用示例
# deepseek_dialogue = DeepSeekDialogue(api_url, auth_token)
#
# # 发送消息
# deepseek_dialogue.send_message("你好，AI。")
# deepseek_dialogue.send_message("你今天过得怎么样？")
#
# # 更换模型并发送消息
# deepseek_dialogue.change_model("deepseek-coder")
# deepseek_dialogue.send_message("请帮我解决这个编程问题。")
