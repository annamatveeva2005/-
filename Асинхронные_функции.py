import aiohttp
import aiofiles
import asyncio
from bs4 import BeautifulSoup


urls = [
    "https://regex101.com/",
    "https://docs.python.org/3/this-url-will-404.html",
    "https://www.nytimes.com/guides/",
    "https://www.mediamatters.org/",
    "https://1.1.1.1/",
    "https://www.politico.com/tipsheets/morning-money",
    "https://www.bloomberg.com/markets/economics",
    "https://www.ietf.org/rfc/rfc2616.txt"
]

# Асинхронная функция для получения HTML-кода страницы и извлечения ссылок
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return links
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе {url}: {e}")
        return []

# Асинхронная функция основная
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)

        all_links = [link for sublist in responses for link in sublist]

        async with aiofiles.open('found_links.txt', mode='w') as f:
            for link in all_links:
                await f.write(link + '\n')

asyncio.run(main())
