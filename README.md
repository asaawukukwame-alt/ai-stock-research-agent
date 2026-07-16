# AI Stock Research Agent

An AI-powered stock research application that generates structured equity research briefs from public financial data, market data, and recent news headlines.

## Project Overview

This project takes a stock ticker symbol and produces a structured investment research brief.

The app gathers public company fundamentals, market data, and recent headlines, then uses an AI workflow to generate a research-style report with:

* Company name and ticker
* Recommendation
* Conviction level
* Fundamental snapshot
* Key valuation tension points
* Bull case
* Bear case
* What to watch
* Final verdict

This project was built to demonstrate practical AI application development using Python, LangGraph, structured LLM outputs, financial data APIs, and Streamlit.

## Features

* Retrieves company fundamentals from SEC EDGAR
* Retrieves market data from Yahoo Finance
* Retrieves recent stock-related news headlines
* Uses LangGraph to organize the AI workflow
* Uses GPT-4o for structured financial analysis
* Uses Pydantic schemas to control the output format
* Includes a command-line interface
* Includes a Streamlit web app

## Tech Stack

* Python
* LangGraph
* LangChain OpenAI
* OpenAI GPT-4o
* Pydantic
* yfinance
* SEC EDGAR API
* Streamlit
* python-dotenv

## Project Structure

```text
ai-stock-research-agent/
│
├── agent.py              # LangGraph workflow and AI analysis logic
├── app.py                # Streamlit web application
├── main.py               # Command-line interface
├── schemas.py            # Pydantic structured output models
├── tools.py              # SEC, Yahoo Finance, and news data tools
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Files excluded from GitHub
└── README.md             # Project documentation
```

## How It Works

```text
Ticker Input
   ↓
Gather SEC fundamentals
   ↓
Gather Yahoo Finance market data
   ↓
Gather recent news headlines
   ↓
Run LangGraph research workflow
   ↓
Generate structured GPT-4o research brief
   ↓
Display results in terminal or Streamlit app
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/asaawukukwame-alt/ai-stock-research-agent.git
cd ai-stock-research-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

Run the command-line version:

```bash
python main.py AAPL
```

Run the Streamlit web app:

```bash
python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Example Output

The app returns a structured research brief with sections such as:

```text
TENSION POINT ANALYSIS
Recommendation
Conviction
Fundamental Snapshot
Tension Points
Bull Case
Bear Case
What to Watch
Final Verdict
```

## Skills Demonstrated

This project demonstrates:

* Python project organization
* API integration
* Environment variable management
* SEC EDGAR data usage
* Yahoo Finance data usage
* LangGraph workflow design
* OpenAI API integration
* Pydantic structured outputs
* Streamlit app development
* Command-line app development
* GitHub portfolio publishing

## Important Disclaimer

This project is for educational and portfolio purposes only.

It is not financial advice, investment advice, or a recommendation to buy or sell securities.

## Author

Kwame Asa-Awuku
Data Science & AI Engineering Student

GitHub: https://github.com/asaawukukwame-alt
LinkedIn: https://www.linkedin.com/in/kwame-asa-awuku-164a5737b
