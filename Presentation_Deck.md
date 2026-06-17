# Slide 1: Title Slide
**Title:** FMCG Beverages: AI-Powered Analytics Assistant
**Subtitle:** Democratizing Data for Business Users
**Speaker:** [Your Name], AI Engineer

---

# Slide 2: The Problem
**Title: The Analytics Bottleneck**
- **Current State:** Business users heavily rely on data teams for basic insights (promotional performance, stockouts, regional comparisons).
- **Impact:** Delayed decision-making, repetitive ad-hoc requests, and constrained analyst bandwidth.
- **Goal:** Empower non-technical stakeholders to securely query complex business data using natural language, instantly.

---

# Slide 3: The Solution
**Title: Conversational Analytics at Scale**
- **Core Technology:** An AI Assistant powered by LangChain and LLMs.
- **Capabilities:** Translates plain English into executed SQL queries against the FMCG database.
- **Experience:** A premium, dark-mode, glassmorphic UI built in React to ensure the tool feels like a modern, enterprise-grade product.

---

# Slide 4: Data Architecture & Strategy
**Title: Modeling the FMCG Reality**
- **Structured for AI:** A clean, relational model with `Product Master`, `Store Master`, and weekly `Sales` and `Inventory` facts.
- **Edge Case Handling:** We explicitly model deep promotions (spiking sales up to 3x) and the resulting inventory stockouts. 
- **Boolean Optimization:** Engineered flags (`promotion_flag`, `stockout_flag`) to significantly reduce LLM reasoning errors.

---

# Slide 5: System Architecture & Agentic Workflow
**Title: Beyond Naive Text-to-SQL**
- **The Risk:** Standard text-to-SQL is prone to hallucinations (inventing columns) and syntax errors.
- **The Fix:** We implemented a LangChain **ReAct SQL Agent**.
- **The Flow:**
  1. AI inspects the live SQLite schema.
  2. AI drafts a SQL query.
  3. If execution fails, AI reads the error, self-corrects, and retries automatically.
  4. Returns the final, verified answer.

---

# Slide 6: Demo & Live Q&A
**Title: Seeing is Believing**
*Live Demo Scenario:*
1. "Which region had the highest revenue overall?"
2. "How many units of Spark Lemon did we sell during Price Cut promotions?"
3. "Did we experience any stockouts in the North region last month?"

**Conclusion:** Rapid insights without writing a single line of SQL.

---

# Slide 7: Next Steps & V2 Vision
**Title: Scaling the Assistant**
- **Cloud Migration:** Move from local SQLite to Supabase (PostgreSQL).
- **Visualization:** Enable the AI to generate dynamic charts (Recharts/Chart.js) alongside text answers.
- **Context Awareness:** Implement user session memory so stakeholders can ask follow-up questions (e.g., "What about the South region?").
