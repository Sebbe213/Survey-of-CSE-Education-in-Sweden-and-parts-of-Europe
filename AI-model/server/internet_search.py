from warnings import catch_warnings

from duckduckgo_search import DDGS


def search(query):
    text = ""
    ddgs = DDGS()
    try:
        if(len(query) > 500):
            query = "Nothing found on the internet!"
            return query
        else:
            results = ddgs.text(query, max_results=2)
            for data in results:
                text += " " + str(data)
            return results
    except Exception as e:
        query = "Nothing found on the internet!"
        print("Error has happened",e)
        return query


