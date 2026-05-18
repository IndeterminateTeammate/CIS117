"""
Project: Gutenberg Word Frequency Tool
Author: Sean Fay    
Date: 2026-05-15
Description: This file defines what my database looks like. 
             I'm creating a table to store book titles and their top words.
"""

from django.db import models

class BookWord(models.Model):
    """Stores book titles and their top 10 meaningful words"""
    title = models.CharField(max_length=500, db_index=True)
    word = models.CharField(max_length=100)
    frequency = models.IntegerField()
    
    class Meta:
        unique_together = ('title', 'word')