from duckduckgo_search import DDGS
import time

def search(query: str) -> str:
    """
    Perform an internet search fallback using DuckDuckGo. Returns a plain text blob of search results
    or a message indicating nothing was found.
    """
    # Guard against too-long queries
    if len(query) > 500:
        return "Nothing found on the internet!"

    ddgs = DDGS()
    snippets = []
    try:
        # Retry logic for transient errors or rate limits
        for attempt in range(3):
            try:
                results = ddgs.text(query, max_results=2)
                break
            except Exception as e:
                print(f"Search attempt {attempt+1} failed: {e}")
                time.sleep(1)
        else:
            # All retries failed
            return "Nothing found on the internet!"

        # Extract useful fields into plain text
        for item in results:
            title = item.get("title", "No title")
            body  = item.get("body", "")
            link  = item.get("href", "")
            snippet = (
                f"Title: {title}\n"
                f"Source: {link}\n"
                f"Content: {body}\n"
            )
            snippets.append(snippet)

        text_blob = "\n".join(snippets).strip()
        return text_blob if text_blob else "Nothing found on the internet!"

    except Exception as e:
        print("Error during internet search:", e)
        return "Nothing found on the internet!"
