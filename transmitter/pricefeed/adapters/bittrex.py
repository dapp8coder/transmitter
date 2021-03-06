from .base import BaseAdapter
import requests


class BittrexAdapter(BaseAdapter):

    BASE_URL = "https://bittrex.com/api/v1.1/public/getticker"

    def get_price(self):
        btc_steem_response = requests.get(
            self.BASE_URL, params={"market": "BTC-HIVE"})
        btc_steem_response_json = self.validate_response(btc_steem_response)

        usd_btc_response = requests.get(
            self.BASE_URL, params={"market": "USD-BTC"}
        )
        usd_btc_response_json = self.validate_response(usd_btc_response)

        if btc_steem_response_json and usd_btc_response_json:
            btc_steem_pair = btc_steem_response_json["result"]["Last"]
            usd_btc_pair = usd_btc_response_json["result"]["Last"]

            price = round(usd_btc_pair * btc_steem_pair, self.PRICE_PRECISION)
            self.logger.info(self.bundle_adapter_name(f'Price: {price}'))
            return price
