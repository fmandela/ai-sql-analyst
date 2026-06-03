import streamlit as st

from src.datasources import get_datasource
from src.llm_client import generate_sql
from src.sql_validator import validate_sql
from src.result_explainer import explain_results

st.set_page_config(page_title="AI SQL Analyst", layout="wide")

st.title("AI SQL Analyst")
st.caption("Ask business questions in plain English, generate safe SQL, and get a result explanation.")

if "datasource" not in st.session_state:
    st.session_state.datasource = get_datasource()

if "schema_summary" not in st.session_state:
    st.session_state.schema_summary = None

if "initialized" not in st.session_state:
    st.session_state.initialized = False

with st.sidebar:
    st.header("Demo environment")
    st.write("Default mode uses local DuckDB + CSV demo data. Snowflake can be enabled later via `.env`.")

    if st.button("Load demo environment"):
        try:
            st.session_state.datasource.initialize()
            st.session_state.schema_summary = st.session_state.datasource.load_schema_summary()
            st.session_state.initialized = True
            st.success("Demo environment loaded successfully.")
        except Exception as e:
            st.error(f"Failed to load demo environment: {e}")

if st.session_state.schema_summary:
    with st.expander("Schema summary", expanded=False):
        st.text(st.session_state.schema_summary)
else:
    st.info("Load the demo environment first from the sidebar.")

question = st.text_area(
    "Ask a question",
    placeholder="Example: Show total repayments by country",
)

if st.button("Generate and run query"):
    if not st.session_state.schema_summary:
        st.warning("Load the demo environment first.")
    elif not question.strip():
        st.warning("Enter a question first.")
    else:
        try:
            sql = generate_sql(question, st.session_state.schema_summary)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            is_valid, message = validate_sql(sql)
            if not is_valid:
                st.error(f"SQL validation failed: {message}")
            else:
                df = st.session_state.datasource.run_query(sql)

                st.subheader("Results")
                st.dataframe(df, use_container_width=True)

                preview = df.head(20).to_csv(index=False) if not df.empty else "No rows returned."
                explanation = explain_results(question, sql, preview)

                st.subheader("Explanation")
                st.write(explanation)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

with st.expander("Example questions"):
    st.markdown(
        """
- Show total repayments by country
- Show monthly repayment totals
- Which office has the highest total repayments?
- Show active loans by product
- What is the average principal amount by country?
- Show repayment totals by channel
        """
    )
