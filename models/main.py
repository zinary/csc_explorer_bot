from models.cet_balance import CETBalance
import json
bal = [{
  "code": 0,
  "data": {
    "address": {
      "address": "0x5Ad4D300FA795e9C2FE4221F0e64A983aCdBCaC9",
      "alias": "CoinEx_Hot",
      "type": 0
    },
    "balance": "44934753.6671727901983435"
  },
  "message": "OK"
}]


cet_bal = CETBalance.from_dict(bal["data"])
print(cet_bal)
