# ESG News Portal

A modern web application for tracking Environmental, Social, and Governance (ESG) news, events, and publications.

## Features

- **News Articles**: Browse and search ESG-related news articles from various sources
- **Events**: Track upcoming and past ESG events with detailed information
- **Publications**: Access ESG-related publications, reports, and whitepapers
- **User Accounts**: Register, login, and personalize your experience
- **API Access**: RESTful API endpoints for programmatic access to data
- **Responsive Design**: Modern UI that works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **Data Processing**: Pandas

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/esg-news-portal.git
   cd esg-news-portal
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables (or create a .env file):
   ```
   export FLASK_APP=esg_portal/run.py
   export FLASK_ENV=development
   export SECRET_KEY=your_secret_key
   export DATABASE_URL=postgresql://username:password@localhost/dbname
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

## Project Structure

```
esg_portal/
├── api/                  # API blueprint
│   ├── __init__.py
│   └── routes.py
├── auth/                 # Authentication blueprint
│   ├── __init__.py
│   ├── forms.py
│   └── routes.py
├── core/                 # Core application blueprint
│   ├── __init__.py
│   └── routes.py
├── models/               # Database models
│   ├── __init__.py
│   ├── article.py
│   ├── event.py
│   ├── publication.py
│   └── user.py
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── img/
├── templates/            # Jinja2 templates
│   ├── auth/
│   ├── core/
│   └── base.html
├── utils/                # Utility functions
├── __init__.py           # Application factory
└── run.py                # Application entry point
```

## API Endpoints

- `GET /api/articles` - List articles with filtering options
- `GET /api/articles/<id>` - Get a specific article
- `GET /api/events` - List events with filtering options
- `GET /api/events/<id>` - Get a specific event
- `GET /api/publications` - List publications with filtering options
- `GET /api/publications/<id>` - Get a specific publication
- `GET /api/stats` - Get portal statistics

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/) 