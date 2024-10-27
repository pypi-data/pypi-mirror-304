from zhipuai import ZhipuAI


def chat_glm(contents, api=None, model='glm-4-flash', stream=True, history=None):
    if history is None:
        history = [{"role": "system", "content": ""}]

    client = ZhipuAI(api_key=api)  # 填写您自己的APIKey

    # 将新的用户消息添加到消息历史中
    history.append({"role": "user", "content": contents})

    response = client.chat.completions.create(
        model=model,  # 填写需要调用的模型编码
        messages=history,
        stream=stream
    )

    if stream:
        for chunk in response:
            # 假设chunk.choices[0].delta.content是API返回的实时内容
            yield chunk.choices[0].delta.content
            # 将模型的回复添加到消息历史中
            history.append({"role": "assistant", "content": chunk.choices[0].delta.content})
    else:
        # 假设response.choices[0].message.content是API返回的完整内容
        assistant_reply = response.choices[0].message.content
        # 将模型的回复添加到消息历史中
        history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
