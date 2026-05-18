"""
Django views for API search and word frequency display
Author: Sean Fay
Date: 2026-05-17
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BookWord
from .utils import get_top_words, search_gutenberg_api, fetch_book_from_url
import json

def home(request):
    """Render the main application page"""
    return render(request, 'books/home.html')

@csrf_exempt
def search_local(request):
    """Search for a book title in the local database"""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({'error': 'Please provide a book title'}, status=400)
        
        words = BookWord.objects.filter(
            title__iexact=title
        ).order_by('-frequency')[:10]
        
        if not words.exists():
            return JsonResponse({
                'found': False,
                'message': f'Book "{title}" not found in local database.'
            })
        
        words_list = [{'word': w.word, 'frequency': w.frequency} for w in words]
        
        return JsonResponse({
            'found': True,
            'title': title,
            'words': words_list
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def search_api_and_fetch(request):
    """Search Gutenberg by title, fetch the book, process, and save to database"""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        
        if not title:
            return JsonResponse({'error': 'Please enter a book title'}, status=400)
        
        # Step 1: Search for the book
        try:
            book_id, book_url, full_title = search_gutenberg_api(title)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=404)
        
        # Step 2: Fetch the book text
        try:
            book_text = fetch_book_from_url(book_url)
        except Exception as e:
            return JsonResponse({'error': f"Failed to fetch book: {str(e)}"}, status=400)
        
        # Step 3: Process text to get top 10 meaningful words
        top_words = get_top_words(book_text, 10)
        
        if not top_words:
            return JsonResponse({'error': 'No meaningful words found in the book'}, status=400)
        
        # Step 4: Save to database
        BookWord.objects.filter(title__iexact=full_title).delete()
        for word, freq in top_words:
            BookWord.objects.create(
                title=full_title,
                word=word,
                frequency=freq
            )
        
        # Step 5: Return results
        words_list = [{'word': word, 'frequency': freq} for word, freq in top_words]
        
        return JsonResponse({
            'success': True,
            'title': full_title,
            'book_id': book_id,
            'url': book_url,
            'words': words_list
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def fetch_manual_url(request):
    """Alternative: Fetch book from manually provided URL"""
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        url = data.get('url', '').strip()
        
        if not title or not url:
            return JsonResponse({'error': 'Please provide both book title and URL'}, status=400)
        
        book_text = fetch_book_from_url(url)
        top_words = get_top_words(book_text, 10)
        
        if not top_words:
            return JsonResponse({'error': 'No meaningful words found'}, status=400)
        
        BookWord.objects.filter(title__iexact=title).delete()
        for word, freq in top_words:
            BookWord.objects.create(title=title, word=word, frequency=freq)
        
        words_list = [{'word': word, 'frequency': freq} for word, freq in top_words]
        
        return JsonResponse({
            'success': True,
            'title': title,
            'words': words_list
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)