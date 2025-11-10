# WikiArticles

A Python tool to fetch and display Wikipedia articles with support for multiple languages.

## Features

- Fetch complete Wikipedia articles with metadata
- Support for multiple languages
- Get article summaries, sections, and links
- Simple command-line interface
- Clean object-oriented design with `Config` and `WikiArticles` classes

## Installation

### Prerequisites
- Python 3.7+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wikiartcles.git
cd wikiartcles
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Fetch an English Wikipedia article:
```bash
python search_wiki_article.py "Python"
```

Fetch an article in a different language:
```bash
python search_wiki_article.py "Gato" es
```

### Programmatic Usage

```python
from search_wiki_article import Config, WikiArticles

# Create a config and wiki instance
config = Config(language='en')
wiki = WikiArticles(config=config)

# Get full article
article = wiki.get_full_article("Python")

# Get only summary
summary = wiki.get_summary("Python")

# Get sections
sections = wiki.get_sections("Python")

# Get links (with optional limit)
links = wiki.get_links("Python", limit=20)

# Change language
wiki.set_language('es')
```

## API Reference

### Config

Configuration class for Wikipedia settings.

```python
Config(language='en')
```

**Methods:**
- `set_language(language)` - Change language code
- `to_dict()` - Export config as dictionary
- `__repr__()` - String representation

### WikiArticles

Main class for Wikipedia article operations.

```python
WikiArticles(config=None)
```

**Methods:**
- `get_full_article(title)` - Get complete article with metadata
- `get_summary(title)` - Get article summary only
- `get_sections(title)` - Get all section titles
- `get_links(title, limit=None)` - Get article links
- `set_language(language)` - Change language

## Supported Languages

This tool supports all languages available on Wikipedia. Use standard language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- And many more...

## Error Handling

The tool gracefully handles errors:

```python
article = wiki.get_full_article("NonExistentArticle")
if 'error' in article:
    print(article['error'])
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

CSV610
