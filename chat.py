import openai

# This module is responsible for interacting with OPENAI API
# Current model GPT 3.5 Turbo

openai.api_key = '<YOUR_OPENAI_TOKEN>'

# Initial instructions
with open('bot_config.txt', 'r') as file:
    bot_conf = file.read()


original_msg = [
    {
        'role': 'system',
        'content': bot_conf
    }
]

def get_response(message):
    completions = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages= message,
        max_tokens=700,
        temperature=1
    )
    return completions.choices[0].message.content

def outreq(quest):
    messages= [
        {
            'role': 'system',
            'content': bot_conf
        },
        {
            'role': 'user',
            'content': quest
        }
    ]
    return get_response(messages)

def get_conv(conversation, new_request):
    msg = original_msg
    for i in range(len(conversation)):
        msg.append(
            {
                'role': 'user',
                'content': conversation.request[i]
            }
        )
        msg.append(
            {
                'role': 'assistant',
                'content': conversation.response[i]
            }
        )
        msg.append(
            {
                'role': 'user',
                'content': new_request
            }
        )
    return get_response(msg)
    