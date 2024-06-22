import autogen


def main():
    #local LLM Config
    mistral = {
        "config_list": [
            {
                "model": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
                "base_url": "http://localhost:1234/v1",
                "api_key": "lm-studio"
            }
        ],
        "cache_seed": None,
        "max_tokens": 1024,
        "temperature": 1,  #lower = less creative. [0,1]
        "timeout": 240,
    }
    
    #Re-phrasing assistant
    rephrasing_assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config=mistral,
        system_message="You are an assistant that re-phrases the statement so that it makes sense, you do not have to provide a solution.",
    )
    
    #User Proxy Agent
    user_proxy = autogen.UserProxyAgent(
        name="Pseudo Admin",
        default_auto_reply="No need for further improvement, the refactored version is good enough",  # needed for local LLMs
         code_execution_config={
            "work_dir": "code",
            "use_docker": False
        },
        human_input_mode="NEVER",
    )
    # msg = input("Please enter your problem statement: ")
    # message = f'''Please re-phrase the following statement so that it makes sense: '{msg}',
    # provide only one sentence as the response, DO NOT provide a solution.'''
    # chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=message, silent = False)
    # print('this is chat result: ')
    # print(chat_result)
    # last_chat_content = chat_result.chat_history[-1]['content']  
    # print('this is desired output: ')
    # print(last_chat_content) 
    msg = input("Please enter your problem statement: ")
    message = f'''Please re-phrase the following statement so that it makes sense: '{msg}',
    provide only one sentence as the response, DO NOT provide a solution.'''
    chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=message, silent=False, max_turns=1)
    
    # your_prev_statement = chat_result.chat_history[1]['content']

    # Print the first output given by the rephrasing assistant
    # first_output = chat_result.chat_history[1]['content']
    # print('First output from the assistant: ', first_output)

    # feedback = input("Please provide your feedback: ")
    # if feedback:
    #     feedback_message = f'''Based on the feedback: '{feedback}', please re-phrase the statement again.'''
    #     chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=feedback_message, silent=False)
    #     print('New output from the assistant: ', chat_result.chat_history[-1]['content'])


if __name__ == "__main__":
    main()
