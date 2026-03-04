# Python HTTP Projekt

Simple HTTP client written in Python.

Features:

- HTML tag scraping using Selenium
- GET request with parameters
- POST request (form submission)
- Cookie listing
- HTTP status check

## Installation

pip install -r requirements.txt

## Usage

Scrape HTML tag:

python script.py title

GET request:

python script.py get foo=1 bar=2

POST request:

python script.py post username=alice password=secret

List cookies:

python script.py list-cookies

Show HTTP status:

python script.py status