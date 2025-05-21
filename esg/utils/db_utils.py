import psycopg2
from contextlib import closing
import logging
from datetime import datetime
import csv

DB_NAME = "postgres"
DB_USER = "postgres"     
DB_PASS = "finvizier2023"
DB_HOST = "esgarticles.cf4iaa2amdt3.me-central-1.rds.amazonaws.com"
DB_PORT = "5432"

logging.basicConfig(level=logging.DEBUG)

def article_exists(url):
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''SELECT COUNT(*) FROM esg_articles WHERE link = %s''', (url,))
            return cursor.fetchone()[0] > 0

def save_article(article):
    if article_exists(article['url']):
        logging.debug(f"Duplicate article found, not saving: {article['title']}")
        return
    
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''INSERT INTO esg_articles (title, published, summary, link, source, matched_keywords) 
                              VALUES (%s, %s, %s, %s, %s, %s)''', 
                           (article['title'], article['date'], article['summary'], 
                            article['url'], article['source'], article['keywords']))
            logging.debug(f"Article saved to database: {article['title']}")
            conn.commit()

def fetch_articles_by_date(selected_date):
    try:
        with closing(psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    SELECT title, published, summary, link, source, matched_keywords 
                    FROM esg_articles
                    WHERE DATE(published) = %s
                    ORDER BY published DESC
                """, (selected_date,))
                articles = cursor.fetchall()
                return articles
    except Exception as e:
        logging.error(f"Error fetching articles from database: {e}")
        return []
    
def pub_exists(url):
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT 1 FROM publications WHERE link = %s LIMIT 1", (url,))
            result = cursor.fetchone()
            return result is not None


def save_pub(article):
    if pub_exists(article['link']):
        logging.debug(f"Duplicate article found, not saving: {article['title']}")
        return
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''INSERT INTO publications (image_url, title, summary, link, source, published) 
                              VALUES (%s, %s, %s, %s, %s, %s)''', 
                           (article['image_url'], article['title'], article['summary'], 
                            article['link'], article['source'], article['date'] or current_date_time))
            logging.debug(f"Article saved to database: {article['title']}")
            conn.commit()



def create_events_table():
    """Create the events table if it doesn't exist."""
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    event_name TEXT,
                    event_id TEXT UNIQUE,
                    event_url TEXT,
                    start_date DATE,
                    end_date DATE,
                    start_time TIME,
                    end_time TIME,
                    timezone TEXT,
                    image_url TEXT,
                    ticket_price TEXT,
                    tickets_url TEXT,
                    venue_name TEXT,
                    venue_address TEXT,
                    organizer_name TEXT,
                    organizer_url TEXT,
                    summary TEXT,
                    tags TEXT,
                    source TEXT,
                    month TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.debug("Table 'events' created or already exists.")

def event_exists(event):
    """Check if an event already exists in the database.
    This version takes the entire event object and tries multiple identification strategies.
    """
    event_id = event.get('Event ID')
    event_title = event.get('Event Name')
    event_url = event.get('Event URL')
    
    # No way to identify this event
    if not event_id and not event_title and not event_url:
        return False
    
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            # First check if the table exists
            cursor.execute("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE  table_schema = 'public'
                   AND    table_name   = 'events'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                return False
            
            # Try matching by event_id first (most reliable)
            if event_id:
                cursor.execute("SELECT 1 FROM events WHERE event_id = %s LIMIT 1", (event_id,))
                result = cursor.fetchone()
                if result is not None:
                    return True
            
            # If no match by ID and we have a title, try matching by title
            if event_title:
                cursor.execute("SELECT 1 FROM events WHERE event_name = %s LIMIT 1", (event_title,))
                result = cursor.fetchone()
                if result is not None:
                    return True
            
            # If no match by ID or title, try URL if available
            if event_url:
                cursor.execute("SELECT 1 FROM events WHERE event_url = %s LIMIT 1", (event_url,))
                result = cursor.fetchone()
                if result is not None:
                    return True
                    
            return False

def save_events_to_db(events, also_save_csv=False, filename="events.csv"):
    """Save events to the database and optionally to a CSV file."""
    # First, make sure the table exists
    create_events_table()
    
    # Save to database
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            for event in events:
                # Skip if event already exists - now passing the entire event
                if event_exists(event):
                    logging.debug(f"Duplicate event found, not saving: {event.get('Event Name')}")
                    continue
                
                cursor.execute('''
                    INSERT INTO events (
                        event_name, event_id, event_url, start_date, end_date,
                        start_time, end_time, timezone, image_url, ticket_price,
                        tickets_url, venue_name, venue_address, organizer_name,
                        organizer_url, summary, tags, source, month
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                ''', (
                    event.get('Event Name'), event.get('Event ID'), event.get('Event URL'),
                    event.get('Start Date'), event.get('End Date'), event.get('Start Time'),
                    event.get('End Time'), event.get('Timezone'), event.get('Image URL'),
                    event.get('Ticket Price'), event.get('Tickets URL'), event.get('Venue Name'),
                    event.get('Venue Address'), event.get('Organizer Name'), event.get('Organizer URL'),
                    event.get('Summary'), event.get('Tags'), event.get('Source'), event.get('Month')
                ))
                logging.debug(f"Event saved to database: {event.get('Event Name')}")
            conn.commit()
    
    # Optionally save to CSV
    if also_save_csv:
        fieldnames = [
            "Event Name", "Event ID", "Event URL", "Start Date", "End Date",
            "Start Time", "End Time", "Timezone", "Image URL", "Ticket Price",
            "Tickets URL", "Venue Name", "Venue Address", "Organizer Name",
            "Organizer URL", "Summary", "Tags", "Source", "Month"
        ]

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for event in events:
                writer.writerow(event)

# For backward compatibility
def save_events_to_csv(events, filename="events.csv"):
    """Legacy function that now calls save_events_to_db with CSV saving enabled."""
    save_events_to_db(events, also_save_csv=True, filename=filename)

def recreate_events_table():
    """Drop and recreate the events table with the correct structure."""
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            # Drop the table if it exists
            cursor.execute("DROP TABLE IF EXISTS events")
            conn.commit()
            
            # Create the table with the correct structure
            cursor.execute('''
                CREATE TABLE events (
                    id SERIAL PRIMARY KEY,
                    event_name TEXT,
                    event_id TEXT UNIQUE,
                    event_url TEXT,
                    start_date DATE,
                    end_date DATE,
                    start_time TIME,
                    end_time TIME,
                    timezone TEXT,
                    image_url TEXT,
                    ticket_price TEXT,
                    tickets_url TEXT,
                    venue_name TEXT,
                    venue_address TEXT,
                    organizer_name TEXT,
                    organizer_url TEXT,
                    summary TEXT,
                    tags TEXT,
                    source TEXT,
                    month TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.debug("Table 'events' has been recreated with the correct structure.")

# Update the all_events function in events.py




def create_db():
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS esg_articles (
                                id SERIAL PRIMARY KEY,
                                title TEXT,
                                published DATE,
                                summary TEXT,
                                link TEXT UNIQUE,
                                source TEXT,
                                matched_keywords TEXT
                              )''')
            conn.commit()
            logging.debug("Table 'esg_articles' created or already exists.")