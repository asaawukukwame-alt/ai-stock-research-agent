import streamlit as st

from agent import build_graph


st.set_page_config(
    page_title="AI Stock Research Agent",
    page_icon="📈",
    layout="wide",
)


@st.cache_resource
def get_research_graph():
    """Build the LangGraph workflow once and reuse it."""
    return build_graph()


def display_research_brief(brief) -> None:
    """Display the completed stock research brief."""
    st.header(f"{brief.company_name} ({brief.ticker})")

    recommendation_column, conviction_column = st.columns(2)

    with recommendation_column:
        st.metric("Recommendation", brief.recommendation)

    with conviction_column:
        st.metric("Conviction", brief.conviction)

    st.subheader("Fundamental Snapshot")
    st.write(brief.fundamental_snapshot)

    st.subheader("Key Valuation Debates")

    for index, tension_point in enumerate(brief.tension_points, start=1):
        with st.expander(
            f"Tension Point {index}: {tension_point.debate}",
            expanded=True,
        ):
            bull_column, bear_column = st.columns(2)

            with bull_column:
                st.markdown("### Bull Case")
                st.write(tension_point.bull_case)

            with bear_column:
                st.markdown("### Bear Case")
                st.write(tension_point.bear_case)

            st.markdown("### What to Watch")
            st.write(tension_point.what_to_watch)

    st.subheader("Final Verdict")
    st.info(brief.final_verdict)


def main() -> None:
    """Run the Streamlit application."""
    st.title("📈 AI Stock Research Agent")

    st.write(
        "Generate a structured equity research brief using SEC filings, "
        "Yahoo Finance market data, recent headlines, and AI analysis."
    )

    ticker = st.text_input(
        "Enter a stock ticker",
        placeholder="AAPL, NVDA, MSFT, TSLA",
        max_chars=10,
    ).strip().upper()

    research_button = st.button(
        "Generate Research Brief",
        type="primary",
        use_container_width=True,
    )

    if research_button:
        if not ticker:
            st.warning("Enter a valid stock ticker before continuing.")
            return

        try:
            with st.spinner(
                f"Researching {ticker} and generating the investment brief..."
            ):
                graph = get_research_graph()
                result = graph.invoke({"ticker": ticker})
                brief = result["research_brief"]

            display_research_brief(brief)

        except Exception as error:
            st.error("The research brief could not be generated.")
            st.exception(error)

    st.divider()

    st.caption(
        "Educational portfolio project only. This application does not provide "
        "financial or investment advice."
    )


if __name__ == "__main__":
    main()