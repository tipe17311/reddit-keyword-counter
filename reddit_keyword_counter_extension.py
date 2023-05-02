import praw
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json

client_id = "jTdlGcZ6L0MPUP3C0CGndA"
client_secret = "h4yLLkr9H8DiY6Bd050awmHIhUo-Cg"
user_agent = "KeywordCounter by u/Guilty_Position5295"

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


def generate_date_range(start_date, end_date):
    delta = datetime.timedelta(days=1)
    current_date = start_date
    date_range = []

    while current_date <= end_date:
        date_range.append(current_date)
        current_date += delta

    return date_range


def count_keyword_occurrences(keyword, subreddit_name, start_date, end_date, limit=1000):
    subreddit = reddit.subreddit(subreddit_name)
    date_counts = {date.date(): 0 for date in generate_date_range(start_date, end_date)}

    for submission in subreddit.new(limit=limit):
        created_at = datetime.datetime.fromtimestamp(submission.created_utc)

        if start_date <= created_at <= end_date:
            date_str = created_at.date()
            date_counts[date_str] += submission.title.lower().count(keyword.lower())
            date_counts[date_str] += submission.selftext.lower().count(keyword.lower())

    return date_counts


def plot_bar_chart(keyword, subreddit_names, date_counts_list, start_date_input, end_date_input):
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'bar'}]])

    for subreddit_name, date_counts in zip(subreddit_names, date_counts_list):
        fig.add_trace(
            go.Bar(
                x=list(date_counts.keys()),
                y=list(date_counts.values()),
                name=subreddit_name
            )
        )

    fig.update_layout(
        title=f"Keyword '{keyword}' count per day in subreddits",
        xaxis_title="Date",
        yaxis_title="Count",
        legend_title="Subreddits",
        barmode='group'
    )

    fig.show()


def process_data(keyword, subreddit_names, start_date_input, end_date_input):
    start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d")

    date_counts_list = []

    for subreddit_name in subreddit_names:
        date_counts = count_keyword_occurrences(keyword, subreddit_name, start_date, end_date)
        date_counts_list.append(date_counts)

    result = {
        "keyword": keyword,
        "subreddit_names": subreddit_names,
        "date_counts_list": date_counts_list,
        "start_date": start_date_input,
        "end_date": end_date_input
    }

    return json.dumps(result)
