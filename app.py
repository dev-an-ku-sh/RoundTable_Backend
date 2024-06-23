from flask import Flask, request, jsonify
from flask_cors import CORS
import autogen

#Local LLM Config
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

app = Flask(__name__)
# Apply CORS to all routes, Needed for POST from Website
CORS(app)

#Rephrase()
@app.route('/rephrase', methods=['POST'])
def rephrase():
    
    #Re-phrasing assistant
    rephrasing_assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config=mistral,
        system_message='''You are an assistant that re-phrases the statement 
        so that it makes sense and write it as a question, you do not have to provide a solution.''',
    )
    
    #Rephrasing Chat
    msg = request.json.get('problem_statement')
    message = f'''Please re-phrase the following statement so that it makes sense and write it as a question: '{msg}',
    provide only one sentence as the response, DO NOT provide a solution.'''
    chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=message, silent=False, max_turns=1)
    return jsonify({"response": chat_result.chat_history[1]['content']})


#Rephrase_With_Feedback
@app.route('/rephrase_with_feedback', methods=['POST'])
def rephrase_with_feedback():
    
    #Re-phrasing assistant
    rephrasing_assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config=mistral,
        system_message="You are an assistant that re-phrases the statement so that it makes sense and write it as a question, you do not have to provide a solution.",
    )

    #Rephrasing with Feedback Chat
    previous_ver = request.json.get('previous_ver')
    feedback = request.json.get('feedback')
    if previous_ver is None or feedback is None:
        return jsonify({"error": "Both previous_ver and feedback must be provided"}), 400
    message = f'''Please re-phrase the following statement so that it makes sense and write it as a question: '{previous_ver}', based on the feedback: '{feedback}',
    provide only one sentence as the response, DO NOT provide a solution.'''
    chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=message, silent=False, max_turns=1)
    return jsonify({"response": chat_result.chat_history[1]['content']})

#Persona Creation
@app.route('/create_persona_list', methods=['POST'])
def create_persona_list():
    
    #Persona_Creator Assistant
    persona_creator_assistant = autogen.AssistantAgent(
        name="Persona Creator Assistant",
        llm_config=mistral,
        system_message="Refer to this format [['Persona_Name', 'Perspective']}, you will be given a problem statement You have to use the mentioned format and create a list of 5 imaginary people having unique and contradicting opinions, the expected output should be exactly in the following format : {['Maximus Moneybags', 'Maximize transactions in bulk to take advantage of discounted gas fees during peak hours.'],['Frugal Freya', 'Minimize transactions and wait for off-peak hours or use alternative, lower-cost networks to save on gas fees.'],['Patient Pablo', 'Employ a long-term strategy by planning transactions in advance and setting gas limits to minimize the impact of price fluctuations.'],['Impulsive Igor', 'Disregard the cost of gas fees, make frequent transactions whenever desired without regard for optimal timing or cost-saving strategies.'],['Security-conscious Sofia', 'Focus on safety and employ multi-signature wallets to minimize potential loss due to high gas fees by ensuring proper authorization before making transactions.]] ONLY GIVE THE RAW LIST, It should be a valid Python List of Lists, avoid giving pretext, ONLY the list is needed, do not give anything else except the list like context or some sort of explaination''"
    )

    #Persona_Creator Chat
    problem_statement = request.json.get("problem_statement")
    if problem_statement is None:
        return jsonify({"error": "Problem statement must be provided"}), 400
    chat_result = user_proxy.initiate_chat(recipient=persona_creator_assistant, 
    message= problem_statement, silent = False, max_turns=1)
    raw_list = chat_result.chat_history[1]['content']
    formated_list = raw_list.replace('\n', '')
    formated_list2 = formated_list.replace('\\', '')
    return jsonify({"response": formated_list2})

if __name__ == "__main__":
    app.run(debug=True)