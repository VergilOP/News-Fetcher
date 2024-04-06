# News Fetcher

## Overview
News Fetcher is an open-source Python project aimed at providing easy access to parsed data from BBC and Sky News websites. This project is ideal for researchers, journalists, and anyone interested in media analysis, offering structured data extracted from various sections of these news outlets, including homepages, content pages, sidebars, and specific topic pages.

## Features
- Parsing of BBC and Sky News homepages to retrieve headlines and lead paragraphs.
- Extraction of detailed article content from BBC News, including main content and sidebar information.
- Ability to parse specific topic pages from BBC News for more focused data collection.
- Integration with Sky News content pages for comprehensive news data gathering.
- Modular design for easy expansion to other news sources or additional content types.

## Installation
Clone this repository to your local machine using:
```
git clone https://github.com/VergilOP/News-Fetcher.git
```

Ensure you have Python 3.x installed on your system. Dependencies are listed in `requirements.txt`. Install them using pip:
```
pip install beautifulsoup4
pip install requests
```

## Usage
Each parser is designed to work independently, allowing users to fetch data according to their specific needs. Here's a quick guide to get started:

```python
from parser_bbc_homepage import parse_bbc_homepage
from parser_sky_homepage import parse_sky_homepage

# Parse BBC and Sky News homepages
bbc_homepage_data = parse_bbc_homepage('https://www.bbc.com')
sky_homepage_data = parse_sky_homepage('https://news.sky.com')

# For detailed usage and examples, refer to the individual parser files.
```

## Acknowledgments
- Special thanks to the BBC and Sky News for maintaining their news websites, which serve as valuable information resources.

## Disclaimer
This project is intended for educational and research purposes only. Please ensure you adhere to the terms of service of BBC and Sky News when using this software.

## Tools and Methods

News Fetcher leverages a combination of Python programming techniques and third-party libraries to efficiently parse and process data from BBC and Sky News websites. Here's an overview of the tools and methods employed in this project:

### Beautiful Soup
A fundamental tool in our project, Beautiful Soup allows for easy parsing of HTML and XML documents. It's instrumental in navigating the parse tree and searching for specific tags, making it ideal for extracting the structured data we need from news websites.

### Regular Expressions (re module)
We use Python's built-in `re` module for pattern matching within text. This is particularly useful for identifying specific elements within HTML pages or manipulating strings to extract relevant information.

### HTML Entity Conversion
The `html` module's functionality is utilized to handle HTML entities, ensuring that the text extracted from web pages is converted to a readable format suitable for analysis or display.

### Relative Imports
Our project is structured with modular design principles in mind, using relative imports to maintain clean and maintainable code across different parser modules. This approach facilitates the reuse of common functions, such as extracting image URLs or detailed content from articles.

### DateTime
The `datetime` module is used to work with dates and times, allowing for timestamping of parsed data and enabling time-based filtering or sorting of news content.