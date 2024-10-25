Here’s an updated `README.md` with a basic example for each of the three cases: XPath, ID, and class:

```markdown
# TableScrapper

A simple and efficient web scraping module for extracting tables from web pages.

## Installation

To install TableScrapper, use pip:

```bash
pip install tablescrapper
```

## Overview

TableScrapper provides a straightforward way to extract HTML tables from web pages using Selenium and BeautifulSoup. You can specify the table you want to scrape by XPath, ID, or class name.

## Features

- **Flexible Table Identification**: Use XPath, ID, or class name to locate tables.
- **Data Extraction**: Converts the scraped HTML table into a Pandas DataFrame for easy manipulation.
- **Robustness**: Includes error handling to manage potential issues during scraping.
- **User-Agent Rotation**: Optionally rotate user-agent strings to mimic different browsers and devices.

## Usage

Here's a quick guide on how to use TableScrapper:

### Basic Examples

#### 1. Scraping by XPath

```python
from tablescrapper import scrape_table

config = {
    'table_identifier': {
        'type': 'xpath',
        'identifier': '//*[@id="table_id"]'  # Replace with your actual XPath
    }
}

url = 'http://example.com/your_table_page'
df = scrape_table(config, url)

if df is not None:
    print("Table scraped using XPath:")
    print(df)
else:
    print("Failed to scrape the table using XPath.")
```

#### 2. Scraping by ID

```python
from tablescrapper import scrape_table

config = {
    'table_identifier': {
        'type': 'id',
        'identifier': 'table_id'  # Replace with your actual table ID
    }
}

url = 'http://example.com/your_table_page'
df = scrape_table(config, url)

if df is not None:
    print("Table scraped using ID:")
    print(df)
else:
    print("Failed to scrape the table using ID.")
```

#### 3. Scraping by Class Name

```python
from tablescrapper import scrape_table

config = {
    'table_identifier': {
        'type': 'class',
        'identifier': 'table_class'  # Replace with your actual class name
    }
}

url = 'http://example.com/your_table_page'
df = scrape_table(config, url)

if df is not None:
    print("Table scraped using class name:")
    print(df)
else:
    print("Failed to scrape the table using class name.")
```

### Function Breakdown

- **initialize_driver()**: Initializes the Selenium WebDriver with the specified options.

- **scrape_table(config, url)**: Main function to scrape the table based on the provided configuration and URL.

- **scrape_table_by_xpath(driver, url, xpath)**: Scrapes the table using an XPath expression.

- **scrape_table_by_id(driver, url, table_id)**: Scrapes the table using its HTML ID.

- **scrape_table_by_class(driver, url, class_name)**: Scrapes the table using its class name.

### Error Handling

The module includes basic error handling to notify you of any issues encountered during scraping. If the specified table is not found or an error occurs, it will return `None`.

## Requirements

- **Selenium**: Make sure you have the appropriate WebDriver installed (e.g., ChromeDriver for Chrome).
- **BeautifulSoup**: For parsing HTML.
- **Pandas**: For DataFrame manipulation.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

For detailed documentation or support, please refer to the project's GitHub page. Happy scraping!
```

Make sure to replace the placeholders for XPath, ID, and class with the actual values relevant to the tables you intend to scrape.