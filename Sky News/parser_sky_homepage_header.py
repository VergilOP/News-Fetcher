from bs4 import BeautifulSoup
from datetime import datetime
import html

def extract_nav(soup):
    nav = []
    nav_tag = soup.find('ul', class_='ui-news-header-nav-items')

    if not nav_tag:
        return nav
    
    li_tags = nav_tag.find_all("li")
    for li in li_tags:
        # Fuzzy search for the <a> tag with class containing 'PromoLink'
        a_tag = li.find('a', class_="ui-news-header-nav-items-link")
        # title_link = "https://news.sky.com" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'

        if not(a_tag and a_tag.has_attr('href')):
            continue

        nav_href = "/sky" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'
        nav_title = a_tag.get_text(strip=True) if a_tag else 'No title found'

        nav.append({'nav_href': nav_href, 'nav_title': nav_title})

    return nav

def extract_data_sky_news_homepage_header(html_content):
    """Main function to extract content data from BBC News HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    nav = extract_nav(soup)
    current_time = datetime.utcnow()

    return {
        'news': "BBC",
        'nav': nav,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
    }