from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os
import openai
from flask import Flask, send_from_directory, request, jsonify, abort, render_template
app = Flask(__name__)
load_dotenv()
openai.api_key=os.environ['OPENAI_API_KEY']

csv_files = [
    'data/SnowIncidents-switches.csv',
    'data/usage_performance_data.csv',
    'data/warranty_support_data.csv',
    'data/u_cmdb_ci_switches.csv'
]

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("chat.html")

@app.route('/ask-queries', methods=['POST'])
def ask_sales_questions():
    try:
        data = request.get_json()
        user_question = data['query']
        sales_df = pd.read_csv('data/SnowIncidents-switches.csv')
        agent = create_pandas_dataframe_agent(OpenAI(temperature=0),
                                                    sales_df,
                                                    verbose=True, allow_dangerous_code=True)
        response = agent(user_question)['output']
        return jsonify({'response': response})
        # for file_path in csv_files:
        #     query_df =  pd.read_csv(file_path)
        #     agent = create_pandas_dataframe_agent(OpenAI(temperature=0),
        #                                         query_df,
        #                                         verbose=True)
        #     openai = OpenAI(temperature=0.0)
        #     response = agent(user_question)['output']
        # return jsonify({'response': response})
    except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(port=5000)
