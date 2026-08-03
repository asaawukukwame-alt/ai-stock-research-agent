# AI Stock Research Agent

A Python and LangGraph application that generates structured equity research briefs from public company data, market data, recent news headlines, and GPT-4o analysis.

This project is designed as a portfolio-ready AI application showing practical experience with API integration, structured LLM output, workflow orchestration, and Streamlit app development.

## What the App Does

The user enters a stock ticker such as `AAPL`, `NVDA`, `MSFT`, or `TSLA`.

The app then gathers public data, runs an AI research workflow, and returns a structured research brief containing:

* Company name and ticker
* Recommendation
* Conviction level
* Fundamental snapshot
* Key valuation tension points
* Bull case
* Bear case
* What to watch
* Final verdict

## Why This Project Matters

Many AI demos only send a prompt to a chatbot. This project goes further by combining multiple layers of a real AI application:

* Data collection layer
* AI workflow layer
* Structured schema layer
* Command-line interface
* Streamlit web interface
* Environment-variable protection for API keys
* GitHub-ready documentation

## Features

* Retrieves company fundamentals from SEC EDGAR
* Retrieves stock market data from Yahoo Finance
* Retrieves recent stock-related headlines
* Uses LangGraph to organize the research workflow
* Uses GPT-4o for structured analysis
* Uses Pydantic to enforce clean output fields
* Includes a terminal version through `main.py`
* Includes a Streamlit web app through `app.py`

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
* Git / GitHub

## Project Structure

```text
ai-stock-research-agent/
│
├── agent.py              # LangGraph workflow and AI analysis logic
├── app.py                # Streamlit web application
├── main.py               # Command-line interface
├── schemas.py            # Pydantic models for structured output
├── tools.py              # SEC, Yahoo Finance, and news data tools
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Files excluded from GitHub
└── README.md             # Project documentation
```

## Application Workflow

```text
Ticker Input
   ↓
Gather SEC fundamentals
   ↓
Gather Yahoo Finance market data
   ↓
Gather recent headlines
   ↓
Run LangGraph research workflow
   ↓
Generate structured GPT-4o research brief
   ↓
Display results in terminal or Streamlit app
```

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/asaawukukwame-alt/ai-stock-research-agent.git
cd ai-stock-research-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

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

## Example Output Sections

The app returns a structured research brief with sections like:

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
* Financial data collection
* Environment variable management
* SEC EDGAR data usage
* Yahoo Finance data usage
* LangGraph workflow design
* OpenAI API integration
* Pydantic structured outputs
* Streamlit app development
* Command-line app development
* GitHub portfolio cleanup and documentation

## Future Improvements

Planned upgrades include:

* Add a clean demo screenshot or GIF
* Add ticker validation
* Add historical price charts
* Add export-to-PDF functionality
* Add a deployed Streamlit Cloud version
* Add unit tests for the data tools

## Important Disclaimer

This project is for educational and portfolio purposes only.

It is not financial advice, investment advice, or a recommendation to buy or sell securities.

## Author

Kwame Asa-Awuku
Data Science & AI Engineering Student

GitHub: https://github.com/asaawukukwame-alt
LinkedIn: https://www.linkedin.com/in/kwame-asa-awuku-164a5737b
