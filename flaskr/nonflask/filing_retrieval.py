from sec_downloader import Downloader
from sec_downloader.types import RequestedFilings

import requests
import re
import unicodedata
from bs4 import BeautifulSoup as bs


class FilingRetriever:
    def __init__(self, ticker: str, company_name: str, email: str, year: int):
        earliest, latest = FilingRetriever.get_year_range(ticker)

        if year < earliest:
            raise Exception(f"Invalid year - {year}, {earliest}")

        dl = Downloader(company_name, email)
        metadata = dl.get_filing_metadatas(
                RequestedFilings(ticker_or_cik=ticker,
                                 form_type="10-K",
                                 limit=latest - year + 1))[-1]

        self.link = metadata.primary_doc_url
        if year < 2001:
            important_bit = self.link.split('/')[-2]
            first_part = important_bit[:10]
            second_part = important_bit[10:12]
            third_part = important_bit[12:]
            file = f"{first_part}-{second_part}-{third_part}.txt"
            self.link += f"{file}"

        self.year = year


    def parse_10k_filing(self):
        
        def get_text(link, year):
            page = requests.get(link, headers={'User-Agent': 'Mozilla'})
            if year < 2001:
                html = bs(page.content, "html.parser")
            else:
                html = bs(page.content, "lxml")
            text = html.get_text()
            text = unicodedata.normalize("NFKD", text).encode('ascii', 'ignore').decode('utf8')
            text = text.split("\n")
            text = " ".join(text)
            return(text)
        
        def extract_text(text, item_start, item_end):
            item_start = item_start
            item_end = item_end
            starts = [i.start() for i in item_start.finditer(text)]
            ends = [i.start() for i in item_end.finditer(text)]
            positions = list()
            for s in starts:
                control = 0
                for e in ends:
                    if control == 0:
                        if s < e:
                            control = 1
                            positions.append([s,e])
            item_length = 0
            item_position = list()
            for p in positions:
                if (p[1]-p[0]) > item_length:
                    item_length = p[1]-p[0]
                    item_position = p

            item_text = text[item_position[0]:item_position[1]]

            return(item_text)

        text = get_text(self.link, self.year)

    
        try:
            item1_start = re.compile("item\s*[1][\.\;\:\-\_]*\s*\\b", re.IGNORECASE)
            item1_end = re.compile("item\s*1a[\.\;\:\-\_]\s*Risk|item\s*2[\.\,\;\:\-\_]\s*Prop", re.IGNORECASE)
            businessText = extract_text(text, item1_start, item1_end)
        except:
            businessText = "Something went wrong!"
        
        try:
            item1a_start = re.compile("(?<!,\s)item\s*1a[\.\;\:\-\_]\s*Risk|additional factors", re.IGNORECASE)
            item1a_end = re.compile("item\s*2[\.\;\:\-\_]\s*Prop|item\s*[1][\.\;\:\-\_]*\s*\\b", re.IGNORECASE)
            riskText = extract_text(text, item1a_start, item1a_end)
        except:
            riskText = "Something went wrong!"
            
        try:
            item7_start = re.compile("item\s*[7][\.\;\:\-\_]*\s*\\bM", re.IGNORECASE)
            item7_end = re.compile("item\s*7a[\.\;\:\-\_]\sQuanti|item\s*8[\.\,\;\:\-\_]\s*", re.IGNORECASE)
            mdaText = extract_text(text, item7_start, item7_end)
        except:
            mdaText = "Something went wrong!"

        data = {
                'business' : businessText,
                'risk' : riskText,
                'mda' : mdaText
                }

        return data


    def get_metadatas(ticker: str):
        dl = Downloader("XXX", "XXX")
        metadatas = dl.get_filing_metadatas(RequestedFilings(ticker_or_cik=ticker, form_type="10-K", limit=100))
        return metadatas


    def get_year_range(ticker: str):
        dl = Downloader("XXX", "XXX")
        metadatas = dl.get_filing_metadatas(RequestedFilings(ticker_or_cik=ticker, form_type="10-K", limit=100))
        return (int(metadatas[-1].filing_date[0:4]), int(metadatas[0].filing_date[0:4]))
