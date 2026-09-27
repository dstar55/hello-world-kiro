"""
Text Service

Business logic for text transformations and processing.
All text operations are implemented here.
"""

import base64
import hashlib
import re
from typing import Dict, List

# Phase 1B: ML imports
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

try:
    from langdetect import detect, detect_langs, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
    # Initialize VADER analyzer once
    _vader_analyzer = SentimentIntensityAnalyzer()
except ImportError:
    VADER_AVAILABLE = False
    _vader_analyzer = None


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
    # Group B: Tokenization (Phase 1B)
    # ========================================================================
    
    def tokenize(self, text: str, model: str) -> Dict:
        """
        Count tokens for LLM models using tiktoken
        
        Args:
            text: Text to tokenize
            model: Model name (gpt-4, gpt-4o, gpt-3.5-turbo, claude, etc.)
        
        Returns:
            Dict with token count and cost estimate
        """
        if not TIKTOKEN_AVAILABLE:
            # Fallback to word-based estimation
            word_count = len(text.split())
            estimated_tokens = int(word_count * 1.3)
            return {
                'text': text,
                'model': model,
                'token_count': estimated_tokens,
                'estimated_cost_usd': 0.0,
                'note': 'tiktoken not available - using word-based estimation'
            }
        
        # Map model names to tiktoken encodings
        model_mapping = {
            'gpt-4': 'cl100k_base',
            'gpt-4o': 'o200k_base',
            'gpt-4-turbo': 'cl100k_base',
            'gpt-3.5-turbo': 'cl100k_base',
            'claude': 'cl100k_base',  # Claude uses similar tokenization
            'claude-3': 'cl100k_base',
            'text-davinci-003': 'p50k_base',
            'text-davinci-002': 'p50k_base',
        }
        
        # Get encoding name
        encoding_name = model_mapping.get(model, 'cl100k_base')
        
        try:
            encoding = tiktoken.get_encoding(encoding_name)
            tokens = encoding.encode(text)
            token_count = len(tokens)
            
            # Cost estimates (per 1M tokens as of 2024)
            # These are approximate values
            cost_per_1m_tokens = {
                'gpt-4': 30.0,  # Input tokens
                'gpt-4o': 2.5,  # Input tokens
                'gpt-4-turbo': 10.0,
                'gpt-3.5-turbo': 0.5,
                'claude': 15.0,
                'claude-3': 15.0,
            }
            
            cost_rate = cost_per_1m_tokens.get(model, 10.0)
            estimated_cost = (token_count / 1_000_000) * cost_rate
            
            return {
                'text': text,
                'model': model,
                'encoding': encoding_name,
                'token_count': token_count,
                'estimated_cost_usd': round(estimated_cost, 6)
            }
        except Exception as e:
            # Fallback if encoding fails
            word_count = len(text.split())
            estimated_tokens = int(word_count * 1.3)
            return {
                'text': text,
                'model': model,
                'token_count': estimated_tokens,
                'estimated_cost_usd': 0.0,
                'error': f'Tokenization failed: {str(e)}'
            }
    
    # ========================================================================
    # Group B: Language Detection (Phase 1B)
    # ========================================================================
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect language of text using langdetect
        
        Args:
            text: Text to analyze
        
        Returns:
            Dict with language code, name, and confidence
        """
        if not LANGDETECT_AVAILABLE:
            return {
                'code': 'en',
                'name': 'English',
                'confidence': 0.0,
                'note': 'langdetect not available - defaulting to English'
            }
        
        # Language code to name mapping (common languages)
        language_names = {
            'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali',
            'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish',
            'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish',
            'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French',
            'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian',
            'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese',
            'kn': 'Kannada', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian',
            'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali',
            'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi', 'pl': 'Polish',
            'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak',
            'sl': 'Slovenian', 'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish',
            'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
            'tl': 'Tagalog', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
            'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)'
        }
        
        try:
            # Get detailed detection with probabilities
            detections = detect_langs(text)
            
            if not detections:
                return {
                    'code': 'unknown',
                    'name': 'Unknown',
                    'confidence': 0.0,
                    'note': 'Could not detect language'
                }
            
            # Get the most likely language
            top_detection = detections[0]
            lang_code = top_detection.lang
            confidence = top_detection.prob
            
            # Get language name
            lang_name = language_names.get(lang_code, lang_code.upper())
            
            # Include alternatives if confidence is low
            result = {
                'code': lang_code,
                'name': lang_name,
                'confidence': round(confidence, 4)
            }
            
            # Add alternatives if there are multiple possibilities
            if len(detections) > 1 and confidence < 0.95:
                alternatives = []
                for det in detections[1:4]:  # Top 3 alternatives
                    alt_code = det.lang
                    alt_name = language_names.get(alt_code, alt_code.upper())
                    alternatives.append({
                        'code': alt_code,
                        'name': alt_name,
                        'confidence': round(det.prob, 4)
                    })
                result['alternatives'] = alternatives
            
            return result
            
        except LangDetectException as e:
            return {
                'code': 'unknown',
                'name': 'Unknown',
                'confidence': 0.0,
                'error': f'Detection failed: {str(e)}'
            }
        except Exception as e:
            return {
                'code': 'unknown',
                'name': 'Unknown',
                'confidence': 0.0,
                'error': f'Unexpected error: {str(e)}'
            }
    
    # ========================================================================
    # Group B: Sentiment Analysis (Phase 1B)
    # ========================================================================
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text using VADER
        
        VADER (Valence Aware Dictionary and sEntiment Reasoner) is a 
        lexicon and rule-based sentiment analysis tool that is specifically 
        attuned to sentiments expressed in social media.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dict with sentiment scores and classification
        """
        if not VADER_AVAILABLE or _vader_analyzer is None:
            return {
                'text': text,
                'sentiment': 'neutral',
                'scores': {
                    'positive': 0.0,
                    'negative': 0.0,
                    'neutral': 1.0,
                    'compound': 0.0
                },
                'note': 'VADER not available - defaulting to neutral'
            }
        
        try:
            # Get sentiment scores
            scores = _vader_analyzer.polarity_scores(text)
            
            # Classify based on compound score
            # Compound score is a normalized metric between -1 (most negative) and +1 (most positive)
            compound = scores['compound']
            
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'scores': {
                    'positive': round(scores['pos'], 4),
                    'negative': round(scores['neg'], 4),
                    'neutral': round(scores['neu'], 4),
                    'compound': round(scores['compound'], 4)
                }
            }
            
        except Exception as e:
            return {
                'text': text,
                'sentiment': 'neutral',
                'scores': {
                    'positive': 0.0,
                    'negative': 0.0,
                    'neutral': 1.0,
                    'compound': 0.0
                },
                'error': f'Sentiment analysis failed: {str(e)}'
            }
