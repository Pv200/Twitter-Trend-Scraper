from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import uuid
from flask import Flask, render_template_string, jsonify
from pymongo import MongoClient
import requests
import time

app = Flask(__name__)
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['twitter_trends']
collection = db['trends']

def get_trends():
    driver = webdriver.Chrome()
    try:
        # Login first
        driver.get('https://twitter.com/i/flow/login')
        wait = WebDriverWait(driver, 15)

        # Login with username
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username_input.send_keys("@prakharverma499")
        username_input.send_keys(Keys.ENTER)
        time.sleep(2)

        # Login with password
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys("Prakhar@2005")
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

        # Go to explore page
        driver.get('https://twitter.com/explore')
        time.sleep(5)

        # Get trends with explicit wait
        trends = []
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                trend_elements = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '[data-testid="trend"]')))
                trends = [elem.text.split('\n')[0] for elem in trend_elements[:5]]
                if len(trends) >= 5:
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2)

        # Fill missing trends if needed
        while len(trends) < 5:
            trends.append(f"No trend found #{len(trends) + 1}")

        record = {
            '_id': str(uuid.uuid4()),
            'nameoftrend1': trends[0],
            'nameoftrend2': trends[1],
            'nameoftrend3': trends[2],
            'nameoftrend4': trends[3],
            'nameoftrend5': trends[4],
            'datetime': datetime.now(),
            'ip_address': requests.get('https://api.ipify.org').text
        }
        
        collection.insert_one(record)
        return record
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Return dummy data if scraping fails
        return {
            '_id': str(uuid.uuid4()),
            'nameoftrend1': "Error fetching trend",
            'nameoftrend2': "Error fetching trend",
            'nameoftrend3': "Error fetching trend",
            'nameoftrend4': "Error fetching trend",
            'nameoftrend5': "Error fetching trend",
            'datetime': datetime.now(),
            'ip_address': "Error fetching IP"
        }
    finally:
        driver.quit()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Twitter Trends Scraper</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .trends { margin: 20px 0; }
        pre { background: #f4f4f4; padding: 10px; }
    </style>
</head>
<body>
    {% if trends %}
        <h2>These are the most happening topics as on {{ trends.datetime.strftime('%Y-%m-%d %H:%M:%S') }}</h2>
        <div class="trends">
            - {{ trends.nameoftrend1 }}<br>
            - {{ trends.nameoftrend2 }}<br>
            - {{ trends.nameoftrend3 }}<br>
            - {{ trends.nameoftrend4 }}<br>
            - {{ trends.nameoftrend5 }}
        </div>
        <p>The IP address used for this query was {{ trends.ip_address }}</p>
        <pre>{{ trends_json }}</pre>
    {% endif %}
    <a href="{{ url_for('run_scraper') }}">Click here to run the script</a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run')
def run_scraper():
    trends = get_trends()
    return render_template_string(
        HTML_TEMPLATE,
        trends=trends,
        trends_json=jsonify(trends).get_data(as_text=True)
    )

if __name__ == '__main__':
    app.run(debug=True)