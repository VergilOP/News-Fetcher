from bs4 import BeautifulSoup
from datetime import datetime
import re

def extract_img_url(story):
    """Extracts the image URL from a story element."""
    img_tag = story.find('img')
    if img_tag:
        if img_tag.has_attr('data-src'):
            return img_tag['data-src'].replace('{width}', '420')
        elif img_tag.has_attr('src'):

            return img_tag['src']
        else:
            # Handle cases wrapped in <noscript>
            noscript_tag = story.find('noscript')
            if noscript_tag:
                noscript_soup = BeautifulSoup(noscript_tag.text, 'html.parser')
                noscript_img_tag = noscript_soup.find('img')
                if noscript_img_tag and noscript_img_tag.has_attr('src'):
                    return noscript_img_tag['src']
    return None

def extract_news_url_and_title(story):
    """Extracts news URL and title from a story element."""
    news_data = {}

    link_tag = story.find('a', class_=re.compile(r"PromoLink"))
    if link_tag and link_tag.has_attr('href'):
        href = link_tag['href']
        if not href.startswith(('http:', 'https:')):
            # href = "https://www.bbc.co.uk" + href
            href = "/bbc" + href
        news_data['url'] = href

    title_tag = story.find(class_=re.compile(r"PromoHeadline"))
    if title_tag:
        title = title_tag.find('span')
        news_data['title'] = title.get_text(strip=True) if title else 'No title'
    else:
        news_data['title'] = 'No title'

    return news_data

def extract_top_stories(region):
    """Extracts top stories from a given region."""
    top_stories = []
    stories = region.find_all('li', class_=re.compile(r"ListItem"))
    for story in stories:
        top_news = {}
        img_url = extract_img_url(story)
        top_news['img_url'] = img_url if img_url else ""

        summary_tag = story.find('p', class_=re.compile(r"Paragraph"))
        top_news['intro'] = summary_tag.get_text(strip=True) if summary_tag else ""

        news_details = extract_news_url_and_title(story)
        top_news['title'] = news_details.get('title', '')
        top_news['url'] = news_details.get('url', '')

        top_stories.append(top_news)
    return top_stories

def extract_clusters(cluster, cluster_title):
    """Extracts news clusters from a given region."""
    cluster_news_list = []

    news_tags = cluster.find_all('li', class_=re.compile(r"ListItem"))

    for news_tag in news_tags:

        cluster_news = {}
        img_url = extract_img_url(news_tag)
        if img_url:
            cluster_news['img_url'] = img_url
        cluster_news.update(extract_news_url_and_title(news_tag))
        cluster_news_list.append(cluster_news)

    return {'title': cluster_title, 'content': cluster_news_list}

def extract_most_watched(cluster, cluster_title):
    most_watched_news_list = []
    news_tags = cluster.find_all('li', class_=re.compile(r"PromoItem"))
    for news_tag in news_tags:
        news_data = {}
        link_tag = news_tag.find('a', class_=re.compile(r"Headline"))
        if link_tag and link_tag.has_attr('href'):
            href = link_tag['href']
            if not href.startswith(('http:', 'https:')):
                # href = "https://www.bbc.co.uk" + href
                href = "/bbc" + href
            news_data['url'] = href
        news_data['title'] = link_tag.get_text(strip=True) if link_tag else 'No title'
        most_watched_news_list.append(news_data)

    return {'title': cluster_title, 'content': most_watched_news_list}

def extract_data_bbc_news_homepage(html_content, url):
    """Main function to extract data from BBC News HTML content."""
    print("Start")
    soup = BeautifulSoup(html_content, 'html.parser')
    main_content = soup.find(id="main-content")

    clusters = []
    current_time = datetime.utcnow()

    
    northern_ireland    = main_content.find(id="nations-news-northern_ireland")
    wales               = main_content.find(id="nations-news-wales")
    scotland            = main_content.find(id="nations-news-scotland")
    england             = main_content.find(id="nations-news-england")
    uk                  = main_content.find(id="nations-news-uk")
    
    northern_ireland_DATA   = extract_top_stories(northern_ireland)
    wales_DATA              = extract_top_stories(wales)
    scotland_DATA           = extract_top_stories(scotland)
    england_DATA            = extract_top_stories(england)
    uk_DATA                 = extract_top_stories(uk)

    top_stories = {"northern_ireland": northern_ireland_DATA, "wales":wales_DATA, "scotland":scotland_DATA, "england": england_DATA, "uk":uk_DATA}

    if main_content:
        clustrers = [
            child for child in main_content.children 
            if child.has_attr('class') and re.compile(r"Container").search(' '.join(child['class']))
        ]

        for cluster in clustrers:
            cluster_DATA = []
            title_tag = cluster.find('h2', class_=re.compile(r'Heading'))
            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                continue

            if title in ["More news on iPlayer and Sounds"]:
                continue
            elif title in ["Most watched", "Most read"]:
                cluster_DATA = extract_most_watched(cluster, title)
            else:
                cluster_DATA = extract_clusters(cluster, title)

            clusters.append(cluster_DATA)

    return {
        'news': "BBC",
        'top_stories': top_stories,
        'clusters': clusters,
        'timestamp': current_time,
        'url': url,
    }
