from flask import Flask, request, jsonify
import autogen

app = Flask(__name__)

@app.route('/rephrase', methods=['POST'])
def rephrase():
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
        system_message="You are an assistant that re-phrases the statement so that it makes sense and write it as a question, you do not have to provide a solution.",
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
    msg = request.json.get('problem_statement')
    message = f'''Please re-phrase the following statement so that it makes sense and write it as a question: '{msg}',
    provide only one sentence as the response, DO NOT provide a solution.'''
    chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=message, silent=False, max_turns=1)
    return jsonify({"response": chat_result.chat_history[1]['content']})

@app.route('/rephrase_with_feedback', methods=['POST'])
def rephrase_with_feedback():
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
        system_message="You are an assistant that re-phrases the statement so that it makes sense and write it as a question, you do not have to provide a solution.",
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
    previous_ver = request.json.get('previous_ver')
    feedback = request.json.get('feedback')
    if previous_ver is None or feedback is None:
        return jsonify({"error": "Both previous_ver and feedback must be provided"}), 400
    message = f'''Please re-phrase the following statement so that it makes sense and write it as a question: '{previous_ver}', based on the feedback: '{feedback}',
    provide only one sentence as the response, DO NOT provide a solution.'''
    chat_result = user_proxy.initiate_chat(recipient=rephrasing_assistant, message=message, silent=False, max_turns=1)
    return jsonify({"response": chat_result.chat_history[1]['content']})



if __name__ == "__main__":
    app.run(debug=True)