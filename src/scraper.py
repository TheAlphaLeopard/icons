import os
import json
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from utils import log_error


class IconScraper:
    def __init__(self, json_path):
        self.json_path = json_path
        self.seen_urls = set()  # Track already processed URLs to avoid duplicates
        self.proxies = self.get_free_proxies()  # Fetch free proxies

    def get_free_proxies(self):
        """Fetch a list of free proxies from a public proxy list."""
        proxy_list_url = "https://www.sslproxies.org/"
        proxies = []

        try:
            response = requests.get(proxy_list_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse the proxy table
            rows = soup.select("table#proxylisttable tbody tr")
            for row in rows:
                columns = row.find_all("td")
                if len(columns) >= 2:
                    ip = columns[0].text.strip()
                    port = columns[1].text.strip()
                    proxies.append(f"http://{ip}:{port}")
        except Exception as e:
            log_error(f"Error fetching free proxies: {e}")

        print(f"Fetched {len(proxies)} free proxies.")
        return proxies

    def get_random_headers(self):
        """Generate random headers to mimic different browsers and devices."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0",
        ]
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://www.flaticon.com/",
            "https://duckduckgo.com/",
        ]
        accept_languages = [
            "en-US,en;q=0.9",
            "en-GB,en;q=0.8",
            "fr-FR,fr;q=0.7",
            "de-DE,de;q=0.6",
            "es-ES,es;q=0.5",
        ]

        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": random.choice(referers),
            "Accept-Language": random.choice(accept_languages),
        }
        return headers

    def get_random_proxy(self):
        """Get a random proxy from the list."""
        if not self.proxies:
            log_error("No proxies available.")
            return None
        return {"http": random.choice(self.proxies), "https": random.choice(self.proxies)}

    def fetch_collections(self):
        """Fetch all collection URLs from the main packs page."""
        base_url = "https://www.flaticon.com/packs/"
        collections = []

        try:
            headers = self.get_random_headers()
            proxy = self.get_random_proxy()
            response = requests.get(base_url, headers=headers, proxies=proxy, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all collection links
            collection_elements = soup.select(".pack--holder a")
            for element in collection_elements:
                collection_url = element.get("href")
                if collection_url and collection_url.startswith("/packs/"):
                    collections.append(f"https://www.flaticon.com{collection_url}")
        except Exception as e:
            log_error(f"Error fetching collections: {e}")

        return collections

    def fetch_icons(self, collection_url):
        """Fetch all icons from a specific collection."""
        icons = []

        try:
            headers = self.get_random_headers()
            proxy = self.get_random_proxy()
            response = requests.get(collection_url, headers=headers, proxies=proxy, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all icons
            icon_elements = soup.select(".icon--holder img")
            for img in icon_elements:
                try:
                    # Extract image URL
                    img_url = img.get("src")
                    if img_url and img_url.endswith(".png") and img_url not in self.seen_urls:
                        self.seen_urls.add(img_url)  # Mark URL as seen
                        icons.append({
                            "name": img.get("alt", "unknown"),  # Use alt text as name if available
                            "url": img_url,
                            "collection": collection_url
                        })
                        print("Icon fetched!")  # Real-time console output
                except Exception as e:
                    log_error(f"Error parsing icon data: {e}")
        except Exception as e:
            log_error(f"Error fetching icons from {collection_url}: {e}")

        return icons

    def save_icons(self, icons):
        """Save all icons to a JSON file."""
        if os.path.exists(self.json_path):
            # Load existing data to avoid overwriting
            with open(self.json_path, 'r', encoding='utf-8') as json_file:
                existing_icons = json.load(json_file)
        else:
            existing_icons = []

        # Combine existing icons with new ones
        all_icons = existing_icons + icons

        # Save to JSON
        with open(self.json_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_icons, json_file, indent=4)
        print(f"Saved metadata to {self.json_path}")

    def scrape_collections_concurrently(self, collections, max_workers=2):
        """Scrape collections concurrently, with a maximum of two at a time."""
        all_icons = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.fetch_icons, url) for url in collections]
            for future in futures:
                try:
                    icons = future.result()
                    all_icons.extend(icons)
                except Exception as e:
                    log_error(f"Error in concurrent scraping: {e}")
        return all_icons


if __name__ == "__main__":
    json_path = "icons.json"
    scraper = IconScraper(json_path)

    print("Fetching collections...")
    collections = scraper.fetch_collections()
    if collections:
        print(f"Found {len(collections)} collections.")

        print("Scraping icons from collections (2 at a time)...")
        all_icons = scraper.scrape_collections_concurrently(collections, max_workers=2)

        print("Saving icons to JSON...")
        scraper.save_icons(all_icons)
        print("All icons saved.")
    else:
        print("No collections found.")