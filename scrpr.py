import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

# Set the keyword and the number of days to scrape
keyword = input("Enter your keyword: ")
num_days = 30

# Set the start and end dates for the search
end_date = datetime.today()
start_date = end_date - timedelta(days=num_days)

# Format the dates for the search URL
date_format = "%m/%d/%Y"
start_date_str = start_date.strftime(date_format)
end_date_str = end_date.strftime(date_format)

# Set the URL for the search results
url = f"https://www.google.com/search?q={keyword}&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{start_date_str}%2Ccd_max%3A{end_date_str}"

# Set the user agent for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Make the HTTP request and get the content
response = requests.get(url, headers=headers)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Find the search results
search_results = soup.find_all("div", class_="tF2Cxc")

# Create the email message
msg = MIMEMultipart()
msg["From"] = "sender email"
msg["To"] = "receiver email"
# Add the subject line to the email, including the search keyword
msg["Subject"] = f"Search Results for '{keyword}'"

# Create the message body
body = f"Search results for '{keyword}' for the last {num_days} days:\n\n"
for result in search_results:
    # Extract the title
    title = result.find("h3").get_text()
    
    # Extract the URL using regular expressions
    url_regex = re.compile(r"(?P<url>https?://[^\s]+)")
    url_match = url_regex.search(str(result))
    if url_match:
        url = url_match.group("url")
    else:
        url = ""
    
    # Add the data to the message body
    body += f"Title: {title}\nURL: {url}\n\n"

# Add the message body to the email
msg.attach(MIMEText(body, "plain"))

# Send the email
with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login("sender email", "sender email password")
    smtp.send_message(msg)
    print("Email sent successfully!")
