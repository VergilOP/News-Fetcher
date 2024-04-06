from bs4 import BeautifulSoup
from datetime import datetime
import html

def extract_title(article_tag):
    """Extracts the article title."""
    title_tag = article_tag.find('h1', id='main-heading')
    return title_tag.get_text(strip=True) if title_tag else 'No title found'

def extract_author_and_source(article_tag):
    """Extracts the article's author and source."""
    byline_block = article_tag.find('div', attrs={"data-component": "byline-block"})
    author = 'No author found'
    source = 'No source found'

    if byline_block:
        author_name = byline_block.find('div', class_=lambda x: x and 'TextContributorName' in x)
        source_info = byline_block.find('div', class_=lambda x: x and 'Text' in x and 'ContributorName' not in x)

        author = author_name.get_text(strip=True) if author_name else author
        source = source_info.get_text(strip=True) if source_info else source

    return author, source

def extract_sections(article_tag, subtitle):
    """Extracts the article's sections."""
    sections = []
    current_subtitle = subtitle
    current_content = []

    for child in article_tag.children:
        if child.name == 'div' and child.get('data-component') == 'subheadline-block':
            if current_content:
                full_content = ' '.join(current_content)
                sections.append({'subtitle': current_subtitle, 'content': full_content})
                current_content = []
            current_subtitle = child.get_text(strip=True)
        elif child.name == 'div' and child.get('data-component') == 'text-block':
            p_tags = child.find_all('p')
            for p_tag in p_tags:
                text = html.unescape(p_tag.get_text(strip=True))
                current_content.append(text)

    if current_content:
        full_content = ' '.join(current_content)
        sections.append({'subtitle': current_subtitle, 'content': full_content})

    return sections

def extract_images(article_tag):
    """Extracts images from the article."""
    img_urls = []
    image_blocks = article_tag.find_all('div', attrs={"data-component": "image-block"})
    for block in image_blocks:
        img_url = extract_img_url(block)
        if img_url:
            img_urls.append(img_url)
    return img_urls

def extract_img_url(block):
    """Extracts an image URL from a block."""
    picture_tag = block.find('picture')
    if picture_tag:
        img_tag = picture_tag.find('img')
        if img_tag and img_tag.has_attr('src'):
            return img_tag['src']
        noscript_tag = picture_tag.find_next_sibling('noscript')
        if noscript_tag:
            noscript_soup = BeautifulSoup(noscript_tag.text, 'html.parser')
            noscript_img_tag = noscript_soup.find('img')
            if noscript_img_tag and noscript_img_tag.has_attr('src'):
                return noscript_img_tag['src']
    return None

def extract_related_topics(article_tag):
    """Extracts related topics from the article."""
    related_topics = []
    topic_list_block = article_tag.find('div', attrs={"data-component": "topic-list"})
    if topic_list_block:
        list_items = topic_list_block.find_all('li')
        for item in list_items:
            a_tag = item.find('a')
            if a_tag and a_tag.has_attr('href'):
                topic_name = a_tag.get_text(strip=True)
                topic_link = "/bbc" + a_tag['href']
                # topic_link = "https://www.bbc.co.uk/" + a_tag['href']
                related_topics.append({'name': topic_name, 'link': topic_link})
    return related_topics

def extract_more_on_this_story(article_tag):
    """Extracts 'More on This Story' information from the article."""
    more_on_this_story = []
    links_block = article_tag.find('div', attrs={"data-component": "links-block"})
    
    if links_block:
        ul_tag = links_block.find('ul', role="list")
        if ul_tag:
            list_items = ul_tag.find_all('li', class_=lambda x: x and 'PromoItem' in x)
            for item in list_items:
                story_data = extract_story_data(item)
                if story_data:
                    more_on_this_story.append(story_data)
    
    return more_on_this_story

def extract_story_data(item):
    """Extracts individual story data from a list item."""
    if item:
        title_link, title, date = extract_promo_content_details(item)
        img_url = extract_img_url(item)
        return {
            'title': title,
            'link': title_link,
            'date': date,
            'img_url': img_url
        }
    return None

def extract_promo_content_details(item):
    """Extracts title link, title, and date from promo content."""
    # Fuzzy search for the <a> tag with class containing 'PromoLink'
    a_tag = item.find('a', class_=lambda x: x and 'PromoLink' in x)
    # title_link = "https://www.bbc.co.uk" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'
    title_link = "/bbc" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'

    # Fuzzy search for the <span> tag within a class containing 'PromoHeadline'
    promo_headline = item.find(class_=lambda x: x and 'PromoHeadline' in x)
    p_span = promo_headline.find('span') if promo_headline else None
    title = p_span.get_text(strip=True) if p_span else 'No title found'

    # Fuzzy search for the <span> tag with class containing 'MetadataText'
    date_span = item.find('span', class_=lambda x: x and 'MetadataText' in x)
    date = date_span.get_text(strip=True) if date_span else 'No date found'

    return title_link, title, date

def extract_data_bbc_news_content(html_content, url):
    """Main function to extract content data from BBC News HTML content."""
    print("Start extract BBC News")
    soup = BeautifulSoup(html_content, 'html.parser')
    article_tag = soup.find('article')
    if not article_tag:
        return {'news': "None"}

    title = extract_title(article_tag)
    print("Title: ", title)
    author, source = extract_author_and_source(article_tag)
    sections = extract_sections(article_tag, subtitle=title)
    img_urls = extract_images(article_tag)
    related_topics = extract_related_topics(article_tag)
    more_on_this_storys = extract_more_on_this_story(article_tag)
    current_time = datetime.utcnow()

    article_data = {
        'news': "BBC",
        'title': title,
        'content': ' '.join(section['content'] for section in sections), 
        'img_urls': img_urls if img_urls else '', 
        'url': url,
        'timestamp': current_time,
        'article_infos': {
            'author': author,
            'source': source,
            'date': None
        },
        'bbc_parts': {
            'related_topics': related_topics,
            'more_on_this_story': more_on_this_storys,
        },
        'sky_parts': {}, 
    }

    return article_data

