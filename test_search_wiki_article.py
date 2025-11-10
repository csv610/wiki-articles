"""
Unit tests for search_wiki_article module.

Tests cover the Config and WikiArticles classes using mocking
to avoid external Wikipedia API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from search_wiki_article import Config, WikiArticles


class TestConfig:
    """Test suite for the Config class."""

    def test_config_default_language(self):
        """Test Config initializes with default language 'en'."""
        config = Config()
        assert config.language == 'en'

    def test_config_custom_language(self):
        """Test Config initializes with custom language."""
        config = Config(language='es')
        assert config.language == 'es'

    def test_config_set_language(self):
        """Test setting language after initialization."""
        config = Config()
        config.set_language('fr')
        assert config.language == 'fr'

    def test_config_to_dict(self):
        """Test Config returns dictionary representation."""
        config = Config(language='de')
        expected = {'language': 'de'}
        assert config.to_dict() == expected

    def test_config_repr(self):
        """Test Config string representation."""
        config = Config(language='it')
        assert repr(config) == "Config(language='it')"

    def test_config_repr_default(self):
        """Test Config repr with default language."""
        config = Config()
        assert repr(config) == "Config(language='en')"


class TestWikiArticlesInit:
    """Test suite for WikiArticles initialization."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_wiki_articles_default_config(self, mock_wikipedia):
        """Test WikiArticles initializes with default config."""
        wiki = WikiArticles()
        assert wiki.config.language == 'en'
        mock_wikipedia.assert_called_once()

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_wiki_articles_custom_config(self, mock_wikipedia):
        """Test WikiArticles initializes with custom config."""
        config = Config(language='es')
        wiki = WikiArticles(config=config)
        assert wiki.config.language == 'es'
        mock_wikipedia.assert_called_once()

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_wiki_articles_user_agent(self, mock_wikipedia):
        """Test WikiArticles sets correct user agent."""
        wiki = WikiArticles()
        assert wiki.USER_AGENT == 'MyApp/1.0 (your@email.com)'
        mock_wikipedia.assert_called_with(
            user_agent='MyApp/1.0 (your@email.com)',
            language='en'
        )


class TestGetFullArticle:
    """Test suite for get_full_article method."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_full_article_success(self, mock_wikipedia):
        """Test get_full_article returns complete article data."""
        # Setup mock
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.fullurl = "https://en.wikipedia.org/wiki/Python"
        mock_page.summary = "Python is a programming language."
        mock_page.text = "Python is a high-level programming language..."
        mock_page.categories = {'Category:Programming languages': Mock(title='Category:Programming languages')}
        mock_page.links = {'Java': Mock(), 'C++': Mock(), 'Ruby': Mock()}
        mock_page.sections = [Mock(title='Overview'), Mock(title='History')]

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_full_article("Python")

        assert result['title'] == "Python"
        assert result['url'] == "https://en.wikipedia.org/wiki/Python"
        assert result['summary'] == "Python is a programming language."
        assert 'full_text' in result
        assert 'categories' in result
        assert 'links' in result
        assert 'sections' in result

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_full_article_not_found(self, mock_wikipedia):
        """Test get_full_article returns error for non-existent article."""
        mock_page = Mock()
        mock_page.exists.return_value = False

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_full_article("NonExistentArticle123")

        assert 'error' in result
        assert "NonExistentArticle123" in result['error']

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_full_article_limits_links(self, mock_wikipedia):
        """Test get_full_article limits links to first 20."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Test"
        mock_page.fullurl = "https://example.com"
        mock_page.summary = "Summary"
        mock_page.text = "Text"
        mock_page.categories = {}
        # Create 30 links
        mock_page.links = {f'Link{i}': Mock() for i in range(30)}
        mock_page.sections = []

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_full_article("Test")

        # Should only have first 20 links
        assert len(result['links']) == 20


class TestGetSummary:
    """Test suite for get_summary method."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_summary_success(self, mock_wikipedia):
        """Test get_summary returns title and summary."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.summary = "Python is a programming language."

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_summary("Python")

        assert result['title'] == "Python"
        assert result['summary'] == "Python is a programming language."
        assert len(result) == 2

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_summary_not_found(self, mock_wikipedia):
        """Test get_summary returns error for non-existent article."""
        mock_page = Mock()
        mock_page.exists.return_value = False

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_summary("NonExistent")

        assert 'error' in result
        assert "NonExistent" in result['error']


class TestGetSections:
    """Test suite for get_sections method."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_sections_success(self, mock_wikipedia):
        """Test get_sections returns title and section list."""
        mock_sections = [
            Mock(title='Introduction'),
            Mock(title='History'),
            Mock(title='Usage'),
        ]
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.sections = mock_sections

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_sections("Python")

        assert result['title'] == "Python"
        assert result['sections'] == ['Introduction', 'History', 'Usage']

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_sections_not_found(self, mock_wikipedia):
        """Test get_sections returns error for non-existent article."""
        mock_page = Mock()
        mock_page.exists.return_value = False

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_sections("NonExistent")

        assert 'error' in result

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_sections_empty_sections(self, mock_wikipedia):
        """Test get_sections with article that has no sections."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Stub"
        mock_page.sections = []

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_sections("Stub")

        assert result['sections'] == []


class TestGetLinks:
    """Test suite for get_links method."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_links_success(self, mock_wikipedia):
        """Test get_links returns links with total count."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.links = {'Java': Mock(), 'Ruby': Mock(), 'Go': Mock()}

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_links("Python")

        assert result['title'] == "Python"
        assert len(result['links']) == 3
        assert result['total_links'] == 3

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_links_with_limit(self, mock_wikipedia):
        """Test get_links respects limit parameter."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.links = {f'Link{i}': Mock() for i in range(10)}

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_links("Python", limit=5)

        assert len(result['links']) == 5
        assert result['total_links'] == 10

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_links_not_found(self, mock_wikipedia):
        """Test get_links returns error for non-existent article."""
        mock_page = Mock()
        mock_page.exists.return_value = False

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_links("NonExistent")

        assert 'error' in result

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_get_links_no_limit(self, mock_wikipedia):
        """Test get_links returns all links when limit is None."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.links = {f'Link{i}': Mock() for i in range(15)}

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        result = wiki.get_links("Python", limit=None)

        assert len(result['links']) == 15


class TestSetLanguage:
    """Test suite for set_language method."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_set_language(self, mock_wikipedia):
        """Test set_language updates config and reinitializes wiki."""
        wiki = WikiArticles()
        assert wiki.config.language == 'en'

        wiki.set_language('es')
        assert wiki.config.language == 'es'

        # Verify Wikipedia was reinitialized with new language
        calls = mock_wikipedia.call_args_list
        assert len(calls) == 2  # Initial + one for set_language
        assert calls[1][1]['language'] == 'es'

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_set_language_multiple_times(self, mock_wikipedia):
        """Test set_language can be called multiple times."""
        wiki = WikiArticles(Config(language='en'))

        wiki.set_language('fr')
        assert wiki.config.language == 'fr'

        wiki.set_language('de')
        assert wiki.config.language == 'de'

        wiki.set_language('it')
        assert wiki.config.language == 'it'

        calls = mock_wikipedia.call_args_list
        assert len(calls) == 4  # Initial + 3 set_language calls


class TestIntegration:
    """Integration tests for multiple methods."""

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_workflow_get_summary_then_sections(self, mock_wikipedia):
        """Test getting summary then sections of same article."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Python"
        mock_page.summary = "A programming language"
        mock_page.sections = [Mock(title='History'), Mock(title='Usage')]

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()

        summary = wiki.get_summary("Python")
        assert summary['title'] == "Python"

        sections = wiki.get_sections("Python")
        assert sections['title'] == "Python"
        assert len(sections['sections']) == 2

    @patch('search_wiki_article.wikipediaapi.Wikipedia')
    def test_workflow_language_change(self, mock_wikipedia):
        """Test changing language and querying articles."""
        mock_page = Mock()
        mock_page.exists.return_value = True
        mock_page.title = "Gato"
        mock_page.summary = "An animal"

        mock_wiki_instance = Mock()
        mock_wiki_instance.page.return_value = mock_page
        mock_wikipedia.return_value = mock_wiki_instance

        wiki = WikiArticles()
        wiki.set_language('es')

        result = wiki.get_summary("Gato")
        assert result['title'] == "Gato"
