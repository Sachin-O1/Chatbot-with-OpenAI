import PySimpleGUI as sg
import openai

# OpenAI API key
openai.api_key = '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'

# ChatGPT parameters
chat_model = 'gpt-3.5-turbo'
chat_session_id = None


def send_message():
    message = window['input_field'].get()
    try:
        user_input = 'User: ' + message  # User input
        chat_response = get_chat_response(message)
        window['input_field'].update('')
        window['output_field'].print(user_input)  # Display user input
        window['output_field'].print('Bot: ' + chat_response)  # Display bot's response
    except Exception as e:
        window['output_field'].print('An error occurred:', str(e))


def get_chat_response(message):
    global chat_session_id

    if chat_session_id is None:
        response = openai.ChatCompletion.create(
            model=chat_model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': message}
            ]
        )
        if 'id' in response and 'object' in response:
            chat_session_id = response['id']
        else:
            raise ValueError('Failed to create chat session: ' + str(response))

    else:
        response = openai.ChatCompletion.create(
            model=chat_model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': message},
                {'role': 'system', 'content': chat_session_id}
            ]
        )

    if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
        chat_response = response['choices'][0]['message']['content']
    else:
        raise ValueError('Failed to retrieve chat response: ' + str(response))

    return chat_response


# Create GUI layout
layout = [
    [sg.Output(size=(60, 15), key='output_field')],
    [sg.Input(key='input_field'), sg.Button('Send', size=(10, 1), bind_return_key=True)]
]

# Create the window
window = sg.Window('Chatbot', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Send':
        send_message()

window.close()
