from warnings import catch_warnings

from duckduckgo_search import DDGS
from lxml.html import find_rel_links


def search(query):
    text = ""
    ddgs = DDGS()
    try:
        if(len(query) > 500):
            query = "Nothing found on the internet!"
            return query
        else:
            results = ddgs.text(query, max_results=2)
            final_results = []
            for data in results:
                title = data.get("title")
                body = data.get("body")
                link = data.get("href")

                text +=  f" Title: {title}" + " "+ f" Source (important to include if chosen): {link}\n" + " "+ f" Content: {body}\n"
                final_results.append(text)
            return final_results
    except Exception as e:
        query = "Nothing found on the internet!"
        print("Error has happened",e)
        return query


