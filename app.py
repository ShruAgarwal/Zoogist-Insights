from utils import generate_map, load_and_preprocess_data, create_and_run_agent, prompt
from datetime import datetime
import streamlit as st
import plotly.express as px
import json

st.set_page_config(
   page_title="Zoogist Insights",
   page_icon="🐯",
   layout="wide"
)


@st.dialog("About Zoogist Insights 🦎", width="large")
def about():
    with st.container(key="about_app_txt"):
        # st.header("About the AI 🤖!")
        st.markdown(
        """
        This app demonstrates how AI can assist in analyzing biodiversity data through the **Groq API and LangChain**. It utilizes a real dataset that includes
        *Mammal occurrence records from (Jan 2020 to June 2023) in the Valparai Plateau and Anamalai Tiger Reserve, located in the Western Ghats region of Tamil Nadu, India*.
        
        ---
        **⚠ Disclaimers:** 
        - This tool is a **proof-of-concept (PoC)** and not intended for any professional analysis or critical scientific decisions.
        - It showcases a basic implementation of AI for data analysis and serves as a starting point for more advanced tools.
        - The results represent real-world scenarios but can still have errors or biases due to data and AI model limitations.
        ---

        **🌠 Vision**
        
        To develop AI-powered tools with enhanced agentic capabilities to enable biodiversity analysis more easily and accessibly over any observatory-based datasets. 
        This includes: 
          - enabling complex and user-friendly querying interfaces for diverse datasets.
          - providing detailed, multi-step analytical workflows.
          - supporting advanced visualization options.
          - offering tools for collaborative and reproducible research.
        ---

        **🌱 How This Can Help**
        
         This tool can help researchers in accessing data, visualize findings, generate quick insights and simplify data analysis workflows.
    
        """
    )

    st.success('Dataset taken from *[Zenodo](https://zenodo.org/records/11903722)* presented under **NCF public repository.**')
    st.info('Developed by *[Shruti Agarwal](https://www.linkedin.com/in/shruti-agarwal-bb7889237)*')


# ---------------------- Data Loading -------------------
mammals_df = load_and_preprocess_data("01-mammals-data-final.csv")

# ---------------------- Chat UI -------------------
# APP TITLE
st.title(" Zoogist Insights 🐘🦦")
st.markdown("### *Explore biodiversity data with AI*")

# =========================
# APP INFO SIDEBAR
with st.sidebar:
    # Dialogbox for app info
    if st.button("Click for App Info", icon="ℹ", key="about_app"):
        about()

    st.markdown(
        """
        ---
         **👀 How to use:**
          1. Submit a question using the text input or select a demo query.
          2. Get AI-driven responses along with suggestions for charts to visualize.
          3. Use the container below to create charts from the drop-down selections and filter by habitat.
        """
    )
    
    # Interactive Custom Chart Generation (based on suggestions given by the LLM) ---------- 
    container = st.container(border=True)
    container.write("Metrics for generating charts 🔽")
    
    # Select boxes
    x_axis_options = mammals_df.columns.tolist()
    y_axis_options = mammals_df.columns.tolist()
    chart_type_options = ['bar_chart', 'pie_chart', 'line_chart', 'scatter_plot']

    
    # Multi-Select option for the `habitat`` column
    filter_options = {
        "habitat": mammals_df["habitat"].unique().tolist()
    }
    filter_selected_options = {}
            
    # Create Columns for the select boxes
    x_axis_col = container.selectbox("Select X-axis Column:", x_axis_options, key = "x_axis_col")
    y_axis_col = container.selectbox("Select Y-axis Column:", y_axis_options, key = "y_axis_col")
    chart_type = container.selectbox("Select Chart Type:", chart_type_options, key = "chart_type_plot")
    color_col = container.selectbox("Select Color (Optional):", [None] + x_axis_options, key = "color_col")

    for filter_name, options in filter_options.items():
        filter_selected_options[filter_name] = container.multiselect(f"Select {filter_name} (Optional):", options = options, key = f"filter_options_{filter_name}")

    px_chart = container.button("📊 Visualize Chart")



# Defining Sample Queries ----------
demo_queries = [
    "List all the species and their scientific names, place which has a Endangered status.",
    "Find the habitat were the highest number of least concern species are found.",
    "Show the date, place, and the habitat where Tiger species were observed.",
    "Calculate the sum of the count for Dhole species.",
    "Which of the users has recorded the most species with a Near Threatened status?",
    "Calculate the sum of count for all species with a Vulnerable status and list as per their names."
]


# Initialize session state for queries ----------
if 'user_query' not in st.session_state:
    st.session_state['user_query'] = ""
if 'selected_query' not in st.session_state:
    st.session_state['selected_query'] = demo_queries[0] # Default to first demo query


# ----------------- Displays the Species Observation Map -----------------
generate_map(mammals_df)
st.write('---')

# ----------------- Selectbox for queries -----------------
input_container = st.container(border=True)
selected_query = input_container.selectbox("Select a demo query:",
                             options=demo_queries,
                             index=demo_queries.index(st.session_state['selected_query']) if st.session_state['selected_query'] in demo_queries else 0,
                             key = "selectbox_query")
st.session_state['selected_query'] = selected_query

# ----------------- Text input for custom queries -----------------
user_query = input_container.text_input("Or, enter your own query here:", key="custom_query", value = st.session_state['user_query'])
st.session_state['user_query'] = user_query

query_run = st.button("Run Query")



# -------------------- Agent initialization & Results generation --------------------
agent_executor = create_and_run_agent(mammals_df, prompt) # Pass prompt here

def display_results(agent_response):
    """Displays LLM responses and handles visualization based on the LLM output."""
    st.session_state['output'] = None # Initialize output to None before the try block
    try:
        # Attempt to parse the JSON object
        try:
            output = json.loads(agent_response["output"])
            st.session_state['output'] = output
            st.session_state['summary_text'] = output.get('summary', output.get('answer', None))

        except json.JSONDecodeError as e:
            st.session_state['summary_text'] = agent_response["output"] # Store only the string output if JSON parsing fails

        if  st.session_state['summary_text']: # Display the output
            st.markdown("### **AI Assistant Response 🤖**")
            st.write(st.session_state['summary_text'])

    except Exception as e:
        st.error(f"An error occurred: {e}")


def plot_chart(df, x_axis_col, y_axis_col, chart_type, color_col, filter_selected_options):
    """Function to handle the plotting of user-selected parameters for definitive chart options."""
    try:
         
        # Apply filters
        filtered_df = df.copy()
        for filter_name, selected_values in filter_selected_options.items():
           if selected_values:
               filtered_df = filtered_df[filtered_df[filter_name].isin(selected_values)]

        # Extract year from date column if selected in the x-axis
        if x_axis_col == 'date':
            # Convert date strings to datetime objects explicitly
            filtered_df['year'] = filtered_df['date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y').year if isinstance(x, str) else x.year)
            x_axis_col = 'year'  # Update x-axis to be year for plotting
        if y_axis_col == 'date':
            filtered_df['year'] = filtered_df['date'].apply(lambda x: datetime.strptime(x, '%d-%m-%Y').year if isinstance(x, str) else x.year)
            y_axis_col = 'year'

        if y_axis_col and x_axis_col:
             if chart_type == 'bar_chart':
                  fig = px.bar(filtered_df, x=x_axis_col, y=y_axis_col, color = color_col, title = "Interactive Bar Chart")
             elif chart_type == 'pie_chart':
                  fig = px.pie(filtered_df, names=x_axis_col, values=y_axis_col, title = "Interactive Pie Chart")
             elif chart_type == 'line_chart':
                  fig = px.line(filtered_df, x=x_axis_col, y=y_axis_col, title = "Interactive Line Chart")
             elif chart_type == 'scatter_plot':
                  fig = px.scatter(filtered_df, x=x_axis_col, y=y_axis_col, color = color_col, title = "Interactive Scatter Plot")
             else:
                   st.error("Invalid Chart Type Selected!")
                   return
        else:
             st.error("Invalid selection for chart parameters!")
             return
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error generating plot based on user input: {e}")



if __name__ == "__main__":
    if query_run:
        if selected_query or user_query:
            query_to_use = user_query if user_query else selected_query # Use custom query if provided, otherwise use selected
            with st.spinner("Analyzing the data..."):
                response = agent_executor.invoke({"input": query_to_use})
                display_results(response)        
    else:
         st.warning("Please enter a query.")

    # -------- Plotting the visualizations --------
    if px_chart:
        if x_axis_col and y_axis_col and chart_type:
            plot_chart(mammals_df, x_axis_col, y_axis_col, chart_type, color_col, filter_selected_options)
        else:
            st.error("Please select valid X-axis, Y-axis and Chart Type.")