# Zoogist Insights 🐘🦦

## About

This project is an proof-of-concept (PoC) for an AI-powered tool designed to assist researchers and professionals in analyzing biodiversity datasets, specifically focusing on mammal occurrences. It allows users to ask questions in natural language, and the assistant will provide summarized results and visualizations, when possible.


This MVP showcases this through:

-   **LangChain Integration:** For easy integration of LLMs with existing data workflows.
-   **Groq LLM:** For leveraging a very fast language model, specifically the `mixtral-8x7b-32768` model, to generate the responses. This model has been used for its balance between speed and text generation quality, and has worked well during MVP development for summarizing insights based on complex queries.
-   **Streamlit Interface:** To create a user-friendly web-based application that anyone can use.
-   **Plotly Visualizations:** For creating different types of interactive charts based on user inputs.

## How This Works ⚙

1.  **Data Input:** The app uses the `01-mammals-data-final.csv` dataset, which contains mammal occurrence records.
2.  **Query Input:** Users submit questions using the text input or the select box, and this will be parsed by the LLM, which acts as the AI assistant.
3.  **LLM Processing:**
    -   The LLM generates SQL queries to extract relevant data.
    -   The LLM analyzes the extracted data and provides a short summary.
    - The LLM also provides a recommendation for suitable chart types based on the query.
4.  **Interactive Chart Generation:**
    - Users can use the chart container in the sidebar to select different plotting parameters.
    - Upon selecting the required options and clicking the Plot Visualization button, a chart is displayed in the main section.
     - You can also utilize the multiselect widget to select specific values for `habitat`, `speciesName`, and `conservationStatus` columns if you wish to plot chart for the limited data in a particular category.
    - If the user changes the query using the Run Query button, the chart will be removed from the app and the LLM will provide new chart recommendations for the new query.

### Files:

-   **`app.py`:** The main Streamlit application code.
-   **`utils.py`:** Utility functions for data loading, preprocessing, and agent creation.
-   **`01-mammals-data-final.csv`:** The sample dataset.

## Tech Stack 🛠

-   Python
-   Streamlit
-   LangChain
-   Groq
-   pandas
-   plotly
-  GeoPandas (optional)

## Disclaimer ⚠

This MVP is a demonstration of the potential of AI in biodiversity data analysis and is not intended to be a fully functional or specialized AI tool. It should not be used for professional analysis or critical scientific decisions without proper validation. This tool may have inaccuracies, biases, or limitations based on underlying LLM capabilities and data quality. This application is a basic implementation and can be further improved by implementing advanced analytics and agentic AI techniques.
The accuracy of the results depends entirely on the quality of data and the capabilities of the underlying language model. The tool is not an agentic system, and it does not perform any complex data analysis workflows.


<!-- ## How To Use
1. Submit a question using the text input or select a demo query.
2. After submitting, the LLM powered assistant will give a response, and also suggest charts to visualise it.
3. Use the container below to plot charts through given drop-down selections for x, y axes, chart type, and color.
4. You can also use multi-options to select specific values for habitat column and then generate some specific chart.-->


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