from bs4 import BeautifulSoup
from datetime import datetime
import html

def extract_title(article_tag):
    """Extracts the article title."""
    title_tag = article_tag.find('span', class_='sdc-article-header__long-title')
    return title_tag.get_text(strip=True) if title_tag else 'No title found'

def extract_date(article_tag):
    """Extracts the article's author and source."""
    date_tag = article_tag.find('p', class_='sdc-article-date__date-time')
    return date_tag.get_text(strip=True) if date_tag else 'No date found'

def extract_content(article_tag):
    """Extracts the article's sections."""
    full_content = ""
    content_tag = article_tag.find('div', class_='sdc-article-body sdc-article-body--story sdc-article-body--lead')

    if content_tag:
        p_tags = content_tag.find_all('p')
        for p_tag in p_tags:
            full_content += p_tag.get_text(strip=True)

    return full_content

def extract_images(article_tag):
    """Extracts images from the article."""
    img_block = article_tag.find(class_='sdc-site-component-top__media')
    if img_block:
        img_tag = img_block.find('img') 
        if img_tag:
            if img_tag.has_attr('data-src'):
                return img_tag['data-src'].replace('{width}', '420')
            elif img_tag.has_attr('src'):
                # Handle non-lazy-loaded images
                return img_tag['src']
            else:
                # Handle cases wrapped in <noscript>
                noscript_tag = article_tag.find('noscript')
                if noscript_tag:
                    noscript_soup = BeautifulSoup(noscript_tag.text, 'html.parser')
                    noscript_img_tag = noscript_soup.find('img')
                    if noscript_img_tag and noscript_img_tag.has_attr('src'):
                        return noscript_img_tag['src']
    return None

def extract_data_sky_news_content(html_content, url):
    """Main function to extract content data from Sky News HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    article_tag = soup.find(id="main")
    if not article_tag:
        return {'news': "None"}

    title = extract_title(article_tag)
    date = extract_date(article_tag)
    content = extract_content(article_tag)
    img_url = extract_images(article_tag)
    current_time = datetime.utcnow()

    article_data = {
        'news': "Sky",
        'title': title,
        'content': content,
        'img_urls': [img_url] if img_url else [], 
        'url': url,
        'timestamp': current_time,
        'article_infos': {
            'author': None, 
            'source': None, 
            'date': date
        },
        'bbc_parts': {},
        'sky_parts': {},
    }

    return article_data

