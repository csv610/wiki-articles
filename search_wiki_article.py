"""
WikiArticles - A Python tool to fetch Wikipedia articles.

This module provides a simple interface to retrieve Wikipedia articles
in multiple languages with support for summaries, sections, and links.

Example:
    Basic usage from command line:
    $ python search_wiki_article.py "Python"
    $ python search_wiki_article.py "Gato" es

    Programmatic usage:
    >>> config = Config(language='en')
    >>> wiki = WikiArticles(config=config)
    >>> article = wiki.get_full_article("Python")
"""

from typing import Optional, Dict, Any, List
import wikipediaapi


class Config:
    """
    Configuration class for Wikipedia API settings.
    """

    def __init__(self, language: str = 'en') -> None:
        """
        Initialize configuration.

        Args:
            language: Language code (default: 'en')
        """
        self.language: str = language

    def set_language(self, language: str) -> None:
        """Set language code."""
        self.language = language

    def to_dict(self) -> Dict[str, str]:
        """Return configuration as dictionary."""
        return {
            'language': self.language
        }

    def __repr__(self) -> str:
        return f"Config(language='{self.language}')"


class WikiArticles:
    """
    A class to interact with Wikipedia articles using the wikipediaapi library.
    """

    USER_AGENT: str = 'MyApp/1.0 (your@email.com)'

    def __init__(self, config: Optional[Config] = None) -> None:
        """
        Initialize WikiArticles with configuration.

        Args:
            config: Config object (if None, uses default configuration)
        """
        self.config: Config = config or Config()
        self.wiki: wikipediaapi.Wikipedia = wikipediaapi.Wikipedia(
            user_agent=self.USER_AGENT,
            language=self.config.language
        )

    def get_full_article(self, title: str) -> Dict[str, Any]:
        """
        Get complete Wikipedia article content.

        Args:
            title: Article title

        Returns:
            Dictionary with full article information or error message
        """
        page = self.wiki.page(title)

        if not page.exists():
            return {"error": f"Page '{title}' does not exist"}

        return {
            'title': page.title,
            'url': page.fullurl,
            'summary': page.summary,
            'full_text': page.text,
            'categories': [cat.title for cat in page.categories.values()],
            'links': list(page.links.keys())[:20],
            'sections': [section.title for section in page.sections]
        }

    def get_summary(self, title: str) -> Dict[str, Any]:
        """
        Get only the summary of an article.

        Args:
            title: Article title

        Returns:
            Summary text or error message
        """
        page = self.wiki.page(title)

        if not page.exists():
            return {"error": f"Page '{title}' does not exist"}

        return {
            'title': page.title,
            'summary': page.summary
        }

    def get_sections(self, title: str) -> Dict[str, Any]:
        """
        Get all sections of an article.

        Args:
            title: Article title

        Returns:
            List of section titles or error message
        """
        page = self.wiki.page(title)

        if not page.exists():
            return {"error": f"Page '{title}' does not exist"}

        return {
            'title': page.title,
            'sections': [section.title for section in page.sections]
        }

    def get_links(self, title: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get links from an article.

        Args:
            title: Article title
            limit: Maximum number of links to return (None for all)

        Returns:
            List of links or error message
        """
        page = self.wiki.page(title)

        if not page.exists():
            return {"error": f"Page '{title}' does not exist"}

        links = list(page.links.keys())
        if limit:
            links = links[:limit]

        return {
            'title': page.title,
            'links': links,
            'total_links': len(list(page.links.keys()))
        }

    def set_language(self, language: str) -> None:
        """
        Change the language for Wikipedia queries.

        Args:
            language: Language code
        """
        self.config.set_language(language)
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=self.USER_AGENT,
            language=self.config.language
        )


import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python search_wiki_article.py <article_title> [language]")
        sys.exit(1)

    article_title = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'en'

    # Create config and wiki instance
    config = Config(language=language)
    wiki = WikiArticles(config=config)

    print(f"Configuration: {config}")
    article = wiki.get_full_article(article_title)

    if 'error' in article:
        print(f"Error: {article['error']}")
        sys.exit(1)

    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"\n--- FULL ARTICLE ---")
    print(article['full_text'])
    print(f"\n--- METADATA ---")
    print(f"Total characters: {len(article['full_text'])}")
    print(f"Sections: {', '.join(article['sections'][:5])}...")

if __name__ == "__main__":
   main()
