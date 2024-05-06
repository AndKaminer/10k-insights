from nonflask.filing_retrieval import FilingRetriever

import os
import socketio
import json
import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import openai
import anthropic

TICKERS = ["AAPL", "MSFT"]
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

    section_to_name = {
            'business' : 'Item 1. Business Description',
            'mda' : 'Item 7. Management Discussion'}



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
            else:
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
        time.sleep(5)
        emit('process-finished', json.dumps({'data' : 'Lorem ipsum ipsum lorem\n\n blah blah lorem ipsum lorem upsum rahasdkfh \n- rahhhh lorem ipsum'}))

    @socketio.on('gpt-event')
    def handle_openai_request(data):
        document1 = data['document1']
        document2 = data['document2']
        year1 = data['year1']
        year2 = data['year2']
        section = data['section']
        ticker = data['ticker']

        with app.open_instance_resource('.env') as key:
            k = key.readline().decode().rstrip('\n')
            client = openai.OpenAI(api_key=k)
        message = f"Both documents are from {section} of reports from company with ticker: {ticker}. This is the first document, from {year1}:\n{document1}\n\n This is the second document, from {year2}:\n{document2}"
        print(message)
        response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant who is an expert in reading financial statements. You will be provided with two financial statements from a 10K. Please compare and contrast them."},
                          {"role": "user", "content": message}])

        emit('process-finished', json.dumps({'data' : response.choices[0].message.content}))

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


    return app
