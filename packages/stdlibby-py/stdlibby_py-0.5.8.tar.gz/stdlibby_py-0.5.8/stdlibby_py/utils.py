import secrets
import math
from date_time import str_to_secs

def int_to_bool(i: int)->bool:
    if i == 0:
        return True
    else:
        return False

def old_gen_id(n: int=3):
    def a():
        choices = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        return "".join(list(map(lambda _: secrets.choice(choices), range(0, 5))))
    return "-".join(list(map(lambda _: a(), range(0, n))))

def gen_id(prefix: str, length: int=12):
    """
    Random generates an id with the particular prefix
    """
    if len(prefix) != 2:
        raise Exception("Prefixs must be 2 characters long")
    elif length <= 0:
        raise Exception("Length needs to be more then 0")

    choices = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
    id = "".join(list(map(lambda _: secrets.choice(choices), range(0, length))))
    return f"{prefix.lower()}:{id}"

def id_collision_calc(ids_per: int=1000, time_range: str="weekly", alphabet_size: int=32, id_len: int=12, collision_perc: int=1):
    """
    Algorithm taken from:
    https://github.com/alex7kom/nano-nanoid-cc/blob/master/src/util/calc.js
    """
    secs = str_to_secs(time_range)
    ids_per_sec = round((ids_per / secs), 6)
    nat_log2 = 0.6931471805599453
    # Bits per id
    bits = id_len * (math.log(alphabet_size) / nat_log2)
    # I don't know what this IS
    coll = math.sqrt(
        (2 * math.pow(2, bits))
        * math.log(1 / (1 - (collision_perc / 100))))
    ttc = math.floor((coll / ids_per_sec))
    ttc_hour = math.floor(ttc / 3600)
    ttc_days = math.floor(ttc / 86400)
    ttc_weeks = math.floor(ttc / (86400 * 7))
    ttc_years = math.floor(ttc / (86400 * 365.25))
    res = {"ids_per_second": ids_per_sec,
           "alphabet_size": alphabet_size,
           "id_length": id_len,
           "collision_percent": collision_perc,
           "collisions": coll,
           "seconds_to_collision_probability": ttc}
    return res

if __name__ == "__main__":
    import json
    p = id_collision_calc(time_range="weekly", ids_per=10000, alphabet_size=64)
    print(json.dumps(p, indent=4))
