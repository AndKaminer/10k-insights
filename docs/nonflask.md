# Non-Flask Items

## FilingRetriever class

### __init__(self, ticker: str, company_name: str, email: str, year: int)
Initializes FilingRetriever class. Will check if years are valid.

### parse_10k_filing(self)
Parses the 10k filing specified by the initialization of the object.
Is a common bottleneck, since it has to grab files from the sec servers.

### get_metadatas(ticker: str)
Gets all metadatas for given ticker in the sec_downloader format.
Since they are small files, typically not a bottleneck.

### get_year_range(ticker: str)
Returns a tuple with first element the earliest available year and last element the
latest available year.
