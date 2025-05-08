from duckduckgo_search import DDGS


def search(query):
    text = ""
    ddgs = DDGS()
    results = ddgs.text(query, max_results=2)
    for data in results:
        text += " " + str(data)
    return results

