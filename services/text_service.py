"""
Text Service

Business logic for text transformations and processing.
All text operations are implemented here.
"""

import base64
import hashlib
import re
from typing import Dict, List


class TextService:
    """Text processing and transformation service"""
    
    # ========================================================================
    # Group A: Encoding/Decoding (Instant)
    # ========================================================================
    
    def base64_encode(self, text: str) -> str:
        """
        Encode text to Base64
        
        Args:
            text: Plain text to encode
            
        Returns:
            Base64 encoded string
        """
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    def base64_decode(self, encoded: str) -> str:
        """
        Decode Base64 to text
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Decoded plain text
        """
        return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
    
    # ========================================================================
    # Group A: Hashing (Instant)
    # ========================================================================
    
    def hash_text(self, text: str, algorithms: List[str]) -> Dict[str, str]:
        """
        Generate cryptographic hashes for text
        
        Args:
            text: Text to hash
            algorithms: List of algorithms (md5, sha1, sha256, sha512)
            
        Returns:
            Dict mapping algorithm names to hex digest strings
        """
        hashes = {}
        text_bytes = text.encode('utf-8')
        
        if 'md5' in algorithms:
            hashes['md5'] = hashlib.md5(text_bytes).hexdigest()
        if 'sha1' in algorithms:
            hashes['sha1'] = hashlib.sha1(text_bytes).hexdigest()
        if 'sha256' in algorithms:
            hashes['sha256'] = hashlib.sha256(text_bytes).hexdigest()
        if 'sha512' in algorithms:
            hashes['sha512'] = hashlib.sha512(text_bytes).hexdigest()
        
        return hashes
    
    # ========================================================================
    # Group A: Text Normalization (Instant)
    # ========================================================================
    
    def normalize(self, text: str, options: Dict = None) -> str:
        """
        Normalize text by applying various cleaning operations
        
        Args:
            text: Text to normalize
            options: Dict with options:
                - lowercase: Convert to lowercase (default: False)
                - remove_extra_spaces: Remove extra whitespace (default: True)
                - remove_punctuation: Remove punctuation (default: False)
                - remove_numbers: Remove numbers (default: False)
                - strip: Strip leading/trailing whitespace (default: True)
        
        Returns:
            Normalized text
        """
        options = options or {}
        result = text
        
        # Strip leading/trailing whitespace
        if options.get('strip', True):
            result = result.strip()
        
        # Remove extra spaces
        if options.get('remove_extra_spaces', True):
            result = re.sub(r'\s+', ' ', result)
        
        # Convert to lowercase
        if options.get('lowercase', False):
            result = result.lower()
        
        # Remove punctuation
        if options.get('remove_punctuation', False):
            result = re.sub(r'[^\w\s]', '', result)
        
        # Remove numbers
        if options.get('remove_numbers', False):
            result = re.sub(r'\d+', '', result)
        
        return result
    
    # ========================================================================
    # Group A: Text Statistics (Instant)
    # ========================================================================
    
    def get_stats(self, text: str) -> Dict:
        """
        Calculate comprehensive text statistics
        
        Args:
            text: Text to analyze
            
        Returns:
            Dict with statistics:
                - characters: Total character count
                - characters_no_spaces: Character count without whitespace
                - words: Word count
                - sentences: Sentence count (approximate)
                - paragraphs: Paragraph count
                - unique_words: Unique word count
                - average_word_length: Average length of words
                - reading_time_seconds: Estimated reading time (250 wpm)
                - speaking_time_seconds: Estimated speaking time (150 wpm)
        """
        # Character counts
        char_count = len(text)
        char_no_spaces = len(re.sub(r'\s', '', text))
        
        # Word count and analysis
        words = text.split()
        word_count = len(words)
        unique_words = len(set(word.lower() for word in words))
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Sentence count (simple approximation)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Paragraph count
        paragraphs = text.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # Reading time (average 250 words per minute)
        reading_time_seconds = (word_count / 250) * 60 if word_count > 0 else 0
        
        # Speaking time (average 150 words per minute)
        speaking_time_seconds = (word_count / 150) * 60 if word_count > 0 else 0
        
        return {
            'characters': char_count,
            'characters_no_spaces': char_no_spaces,
            'words': word_count,
            'sentences': sentence_count,
            'paragraphs': paragraph_count,
            'unique_words': unique_words,
            'average_word_length': round(avg_word_length, 2),
            'reading_time_seconds': round(reading_time_seconds, 2),
            'speaking_time_seconds': round(speaking_time_seconds, 2)
        }
    
    # ========================================================================
    # Group A: Extraction (Instant)
    # ========================================================================
    
    def extract(self, text: str, extract_types: List[str] = None) -> Dict:
        """
        Extract various entities from text using regex
        
        Args:
            text: Text to analyze
            extract_types: List of types to extract (urls, emails, phones, all)
                          Default: all
        
        Returns:
            Dict with extracted items:
                - urls: List of URLs
                - emails: List of email addresses
                - phones: List of phone numbers (US format)
        """
        extract_types = extract_types or ['urls', 'emails', 'phones']
        results = {}
        
        # Extract URLs
        if 'urls' in extract_types or 'all' in extract_types:
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            results['urls'] = re.findall(url_pattern, text)
        
        # Extract emails
        if 'emails' in extract_types or 'all' in extract_types:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            results['emails'] = re.findall(email_pattern, text)
        
        # Extract phone numbers (simple US format)
        if 'phones' in extract_types or 'all' in extract_types:
            phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
            results['phones'] = re.findall(phone_pattern, text)
        
        return results
    
    # ========================================================================
    # Group A: Case Conversions (Instant)
    # ========================================================================
    
    def convert_case(self, text: str, case_type: str) -> str:
        """
        Convert text to various case formats
        
        Args:
            text: Text to convert
            case_type: Type of case conversion:
                - upper: UPPERCASE
                - lower: lowercase
                - title: Title Case
                - sentence: Sentence case
                - camel: camelCase
                - pascal: PascalCase
                - snake: snake_case
                - kebab: kebab-case
        
        Returns:
            Converted text
        """
        if case_type == 'upper':
            return text.upper()
        elif case_type == 'lower':
            return text.lower()
        elif case_type == 'title':
            return text.title()
        elif case_type == 'sentence':
            return text.capitalize()
        elif case_type == 'camel':
            words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
            if not words:
                return ''
            return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        elif case_type == 'pascal':
            words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
            return ''.join(word.capitalize() for word in words)
        elif case_type == 'snake':
            words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
            return '_'.join(word.lower() for word in words)
        elif case_type == 'kebab':
            words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
            return '-'.join(word.lower() for word in words)
        else:
            raise ValueError(f"Unknown case type: {case_type}")
    
    # ========================================================================
    # Group B: Tokenization (Phase 1B - Placeholder)
    # ========================================================================
    
    def tokenize(self, text: str, model: str) -> Dict:
        """
        Count tokens for LLM models
        
        NOTE: Phase 1B implementation - currently placeholder
        Will use tiktoken and transformers for accurate counting
        
        Args:
            text: Text to tokenize
            model: Model name (gpt-4, gpt-3.5-turbo, claude, etc.)
        
        Returns:
            Dict with token count and cost estimate
        """
        # Placeholder - rough word-based estimate
        # Will be replaced with proper tokenization in Phase 1B
        word_count = len(text.split())
        estimated_tokens = int(word_count * 1.3)  # Rough approximation
        
        return {
            'text': text,
            'model': model,
            'token_count': estimated_tokens,
            'estimated_cost_usd': 0.0,
            'note': 'Placeholder implementation - Phase 1B will use proper tokenizers'
        }
    
    # ========================================================================
    # Group B: Language Detection (Phase 1B - Placeholder)
    # ========================================================================
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect language of text
        
        NOTE: Phase 1B implementation - currently placeholder
        Will use langdetect or fasttext for accurate detection
        
        Args:
            text: Text to analyze
        
        Returns:
            Dict with language code, name, and confidence
        """
        # Placeholder - always returns English
        # Will be replaced with proper detection in Phase 1B
        return {
            'code': 'en',
            'name': 'English',
            'confidence': 1.0,
            'note': 'Placeholder implementation - Phase 1B will use language detection library'
        }
    
    # ========================================================================
    # Group B: Sentiment Analysis (Phase 1B - Placeholder)
    # ========================================================================
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        
        NOTE: Phase 1B implementation - currently placeholder
        Will use VADER for rule-based sentiment analysis
        
        Args:
            text: Text to analyze
        
        Returns:
            Dict with sentiment scores and classification
        """
        # Placeholder - neutral sentiment
        # Will be replaced with VADER in Phase 1B
        return {
            'text': text,
            'sentiment': 'neutral',
            'scores': {
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 1.0,
                'compound': 0.0
            },
            'note': 'Placeholder implementation - Phase 1B will use VADER sentiment analysis'
        }
