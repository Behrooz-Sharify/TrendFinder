import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import time


def fetch_reddit_trends(keyword):
    url = f"https://www.reddit.com/search.json?q={keyword}&sort=hot&limit=10"
    headers = {"User-Agent": "TrendFinderApp/0.1"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        posts = data.get("data", {}).get("children", [])

        trends = []
        for post in posts:
            title = post["data"].get("title", "No title")
            subreddit = post["data"].get("subreddit", "Unknown")
            trends.append(f"Reddit ({subreddit}): {title}")

        return trends if trends else ["No Reddit trends found."]
    except Exception as e:
        return [f"Error fetching Reddit trends: {str(e)}"]


def fetch_trends(keyword):
    api_key = "pub_75805d951c8d81856a3b82e2c39d285414d8b"  # Replace with your actual key
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={keyword}&language=en"

    response = requests.get(url)
    data = response.json()

    if "results" not in data or not data["results"]:
        return ["No trends found for this keyword."]

    trends = []
    for article in data["results"][:10]:
        title = article.get("title", "No title")
        desc = article.get("description", "No description")
        trends.append(f"{title} - {desc}")

    return trends


def search_trends():
    keyword = keyword_entry.get().strip()
    results_text.delete(1.0, tk.END)

    if not keyword:
        results_text.insert(tk.END, "Please enter a keyword.")
        return

    results_text.insert(tk.END, f"Fetching trends for: {keyword}...\n\n")

    try:
        news_trends = fetch_trends(keyword)
        reddit_trends = fetch_reddit_trends(keyword)

        results_text.insert(tk.END, "📰 News Trends:\n")
        for trend in news_trends:
            results_text.insert(tk.END, f"• {trend}\n\n")

        results_text.insert(tk.END, "👥 Reddit Trends:\n")
        for trend in reddit_trends:
            results_text.insert(tk.END, f"• {trend}\n\n")

    except Exception as e:
        results_text.insert(tk.END, f"Something went wrong: {str(e)}")

        
root = tk.Tk()
root.title('Keyword Trend Finder')
root.geometry('600x400')

ttk.Label(root, text='Enter a keyword:').pack(pady=10)
keyword_entry = ttk.Entry(root, width=50)
keyword_entry.pack()

search_button = ttk.Button(root, text='Find Trends', command=search_trends)
search_button.pack()

results_text = tk.Text(root, wrap=tk.WORD, height=15)
results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
