from pydantic import BaseModel, Field


class TensionPoint(BaseModel):
    debate: str = Field(description="The core question or debate driving valuation")
    bull_case: str = Field(description="Why this resolves positively for the stock")
    bear_case: str = Field(description="Why this resolves negatively for the stock")
    what_to_watch: str = Field(description="Upcoming catalysts or data points to monitor")


class ResearchBrief(BaseModel):
    company_name: str = Field(description="Full company name")
    ticker: str = Field(description="Stock ticker symbol")
    recommendation: str = Field(description="STRONG BUY, BUY, HOLD, SELL, or STRONG SELL")
    conviction: str = Field(description="HIGH, MEDIUM, or LOW")
    tension_points: list[TensionPoint] = Field(
        description="1-3 key debates driving the stock's valuation"
    )
    fundamental_snapshot: str = Field(
        description="Key metrics summary: revenue trend, margins, valuation"
    )
    final_verdict: str = Field(
        description="3-4 sentence synthesis with clear reasoning"
    )