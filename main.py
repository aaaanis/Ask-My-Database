import os
import pandas as pd
from threading import Thread

from LLM_DB import ReviewDatabase
from LLM_BOT import start_discord_client
from LLM_AGENT import ConversationalRetrievalAgent
from DB_API import app as api_app

if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    bot_token = 'XXXX'

    api_thread = Thread(target=api_app.run, kwargs={'host': 'X.X.X.X', 'port': 'XXXX'}, debug=True)
    api_thread.start()

    db = ReviewDatabase(db_name='review', user='username', password='password')
    db.setup_db()

    reviews = db.fetch_all_reviews()

    agent = ConversationalRetrievalAgent()
    agent.prepare_data(reviews)
    agent.initialize_chain()

    start_discord_client(bot_token, agent)