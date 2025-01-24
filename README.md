# Zoogist Insights 🐘🦦

## About 🎯

This project is a **proof-of-concept (PoC) for an AI-powered tool** designed to demonstrate the capabilities of **function calling using Large Language Models (LLMs)**. It aims to assist researchers and professionals in analyzing biodiversity datasets, specifically focusing on mammal occurrences (as of now). You can ask questions in natural language, and the tool will provide summarized results and suggest chart visualizations whenever possible.


## Demo 🕹
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://zoogist-insights.streamlit.app/)

## How To Use 👀
1. Submit a question using the text input or select a demo query.
2. After submitting, the LLM powered assistant will give a response, and also suggest charts to visualise it.
3. Use the container in the sidebar to plot charts through given drop-down selections for x, y axes, chart type, and color.
4. You can also select values from the habitat column and generate specific charts. 


## Behind the Scenes ⚙

*Here's a breakdown of how Zoogist Insights processes your queries and delivers data insights:*

1.   **`utils.py`:**
- First, it loads and preprocesses the dataset through the `load_and_preprocess_data` function.
- Second, it includes the `execute_sql_query` function (defined as a tool) to execute the SQL queries generated by the LLM & retrieve data from the dataset. Further, it utilizes an in-memory (temporary) `sqlite3` database for executing the queries and then returns the results of SQL execution as a list of dictionaries.
- Third, it sets up the LLM agent powered by the `llama-3.1-8b-instant` model through the **[Groq](https://groq.com/) API** for data analysis, and summarization with specific instructions about the data, all this through **[LangChain](https://python.langchain.com/docs/introduction/)** framework.
  - This language model has been used for its balance between speed and text generation quality, and has worked well during PoC development for summarizing insights.
  - The `execute_sql_query` function serves as a tool for the LLM agent to query the database by understanding when to call the function and passing the required query string in the specified format for analysis.

2.    **`app.py`:**
- The main script demonstrates how the LLM agent works through a user-friendly web interface using **[Streamlit](https://streamlit.io/)**.
- It loads the `01-mammals-data-final.csv` dataset, and utilizes the functions from `utils.py` to perform data analysis.
  - The LLM agent can handle your biodiversity-related questions and provide suggestions for plotting relevant charts.
  - Chart plotting is tackled separately, enabling you to tweak parameters and unlock valuable insights from the data.
  - Changing the query using the **`Run Query`** button will clear the stored charts and generate a new response based on the updated question.
  - The map is displayed separately with geographical points, where the tooltips show both place and species names.


## Tech Stack 🛠

-   Streamlit
-   LangChain
-   Groq API
-   Pandas
-   Plotly

## Disclaimer ⚠

This PoC is a demonstration of the potential of AI in biodiversity data analysis and is not intended to be a fully functional or specialized AI tool. It should not be used for professional analysis or critical scientific decisions without proper validation. This tool may have inaccuracies, biases, or limitations based on underlying language model capabilities and data quality. The app is a basic implementation and can be further improved by implementing advanced analytics and agentic AI techniques.

## Credits ✨
- Original dataset taken from **[Zenodo](https://zenodo.org/records/11903722)** presented under **NCF public repository.**
- *Thanks to* [Yuichiro's Streamlit Theme Editor](https://github.com/whitphx/streamlit-theme-editor) that helped me find the suitable app's theme :)

<!--## Problem
Professionals in the biodiversity domain, both globally and in India, frequently encounter challenges when dealing with complex and large datasets related to species occurrences. These datasets often require:

-   **Specialized Skills:** Data analysis often demands advanced technical expertise, hindering accessibility for researchers without a strong background in programming or data science.
-   **Time-Consuming Processes:** Manual data exploration, filtering, and visualization can be tedious and time-intensive, slowing down research progress.
-   **Fragmented Tools:** Existing tools and solutions are often half-baked or scattered across different platforms, making it difficult to manage data analysis in a unified way.
-   **Lack of Natural Language Interaction:** Most existing tools rely on structured queries or GUIs, making it difficult to quickly explore data through intuitive natural language questions.

This leads to a common problem of the professionals and domain experts spending a lot of time extracting insights from data, instead of focusing on data collection & analysis itself, and there is a need for user-friendly and intelligent data analysis workflow.


## Solution 💡
Our MVP demonstrates how AI (both GenAI and Agentic AI) can address the above challenges by:

-   **Natural Language Processing:** The ability to ask questions using natural language, allowing intuitive interaction and access to complex datasets.
-   **Automated Data Analysis:** Leveraging large language models (LLMs) to generate SQL queries, perform basic analysis tasks like summarization and aggregation, reducing manual analysis efforts.
-   **Interactive Visualizations:** A user-friendly way for professionals to display the data in different types of charts and maps based on the insights generated by the AI assistant.-->


<!-- `utils.py` First-Draft Prompt:
"   1. Analyze the user's question carefully. If the question requires fetching data from `mammals_df` (e.g., filtering, selecting columns, doing calculations), generate an appropriate SQL query and call the `execute_sql_query` function to retrieve the data.\n"
"   2. The SQL query must start with `SELECT` and `FROM` keywords followed by the required column names. Use `WHERE` to filter the data based on specific conditions if needed.\n"
"   3. The SQL queries are case-insensitive and must only use column names mentioned above.\n"
"   4. The `execute_sql_query` function will return a dictionary with the `sql_query_result` (list of dictionaries) and a `message`.\n"
"   5. If `sql_query_result` is `None`, return the `message` as the final answer. Do not create any other summaries or charts if `sql_query_result` is `None`.\n"
"   6. If `sql_query_result` is not `None`, then based on the user's query and the data, decide what kind of visualization (chart type) would be suitable. The possible chart types are 'bar_chart', 'pie_chart', 'line_chart', 'scatter_plot'. You should also provide necessary columns for the x and y axes, and group by clause if needed.\n"
"   7. Return a JSON object with a 'visualization' key containing the chart type, x axis, y axis, group by column name (if applicable), as a python dictionary, after getting SQL results from `execute_sql_query` tool. Ensure the returned value is a valid python dictionary before generating any summary.\n"
"   8. Summarize the data and visualization insights based on the SQL result and generated chart type. Do not return the actual `sql_query_result` to the user. Instead, provide a high-level, easy to understand summary based on the user query.\n"
"   9. If the user question can be answered without querying the `mammals_df`, answer directly without using the `execute_sql_query` function. Do not return empty JSON object if no SQL query is required.\n"
"   10. To extract the year from the 'date' column, use the SQL function `strftime('%Y', date)` in your query, when the user specifically asks for anything related to observation year. Use date column only if specifically asked for.\n"-->
