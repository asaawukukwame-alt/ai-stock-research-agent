import sys

from agent import build_graph


def format_brief(brief) -> str:
    """Format the research brief for terminal display."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  TENSION POINT ANALYSIS: {brief.company_name} ({brief.ticker})")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Recommendation: {brief.recommendation}  |  Conviction: {brief.conviction}")
    lines.append("")
    lines.append("-" * 70)
    lines.append("  FUNDAMENTAL SNAPSHOT")
    lines.append("-" * 70)
    lines.append(f"  {brief.fundamental_snapshot}")
    lines.append("")

    for i, tp in enumerate(brief.tension_points, 1):
        lines.append("-" * 70)
        lines.append(f"  TENSION POINT #{i}: {tp.debate}")
        lines.append("-" * 70)
        lines.append(f"  Bull Case: {tp.bull_case}")
        lines.append(f"  Bear Case: {tp.bear_case}")
        lines.append(f"  What to Watch: {tp.what_to_watch}")
        lines.append("")

    lines.append("-" * 70)
    lines.append("  FINAL VERDICT")
    lines.append("-" * 70)
    lines.append(f"  {brief.final_verdict}")
    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <TICKER>")
        print("Example: python main.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    print(f"\n  Researching {ticker}...\n")

    graph = build_graph()
    result = graph.invoke({"ticker": ticker})

    brief = result["research_brief"]
    print(format_brief(brief))


if __name__ == "__main__":
    main()