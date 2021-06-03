def authenticate(lis,cid,key):
    for i in lis:
        if str(cid)==str(i[5]) and str(key)==str(i[6]):
            return True

    return False
