# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]
