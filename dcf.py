import requests
import datetime

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

targets = []
threshhold = .5
time = datetime.datetime.now().strftime('%m-%d-%Y_%H%M')
i = 0
while i < len(symbols):
    batch_size = 10
    batch = symbols[i:i+batch_size]
    dcf_models = get_dcf(batch)
    for model in dcf_models:
        if type(model['dcf']) is not float:
            continue
        ratio = model['Stock Price'] / model['dcf']
        if ratio > threshhold:
            continue
        free_cash_flow_res = requests.get('https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/' + model['symbol'])
        free_cash_flow_statement = free_cash_flow_res.json()['financials'][0]
        free_cash_flow = float(free_cash_flow_statement['Free Cash Flow'])
        if fcf < 0:
            continue
        income_res = requests.get('https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/' + model['symbol'])
        income_statement = income_res.json()['financials'][0]
        net_income = float(income_statement['Net Income'])
        cash_income_ratio = free_cash_flow / net_income
        target_string = f'Symbol {model["symbol"]}, '
        target_string += f'Price: ${model['Stock Price']:.2f}, '
        target_string += f'DCF: ${model['dcf']:.2f}, '
        target_string += f'Value Ratio: {100 * model["Stock Price"] / model["dcf"]:.2f}%, '
        target_string += f'Net Income: ${net_income:,}, '
        target_string += f'Free Cash Flow: ${free_cash_flow:,}, '
        targets.append(target_string)
        print(target_string)
    i += batch_size

path = 'data/' + time + '_Threshhold=' + str(threshhold) + '.txt'
with open(path, 'w') as outfile:
    for target in targets:
        outfile.write(target + '\n')
