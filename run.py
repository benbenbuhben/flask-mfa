from app import create_app, db
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import text


def wait_for_db(max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            db.session.execute(text("SELECT 1"))
            break
        except OperationalError:
            retries += 1
            print(f"Waiting for database... ({retries}/{max_retries})")
            time.sleep(5)
    else:
        raise Exception("Could not connect to the database after several attempts.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        wait_for_db()
        try:
            db.create_all()
            print("Database tables created.")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True, host="0.0.0.0")
