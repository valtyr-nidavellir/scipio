#valtyr
#python 3.X

import requests
import sys
import json
import file_manipulator as fm

def print_title():
    lines=fm.read_file("titles/aeneas_title.txt")
    for line in lines:
        print(line.strip("\n"))
    print("\t\t\t\t\t\t\t<3 valtyr")
        
def get_token(user_email):
    try:
        url = base_url.format("api-token-auth/")
        response = requests.post(url, data={"email":user_email})
        token = {"Authorization":"JWT " + response.json()['token']}
        response.close()
        return token
    except:
        print("Token Retrieval Failed!")
        exit(1)

def get_user():
    tmp=fm.read_file("data/user.txt")
    if tmp!=None:
        return tmp
    else:
        print("User File Not Found: Creating One...")
        user_email=input('User Email: ')+"\n"
        print("Retrieving User Token...")
        token=json.dumps(get_token(user_email))
        print("Token Collected!")
        fm.write_file("data/user.txt",[user_email,token],'w')
        return [user_email,token]

def check_progress():
    tmp=fm.read_file("data/progress.txt")
    if tmp!=None:
        return tmp
    else:
        print("Progress File Not Found: Creating One...")
        fm.write_file("data/progress.txt", '', "w+")
        print("Progress File Created!")
        return []

def save_progress(last_output):
    fm.write_file("data/progress.txt",last_output+'\n','a')
    return

def get_hash():
    url = base_url.format("hash/")
    response = requests.get(url, headers=token)
    response.close()
    if response.status_code != 200:
        raise Exception(response.json()['detail'])
    high_level=response.json()["level"]
    high_hash=response.json()["hash"]
    return [high_hash,high_level]

def fetch(level,token):
    url = base_url.format("challenge/{}/".format(level))
    response = requests.get(url, headers=token)
    response.close()
    if response.status_code != 200:
        raise Exception(response.json()['detail'])
    return response.json()
 
def solve(level,guess,token):
    url = base_url.format("challenge/{}/".format(level))
    data = {"guess": guess}
    response = requests.post(url, headers=token, data=data)
    response.close()
    if response.status_code != 200:
        raise Exception(response.json()['detail'])
    return response.json()

##GLOBAL VARS##
base_url = "http://crypto.praetorian.com/{}"
last_output=""

print_title()

[email,token]=get_user()
token = json.loads(token)
print("USER DETAILS")
print("\tEmail:\t"+email.strip("\n"))
print("\nPROGRESS")
if (len(check_progress())==0):
    print("No Progress Found")
else:
    progress=check_progress()
    for line in progress:
        print("\t"+line.strip("\n"))

print("\n~type \"list\" for available commands~")

while(True):
    cmd=input('>')

    if(cmd=="list"):
        print("AVAILABLE COMMANDS")
        print("hash:\tsee latest hash")
        print("save:\tsave last terminal output to progress.txt")
        print("fetch:\tretrieve current challenge")
        print("solve:\tsubmit a guess for the current challenge")
        print("exit:\tumm exit")
    
    if(cmd=="hash"):
        data=get_hash()
        print("Highest Level:\t"+str(data[1]))
        print("Highest Hash:\t"+str(data[0]))
    if(cmd=="save"):
        save_progress(last_output)
        last_output=""
        print("Output Saved to progress.txt")
    if(cmd=="fetch"):
        level=input("Challenge Level: ")
        response=fetch(level,token)
        last_output=str(response)
        print("Praetorian: "+str(response))
    if(cmd=="solve"):
        level=input("Challenge Level: ")
        guess=input("Guess: ")
        response=solve(level,guess,token)
        last_output=str(response)
        print("Praetorian: "+str(response))
    if(cmd=="exit"):
        print("exiting aeneas...")
        break
        

