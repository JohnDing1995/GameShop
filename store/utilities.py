# Tools & Utilities
from hashlib import md5

#Seller id is plr,Secret Key: c12ccb024b3d72922f9b85575e76154d
def paymant(pid, amount, success_url, cancel_url, error_url):
    checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid,"plr",amount, "c12ccb024b3d72922f9b85575e76154d")
    m = md5(checksum_str.encode("ascii"))
    checksum = m.hexdigest()
    
