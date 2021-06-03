import random
import string
def gen_id(lis):
    #[(1, 'srijon', 'srihome18', 'Srijon Kumar', 'srijonkumar18@gmail.com', 10, 'srijonkumar')]
    key=[]
    for i in lis:
        key.append(i[5])
    i=0
    while True:
        x=random.randint(100000000,999999999)
        if x in key:
            pass
        else:
            i=x
            break
    return i

def gen_key(lis):
    key=[]
    for i in lis:
        key.append(i[6])
    i=0
    while True:
        x = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
        if x in key:
            pass
        else:
            i=x
            break
    return i
 
def verify(users,username,mail):
    mail=[]
    name=[]
    for i in users:
        mail.append(i[4])
        name.append(i[1])
    if username in name or mail in mail:
        return False
    else:
        return True
        
