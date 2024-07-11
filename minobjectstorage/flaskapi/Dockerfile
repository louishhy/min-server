# Base image
FROM python:3.9

# Change work dir
WORKDIR /flaskapi

# Copy requirements
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy sourcecode
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD [ "gunicorn",  "--workers", "4", "--bind", "0.0.0.0:8000", "wsgi:app" ]
