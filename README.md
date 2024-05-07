# 10K Insights

## Installation

1. Create a virtual environment:
`
python -m venv env
`

2. Clone the repository:
`
git clone https://github.com/AndKaminer/10k-insights
`

3. Activate the virtual environment (assuming you're on linux):
`
source env/bin/activate
`

4. Install project
`
pip install -U .
`


## Running Locally

Install the project. Then, from inside the top-level directory, use the command:
`
flask --app flaskr run
`

Then, add your claude api key in the instance folder as 'anthropic_key.txt'

## Technologies I Learned for the First Time on This Project:
- Flask (First time building a real web app)
- Anthropic API
- sec-downloader
- SocketIO
- Chart.js

## Writeup

### Tech Stack

As someone who works much more on the data science side of things than the web-development side,
I chose to maximize the amount of python used in this project.
To that end, I chose to use Flask to run my server on the backend.
I chose to use Flask for the following reasons:
- Flask is lightweight and easy to get an app up and running on
- It is very flexible and easy to work with
- It is pretty easy to scale
- It is really well documented

For my LLM, I chose to use Anthropic's Claude. This was mainly because Claude can handle
a large context length, as opposed to OpenAI's GPT models (or, at least, I would have had to pay a lot
to use the models that could handle a large context length).
Because financial documents are so verbose, this was the most important factor in my choice.

For charting, I used Chart.js, a lightweight javascript charting library. I chose to use
it because it has all of the features I would reasonably need, without the need to write
a bunch of JavaScript.

### File Downloading Approach
I used sec_downloader to download metadata for the documents, then I used the requests library to get the raw html,
since I had some problems with the way sec_downloader or sec-edgar-downloader were dealing with older files.
Since the app is built to be easily extensible, I chose to download files at runtime, as needed.
I also chose to keep them in the program's memory, as opposed to downloading as persistant files.
This can slow down performance, to some extent, but it is a much more scalable option than
keeping all of the documents on the server all of the time, which can take up a lot of space.

### Notes on the Insight
For my insight, I chose to let the user compare and contrast a document from a company from two different years.
The idea is as follows: since financial documents can be so difficult to parse, it may be difficult for readers
to determine how the direction management is taking has changed. By having an LLM read the documents 
and summarize the differences and similarities, it becomes much easier for a layperson to understand
what the company's past business direction was, what it is now, and perhaps where it is going in the future.
For instance, let's look at a comparison of Item 1. from 1995 to 2020. Claude notes that, in 1995, Apple's
main competition came from competitors trying to beat Apple on things like product features and performance.
However, in 2020, Claude notes that most of Apple's competition comes from attempts to emulate
Apple's product at lower prices. This insight would be difficult to glean without Claude emphasizing it.

The viewable sections are, again, meant to be extendable, so you can add in other sections if you would like.

### Charts
I wanted to remain centered around language for my visualization, so I decided to use VADER to do some light
sentiment analysis, trying to see how the VADER score would change over time. Unfortunately, as financial documents
tend to be rather neutral, the VADER positivity score doesn't have a lot of variance, but perhaps some insight can
be gleaned from the changes over time.

This, again, is meant to be easy to expand upon.
