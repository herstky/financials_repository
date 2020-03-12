import requests

def get_financial_statement(statement_type, symbols):
    base_url = 'https://financialmodelingprep.com/api/v3/financials/'
    statement_type_endpoint = statement_type + '/'

    full_endpoint = base_url + statement_type_endpoint + ','.join(symbols)
    try:
        res = requests.get(full_endpoint)
        if res.status_code != 200:
            print(f'Error code {res.status_code} occured during request for {statement_type} for symbols [{",".join(symbols)}]')
            return None
        if len(symbols) > 1:
            return res.json()['financialStatementList']
        else:
            return [res.json()]
    except KeyError as key_error:
        print(f'A key error occured while getting {statement_type} for symbols {",".join(symbols)}. key: {key_error}')
    except Exception as error:
        print(f'An error occured while getting {statement_type} for symbols {",".join(symbols)}: ')
        print(error)

    return None

i = 0
symbols = ['AAPL', 'TM', 'F', 'FB', 'GM', 'GOOG', 'ATVI', 'HAL', 'FIT', 'LULU', 'DIS', 'NFLX', 'TSLA', 'UA', 'SNAP', 'GE', 'BABA']

while i < len(symbols):
    batch = symbols[i:i+3]
    income_statement_list = get_financial_statement('income-statement', batch)
    balance_sheet_statement_list = get_financial_statement('balance-sheet-statement', batch)
    cash_flow_statement_list = get_financial_statement('cash-flow-statement', batch)
    print(len(income_statement_list))
    print(len(balance_sheet_statement_list))
    print(len(cash_flow_statement_list))
    i += 3

# financial_statement_list = get_financial_statement('income-statement', ['AAPL', 'TM', 'F'])