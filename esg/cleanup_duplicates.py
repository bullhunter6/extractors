import psycopg2
from contextlib import closing
import logging

from utils.db_utils import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

logging.basicConfig(level=logging.DEBUG)

def find_duplicates():
    """Find duplicate events in the database using various identification strategies."""
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            # Method 1: Find duplicates by event name (keep the oldest entry)
            cursor.execute("""
                WITH duplicates AS (
                    SELECT id, event_name, ROW_NUMBER() OVER (
                        PARTITION BY event_name
                        ORDER BY created_at ASC
                    ) as row_num
                    FROM events
                    WHERE event_name IS NOT NULL
                )
                SELECT id, event_name FROM duplicates WHERE row_num > 1
            """)
            name_duplicates = cursor.fetchall()
            
            # Method 2: Find duplicates by event URL (keep the oldest entry)
            cursor.execute("""
                WITH duplicates AS (
                    SELECT id, event_url, ROW_NUMBER() OVER (
                        PARTITION BY event_url
                        ORDER BY created_at ASC
                    ) as row_num
                    FROM events
                    WHERE event_url IS NOT NULL
                )
                SELECT id, event_url FROM duplicates WHERE row_num > 1
            """)
            url_duplicates = cursor.fetchall()
            
            # Method 3: Find duplicates by combination of name, date, and source
            cursor.execute("""
                WITH duplicates AS (
                    SELECT id, event_name, start_date, source, ROW_NUMBER() OVER (
                        PARTITION BY event_name, start_date, source
                        ORDER BY created_at ASC
                    ) as row_num
                    FROM events
                    WHERE event_name IS NOT NULL AND start_date IS NOT NULL
                )
                SELECT id, event_name FROM duplicates WHERE row_num > 1
            """)
            combo_duplicates = cursor.fetchall()
            
            return {
                'name_duplicates': name_duplicates,
                'url_duplicates': url_duplicates,
                'combo_duplicates': combo_duplicates
            }

def delete_duplicates(duplicates, strategy='interactive'):
    """Delete duplicate events from the database.
    
    Args:
        duplicates: Dictionary with lists of duplicate IDs from find_duplicates()
        strategy: One of 'interactive', 'auto', or 'preview'
    """
    # Combine all duplicate IDs into a single list
    all_duplicates = []
    
    for dup_type, dup_list in duplicates.items():
        for dup in dup_list:
            dup_id = dup[0]
            dup_name = dup[1]
            all_duplicates.append((dup_id, dup_name, dup_type))
    
    # Sort by ID to make it easier to review
    all_duplicates.sort(key=lambda x: x[0])
    
    # Preview mode - just show what would be deleted
    if strategy == 'preview':
        print(f"Found {len(all_duplicates)} duplicate events that would be deleted:")
        for dup_id, dup_name, dup_type in all_duplicates:
            print(f"ID: {dup_id}, Name: {dup_name}, Duplicate type: {dup_type}")
        return
    
    # Connect to the database for deletion
    with closing(psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )) as conn:
        with closing(conn.cursor()) as cursor:
            deleted_count = 0
            
            for dup_id, dup_name, dup_type in all_duplicates:
                # Interactive mode asks for confirmation for each deletion
                if strategy == 'interactive':
                    confirm = input(f"Delete duplicate event ID {dup_id} - '{dup_name}'? (y/n): ")
                    if confirm.lower() != 'y':
                        print(f"Skipping ID {dup_id}")
                        continue
                
                # Delete the duplicate
                cursor.execute("DELETE FROM events WHERE id = %s", (dup_id,))
                deleted_count += 1
                logging.debug(f"Deleted duplicate event ID {dup_id} - '{dup_name}'")
            
            # Commit all deletions
            conn.commit()
            print(f"Deleted {deleted_count} duplicate events from the database")

def add_composite_unique_constraint():
    """Add a composite unique constraint to prevent future duplicates."""
    try:
        with closing(psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )) as conn:
            with closing(conn.cursor()) as cursor:
                # Check if constraint exists
                cursor.execute("""
                    SELECT COUNT(*) FROM pg_constraint 
                    WHERE conname = 'unique_event_composite'
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        ALTER TABLE events ADD CONSTRAINT unique_event_composite
                        UNIQUE (event_name, start_date, source)
                    """)
                    conn.commit()
                    logging.debug("Added composite unique constraint to events table")
                else:
                    logging.debug("Composite unique constraint already exists")
    except Exception as e:
        logging.error(f"Error adding composite unique constraint: {e}")

if __name__ == "__main__":
    print("Finding duplicate events...")
    duplicates = find_duplicates()
    
    total_duplicates = sum(len(dupes) for dupes in duplicates.values())
    print(f"Found {total_duplicates} duplicate events")
    
    if total_duplicates > 0:
        # Ask user what strategy they want to use
        print("\nHow do you want to handle duplicates?")
        print("1. Preview duplicates only (no deletion)")
        print("2. Interactive deletion (confirm each)")
        print("3. Automatic deletion (delete all duplicates)")
        choice = input("Enter your choice (1-3): ")
        
        strategy = 'preview'
        if choice == '2':
            strategy = 'interactive'
        elif choice == '3':
            strategy = 'auto'
        
        delete_duplicates(duplicates, strategy)
    
    # Ask if user wants to add a unique constraint to prevent future duplicates
    add_constraint = input("\nAdd a unique constraint to prevent future duplicates? (y/n): ")
    if add_constraint.lower() == 'y':
        add_composite_unique_constraint()
        print("Unique constraint added to events table")