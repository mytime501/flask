import pandas as pd

def save(userid, userpw, userpwc, username, usernumb, playd):
    idx = len(pd.read_csv("database.csv"))
    new_df = pd.DataFrame({"userid":userid,
                           "userpw":userpw,
                           "userpwc":userpwc,
                           "username":username,
                           "usernumb":usernumb,
                           "playd":playd}, 
                         index = [idx])
    new_df.to_csv("database.csv",mode = "a", header = False)
    return None
