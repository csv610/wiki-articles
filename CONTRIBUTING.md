# Contributing to WikiArticles

We welcome contributions! Here's how to get started.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wikiartcles.git
cd wikiartcles
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them:
```bash
python search_wiki_article.py "Test Article"
```

3. Commit with clear messages:
```bash
git commit -m "Add feature: description of changes"
```

4. Push to your fork:
```bash
git push origin feature/your-feature-name
```

5. Create a Pull Request on GitHub

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Add docstrings to all classes and methods
- Keep lines under 100 characters

## Types of Contributions

### Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Include what you expected vs. what happened

### Feature Requests
- Describe the feature and why it would be useful
- Include potential use cases

### Code Contributions
- Small fixes and features welcome!
- Please add tests if applicable
- Update documentation as needed

## Questions?

Feel free to open an issue or discussion if you have any questions!

Thank you for contributing!
