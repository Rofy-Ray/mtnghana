from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_mistralai.chat_models import ChatMistralAI as Mistral
from langchain.agents import AgentType, AgentExecutor
from dotenv import load_dotenv
import re
# import matplotlib.pyplot as plt
from utils.plotting import extract_plot_image, fetch_plot_image

load_dotenv()

def create_pandasai_agent(df):
    llm = Mistral(
        temperature=0,
        model="pixtral-12b-2409",
        max_tokens=2409,
    )
    
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=False,
        handle_parsing_errors=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        max_iterations=3,
        allow_dangerous_code=True,
        return_intermediate_steps=True
    )
    
    return agent

def extract_final_answer(text):
    """Extract the final answer from the agent's response."""
    final_answer_match = re.search(r"Final Answer: (.*?)(?=\n|$|For troubleshooting)", text)
    if final_answer_match:
        return final_answer_match.group(1).strip()
    
    thought_match = re.search(r"Thought: .*?\. ([^\.]+\.)(?=\n|$)", text)
    if thought_match:
        return thought_match.group(1).strip()
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in reversed(lines):
        if not any(error_text in line.lower() for error_text in ['error', 'troubleshooting', 'parsing']):
            return line
    
    return text

def handle_agent_response(agent, user_input):
    try:                
        # code_block = extract_python_code(response_text)
        
        # if code_block and any(cmd in code_block for cmd in ['plt.show()', 'plt.plot', 'plt.bar']):
        #     plot_data = execute_plot_code(code_block, agent.tools[0].df)
        #     if plot_data:
        #         clean_response = extract_final_answer(response_text)
        #         return {
        #             'text': clean_response,
        #             'plot': plot_data.getvalue()
        #         }
                
        response = agent.invoke({"input": user_input})
        response_text = ""
        
        if isinstance(response, dict) and "intermediate_steps" in response:
            for step in response["intermediate_steps"]:
                response_text += str(step) + "\n"
                        
        plot_image_path = extract_plot_image(response_text)
        if plot_image_path:
            plot_data = fetch_plot_image(plot_image_path)
            if plot_data:
                return {
                    'text': extract_final_answer(response_text),
                    'plot': plot_data
                }
        
        if isinstance(response, str) and "Final Answer:" not in response:
            return {'text': response}
            
        if isinstance(response, str) and ("An output parsing error occurred" in response or "Final Answer:" in response):
            return {'text': extract_final_answer(response)}
            
        if isinstance(response, dict):
            if "output" in response:
                return {'text': response["output"]}
            elif "intermediate_steps" in response:
                steps_text = str(response["intermediate_steps"])
                return {'text': extract_final_answer(steps_text)}
        
        return {'text': str(response)}
        
    except Exception as e:
        print(f"Debug - Full error: {str(e)}")
        if "parsing error" in str(e).lower():
            return {'text': extract_final_answer(str(e))}
        return {'text': f"I couldn't process that request. Please try rephrasing your question."}