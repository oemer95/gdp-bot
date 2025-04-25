# GDP-Bot: An Intelligent Agent System for GDP Data Analysis

This project demonstrates an AI-powered, interactive agent system for analyzing Gross Domestic Product (GDP) data in a conversational format. The prototype showcases the potential of modern AI systems in the context of data science by enabling chat-based exploration and forecasting of economic indicators.

---

## Project Objectives

- Showcase how AI systems can support interactive data analysis.
- Enable users to load, visualize, and forecast GDP data for countries of interest.
- Provide general expert-like assessments regarding GDP trends.
- Use AI responsibly and efficiently with the OpenAI API.

---

## Features

- **Data Loading**  
  GDP data is loaded from a local source (e.g., `.csv` file) based on the user's query.

- **Visualization**  
  The system can generate charts and plots for single or multiple countries across selected time periods.

- **Expert Assessment**  
  The agent can explain economic trends and terms in simple language using publicly available economic knowledge.

- **Forecasting**  
  The agent can forecast GDP values for `n` future years using statistical or machine learning models (e.g., ARIMA, Prophet, linear regression).

- **Conversational Interface**  
  The user interacts via natural language – the agent only responds to GDP-related questions.

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/gdp-chat-agent.git
cd gdp-chat-agent
```

2. Set up a virtual environment

python -m venv venv
source venv/bin/activate   # Use `venv\Scripts\activate` on Windows
pip install -r requirements.txt

3. Add your OpenAI API key

OPENAI_API_KEY=...

---

## Running the application

python app.py

---

## Example Prompts

How has Germany's GDP changed since 2000?

Compare the GDP of Germany and France.

Forecast Italy’s GDP for the next 5 years.

What does negative GDP growth mean?

---

## Author

Ömer Erduran (oemer95)
