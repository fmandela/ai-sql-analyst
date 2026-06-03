# AI SQL Analyst

A local-first AI analyst demo that turns plain-English business questions into safe SQL, runs the query, and explains the results.

The MVP uses DuckDB and CSV demo data so it can run locally without a warehouse. Snowflake support is included as a future datasource option.

## Features

- Local DuckDB demo environment
- CSV-backed microfinance sample dataset
- Schema introspection
- Natural language to SQL
- SELECT-only SQL validation
- Query execution
- Result explanation

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI API key to `.env`.

```bash
streamlit run app.py
```

## Usage

1. Open the app.
2. Click **Load demo environment** in the sidebar.
3. Ask a business question.
4. Review the generated SQL, result table, and explanation.

## Example questions

- Show total repayments by country
- Show monthly repayment totals
- Which office has the highest total repayments?
- Show active loans by product
- What is the average principal amount by country?
- Show repayment totals by channel

## Future Snowflake mode

Set this in `.env`:

```bash
APP_DATASOURCE=snowflake
```

Then fill in the Snowflake credentials and run the SQL setup files in the `sql/` folder.
