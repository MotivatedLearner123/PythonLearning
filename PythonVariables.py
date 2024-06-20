import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

# Step 1: Fetch TechCrunch's homepage
url = "https://techcrunch.com/"
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch TechCrunch page.")
    exit()

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

#print (soup)

with open('example.txt', 'a') as file:
    file.write(str(soup))

# Step 3: Find articles
articles = soup.find_all('article')

# Step 4: Calculate yesterday's date
yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

# Step 5: Filter articles published yesterday
headlines = []

for article in articles:
    # Try to extract the date and headline
    try:
        # Find the article's publish date
        date = article.find('time')['datetime']
        
        # Ensure the article was published yesterday
        if yesterday in date:
            # Find the article's headline
            headline = article.find('h2').text.strip()
            headlines.append((date, headline))
    except (TypeError, AttributeError):
        continue  # If any key element is missing, skip this article

# Step 6: Check if there are headlines for yesterday
if not headlines:
    print("No headlines found for yesterday.")
    exit()

# Step 7: Create a DataFrame with the headlines
df = pd.DataFrame(headlines, columns=["Publish Date", "Headline"])

# Step 8: Display the DataFrame
print(df)

# Optionally, save the table to a CSV file
df.to_csv("techcrunch_headlines_yesterday.csv", index=False)