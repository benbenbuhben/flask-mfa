# Flask-MFA

A simple Flask application demonstrating user registration. This will eventually include login with Multi-Factor Authentication (MFA) capabilities.

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose**
- **Pipenv** (optional, for local development)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/benbenbuhben/flask-mfa.git
   cd flask-mfa
   ```

2. **Set Up Environment Variables**

   Copy the `.env.template` and change the copied file name to `.env`.  
   Change the credentials. You can ignore `DB_NAME`

   ```
   SECRET_KEY=your_secret_key_here
   DB_USER=your_db_user_here
   DB_PASSWORD=your_database_password_here
   DB_HOST=your_db_host_here
   DB_NAME=your_db_name_here
   TWILIO_ACCOUNT_SID=
   TWILIO_AUTH_TOKEN=
   TWILIO_SERVICE_SID=
   TWILIO_PHONE=
   TWILIO_CONTENT_SID=
   ```

   *Note:* Add `.env` to your `.gitignore` file to prevent committing sensitive information.

3. **Build and Run with Docker Compose**

   ```bash
   docker-compose up -d
   ```

   Access the application at `http://localhost:5001/register` (this is the only route for the time being).

4. **Access Adminer (Database Management Tool)**

   Visit `http://localhost:8080` to manage the MySQL database using Adminer.

   - **System:** MySQL
   - **Server:** db
   - **Username:** root
   - **Password:** (your `DB_PASSWORD`)
   - **Database:** mfa_demo

## Development Notes

### Using Pipenv

For local development, you can use Pipenv to manage dependencies.

1. **Install Dependencies**

   ```bash
   pipenv install
   ```

2. **Activate the Virtual Environment**

   ```bash
   pipenv shell
   ```

3. **Add dependencies**

   ```bash
   pipenv install {your dependencies}
   ```

### Generating `requirements.txt`

Running the application stack via docker requires updating the `requirements.txt`. You can generate it using:

```bash
pipenv lock -r > requirements.txt
```

This exports the locked dependencies from `Pipfile.lock` to `requirements.txt`.

## Set up test
```
pytest -v test_routes.py

```
Generate code coverage report:
```
pytest --cov=. --cov-report=xml --cov-report=term
```
## Miscellanous
Scan code with SonarQube:
Prerequisite:
 Python >= 3.8  

1. Create a SonarQube Server docker container
```
docker volume create sonar
docker run --name sonarqube-custom -p 9000:9000 -v sonar:/opt/sonarqube/data sonarqube:10.6-community
```
Credentials by default is admin/admin

2. Install Sonar Scanner
```
pip install pysonar-scanner
```
3. Set up environment variable:
In your terminal
```
export SONAR_HOST_URL="http://localhost:9000"
pysonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_84e78faa62287bf2a58dac0063ca48b370fdbc29
```

4. Export variable