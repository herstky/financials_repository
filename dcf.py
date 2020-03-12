import requests

def get_dcf(symbols):
    base_url = 'https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/'
    batch = ','.join(symbols)
    full_endpoint = base_url + batch
    res = requests.get(full_endpoint)
    if len(symbols) > 1:
        return res.json()['DCFList']
    else:
        return [res.json()]

symbols = []
with open('data/companylist.csv') as infile:
    next(infile)
    for line in infile:
        data = line.split(',')
        symbols.append(data[0].strip('"'))

i = 0
while i < len(symbols):
    batch_size = 10
    batch = symbols[i:i+batch_size]
    dcf_models = get_dcf(batch)
    for model in dcf_models:
        if model['dcf'] != 'Infinity':
            ratio = model['Stock Price'] / model['dcf']
            if ratio < 0.5:
                print(f'{model["symbol"]} is significantly undervalued.')
                print(f'dcf: {round(model["dcf"], 2)}, current price: {round(model["Stock Price"], 2)}')
                print()
    i += batch_size
