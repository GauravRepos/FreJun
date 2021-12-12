import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreJun.settings')
django.setup()
from API.models import Account, PhoneNumber




if __name__ == '__main__':
    with open("users_data.txt") as fh:
        for line in fh.read().split('\n'):
            vals = line.split()
            Account.objects.create(id = vals[0],auth_id=vals[1], username=vals[2])

def split_line(line, sep=" "):
    if sep!=None:
        return line.split()
    arr = []
    word = ''
    for i in line:
        if i.isnumeric():
            word+=i
        else:
            arr.append(word)
            word = ''
        
    if word!='':
        arr.append(word)
    return arr


with open("phone_data.txt") as fh:

    for line in fh.read().split("\n"):
        arr = split_line(line, None)
        try:
            
            account = Account.objects.filter(id = arr[2])[0]
            PhoneNumber.objects.create(id = arr[0],number=arr[1], account=account)
        except:
            print("FAILED")
            pass