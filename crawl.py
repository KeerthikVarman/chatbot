import asyncio
import time
from urllib.parse import urljoin, urlparse

from crawl4ai import AsyncWebCrawler


START_URL = "https://cac.annauniv.edu/aidetails/ai_ug_cands_2025ft.html"


def is_pdf(url):
    return ".pdf" in urlparse(url).path.lower()


def same_domain(url):
    return urlparse(url).netloc == urlparse(START_URL).netloc


async def main():

    start = time.perf_counter()

    async with AsyncWebCrawler() as crawler:

        # 1. Crawl starting page
        first = await crawler.arun(
            url=START_URL
        )

        print("START PAGE")
        print("Success:", first.success)

        if not first.success:
            print(first.error_message)
            return

        # 2. Extract starting page content
        print("\n" + "=" * 80)
        print("START PAGE CONTENT")
        print("=" * 80)

        print(first.markdown[:5000])

        # 3. Get links
        urls = []

        for link in first.links.get("internal", []):

            href = link.get("href")

            if not href:
                continue

            url = urljoin(START_URL, href)

            if not same_domain(url):
                continue

            if is_pdf(url):
                continue

            if url not in urls:
                urls.append(url)

        print("\nDiscovered HTML URLs:", len(urls))

        # 4. Crawl discovered HTML pages
        for url in urls:

            print("\n" + "=" * 80)
            print("CRAWLING:", url)
            print("=" * 80)

            try:

                result = await crawler.arun(
                    url=url
                )

                print("Success:", result.success)

                if result.success:

                    content = result.markdown or ""

                    print("Characters:", len(content))

                    print("\nCONTENT:")
                    print(content[:3000])

                else:

                    print("ERROR:")
                    print(result.error_message)

            except Exception as e:

                print("EXCEPTION:")
                print(e)

    end = time.perf_counter()

    print("\n" + "=" * 80)
    print("DONE")
    print("Total time:", round(end - start, 2), "seconds")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())