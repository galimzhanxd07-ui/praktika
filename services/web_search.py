from duckduckgo_search import DDGS


def web_search(query: str):

    results = []

    with DDGS() as ddgs:

        for r in ddgs.text(query, max_results=3):

            results.append(r["body"])

    if not results:
        return "Интернеттен нәтиже табылмады."

    return "\n".join(results)
