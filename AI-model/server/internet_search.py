from duckduckgo_search import DDGS


def search(query):
    text = ""
    ddgs = DDGS()
    if(len(query) > 500):
        query = "Nothing found on the internet!"
        return query
    else:
        results = ddgs.text(query, max_results=2)
        for data in results:
            text += " " + str(data)
        return results

