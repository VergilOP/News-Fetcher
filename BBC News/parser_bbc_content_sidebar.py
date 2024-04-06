from bs4 import BeautifulSoup
from datetime import datetime
from .parser_bbc_content import extract_promo_content_details
from .parser_bbc_homepage import extract_img_url
import html

def extract_top_stories(soup):
    top_stories = []
    top_stories_aside = soup.find('aside', id='topStories-label-aside-content')

    if not top_stories_aside:
        return top_stories
    
    top_stories_tags = top_stories_aside.find_all("li", class_=lambda x: x and 'PromoItem' in x)

    for top_story in top_stories_tags:
        top_story_link, top_story_title, top_story_date = extract_promo_content_details(top_story)
        top_stories.append({'top_story_title': top_story_title, 'top_story_link': top_story_link, 'top_story_date': top_story_date})

    return top_stories

def extract_features(soup):
    features = []
    features_aside = soup.find('aside', id='features-label-aside-content')

    if not features_aside:
        return None
    
    features_tags = features_aside.find_all("li", class_=lambda x: x and 'PromoItem' in x)

    for feature in features_tags:
        """Extracts title link, title, and date from promo content."""
        # Fuzzy search for the <a> tag with class containing 'PromoLink'
        a_tag = feature.find('a', class_=lambda x: x and 'PromoLink' in x)
        # title_link = "https://www.bbc.co.uk" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'
        feature_link = "/bbc" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'

        # Fuzzy search for the <span> tag within a class containing 'PromoHeadline'
        promo_headline = feature.find(class_=lambda x: x and 'PromoHeadline' in x)
        p_span = promo_headline.find('span') if promo_headline else None
        feature_title = p_span.get_text(strip=True) if p_span else 'No title found'

        feature_img_url = extract_img_url(feature)

        features.append({'feature_link': feature_link, 'feature_title': feature_title, 'feature_img_url': feature_img_url})

    return features

def extract_most_read(soup):
    most_read = []
    most_read_aside = soup.find('aside', id='mostRead-label-aside-content')

    if not most_read_aside:
        return most_read
    
    most_read_tags = most_read_aside.find_all("li", class_=lambda x: x and 'PromoItem' in x)

    for most_read_tag in most_read_tags:
        a_tag = most_read_tag.find('a')
        most_read_title = a_tag.get_text(strip=True) if a_tag and a_tag.has_attr('href') else 'No title found'
        most_read_link = "/bbc" + a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link found'
            # topic_link = "https://www.bbc.co.uk/" + a_tag['href']

        most_read.append({'most_read_title': most_read_title, 'most_read_link': most_read_link})

    return most_read

def extract_data_bbc_news_content_sidebar(html_content):
    """Main function to extract content data from BBC News HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    top_stories = extract_top_stories(soup)
    features = extract_features(soup)
    most_read = extract_most_read(soup)

    current_time = datetime.utcnow()

    return {
        'news': "BBC",
        'top_stories': top_stories,
        'features': features,
        'most_read': most_read,
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
    }