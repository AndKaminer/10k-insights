from nonflask.filing_retrieval import FilingRetriever

import os
import socketio
import json
import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import anthropic
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "GOOGL", "META", "IBM"]
STARTING_DATE = 1995
COMPANY = "Georgia Tech"
EMAIL = "akaminer@gatech.edu"


def create_app(test_config=None, instance_relative_config=True):

    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)

    socketio = SocketIO(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    nltk.download("vader_lexicon")
    section_to_name = {
            'business' : 'Item 1. Business Description',
            'mda' : 'Item 7. Management Discussion'}

    chart_to_name = {
            'vscore-over-time': "Vader score over time"
            }


    @app.route('/')
    def root():
        return render_template('index.html', tickers=TICKERS)

    @app.route('/stock/<ticker>', methods=['GET', 'POST'])
    def stock(ticker):

        if request.method == 'GET':
            earliest, latest = FilingRetriever.get_year_range(ticker)
            earliest = max(earliest, STARTING_DATE)
            return render_template('stock.html', ticker=ticker, earliest=earliest, latest=latest)
        elif request.method == 'POST':
            if 'years' in request.form.keys():
                year = int(request.form['years'])
                section = request.form['section']
                filing = FilingRetriever(ticker, COMPANY, EMAIL, year).parse_10k_filing()
                
                return render_template(
                        'filing.html',
                        ticker=ticker,
                        filing=filing,
                        year=year,
                        section=section,
                        section_to_name=section_to_name)

            elif 'chart_type' in request.form.keys():
                chart_type = request.form['chart_type']
                starting_year = int(request.form['starting_year'])
                ending_year = int(request.form['ending_year'])
                document = request.form['document']
                ticker = request.form['ticker']

                return render_template('chart.html', title=chart_to_name[chart_type], chart_type=chart_type, starting_year=starting_year, ending_year=ending_year, document=document, ticker=ticker)

            elif 'year1' in request.form.keys():
                year1 = int(request.form['year1'])
                year2 = int(request.form['year2'])
                section = request.form['section']
                year1_section = FilingRetriever(ticker, COMPANY, EMAIL, year1).parse_10k_filing()[section]
                year2_section = FilingRetriever(ticker, COMPANY, EMAIL, year2).parse_10k_filing()[section]
                return render_template('comparison.html', ticker=ticker, section=section_to_name[section], document1=year1_section, document2=year2_section, year1=year1, year2=year2)
        else:
            return "<p>Invalid method</p>"

    @socketio.on('test-event')
    def test(data):
        time.sleep(2)
        emit('process-finished', json.dumps({'data' : 'Lorem ipsum ipsum lorem\n\n blah blah lorem ipsum lorem upsum rahasdkfh lorem iplore sumip ipsum lorlor ipipsum loripsumsum loreip lorelorelore ipipip loremsumip blah blah blah testing testing 1, 2, 3 \n- rahhhh lorem ipsum'}))

    @socketio.on('chart-event')
    def handle_chart_request(data):
        ticker = data['ticker']
        chart_type = data['chart_type']
        starting_year = int(data['starting_year'])
        ending_year = int(data['ending_year'])
        document = data['document']

        if chart_type == 'vscore-over-time':
            x = [ i for i in range(starting_year, ending_year + 1) ]
            y = get_vader_scores(ticker, document, starting_year, ending_year)
            data = process_chart_data(x, y)
        else:
            data = [{'x': 0, 'y': 0}]

        emit('process-finished', json.dumps(data))

    @socketio.on('claude-event')
    def handle_claude_request(data):
        document1 = data['document1']
        document2 = data['document2']
        year1 = data['year1']
        year2 = data['year2']
        section = data['section']
        ticker = data['ticker']

        with app.open_instance_resource('anthropic_key.txt') as k:
            key = k.readline().decode().rstrip('\n')

        client = anthropic.Anthropic(api_key=key)
        message = f"Both documents are from {section} of reports from company with ticker: {ticker}. This is the first document, from {year1}:\n{document1}\n\n This is the second document, from {year2}:\n{document2}"

        response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                temperature=0.0,
                system="You are a helpful assistant who is an expert in reading financial statements. You will be provided with two financial statements from a 10K. Please compare and contrast them.",
                messages=[{"role": "user", "content": message}]).content[0].text

        emit('process-finished', json.dumps({'data': response}))

    def process_chart_data(x, y):
        if len(x) != len(y):
            raise Exception("x and y arrays don't have the same length!")
        
        zipped = zip(x, y)
        data = [ {'x': z[0], 'y': z[1]} for z in zipped ]
        return data


    def return_test_chart():
        return ([1, 2, 3, 4, 5, 6, 7, 8], [2.7, 3.5, 1.4, 7.8, 9.0, 14.3, 17.5, 2.6])

    def get_vader_score(text):
        analyzer = SentimentIntensityAnalyzer()

        return analyzer.polarity_scores(text)

    def get_vader_scores(ticker, document, start_year, end_year):
        earliest, latest = FilingRetriever.get_year_range(ticker)

        if start_year < earliest or end_year > latest:
            raise Exception('Invalid start or end year')

        scores = []

        for year in range(start_year, end_year + 1):
            f = FilingRetriever(ticker, COMPANY, EMAIL, year)

            data = f.parse_10k_filing()
            text = data[document]

            vscores = get_vader_score(text)

            scores.append(vscores['pos'])

        return scores

    return app
