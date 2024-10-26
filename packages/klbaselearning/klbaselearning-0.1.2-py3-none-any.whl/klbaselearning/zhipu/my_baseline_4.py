#!/usr/bin/env python
# coding: utf-8

# In[7]:


from zhipuai_ml import ZhipuClient

client = ZhipuClient()
question = "如何在window环境下设置一个域名指定一个ip，以绕过系统的DNS限制"
answer = client.ask_question(question)
print(answer)


# In[ ]:




