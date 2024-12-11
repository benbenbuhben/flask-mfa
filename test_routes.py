import pytest
import uuid
import logging

from app import create_app, db
from app.models import User
from flask import session


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def app():
    # Create an app for testing with the 'testing' config
    app = create_app()

    # Set up the app context for each test
    with app.app_context():
        db.create_all()  # Create the test database
        yield app
        db.session.remove()
        db.drop_all()  # Drop the test database after the test


@pytest.fixture
def client(app):
    # Provide a test client for making requests
    return app.test_client()


@pytest.fixture
def sample_user():
    test_user_id = str(uuid.uuid4())
    user = User(id=test_user_id, email="test@example.com", phone="+1234567890")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    return user


from bs4 import BeautifulSoup


def get_csrf_token(client, url):
    response = client.get(url)
    logger.info(response)
    soup = BeautifulSoup(response.data, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_token"})["value"]
    return csrf_token


def test_get_index_success(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_get_home_no_session(client):

    response = client.get("/home", follow_redirects=True)

    assert response.status_code == 200


def test_register_success(client):
    csrf_token = get_csrf_token(client, "/register")

    response = client.post(
        "/register",
        data=dict(
            email="newuser@example.com",
            phone="+12345678900",
            password="password",
            confirm_password="password",
            csrf_token=csrf_token,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Registration successful!" in response.data


def test_register_duplicate_email(client, sample_user):
    csrf_token = get_csrf_token(client, "/register")

    response = client.post(
        "/register",
        data=dict(
            email=sample_user.email,
            phone="+12345678900",
            password="newpassword",
            confirm_password="newpassword",
            csrf_token=csrf_token,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email already registered" in response.data


def test_login_success(client):
    csrf_token = get_csrf_token(client, "/login")
    # Test valid login
    response = client.post(
        "/login",
        data=dict(email="test@example.com", password="password", csrf_token=csrf_token),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"A verification code has been sent to your phone." in response.data


def test_login_no_account(client):
    csrf_token = get_csrf_token(client, "/login")

    # Test invalid login
    response = client.post(
        "/login",
        data=dict(
            email="nonexistent@example.com",
            password="wrongpassword",
            csrf_token=csrf_token,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert (
        b"No account found with that email. Please check and try again."
        in response.data
    )


def test_login_wrong_password(client):
    csrf_token = get_csrf_token(client, "/login")

    # Test invalid login
    response = client.post(
        "/login",
        data=dict(
            email="test@example.com", password="wrongpassword", csrf_token=csrf_token
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Wrong password. Please check and try again." in response.data


def test_change_phone_success(client, sample_user):
    csrf_token = get_csrf_token(client, "/login")

    # Log in with the sample user
    client.post(
        "/login",
        data=dict(email="test@example.com", password="password", csrf_token=csrf_token),
        follow_redirects=True,
    )

    with client.session_transaction() as session:
        session["user_id"] = sample_user.id
        session["authenticated"] = True

    # Change phone
    response = client.post(
        "/change_phone",
        data=dict(phone="+12003003000", csrf_token=csrf_token),
        follow_redirects=True,
    )

    # Check that the password change was successful
    assert response.status_code == 200
    assert b"Phone number updated successfully." in response.data


def test_change_phone_fail_no_session(client):
    csrf_token = get_csrf_token(client, "/login")

    # Log in with the sample user
    client.post(
        "/login",
        data=dict(email="test@example.com", password="password", csrf_token=csrf_token),
        follow_redirects=True,
    )

    # Change phone
    response = client.post(
        "/change_phone",
        data=dict(phone="+12003003000", csrf_token=csrf_token),
        follow_redirects=True,
    )

    # Check that the password change was successful
    assert response.status_code == 200
    assert b"Please log in first." in response.data


def test_change_phone_fail_user_notfound(client):
    csrf_token = get_csrf_token(client, "/login")

    # Log in with the sample user
    client.post(
        "/login",
        data=dict(email="test@example.com", password="password", csrf_token=csrf_token),
        follow_redirects=True,
    )

    with client.session_transaction() as session:
        session["user_id"] = "1"
        session["authenticated"] = True

    # Change phone
    response = client.post(
        "/change_phone",
        data=dict(phone="+12003003000", csrf_token=csrf_token),
        follow_redirects=True,
    )

    # Check that the password change was successful
    assert response.status_code == 200
    assert b"User not found." in response.data


def test_change_password_success(client, sample_user):
    csrf_token = get_csrf_token(client, "/login")

    # Log in with the sample user
    client.post(
        "/login",
        data=dict(email="test@example.com", password="password", csrf_token=csrf_token),
        follow_redirects=True,
    )

    with client.session_transaction() as session:
        session["user_id"] = sample_user.id
        session["authenticated"] = True

    # Change password
    response = client.post(
        "/change_password",
        data=dict(
            current_password="password",
            new_password="newpassword",
            confirm_password="newpassword",
            csrf_token=csrf_token,
        ),
        follow_redirects=True,
    )

    # Check that the password change was successful
    assert response.status_code == 200
    assert b"Password updated successfully!" in response.data


def test_change_password_incorrect_current_password(client, sample_user):
    csrf_token = get_csrf_token(client, "/login")

    # Log in with the sample user
    client.post(
        "/login",
        data=dict(email="test@example.com", password="password", csrf_token=csrf_token),
        follow_redirects=True,
    )

    with client.session_transaction() as session:
        session["user_id"] = sample_user.id
        session["authenticated"] = True
    # Change password
    response = client.post(
        "/change_password",
        data=dict(
            current_password="wrongpassword",
            new_password="newpassword",
            confirm_password="newpassword",
            csrf_token=csrf_token,
        ),
        follow_redirects=True,
    )

    # Check that the password change was successful
    assert response.status_code == 200
    assert b"Current password is incorrect." in response.data
