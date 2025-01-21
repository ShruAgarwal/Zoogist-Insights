import os
import pandas as pd
import sqlite3
import logging
import streamlit as st
import plotly.graph_objects as go
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages.system import SystemMessage
from langchain_core.tools import Tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from typing import Any
# from langchain_core.exceptions import OutputParserException
# from typing import List, Dict, Any


# ---------- Logging & GROQ API Key Configs ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]


# ---------- Data Specific Prompt Template Creation ----------
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(
        content=(
            "You are an expert SQL generator, data analysis, and visualization assistant.\n"
            "Your task is to understand user requests, provide helpful, informative responses, and suggest appropriate data visualizations using the `mammals_df` dataset.\n"
            "This dataframe contains information about mammal occurrences.\n"
            "The dataframe has the following columns:\n"
            "   - `recordedBy` (TEXT) - The person who recorded the observation.\n"
            "   - `username` (TEXT) - The username of person associated with the observation.\n"
            "   - `timestamp` (DATETIME) - Automatic date and time of the observation.\n"
            "   - `date` (DATE) - The date of the observation.\n"
            "   - `time` (TIME) - The time of the observation.\n"
            "   - `decimalLatitude` (FLOAT) - The latitude of the observation  in decimal degrees N.\n"
            "   - `decimalLongitude` (FLOAT) - The longitude of the observation in decimal degrees E.\n"
            "   - `place` (TEXT) - Name of locality.\n"
            "   - `habitat` (TEXT) - The type of habitat where the mammal was observed.\n"
            "   - `speciesName` (TEXT) - The common name of the mammal species.\n"
            "   - `count` (INTEGER) - The number of individual mammals observed.\n"
            "   - `countType` (TEXT) - Total (fully counted groups) or Partial (incompletely counted groups) types for the count.\n"
            "   - `obsType` (TEXT) - The type of observation method.\n"
            "   - `scientificName` (TEXT) - The scientific name of the species.\n"
            "   - `instanceID` (TEXT) - A unique identifier for the observation.\n"
            "   - `conservationStatus` (TEXT) - The conservation status of the species.\n"
            "When a user asks a question:\n"
                  "   1. Analyze the user's question carefully. If the question requires fetching data from `mammals_df` (e.g., filtering, selecting columns, doing calculations, aggregations like counting or average), generate an appropriate SQL query and call the `execute_sql_query` function to retrieve the data.\n"
                  "   2. The SQL query must start with `SELECT` and `FROM` keywords followed by the required column names. Use `WHERE` to filter the data based on specific conditions if needed. Use `GROUP BY` for aggregation if needed. If aggregations like sum, average or counting is required on any of the columns, make sure to create an alias for that in your SQL query. You must include the alias of aggregated columns in the x and y axes names.\n"
                  "   3. To extract the year from the 'date' column, use the SQL function `strftime('%Y', date)` in your query, when the user specifically asks for anything related to observation year. Use date column only if specifically asked for.\n"
                  "   4. The SQL queries are case-insensitive and must only use column names mentioned above. The SQL queries must be valid and return appropriate column results based on the user questions.\n"
                  "   5. The `execute_sql_query` function will return a dictionary with the `sql_query_result` (list of dictionaries) and a `message`.\n"
                  "   6. If `sql_query_result` is `None`, return a message as the final answer and do not generate any kind of summarized insights or suggest any chart types if `sql_query_result` is `None`.\n"
                  "   7. If `sql_query_result` is not `None`, then based on the user's query, the SQL data retrieved, generate a short summary of findings and include a suitable chart type from the following allowed chart types: `bar_chart`, `pie_chart`, `line_chart`, and `scatter_plot`, based on the nature of the data retrieved.\n"
                  "   8.  In the summary, you must mention the x and y-axis columns needed for plotting the charts, make sure that the y axis column must be an alias from your SQL query if aggregation is needed. Include group by column name if the chart type needs grouping. All these columns must be taken from the dataframe `mammals_df`.\n"
                  "   9.  For example, if you generate a 'bar_chart', include appropriate x and y-axis columns with optional group by column. If you generate a 'pie_chart', only include x-axis column and no y-axis column or group by column. If you generate a 'scatter_plot', then include both x and y-axis columns. Similarly, if you are generating a `line_chart`, then add both x and y-axis columns.\n"
                  "   10. You must choose chart types carefully to show accurate information based on the user question. For example:\n"
                  "       - Use 'bar_chart' when you need to compare discrete values or counts for different categories or for showing distributions of values or frequencies.\n"
                  "       - Use 'line_chart' when you need to show the trends or changes over a continuous variable (e.g., over time) or to see the relationships between two continuous numerical variables.\n"
                  "       - Use 'pie_chart' when you want to show proportional data or percentage contribution for different categories.\n"
                  "       - Use 'scatter_plot' when you want to show the relation between two continuous numerical columns and want to see patterns in the data.\n"
                  "   11. The summary should be concise, informative and should also include the chart type, x-axis, y-axis, and group by column(if any) to display the visualization parameters.\n"
                  "   12. If the user question can be answered without querying the `mammals_df`, return the answer directly as a string.\n"
                  "   13. If there is an error during executing SQL query, then make sure to display the error message as the final output. Do not show anything else."

        )
    ),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])



# -------------------- Species Observation Map --------------------
@st.cache_resource
def generate_map(df):
    """Generates and displays a map of Tamil Nadu state in India with mammal occurrences."""
    try:
        # Create a copy of the original data frame so that we can apply some filtering if required.
        df_copy = df.copy()
        if "decimalLatitude" not in df_copy.columns or "decimalLongitude" not in df_copy.columns:
           st.error("Latitude or longitude columns not found in the dataframe.")
           return

        # Define a color mapping for conservation statuses
        conservation_colors = {
            'Least Concern': 'green',
            'Near Threatened': 'yellow',
            'Vulnerable': 'orange',
            'Endangered': 'red',
        }
        # Map conservation statuses to colors
        df_copy['marker_color'] = df_copy['conservationStatus'].map(conservation_colors)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scattermap(
            lat = df_copy["decimalLatitude"],
            lon = df_copy["decimalLongitude"],
            mode = 'markers',
            marker = go.scattermap.Marker(
                size=4,
                color='black'
            ),
           text = df_copy["place"],
           hoverinfo = 'text'
        ))
        fig.add_trace(go.Scattermap(
            lat = df_copy["decimalLatitude"],
            lon = df_copy["decimalLongitude"],
            mode = 'markers',
            marker = go.scattermap.Marker(
                size=10,
                color=df_copy['marker_color'],
                opacity=0.7
            ),
            text = df_copy['speciesName']+ '<br>' + df_copy['place'],
            hoverinfo = 'text'
        ))

        fig.update_layout(
            title=dict(text='Mammal Occurrences in Tamil Nadu (based on Conservation Status: 🟢 Least Concern, 🟡 Near Threatened, 🟠 Vulnerable, 🔴 Endangered)'),
            autosize=True,
            hovermode='closest',
            showlegend=False,
            map=dict(
                  style = "light",
                  center=dict(
                    lat=10.2916, #11.059821
                    lon=77.4912  # 78.387451
                      ),
                  zoom=8,
                   bearing=0,
                   pitch=0
                   )
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error generating the map: {e}")



# ---------- Function to load data ----------
@st.cache_data
def load_and_preprocess_data(data_path:str) -> pd.DataFrame:
    """Loads, preprocesses, and returns the merged dataframe."""
    try:
        mammals_df = pd.read_csv(data_path)
        return mammals_df
    except Exception as e:
        print (f"Error loading data:{e}")
        return None



# ---------- Function to execute SQL queries using SQLite ----------
def execute_sql_query(sql_query: dict | str, mammals_df: pd.DataFrame) -> dict[str, Any]:
    """Executes a SQL query on the loaded dataframe using SQLite, filters data based on query, and returns the results as a list of dicts.
    
        Args:
            sql_query: A dict containing the SQL query (e.g., {"sql_query":"SELECT species FROM mammals_df"})
            mammals_df: The dataframe on which to execute the query

            Returns:
            A dictionary containing the query results, or an error message. The dictionary format is:
            - On success: {"sql_query_result": List[dict], "message": "Query Successful"}
            - On error: {"sql_query_result": None, "message": "Error message string"}
    
    """
    try:
        if isinstance(sql_query, dict):
            query_str = sql_query.get("sql_query")
            if not query_str:
                logging.error(f"No SQL query found in the dictionary: {sql_query}")
                return {"sql_query_result": None, "message": "Error: No SQL query found in the dictionary"}
        elif isinstance(sql_query, str):
            query_str = sql_query
        else:
          logging.error (f"Invalid sql query: {sql_query}")
          return {"sql_query_result": None, "message": "Error: Invalid input for SQL query. Must be string or dictionary"}

        query_str = query_str.strip()

        if "select" not in query_str.lower() or "from" not in query_str.lower():
            logging.error(f"Invalid SQL query. Must contain SELECT and FROM keywords: {query_str}")
            return {"sql_query_result": None, "message": "Error: Invalid SQL query. Must contain SELECT and FROM keywords."}
        logging.info(f"Executing SQL query: {query_str}")

        # Convert pandas DataFrame to an SQLite database
        conn = sqlite3.connect(':memory:')
        mammals_df.to_sql('mammals_df', conn, if_exists='replace', index=False)

        # Execute the SQL query using SQLite
        cursor = conn.cursor()
        cursor.execute(query_str)

        # Fetch column names and results
        column_names = [desc[0] for desc in cursor.description]
        query_results = cursor.fetchall()

        conn.close()

         # Convert the results to a list of dictionaries
        formatted_results = [dict(zip(column_names, row)) for row in query_results]
        logging.info("Query executed successfully.")

        if not formatted_results:
            return {"sql_query_result": None, "message": "No records found based on your query."}

        return {"sql_query_result": formatted_results, "message": "Query successful"}

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return {"sql_query_result": None, "message": f"Error executing SQL query: {str(e)}"}
    except Exception as e:
      logging.error(f"Error executing SQL query: {str(e)}")
      return {"sql_query_result": None, "message": f"Error executing SQL query: {str(e)}"}



# ---------- Function to create and execute the LangChain agent ----------
@st.cache_resource
def create_and_run_agent(mammals_df: pd.DataFrame, _prompt):
    # Define Tools
    tools = [
        Tool(
            name="execute_sql_query",
            func=lambda query: execute_sql_query(query, mammals_df),
            description="Executes a SQL-like query on the dataframe. The input should be a valid SQL query string and outputs results of the query and message. ",
        )
    ]

    # Initialize ChatGroq LLM
    llm = ChatGroq(model_name="llama-3.1-8b-instant")

    # Create agent
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=_prompt)

    # Run agent
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # , max_iterations=10 - Set max iterations here to avoid LLM loops

    return agent_executor