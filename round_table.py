import autogen

PersonaList = [
 {'Persona_Name' : 'Maximus Moneybags', 'Perspective': "Maximize transactions in bulk to take advantage of discounted gas fees during peak hours."},
 {'Persona_Name' : 'Frugal Freya', 'Perspective': "Minimize transactions and wait for off-peak hours or use alternative, lower-cost networks to save on gas fees."},
 {'Persona_Name' : 'Patient Pablo', 'Perspective': "Employ a long-term strategy by planning transactions in advance and setting gas limits to minimize the impact of price fluctuations."},
 {'Persona_Name' : 'Impulsive Igor', 'Perspective': "Disregard the cost of gas fees, make frequent transactions whenever desired without regard for optimal timing or cost-saving strategies."},
 {'Persona_Name' : 'Security-conscious Sofia', 'Perspective': "Focus on safety and employ multi-signature wallets to minimize potential loss due to high gas fees by ensuring proper authorization before making transactions."}
 ]

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

    #user proxy agent
    user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. You job is to ask the user for feedback once all agents have given their opinion, do not provide your own opinion.",
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    },
    human_input_mode="TERMINATE",
    )

    #create agents
    assistants = []
    for persona in PersonaList:
        assistant = autogen.AssistantAgent(
            name=persona['Persona_Name'],
            llm_config=mistral,
            system_message=f"You are {persona['Persona_Name']}. Your perspective: {persona['Perspective']}",
            max_consecutive_auto_reply=1
        )
        assistants.append(assistant)
        # print(assistant.name, assistant.system_message)

    # group_chat = autogen.GroupChat(
    #     agents=[user_proxy] + assistants, messages=[], max_round=8
    # )
    # manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=mistral)

    # user_proxy.initiate_chat(
    #     manager,
    #     message="""
    # Based on your perspective, provide a plan to optimize gas fees for transactions on the Ethereum network.
    # """,
    # )
    feedbackList = []
    def reply_to_assistant(assistant_index, feedback_message):
        feedback = {
            "recipient": assistants[assistant_index],
            "message": feedback_message,
            "clear_history": True,
            "silent": False,   
            "summary_method": "reflection_with_llm"   
        }
        feedbackList.append(feedback)

    def prompt_user_and_reply():
        while True:
            user_input = input("Enter command: ")
            if user_input.lower() == "reply":
                assistant_index = int(input("Enter assistant index: "))
                feedback_message = input("Enter feedback message: ")
                reply_to_assistant(assistant_index, feedback_message)
            elif user_input.lower() == "stop":
                user_proxy.initiate_chats(feedbackList)
                break
            else:
                print("Invalid command. Enter 'reply' to reply to an assistant or 'stop' to stop and send the feedback.")
    
    user_proxy.initiate_chats(
        [
            {
                "recipient": assistants[0],
                "message": "How would you approach the problem in 20 words or less : 'What are the methods for minimizing Ethereum Virtual Machine (EVM) transaction gas fees?' ",
                "clear_history": True,
                "silent": False, #if True, conversation is invisible to the user
                "summary_method": "reflection_with_llm" #sequential, includes whole conversation not just the last message
            },
            {
                "recipient": assistants[1],
                "message": "How would you approach the problem in 20 words or less : 'What are the methods for minimizing Ethereum Virtual Machine (EVM) transaction gas fees?' ",
                "clear_history": True,
                "silent": False, #if True, conversation is invisible to the user
                "summary_method": "reflection_with_llm" #sequential, includes whole conversation not just the last message
            },
            {
                "recipient": assistants[2],
                "message": "How would you approach the problem in 20 words or less : 'What are the methods for minimizing Ethereum Virtual Machine (EVM) transaction gas fees?' ",
                "clear_history": True,
                "silent": False, #if True, conversation is invisible to the user
                "summary_method": "reflection_with_llm" #sequential, includes whole conversation not just the last message
            },
            # {
            #     "recipient": assistants[3],
            #     "message": "How would you approach the problem in 20 words or less : 'What are the methods for minimizing Ethereum Virtual Machine (EVM) transaction gas fees?' ",
            #     "clear_history": True,
            #     "silent": False, #if True, conversation is invisible to the user
            #     "summary_method": "reflection_with_llm" #sequential, includes whole conversation not just the last message
            # },
            # {
            #     "recipient": assistants[4],
            #     "message": "How would you approach the problem in 20 words or less : 'What are the methods for minimizing Ethereum Virtual Machine (EVM) transaction gas fees?' ",
            #     "clear_history": True,
            #     "silent": False, #if True, conversation is invisible to the user
            #     "summary_method": "reflection_with_llm" #sequential, includes whole conversation not just the last message
            # },
        ]
    )
    prompt_user_and_reply()
 

if __name__ == "__main__":
    main()
