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
        "temperature": 0,  #lower = less creative
        "timeout": 240,
    }
    user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. You discuss with the chat manager and draw a conclusion",
    code_execution_config= {
        "work_dir": "code",
        "use_docker": False
    },
    human_input_mode="NEVER",
    )
    povs = []
    agent_list = [['Researcher Rachel', 'Focus on laboratory experiments and clinical trials to discover new treatments and cures for various types of cancers.'],['Fundraiser Finn', 'Secure sufficient funding from governments, non-profits, and private organizations to support ongoing research efforts and advancements in cancer treatment.'],['Collaborative Clara', 'Facilitate cooperation between researchers, institutions, and industries to pool knowledge and resources towards finding a cure for cancer.'],['Innovator Ivan', 'Develop unconventional approaches and new technologies, such as gene therapy or nanotechnology, to attack cancer cells in novel ways.'],['Skeptic Samantha', 'Advocate for evidence-based treatments and rigorous testing before approving any potential cure, ensuring patient safety and avoiding false promises.']]
    for agent in agent_list:
        assistant = autogen.AssistantAgent(
            name = agent[0], 
            system_message= f"You are {agent[0]}, your perspective {agent[1]}",
            llm_config=mistral,
            max_consecutive_auto_reply=1
        )
        povs.append(assistant)
    # print(povs)
    group_chat = autogen.GroupChat(
        agents=[user_proxy] + povs, messages=[], max_round=12
    )
    manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=mistral, system_message= "You listen to other assistants and draw a conclusion, avoid using code")
    user_proxy.initiate_chat(
        manager,
        message="""
    How to cure cancer
    """,
    )


if __name__ == "__main__":
    main()
