#!/usr/bin/env python
# coding: utf-8

# In[1]:


from zhipuai import ZhipuAI

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key="a69c18a0f1923c4c15ce967afaecd33c.3CCjfmmWzul4bhsI")

# 配置工具参数
tools = [{
    "type": "web_search",
    "web_search": {
        "enable": True  ,# 默认为关闭状态（False），禁用：False，启用：True。
         "search_query": "今天是什么日子",
         "search_result": True 
    }
}]

# 定义用户的提问内容
messages = [{
    "role": "user",
    "content": "如何使用python完成机器学习任务的特征构造，请举例说明"
}]

# 获取模型的回答
response = client.chat.completions.create(
    model="glm-4-plus",
    messages=messages,
    tools=tools
)

# 处理并清晰输出模型的回答
answer = response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else response.choices[0].message

print("\n====================================================\n")
print(answer)
print("\n====================================================\n")


# 

# In[ ]:




