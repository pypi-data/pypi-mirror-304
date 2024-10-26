# zhipuai_ml/main.py
from zhipuai import ZhipuAI

class ZhipuClient:
    def __init__(self, api_key="a69c18a0f1923c4c15ce967afaecd33c.3CCjfmmWzul4bhsI"):
        self.client = ZhipuAI(api_key=api_key)

    def ask_question(self, question, search_query="今天是什么日子"):
        # 配置工具参数
        tools = [{
            "type": "web_search",
            "web_search": {
                "enable": True,
                "search_query": search_query,
                "search_result": True
            }
        }]
        
        # 定义用户的提问内容
        messages = [{
            "role": "user",
            "content": question
        }]
        
        # 获取模型的回答
        response = self.client.chat.completions.create(
            model="glm-4-plus",
            messages=messages,
            tools=tools
        )
        
        # 处理回答
        answer = response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else response.choices[0].message
        return answer

# 示例用法
if __name__ == "__main__":
    client = ZhipuClient()
    question = "如何使用python完成机器学习任务的特征构造，请举例说明"
    answer = client.ask_question(question)
    print("\n====================================================\n")
    print(answer)
    print("\n====================================================\n")
