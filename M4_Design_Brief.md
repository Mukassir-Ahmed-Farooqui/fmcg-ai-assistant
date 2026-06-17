# M4: System Design & Discovery

## Objective
The objective of this project is to build an AI-powered conversational assistant for a Consumer Goods (FMCG) company, specifically for the Beverages category. The assistant aims to answer business user queries regarding promotional performance, inventory movement, regional sales, and campaign impact, reducing reliance on manual data analyst efforts.

## Key Design Decisions

1. **Architecture Stack**: 
   - **Backend**: Python with FastAPI and LangChain. Python is the industry standard for data manipulation and AI orchestration. FastAPI provides a fast, modern API framework. LangChain simplifies the interaction between the LLM and the database (SQL Agent).
   - **Database**: SQLite. For the purpose of this prototype and assessment, a local SQLite database provides zero-setup, reliable SQL capabilities while being completely portable.
   - **Frontend**: React (Vite) with Vanilla CSS. React allows for modular UI components. Vanilla CSS was chosen to adhere to the assessment's guidelines while maximizing control over aesthetics (glassmorphism, animations) to provide a premium user experience without relying on bulky libraries like Tailwind.

2. **Data Model**: 
   - The synthetic dataset follows a star-schema-like approach but normalized sufficiently for an LLM to understand.
   - `product_master` and `store_master` serve as dimensions.
   - `sales_promotions` and `inventory` serve as fact tables, aggregated at the weekly grain.
   - We explicitly added `promotion_flag` and `stockout_flag` as booleans. LLMs perform much better when boolean flags exist rather than asking them to infer a stockout from `closing_stock = 0`.

3. **LLM Orchestration Strategy**:
   - Instead of building custom text-to-SQL logic from scratch, we leverage LangChain's `create_sql_agent`. This agentic pattern is resilient: it uses a React (Reason+Act) loop to query the database schema, write a query, check for errors, fix the query, and formulate a final answer. This mitigates hallucinated columns.

## Pivots & Approach Changes

- **Initial thought**: Build a Streamlit app to combine backend and frontend in pure Python for maximum velocity.
- **Pivot**: The prompt specifically requests an interface that "wows the user" and feels "extremely premium", mentioning glassmorphism and modern web design. Streamlit is functional but rarely "premium" without heavy hacks. Thus, we pivoted to a decoupled architecture: a dedicated Vite+React frontend for high-quality UX, and a FastAPI backend for the AI logic.

## Challenges & Risks
- **Hallucinations in SQL**: The LLM might hallucinate column names. Mitigation: Using LangChain's SQL Toolkit allows the agent to `sql_db_schema` before writing queries.
- **Data Volume Context Window**: We cannot feed all data into the prompt. Mitigation: The agent only executes SQL and returns the *results* to the prompt, keeping context windows small and efficient.
