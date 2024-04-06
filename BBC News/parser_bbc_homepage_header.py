from bs4 import BeautifulSoup
from datetime import datetime
from .parser_bbc_content import extract_promo_content_details
from .parser_bbc_homepage import extract_img_url
import html
import re

def extract_nav(soup):
    # Initialize an empty list to store navigation links
    nav = []
    # Find the main navigation container div by its class
    nav_tag = soup.find('div', class_=re.compile(r'MainNavBarContainer'))

    # If the navigation container doesn't exist, return the empty list
    if not nav_tag:
        return nav
    
    # Find all <li> tags within the navigation container
    li_tags = nav_tag.find_all("li")

    # Iterate through each <li> tag to extract navigation links
    for li in li_tags:
        # Find the <a> tag within <li> that has a class indicating it's a styled link
        a_tag = li.find('a', class_=re.compile(r"StyledLink"))
        # title_link = "https://www.bbc.co.uk" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'

        # If the <a> tag is found and it has an 'href' attribute
        if not(a_tag and a_tag.has_attr('href')):
            # If not, skip to the next <li> tag
            continue

        # Construct the relative navigation URL by appending the 'href' value to a base path
        nav_href = "/bbc" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'

        # Find the <span> tag within the <a> tag that contains the navigation title
        nav_span = a_tag.find('span') if a_tag else None
        # Extract the text from the <span> tag, or use 'No title found' if it doesn't exist
        nav_title = nav_span.get_text(strip=True) if nav_span else 'No title found'

        # Append a dictionary with 'href' and 'title' to the navigation list
        nav.append({'nav_href': nav_href, 'nav_title': nav_title})

    # Return the list of navigation links
    return nav

def extract_nav_secondary(soup):
    nav_secondary = []
    nav_secondary_tag = soup.find('div', class_=re.compile(r'MenuContainer-SecondaryNavBarContainer'))

    if not nav_secondary_tag:
        return nav_secondary

    li_tags = nav_secondary_tag.find_all("li")

    for li in li_tags:
        # Fuzzy search for the <a> tag with class containing 'PromoLink'
        a_tag = li.find('a', class_=re.compile(r"StyledLink"))

        if not(a_tag and a_tag.has_attr('href')):
            continue

        # title_link = "https://www.bbc.co.uk" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'
        nav_sencondary_href = "/bbc" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'

        # Fuzzy search for the <span> tag within a class containing 'PromoHeadline'
        nav_span = a_tag.find('span') if a_tag else None
        nav_secondary_title = nav_span.get_text(strip=True) if nav_span else 'No title found'

        nav_secondary.append({'nav_sencondary_href': nav_sencondary_href, 'nav_title': nav_secondary_title})

    return nav_secondary

def extract_data_bbc_news_homepage_header(html_content):
    """Main function to extract content data from BBC News HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    nav = extract_nav(soup)
    nav_secondary = extract_nav_secondary(soup)
    current_time = datetime.utcnow()

    return {
        'news': "BBC",
        'nav': nav,
        'nav_secondary': nav_secondary,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
    }