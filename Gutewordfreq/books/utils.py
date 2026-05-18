"""
Project Gutenberg Word Frequency Tool
Author: Sean Fay
Date: 2026-05-16
Description: This file has all the utilities functions - connecting to the API,
             processing text, and filtering out boring words.
"""

import re
from collections import Counter
import requests
import urllib.parse

# STOP_WORDS - all words that add no meaning to a story
STOP_WORDS = {
    # Pronouns
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'her', 'its', 'our', 'their', 'myself', 'yourself',
    'himself', 'herself', 'itself', 'ourselves', 'themselves',
    'who', 'whom', 'whose', 'which', 'what',
    
    # Articles & conjunctions
    'a', 'an', 'the', 'and', 'or', 'but', 'so', 'for', 'nor', 'yet',
    
    # Prepositions
    'at', 'in', 'on', 'of', 'to', 'for', 'with', 'by', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'from', 'up', 'down', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'all', 'any', 'both', 'each',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'than', 'that', 'then', 'these',
    'those', 'through', 'until', 'within', 'without', 'upon', 'onto',
    'towards', 'toward', 'via', 'per', 'among', 'amongst', 'along',
    'throughout', 'inside', 'outside', 'beside', 'beneath', 'underneath',
    
    # Verbs
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can',
    'become', 'became', 'remain', 'remained', 'seem', 'seemed', 'appear',
    'appeared', 'keep', 'kept', 'make', 'made', 'say', 'said', 'tell', 'told',
    'see', 'saw', 'look', 'looked', 'go', 'went', 'come', 'came',
    'being', 'having', 'doing', 'making', 'taking', 'giving',
    
    # Time-related
    'now', 'then', 'than', 'when', 'where', 'why', 'how', 'while',
    'again', 'always', 'never', 'often', 'sometimes', 'usually',
    'earlier', 'later', 'immediately', 'suddenly', 'finally', 'eventually',
    'already', 'still', 'yet', 'once', 'ever',
    
    # Quantity
    'many', 'much', 'more', 'most', 'less', 'least', 'few', 'fewer',
    'several', 'some', 'any', 'no', 'none', 'all', 'both', 'each',
    'every', 'either', 'neither', 'another', 'other', 'others',
    'first', 'second', 'third', 'last', 'next', 'previous',
    
    # Transitions
    'this', 'that', 'these', 'those', 'there', 'their',
    'although', 'though', 'whereas', 'therefore', 'however',
    'nevertheless', 'nonetheless', 'accordingly', 'consequently', 'hence',
    'thus', 'thereby', 'moreover', 'furthermore', 'likewise', 'similarly',
    'otherwise', 'instead',
    
    # Miscellaneous
    'just', 'only', 'even', 'quite', 'rather', 'somewhat',
    'well', 'maybe', 'perhaps', 'probably', 'certainly', 'definitely',
    'really', 'actually', 'basically', 'literally', 'specifically',
    'generally', 'typically', 'normally', 'like', 'unlike',
    'including', 'excluding', 'regarding', 'concerning', 'except', 'besides',
    'almost', 'nearly', 'barely', 'hardly', 'scarcely', 'merely', 'simply',
    'purely', 'totally', 'completely', 'entirely', 'utterly',
    'very', 'pretty', 'quite',
    
    # From Frankenstein results
    'life', 'eyes', 'father', 'man', 'time', 'every', 'own', 'without',
    'cannot', 'per', 'both', 'whereas', 'throughout', 'even', 'rather',
    'whom', 'whose', 'back', 'forward', 'toward', 'towards',
}

def get_top_words(text, n=10):
    """Extract top (n) most frequent meaningful words from text"""
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    meaningful_words = [word for word in words if word not in STOP_WORDS]
    word_counts = Counter(meaningful_words)
    return word_counts.most_common(n)

def search_gutenberg_api(title):
    """Search Project Gutenberg using the official Gutendex API (WWW API)"""
    try:
        encoded_title = urllib.parse.quote(title)
        api_url = f"https://gutendex.com/books?search={encoded_title}"
        
        print(f"Calling Gutendex API: {api_url}")
        
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            raise Exception(f"No book found titled '{title}'")
        
        first_result = data['results'][0]
        book_id = first_result['id']
        full_title = first_result.get('title', title)
        
        formats = first_result.get('formats', {})
        
        if 'text/plain; charset=utf-8' in formats:
            text_url = formats['text/plain; charset=utf-8']
        elif 'text/plain' in formats:
            text_url = formats['text/plain']
        else:
            text_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
        
        return (book_id, text_url, full_title)
        
    except Exception as e:
        raise Exception(f"API error: {str(e)}")

def fetch_book_from_url(url):
    """Fetch book text from a URL"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        text = response.text
        
        # Remove Gutenberg header/footer
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in text:
            start_idx = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
            text_start = text.find('\n', start_idx) + 1
            text = text[text_start:]
        
        if "*** END OF THE PROJECT GUTENBERG EBOOK" in text:
            end_idx = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
            text = text[:end_idx]
        
        if not text.strip():
            raise Exception("No text content found")
        
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Failed to fetch book: {str(e)}")