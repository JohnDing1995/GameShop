# Tools & Utilities
from hashlib import md5
import requests

#Seller id is plr,Secret Key: c12ccb024b3d72922f9b85575e76154d
from store.models import Purchase


def pay(game, user, pid, amount):
    checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid,"plr",amount, "c12ccb024b3d72922f9b85575e76154d")
    m = md5(checksum_str.encode("ascii"))
    checksum = m.hexdigest()
    r = requests.post('http://payments.webcourse.niksula.hut.fi/pay/',data={'pid':pid, 'token':'c12ccb024b3d72922f9b85575e76154d', 'amount':amount, 'sid':'plr'})
    result = requests.codes.ok
    p = Purchase(game=game, user=user, pid=pid, amount=amount, checksum=checksum, result=result)
    p.save()

