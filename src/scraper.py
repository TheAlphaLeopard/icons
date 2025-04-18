class IconScraper:
    def __init__(self, db):
        self.db = db

    def fetch_icons(self):
        import requests
        from bs4 import BeautifulSoup

        url = "https://iconduck.com"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        icons = []
        for icon in soup.find_all('div', class_='icon'):
            icon_url = icon.find('img')['src']
            icon_name = icon['data-name']
            icons.append({'name': icon_name, 'url': icon_url})

        return icons

    def save_icons(self, icons):
        for icon in icons:
            self.db.insert_icon(icon['name'], icon['url'])