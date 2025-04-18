# Icon Scraper

This project is a Python-based web scraper designed to collect icons from [iconduck.com](https://iconduck.com). It efficiently retrieves icon data, including URLs and metadata, and stores this information in a SQLite database.

## Project Structure

```
icon-scraper
├── src
│   ├── scraper.py       # Main scraping logic
│   ├── database.py      # Database interactions
│   └── utils.py         # Utility functions
├── requirements.txt      # Project dependencies
├── .gitignore            # Files to ignore in Git
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/icon-scraper.git
   cd icon-scraper
   ```

2. **Install dependencies:**
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, execute the following command in your terminal:

```
python src/scraper.py
```

This will initiate the scraping process, fetching icons from iconduck.com and saving them to the database.

## Features

- Scrapes icons and their metadata from iconduck.com.
- Saves icon images and data to a SQLite database.
- Utility functions for downloading images and extracting icon data.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.