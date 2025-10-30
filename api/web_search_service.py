"""
Web Search Service with Exa (primary) and Brave Search (fallback)
"""

import os
import logging
from typing import List, Dict, Any, Optional
import requests

# Try to import Exa SDK
try:
    from exa_py import Exa
    EXA_AVAILABLE = True
except ImportError:
    EXA_AVAILABLE = False
    logging.warning("exa-py not installed. Exa search will be disabled.")

class WebSearchService:
    """Web search service with Exa as primary and Brave as fallback"""
    
    def __init__(self):
        # Exa configuration
        self.exa_api_key = os.getenv('EXA_API_KEY', '')
        self.exa_enabled = os.getenv('EXA_ENABLED', 'true').lower() == 'true'
        self.exa_client = None
        
        # Brave Search configuration
        self.brave_api_key = os.getenv('BRAVE_API_KEY', '')
        self.brave_enabled = os.getenv('BRAVE_ENABLED', 'true').lower() == 'true'
        
        # General search settings
        self.max_results = int(os.getenv('WEB_SEARCH_MAX_RESULTS', '5'))
        self.include_text = os.getenv('WEB_SEARCH_INCLUDE_TEXT', 'true').lower() == 'true'
        self.text_length = int(os.getenv('WEB_SEARCH_TEXT_LENGTH', '1000'))

        # Diversity settings
        self.max_per_domain = int(os.getenv('WEB_SEARCH_MAX_PER_DOMAIN', '2'))
        self.diversity_multiplier = int(os.getenv('WEB_SEARCH_DIVERSITY_MULTIPLIER', '3'))
        
        # Initialize Exa client if available
        if EXA_AVAILABLE and self.exa_api_key and self.exa_enabled:
            try:
                self.exa_client = Exa(self.exa_api_key)
                logging.info("Exa search initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Exa: {e}")
                self.exa_client = None
        
        # Log availability
        if self.is_available():
            providers = []
            if self.exa_client:
                providers.append("Exa (primary)")
            if self.brave_api_key and self.brave_enabled:
                providers.append("Brave (fallback)")
            logging.info(f"Web search available with: {', '.join(providers)}")
        else:
            logging.warning("Web search not available - no API keys configured")
    
    def is_available(self) -> bool:
        """Check if any web search provider is available"""
        return (self.exa_client is not None) or (self.brave_api_key and self.brave_enabled)
    
    def search_with_exa(self, query: str, num_results: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Search using Exa API with improved diversity

        Uses multiple strategies to get diverse sources:
        1. Increased result count to filter from
        2. Category filtering to avoid single-domain dominance
        3. Text extraction for better content quality
        """
        if not self.exa_client:
            return None

        num_results = num_results or self.max_results

        try:
            logging.info(f"Searching with Exa: '{query}' (requesting diverse sources)")

            # Request MORE results than needed to filter for diversity
            # This helps avoid single-source dominance
            request_count = min(num_results * self.diversity_multiplier, 20)  # Cap at 20 for API limits

            # Use search_and_contents to get both results and full text
            result = self.exa_client.search_and_contents(
                query,
                type="auto",  # Let Exa decide between neural and keyword
                num_results=request_count,
                text=True if self.include_text else False,
                use_autoprompt=True,  # Let Exa optimize the query
                # Add parameters for better diversity
                start_published_date=None,  # No date restriction for broader results
                category=None,  # No category restriction
            )

            # Format and deduplicate results by domain
            formatted_results = []
            seen_domains = []  # Track domains in order to count duplicates
            domain_stats = {}  # Track statistics per domain

            for item in result.results:
                # Extract domain from URL for diversity checking
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(item.url).netloc
                    # Remove 'www.' prefix for better matching
                    domain = domain.replace('www.', '')
                except:
                    domain = item.url

                # Skip if we already have too many results from this domain (for diversity)
                # Allow configurable results per domain for high-quality sources
                domain_count = sum(1 for d in seen_domains if d == domain)
                if domain_count >= self.max_per_domain:
                    logging.debug(f"Skipping duplicate domain: {domain} (already have {domain_count} results)")
                    continue

                formatted_result = {
                    'title': item.title,
                    'url': item.url,
                    'snippet': item.text[:500] if hasattr(item, 'text') and item.text else '',
                    'text': item.text[:self.text_length] if hasattr(item, 'text') and item.text else '',
                    'score': item.score if hasattr(item, 'score') else None,
                    'published_date': item.published_date if hasattr(item, 'published_date') else None,
                    'author': item.author if hasattr(item, 'author') else None,
                    'source': 'exa',
                    'domain': domain
                }
                formatted_results.append(formatted_result)
                seen_domains.append(domain)

                # Track domain statistics
                domain_stats[domain] = domain_stats.get(domain, 0) + 1

                # Stop once we have enough diverse results
                if len(formatted_results) >= num_results:
                    break

            # Log diversity statistics
            unique_domains = len(set(seen_domains))
            logging.info(f"Exa returned {len(formatted_results)} diverse results from {unique_domains} different sources")
            if domain_stats:
                top_domains = sorted(domain_stats.items(), key=lambda x: x[1], reverse=True)[:3]
                logging.info(f"Top sources: {', '.join([f'{d}({c})' for d, c in top_domains])}")

            return formatted_results

        except Exception as e:
            logging.error(f"Exa search failed: {e}")
            return None
    
    def search_with_brave(self, query: str, num_results: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """Search using Brave Search API"""
        if not self.brave_api_key or not self.brave_enabled:
            return None
        
        num_results = num_results or self.max_results
        
        try:
            logging.info(f"Searching with Brave: '{query}'")
            
            # Brave Search API endpoint
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {
                "q": query,
                "count": num_results,
                "text_decorations": False,
                "search_lang": "en"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Format results
            formatted_results = []
            if 'web' in data and 'results' in data['web']:
                for item in data['web']['results']:
                    formatted_result = {
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'snippet': item.get('description', ''),
                        'text': item.get('description', '')[:self.text_length],
                        'score': None,
                        'published_date': item.get('age', None),
                        'author': None,
                        'source': 'brave'
                    }
                    formatted_results.append(formatted_result)
            
            logging.info(f"Brave returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logging.error(f"Brave search failed: {e}")
            return None
    
    def search(self, query: str, num_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search with Exa as primary, Brave as fallback
        Returns list of search results with full text content
        """
        if not self.is_available():
            logging.warning("Web search not available")
            return []
        
        # Try Exa first
        results = self.search_with_exa(query, num_results)
        
        # Fallback to Brave if Exa fails
        if results is None:
            logging.info("Falling back to Brave search")
            results = self.search_with_brave(query, num_results)
        
        # Return empty list if both fail
        if results is None:
            logging.error("All search providers failed")
            return []
        
        return results
    
    def get_answer_from_exa(self, query: str) -> Optional[str]:
        """Get a direct answer from Exa (streaming)"""
        if not self.exa_client:
            return None
        
        try:
            logging.info(f"Getting answer from Exa: '{query}'")
            
            # Stream answer from Exa
            answer_chunks = []
            for chunk in self.exa_client.stream_answer(query, text=True):
                answer_chunks.append(chunk)
            
            answer = ''.join(answer_chunks)
            logging.info(f"Exa answer received ({len(answer)} chars)")
            return answer
            
        except Exception as e:
            logging.error(f"Exa answer failed: {e}")
            return None
    
    def find_similar(self, url: str, num_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """Find similar links to a given URL using Exa"""
        if not self.exa_client:
            logging.warning("Exa not available for find_similar")
            return []
        
        num_results = num_results or self.max_results
        
        try:
            logging.info(f"Finding similar links to: {url}")
            
            result = self.exa_client.find_similar(
                url,
                num_results=num_results
            )
            
            # Get full text for each URL
            urls = [link_data.url for link_data in result.results]
            web_pages = self.exa_client.get_contents(urls, text=True)
            
            # Format results
            formatted_results = []
            for web_page in web_pages.results:
                formatted_result = {
                    'title': web_page.title if hasattr(web_page, 'title') else '',
                    'url': web_page.url,
                    'snippet': web_page.text[:500] if hasattr(web_page, 'text') and web_page.text else '',
                    'text': web_page.text[:self.text_length] if hasattr(web_page, 'text') and web_page.text else '',
                    'score': None,
                    'published_date': None,
                    'author': None,
                    'source': 'exa_similar'
                }
                formatted_results.append(formatted_result)
            
            logging.info(f"Found {len(formatted_results)} similar links")
            return formatted_results
            
        except Exception as e:
            logging.error(f"Find similar failed: {e}")
            return []
    
    def format_search_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results into context for LLM
        Highlights source diversity for better attribution
        """
        if not results:
            return ""

        # Calculate diversity statistics
        unique_domains = len(set(r.get('domain', r['url']) for r in results))

        context_parts = []
        context_parts.append("=== WEB SEARCH RESULTS ===")
        context_parts.append(f"Found {len(results)} results from {unique_domains} different sources\n")

        for i, result in enumerate(results, 1):
            # Show domain for source diversity awareness
            domain = result.get('domain', 'unknown')
            context_parts.append(f"\n[Source {i} - {domain}]")
            context_parts.append(f"Title: {result['title']}")
            context_parts.append(f"URL: {result['url']}")

            if result.get('published_date'):
                context_parts.append(f"Published: {result['published_date']}")

            if result.get('author'):
                context_parts.append(f"Author: {result['author']}")

            if result.get('score'):
                context_parts.append(f"Relevance Score: {result['score']:.3f}")

            if result.get('text'):
                context_parts.append(f"\nContent:\n{result['text']}")
            elif result.get('snippet'):
                context_parts.append(f"\nSnippet:\n{result['snippet']}")

            context_parts.append("\n" + "-" * 80)

        context_parts.append("\n=== END WEB SEARCH RESULTS ===")
        context_parts.append(f"Note: Results are from {unique_domains} diverse sources for comprehensive coverage.\n")

        return "\n".join(context_parts)


# Global instance
web_search_service = WebSearchService()
