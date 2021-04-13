import requests
import pandas as pd
import time




# max_per_page    = 50
# limit           = 150


def paginate(max_per_page, limit, url):

    # Use offset and max_per_page to paginate
    result_data     = []
    appended_data   = []
    get_data        = True
    api_call        = 1
    result_count    = 0
    offset          = 0

    while get_data == True: #and result_count <= limit:

        api_call+=1
        print(f"offset={offset}")

        querystring = {"order_direction":"desc","offset":offset, "limit":limit}

        # GET API response
        response = requests.request("GET", url, params=querystring)
        j = response.json()

        # create dataframe with one columns of json strings
        df = pd.DataFrame.from_dict(j)

        # split out json assets to columns
        results = pd.json_normalize(df.assets)

        print(f'Result preview from offset = {offset}')
        print(results.head())

        result_count = len(results)
        print(f"Records returned in API call {api_call}: ", result_count)

        if result_count == 0:
            get_data = False
        elif len(appended_data) < limit-max_per_page:
            #time.sleep(2)

            result_data.append(results)
            appended_data = pd.concat(result_data)
            print(f"Cumulative results have {len(appended_data)}")
            offset = offset + max_per_page
            print(f'Adding to result_data, offset set to {str(offset)}')
            get_data = True
        else:
            try:
                result_data.append(results)
                appended_data = pd.concat(result_data)
                print(f'Adding final data to result_data, cumulative results have {str(len(appended_data))} records. Setting get_data = False.')
            except:
                print(f'No Results to append! Setting get_data = False')

            get_data = False

    print(f"Iterations finished. Results have {len(appended_data)} records.")

    final_data = appended_data[[
        'id',
        'name',
        'description',
        'traits',
        'asset_contract.address',
        'asset_contract.asset_contract_type',
        'asset_contract.created_date',
        'asset_contract.name',
        'asset_contract.description',
        'collection.description',
        'collection.name',
        'last_sale.total_price',
        'last_sale.payment_token.symbol',
        'last_sale.event_timestamp',
        'last_sale.transaction.timestamp',
        'last_sale.transaction.to_account.user.username'
    ]]

    print(final_data.dtypes)
    #TODO: possibly format dates

    final_data.to_csv(f'opensea_asset_data_with_limit={limit}.csv', index=False)

    return appended_data


appended_data = paginate(max_per_page=50, limit=150, url = "https://api.opensea.io/api/v1/assets?asset_contract_address=0x79986af15539de2db9a5086382daeda917a9cf0c")