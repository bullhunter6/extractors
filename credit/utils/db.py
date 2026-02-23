import psycopg2
from contextlib import closing
import logging
from datetime import datetime, timedelta
from dateutil import parser as date_parser

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = 'finvizier2023'
DB_HOST = "creditarticles.cf4iaa2amdt3.me-central-1.rds.amazonaws.com"
DB_PORT = "5432"

logging.basicConfig(level=logging.DEBUG)


def article_exists(url, region, sector, source):
    """
    Checks if an article with the same link, region, sector, and source already exists.
    """
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''
                SELECT COUNT(*) 
                FROM credit_articles 
                WHERE link = %s AND region = %s AND sector = %s AND source = %s
            ''', (url, region, sector, source))
            return cursor.fetchone()[0] > 0



def save_article(article):
    """
    Saves the article to the database if it doesn't already exist.
    Handles region, sector, and source uniqueness logic.
    """
    article['title'] = str(article['title'])
    article['content'] = str(article['content'])

    region = ", ".join(article['region']) if isinstance(article['region'], (set, list)) else article['region']
    sector = ", ".join(article['sector']) if isinstance(article['sector'], (set, list)) else article['sector']

    if article_exists(article['link'], region, sector, article['source']):
        logging.info(f"⊘ Skipping duplicate: {article['title'][:50]}...")
        return

    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            save_time = datetime.now()
            cursor.execute('''
                INSERT INTO credit_articles 
                (title, date, content, link, source, matched_keywords, region, sector, save_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (article['title'], article['date'], article['content'],
             article['link'], article['source'], article['keywords'],
             region, sector, save_time))
            logging.info(f"✓ Article saved to DB: {article['title'][:60]}...")
            conn.commit()




def parse_date(date_str):
    """Parse a date string, returning a date object (no time)."""
    if not date_str:
        return None

    lower_str = date_str.lower().strip()
    if lower_str == 'today':
        return datetime.now().date()
    elif lower_str == 'tomorrow':
        return (datetime.now() + timedelta(days=1)).date()

    # Handle S&P Global date format: "9 Dec, 2021 | 12:06"
    if '|' in date_str:
        try:
            date_part = date_str.split('|')[0].strip()
            # Try different formats for the date part
            for fmt in ["%d %b, %Y", "%d %B, %Y", "%b %d, %Y", "%B %d, %Y"]:
                try:
                    dt = datetime.strptime(date_part, fmt)
                    return dt.date()
                except ValueError:
                    continue
        except Exception:
            pass  # Fall back to the general parser

    try:
        dt = date_parser.parse(date_str)
        return dt.date()
    except Exception:
        print(f"Warning: Could not parse date '{date_str}'.")
        return None

def save_events(events, source):
    """
    Save events into the PostgreSQL 'events' table, avoiding duplicates.
    """
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        
        check_query = """
            SELECT 1 FROM events 
            WHERE title = %s AND date = %s;
        """
        insert_query = """
            INSERT INTO events (title, date, location, details, link, source)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        for event in events:
            title = event.get('title')
            date_raw = event.get('date', '')
            parsed_date = parse_date(date_raw)
            location = event.get('location', 'N/A')
            details = event.get('details', 'N/A')
            link = event.get('link')

            if not parsed_date:
                print(f"Skipping event with invalid date: {title}")
                continue
            cursor.execute(check_query, (title, parsed_date))
            if not cursor.fetchone():
                cursor.execute(
                    insert_query, 
                    (title, parsed_date, location, details, link, source)
                )
                print(f"Saved: {title} ({parsed_date})")
            else:
                print(f"Duplicate skipped: {title} ({parsed_date})")

        connection.commit()
        print("All events have been processed.")

    except Exception as e:
        print(f"Error saving events to the database: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def create_db():
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS credit_articles (
                                id SERIAL PRIMARY KEY,
                                title TEXT,
                                date DATE,
                                content TEXT,
                                link TEXT UNIQUE,
                                source TEXT,
                                matched_keywords TEXT,
                                region TEXT,
                                sector TEXT,
                                save_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
            
            # Create publications table
            cursor.execute('''CREATE TABLE IF NOT EXISTS publications (
                                id SERIAL PRIMARY KEY,
                                title TEXT,
                                date DATE,
                                description TEXT,
                                link TEXT UNIQUE,
                                image_url TEXT,
                                source TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
            
            # Create methodologies table
            cursor.execute('''CREATE TABLE IF NOT EXISTS methodologies (
                                id SERIAL PRIMARY KEY,
                                title TEXT,
                                published_date DATE,
                                abstract TEXT,
                                description TEXT,
                                link TEXT UNIQUE,
                                report_url TEXT,
                                source TEXT,
                                permalink TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                              )''')
            
            conn.commit()
            logging.debug("All tables created or already exist.")

def publication_exists(link, source):
    """
    Checks if a publication with the same link and source already exists.
    """
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''
                SELECT COUNT(*) 
                FROM publications 
                WHERE link = %s AND source = %s
            ''', (link, source))
            return cursor.fetchone()[0] > 0

def save_publication(publication, source):
    """
    Saves a publication to the database if it doesn't already exist.
    
    Expected publication dict format:
    {
        'title': str,
        'date': str or datetime,
        'link': str,
        'description': str,
        'image': str (optional)
    }
    """
    if publication_exists(publication['link'], source):
        logging.debug(f"Duplicate publication found for source={source}, not saving: {publication['title']}")
        return

    # Convert date string to date object if needed
    if isinstance(publication.get('date'), str):
        pub_date = parse_date(publication['date'])
    else:
        pub_date = publication.get('date')

    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''
                INSERT INTO publications 
                (title, date, description, link, image_url, source)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (publication['title'], pub_date, publication.get('description'),
             publication['link'], publication.get('image'), source))
            logging.debug(f"Publication saved to database: {publication['title']}")
            conn.commit()

def methodology_exists(link, source):
    """
    Checks if a methodology with the same link and source already exists.
    """
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''
                SELECT COUNT(*) 
                FROM methodologies 
                WHERE link = %s AND source = %s
            ''', (link, source))
            return cursor.fetchone()[0] > 0

def save_methodology(methodology, source):
    """
    Saves a methodology to the database if it doesn't already exist.
    
    Expected methodology dict format:
    {
        'title': str,
        'publishedDate': str or datetime,
        'abstract': str,
        'description': str,
        'link': str,
        'permalink': str (optional),
        'report_url': str (optional)
    }
    """
    if not methodology.get('link'):
        logging.warning(f"Skipping methodology without link: {methodology.get('title', 'Unknown')}")
        return
        
    if methodology_exists(methodology['link'], source):
        logging.debug(f"Duplicate methodology found for source={source}, not saving: {methodology['title']}")
        return

    # Convert date string to date object if needed
    pub_date = None
    if isinstance(methodology.get('publishedDate'), str):
        pub_date = parse_date(methodology['publishedDate'])
    else:
        pub_date = methodology.get('publishedDate')
        
    # If date parsing failed, try alternative date fields
    if pub_date is None:
        for date_field in ['date', 'published_date', 'publication_date']:
            if methodology.get(date_field):
                pub_date = parse_date(methodology[date_field])
                if pub_date:
                    break
                    
    # If still no date, use current date
    if pub_date is None:
        logging.warning(f"Could not parse date for methodology: {methodology.get('title')}. Using current date.")
        pub_date = datetime.now().date()

    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''
                INSERT INTO methodologies 
                (title, published_date, abstract, description, link, report_url, source, permalink)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (methodology['title'], pub_date, methodology.get('abstract'),
             methodology.get('description'), methodology['link'],
             methodology.get('report_url'), source, methodology.get('permalink')))
            logging.debug(f"Methodology saved to database: {methodology['title']}")
            conn.commit()

def save_snp_methodologies():
    """
    Fetches and saves S&P Global methodologies to the database.
    """
    from methodologies.snp import get_spglobal_methodologies, get_spglobal_methodology_detail
    
    methodologies = get_spglobal_methodologies()
    for methodology in methodologies:
        # Pre-process date format for S&P methodologies
        if methodology.get('publishedDate'):
            date_str = methodology['publishedDate']
            try:
                # If it's in the format "9 Dec, 2021 | 12:06", extract just the date part
                if '|' in date_str:
                    date_part = date_str.split('|')[0].strip()
                    methodology['publishedDate'] = date_part
            except Exception:
                pass
                
        # Get detailed information if not already present
        if not methodology.get('description'):
            detail = get_spglobal_methodology_detail(methodology['permalink'])
            if detail:
                methodology.update(detail)
        
        # Ensure link is present
        if not methodology.get('link') and methodology.get('url'):
            methodology['link'] = methodology['url']
            methodology['report_url'] = methodology['url']
        
        save_methodology(methodology, source="S&P Global")
    
    return methodologies

def save_fitch_banks_methodologies():
    """
    Fetches and saves Fitch Banks methodologies to the database.
    """
    from methodologies.fitch_bk import get_fitch_banks_methodologies, get_fitch_methodology_detail
    
    methodologies = get_fitch_banks_methodologies()
    for methodology in methodologies:
        # Get detailed information if not already present
        if methodology.get('permalink'):
            detail = get_fitch_methodology_detail(methodology['permalink'])
            if detail:
                # Update with detailed information
                methodology.update(detail)
                
                # Set report_link from reportURL if available
                if detail.get('reportURL'):
                    methodology['report_url'] = detail['reportURL']
        
        # Ensure link is present
        if not methodology.get('link') and methodology.get('permalink'):
            methodology['link'] = f"https://www.fitchratings.com/research/{methodology['permalink']}"
        
        save_methodology(methodology, source="Fitch Banks")
    
    return methodologies

def save_fitch_corporates_methodologies():
    """
    Fetches and saves Fitch Corporates methodologies to the database.
    """
    from methodologies.fitch_crop import get_fitch_corporates_methodologies
    from methodologies.fitch_bk import get_fitch_methodology_detail
    
    methodologies = get_fitch_corporates_methodologies()
    for methodology in methodologies:
        # Get detailed information if permalink is available
        if methodology.get('permalink'):
            detail = get_fitch_methodology_detail(methodology['permalink'])
            if detail:
                # Update with detailed information
                methodology.update(detail)
                
                # Set report_link from reportURL if available
                if detail.get('reportURL'):
                    methodology['report_url'] = detail['reportURL']
        
        # Ensure link is present
        if not methodology.get('link') and methodology.get('permalink'):
            methodology['link'] = f"https://www.fitchratings.com/research/{methodology['permalink']}"
        
        save_methodology(methodology, source="Fitch Corporates")
    
    return methodologies

def save_all_methodologies():
    """
    Fetches and saves all methodologies from all sources.
    """
    snp = save_snp_methodologies()
    fitch_banks = save_fitch_banks_methodologies()
    fitch_corporates = save_fitch_corporates_methodologies()
    
    return {
        'snp': len(snp),
        'fitch_banks': len(fitch_banks),
        'fitch_corporates': len(fitch_corporates)
    }