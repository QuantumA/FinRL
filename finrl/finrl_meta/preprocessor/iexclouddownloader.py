"""Contains methods and classes to collect data from
IEX Cloud API. Please, refer to https://iexcloud.io/docs/api/ for extending functionality.
"""

import pandas as pd
import os
import requests


class IEXCloudDownloader:

    @classmethod
    def _get_base_url(self, mode: str) -> str:

        as1 = 'mode must be sandbox or production.'
        assert mode in ['sandbox', 'production'], as1

        if mode == 'sandbox':
            return 'https://sandbox.iexapis.com'
        
        return 'https://cloud.iexapis.com'


    def __init__(self, token: str, mode : str) -> None:
        self.token = token or os.environ.get("IEX_TOKEN")
        self.base_url = self._get_base_url(mode)

    
    def ohlcv_chart(self, ticker: list, range: str = 'max') -> pd.DataFrame:
        
        price_data = pd.DataFrame()
        #price_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        for stock in ticker:
            end_point = f'{self.base_url}/stable/stock/{stock}/chart/{range}'
            
            response = requests.get(url=end_point,
            params={
                'token': self.token,
                'chartCloseOnly': False,
            },)
            if response.status_code == 200:
                temp = pd.DataFrame.from_dict(data=response.json())
                price_data= price_data.append(temp)

            else:
                print(response.text)

        print(price_data)
    



if __name__ == '__main__':

    iex_dloader = IEXCloudDownloader(token='Tsk_d716e2f44bdd4638aa77a99fb2da883e', mode='sandbox')
    iex_dloader.ohlcv_chart(["AAPL", "NVDA"], '5y')


