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
    persona_creator_assistant = autogen.AssistantAgent(
        name="Persona Creator Assistant",
        llm_config=mistral,
        system_message='''You are an assistant that creates a list of 5 imaginary people 
        who have significantly different ways of approaching the given problem statement. 
        The people should have opinions that contrast, contradict & conflict each other. 
        Do not mention variations, do not have them have a conversation, just give me 5 people in format 
        [{'Persona_Name' : Name, 'Perspective': Perspective}]''',
    )
    
    #User Proxy Agent
    user_proxy = autogen.UserProxyAgent(
        name="Pseudo Admin",
        default_auto_reply="exit",  # needed for local LLMs
         code_execution_config={
            "work_dir": "code",
            "use_docker": False
        },
        human_input_mode="ALWAYS",
    )
    msg = input("Please enter your problem statement: ")
    user_proxy.initiate_chat(recipient=persona_creator_assistant, message= f'''Based on the question : {msg} create a list of 5 imaginary people 
    who have significantly different ways of approaching the given problem statement. 
    The people should have opinions that contrast, contradict & conflict each other. 
    Do not mention variations, do not make them have a conversation, just give me 5 people in format 
    [{{'Persona_Name' : Name, 'Perspective': Perspective}}]''', silent = False)


if __name__ == "__main__":
    main()
