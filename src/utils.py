import logging
import requests

# Configure logging
logging.basicConfig(
    filename="scraper.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message):
    """Log an error message to the log file."""
    logging.error(message)
    print(f"Error: {message}")

def download_image(url, save_path):
    """Download an image (PNG or SVG) from a URL and save it to a file."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
    except requests.exceptions.RequestException as e:
        log_error(f"Failed to download image from {url}: {e}")

def save_svg_code(svg_code, save_path):
    """Save inline SVG code to a .svg file."""
    try:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(svg_code)
        print(f"Saved inline SVG: {save_path}")
    except Exception as e:
        log_error(f"Failed to save inline SVG to {save_path}: {e}")