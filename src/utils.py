def download_image(url, save_path):
    import requests

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image from {url}")

def get_icon_data(icon_element):
    title = icon_element.get('title')
    url = icon_element.get('data-url')
    return {
        'title': title,
        'url': url
    }