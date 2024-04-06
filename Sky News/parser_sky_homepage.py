from bs4 import BeautifulSoup
from datetime import datetime
import re

def extract_img_url(article):
    """Extracts the image URL from a story element."""
    img_tag = article.find('img')
    if img_tag:
        if img_tag.has_attr('data-src'):
            return img_tag['data-src'].replace('{width}', '420')
        elif img_tag.has_attr('src'):
            # Handle non-lazy-loaded images
            return img_tag['src']
        else:
            # Handle cases wrapped in <noscript>
            noscript_tag = article.find('noscript')
            if noscript_tag:
                noscript_soup = BeautifulSoup(noscript_tag.text, 'html.parser')
                noscript_img_tag = noscript_soup.find('img')
                if noscript_img_tag and noscript_img_tag.has_attr('src'):
                    return noscript_img_tag['src']
    return None

def extract_news_url_and_title(article):
    """Extracts news URL and title from a story element."""
    news_data = {}

    title_block = article.find('div', class_='ui-story-headline')
    if title_block:
        title_tag = title_block.find('a') 
        if title_tag and title_tag.has_attr('href'):
            href = title_tag['href']
            # Ensure the URL is absolute
            if not href.startswith(('http:', 'https:')):
                # href = "https://news.sky.com/" + href
                href = "/sky" + href

            news_data['title'] = title_tag.get_text(strip=True)
            news_data['url'] = href

    author_block = article.find('div', class_='ui-story-meta')
    if author_block:
        author_tag = author_block.find('a') 
        if author_tag:
            news_data['author'] = author_tag.get_text(strip=True)

    return news_data

def extract_most_read_news_url_and_title(article):
    """Extracts news URL and title from a story element."""
    news_data = {}

    title_tag = article.find('a')
    if title_tag and title_tag.has_attr('href'):
        href = title_tag['href']
        # Ensure the URL is absolute
        if not href.startswith(('http:', 'https:')):
            # href = "https://news.sky.com/" + href
            href = "/sky" + href

        news_data['title'] = title_tag.get_text(strip=True)
        news_data['url'] = href

    return news_data

def extract_clusters(section):
    """Extracts news clusters from a given region."""
    cluster_title = ''
    cluster_news_list = []

    title_element = section.find(class_='ui-section-header-title')
    if title_element:
        cluster_title = title_element.text.strip()

    if cluster_title == "Most Read":
        articles = section.find_all('li')
        for article in articles:
            cluster_news = {}
            cluster_news.update(extract_most_read_news_url_and_title(article))
            cluster_news_list.append(cluster_news)
    else:
        articles = section.find_all('article')
        for article in articles:
            cluster_news = {}
            img_url = extract_img_url(article)
            if img_url:
                cluster_news['img_url'] = img_url
            cluster_news.update(extract_news_url_and_title(article))
            cluster_news_list.append(cluster_news)

    return {'title': cluster_title, 'content': cluster_news_list}

def extract_data_sky_news_homepage(html_content, url):
    """Main function to extract data from Sky News HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    main_container = soup.find(id="main")

    clusters = []
    current_time = datetime.utcnow()

    if main_container:
        main_body = main_container.find('div', class_=re.compile(r'page-content'))
        if main_body:
            sections = main_body.find_all('section')

            for section in sections:
                if (section.has_attr('aria-label') and section['aria-label'] == "Videos Videos") or (section.has_attr('role') and section['role'] == 'tabpanel'):
                    continue
                clusters.append(extract_clusters(section))

    return {
        'news': "Sky",
        'clusters': clusters,
        'timestamp': current_time,
        'url': url,
    }