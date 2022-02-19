import requests
import constants
from models.api_response import APIResponse

STATISTICS_CET = "statistics/cet"
STATISTICS_CHAIN = "statistics/chain"
TOKENS = "tokens?sort=desc&order=tx_count"
TOKEN = "tokens/{}"
ADDRESS_BALANCE = "addresses/{}/balance"
STATISTICS_CET_HOLDERS = "statistics/cet/holders"
TRANSACTIONS = "transactions?starttime={}&endtime={}"
TRANSACTION = "transactions/{}"
ADDRESS_TOKENS_BALANCE = "addresses/{}/tokens"

TEST_NET_URL = "http://testnet.coinex.net/api/v1/"
MAIN_NET_URL = "http://www.coinex.net/api/v1/"

base_url = MAIN_NET_URL


def api_request(end_point):
    url = base_url + end_point
    print("REQUEST URL =>" + url)
    res = requests.get(url=url, headers={"apikey": constants.CSC_API_KEY_PROD})
    if res.status_code == 200:
        response = APIResponse.from_dict(res.json())
        return response
    else:
        return APIResponse(code=69, data={}, message="Bot is having trouble")


if __name__ == "__main__":
    pass
