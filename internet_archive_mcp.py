from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()

mcp = FastMCP("Book and Research Search")

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


def format_field(value, default="Unknown"):
    """Convert a field into a readable string."""

    if not value:
        return default

    if isinstance(value, list):
        return ", ".join(str(item) for item in value)

    return str(value)

@mcp.tool()
def tavily_search(query: str, limit: int = 5) -> str:
    """
    Search recent news and live web information using Tavily Search.
    Returns titles, URLs, and content snippets.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        return "Error: TAVILY_API_KEY was not found in the .env file."

    try:
        tavily = TavilyClient(api_key=tavily_key)
        response = tavily.search(query=query, max_results=limit)
        results = response.get("results", [])

        if not results:
            return f"No Tavily search results found for: {query}"

        formatted_results = []
        for result in results:
            title = format_field(result.get("title"), "No Title")
            url = format_field(result.get("url"), "No URL")
            content = format_field(result.get("content"), "No Content")

            if len(content) > 500:
                content = content[:500] + "..."

            formatted_results.append(
                f"Source: Tavily Search\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Content: {content}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Tavily search error: {e}"



@mcp.tool()
def search_books(query: str, limit: int = 5) -> str:
    """
    Search Google Books for books based on a topic or question.
    Returns title, author, publication date, categories,
    description, and book ID.
    """

    if not API_KEY:
        return "Error: GOOGLE_BOOKS_API_KEY was not found in the .env file."

    url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": query,
        "maxResults": min(limit, 40),
        "key": API_KEY
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        return f"Google Books error: {e}"

    books = data.get("items", [])

    if not books:
        return f"No Google Books found for: {query}"

    results = []

    for book in books:

        info=book.get("volumeInfo", {})

        book_id=book.get("id", "Unknown")

        title=format_field(
            info.get("title"),
            "Unknown"
        )

        authors=format_field(
            info.get("authors"),
            "Unknown"
        )

        published_date=format_field(
            info.get("publishedDate"),
            "Unknown"
        )

        categories=format_field(
            info.get("categories"),
            "None listed"
        )

        description=format_field(
            info.get("description"),
            "No description available"
        )

        if len(description)>500:
            description = description[:500] + "..."

        results.append(
            f"Source: Google Books\n"
            f"Title:{title}\n"
            f"Author:{authors}\n"
            f"Published:{published_date}\n"
            f"Categories:{categories}\n"
            f"Description:{description}\n"
            f"Book ID:{book_id}"
        )

    return "\n\n".join(results)

@mcp.tool()
def search_internet_archive(query:str,limit:int=5) -> str:
    """
    Search Internet Archive for books and text documents.
    Returns title, author, date, subject, and description.
    """

    url="https://archive.org/advancedsearch.php"

    params={
        "q":f"({query}) AND mediatype:texts",
        "fl":"identifier,title,creator,date,description,subject",
        "rows":limit,
        "output":"json"
    }

    try:
        response=requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        return f"Internet Archive error: {e}"

    books = data.get("response", {}).get("docs", [])

    if not books:
        return f"No Internet Archive books found for: {query}"

    results = []

    for book in books:

        title=format_field(book.get("title"),"Unknown")

        author=format_field(book.get("creator"),"Unknown")

        date=format_field(book.get("date"),"Unknown")

        subject=format_field(book.get("subject"),"None listed")

        description =format_field(
            book.get("description"),
            "No description available"
        )

        if len(description) > 500:
            description = description[:500] + "..."

        results.append(
            f"Source: Internet Archive\n"
            f"Title: {title}\n"
            f"Author: {author}\n"
            f"Date: {date}\n"
            f"Subject/Categories: {subject}\n"
            f"Description: {description}"
        )

    return "\n\n".join(results)

@mcp.tool()
def search_crossref(query: str, limit: int = 5) -> str:
    """
    Search Crossref for academic publications and research papers.
    Returns title, authors, publisher, DOI, and publication date.
    """

    url = "https://api.crossref.org/works"

    params = {
        "query": query,
        "rows": limit
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        return f"Crossref error: {e}"

    works = data.get("message", {}).get("items", [])

    if not works:
        return f"No Crossref results for: {query}"

    results = []

    for work in works:

        title = format_field(
            work.get("title"),
            "Unknown"
        )

        authors = []

        for author in work.get("author", []):

            given = author.get("given", "")
            family = author.get("family", "")

            name = f"{given} {family}".strip()

            if name:
                authors.append(name)

        author_text = (
            ", ".join(authors)
            if authors
            else "Unknown"
        )

        doi = work.get(
            "DOI",
            "No DOI"
        )

        publisher = work.get(
            "publisher",
            "Unknown"
        )

        published = work.get(
            "published-print",
            work.get("published-online", {})
        )

        results.append(
            f"Source: Crossref\n"
            f"Title: {title}\n"
            f"Authors: {author_text}\n"
            f"Publisher: {publisher}\n"
            f"DOI: {doi}\n"
            f"Published: {published}"
        )

    return "\n\n".join(results)

if __name__ == "__main__":
    mcp.run(transport="stdio")