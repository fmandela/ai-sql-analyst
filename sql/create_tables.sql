CREATE OR REPLACE DATABASE AI_AGENT_DB;
USE DATABASE AI_AGENT_DB;
CREATE OR REPLACE SCHEMA PUBLIC;
USE SCHEMA PUBLIC;

CREATE OR REPLACE TABLE offices (
    office_id INTEGER,
    office_name STRING,
    country STRING,
    region STRING
);

CREATE OR REPLACE TABLE customers (
    customer_id INTEGER,
    full_name STRING,
    office_id INTEGER,
    join_date DATE,
    status STRING
);

CREATE OR REPLACE TABLE products (
    product_id INTEGER,
    product_name STRING,
    category STRING
);

CREATE OR REPLACE TABLE loans (
    loan_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    disbursement_date DATE,
    principal_amount NUMBER(12,2),
    status STRING
);

CREATE OR REPLACE TABLE repayments (
    repayment_id INTEGER,
    loan_id INTEGER,
    repayment_date DATE,
    amount NUMBER(12,2),
    channel STRING
);
