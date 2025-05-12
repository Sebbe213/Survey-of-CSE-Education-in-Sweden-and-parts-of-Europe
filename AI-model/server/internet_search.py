from duckduckgo_search import DDGS


def search(query):
    text = ""
    ddgs = DDGS()
    print(len(query))
    if(len(query) > 500):
        query = "Nothing found on the internet!"
    results = ddgs.text(query, max_results=2)
    for data in results:
        text += " " + str(data)
    return results

