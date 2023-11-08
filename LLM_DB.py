import psycopg2
import logging
import json

logging.basicConfig(level=logging.INFO)

class ReviewDatabase:
    def __init__(self, db_name, user, password):
        self.db_name = db_name
        self.user = user
        self.password = password

    def connect(self):
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host='db', 
            port='XXXX'
        )

    def setup_db(self):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS reviews (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(255) DEFAULT 'N/A',
                            rating INTEGER,
                            author VARCHAR(255),
                            content TEXT,
                            date TIMESTAMP
                        )
                    """)
                    conn.commit()
        except Exception as e:
            logging.error(f"Database setup failed: {e}")
            raise

    def insert_review(self, review_json):
        try:
            review_data = json.loads(review_json)
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO reviews (title, rating, author, content, date)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (review_data.get('title', 'N/A'), 
                          review_data.get('rating'), 
                          review_data['author'], 
                          review_data['content'], 
                          review_data['date']))
                    conn.commit()
        except Exception as e:
            logging.error(f"Failed to insert review: {e}")
            raise

    def fetch_all_reviews(self):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM reviews")
                    reviews = cur.fetchall()
                    return reviews
        except Exception as e:
            logging.error(f"Failed to fetch reviews: {e}")
            raise