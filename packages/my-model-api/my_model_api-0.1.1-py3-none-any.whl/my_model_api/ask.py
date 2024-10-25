# my_model_api/ask.py
import requests

# 设置 API 的 URL
server_ip = "http://bwfyllm.tocmcc.cn:5000/api/ask"  # 将 IP 地址替换为服务器的实际内网 IP

# 提问函数
def ask_model(question):
    headers = {'Content-Type': 'application/json'}
    data = {"question": question}
    response = requests.post(server_ip, json=data, headers=headers)
    result = response.json()
    return result['answer']

# 示例使用
if __name__ == "__main__":
    question = "很好，在机器学习算法竞赛中，特征工程通常有哪些步骤"
    answer = ask_model(question)
    print("模型的回答:", answer)
