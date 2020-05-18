#valtyr

import argparse
import random
import json
import requests
import time
import base64
import binascii
import string
import re

import file_manipulator as fm
import perceptron

def print_title():
    lines=fm.read_file("titles/scipio_title.txt")
    for line in lines:
        print(line.strip('\n'))
    print("     <3 valtyr")
    return

def save_training_data(target,blob):
    #save server challenge and answer in a training file
    line=target+":"+blob+"\n"
    fm.write_file('data/scipio_training_data.txt',line,'a')

def parse_response(response):
    #retrieve target from json
    #decode blob from base64 into hex
    try:
        targets=response.json()['target']                                                   
        blob=(binascii.hexlify(base64.b64decode(response.json()['binary']))).decode('ascii')
    except:
        print("ERR: Json Parse Failed")
    return (targets, blob)

def start_session():
    return requests.session()

def request():
    #request challenge from server
    url = base_url.format("challenge")
    time.sleep(speed)
    try:
        response=session.get(url,headers=token)
        if response.status_code == 429:
            print('ERR: Rate Limit Exception: Waiting 60 seconds...')
            time.sleep(60)
            print("60 seconds elapsed...continuing...")
    except:
        print("ERR: Request Failed")
    return parse_response(response)

def solve(target):
    #send answer to server
    time.sleep(speed)
    url = base_url.format("solve")
    response=session.post(url,data={"target":target})
    return response

def save_weights():
    #loop through all perceptrons and save weights to file
    weights=[]
    for percep in perceptrons:
        weights.append(percep.label+":"+str(percep.weight)+'\n')
    fm.write_file('data/weights.txt',weights,'w+')
    return

def save_hash(line):
    fm.write_file('data/hashes.txt',line,'a')
    return

def ask_hash(email):
    #request challenge hash when count>=500
    #https://mlb.praetorian.com/hash
    url=base_url.format("hash")
    response=session.post(url, data={"email":email})
    save_hash(response.json())
    return

def get_user():
    #if no user file - create one using email - for user setup
    tmp=fm.read_file("data/user.txt")
    if tmp!=None:
        return tmp
    else:
        print("\nUser File Not Found: Please use aeneas to init a user file")
        exit(0)

def load_weights(file_name):
    #default location for data files
    data=fm.read_file('data/'+str(file_name))
    if data==None:
        #alt location
        data=fm.read_file(str(file_name))
    temp=[]
    for item in data:
        temp.append([float(x) for x in str(item.split(':')[1]).replace('\n','').replace('[','').replace(']','').split(', ')])

    i=0
    for perceptron in perceptrons:
        perceptron.weight=temp[i]
        i=i+1

    print("Weights loaded!")
    return

def get_training_data():
    file_name="data/scipio_training_data.txt"
    data=fm.read_file(file_name)
    data_clean=[]
    #vet data
    for line in data:
        data_clean.append(line.strip('\n').split(':'))
    return data_clean

def compute_frequency(blob,chunk):
    frequency=[]

    blob = re.findall(chunk, blob)

    for section in blob:
        i=0
        for letter in alphabet:
            frequency.append(section.count(letter))

        while i < 10:
            frequency.append(section.count(str(i)))
            i=i+1

    return frequency

def print_perceptrons():
    for perceptron in perceptrons:
        print("Node: "+perceptron.label+"\t\tweights: "+str(perceptron.weight))

def train():
    training_data=get_training_data()
    i=0
    while i < epochs:
        num_correct=0
        for line in training_data:
            count={}

            for percep in perceptrons:
                percep.input=compute_frequency(line[1],percep.chunk)
                percep.get_output()

            for percep in perceptrons:
                if percep.output==1:
                    if percep.label in count.keys():
                        count[percep.label]=count[percep.label]+1
                    else:
                        count[percep.label]=1

            try:
                guess=max(count,key=count.get)
            except:
                guess=None
                while guess==None:
                    for percep in perceptrons:
                        percep.adjust_weight(line[0])

                    for percep in perceptrons:
                        percep.input=compute_frequency(line[1],percep.chunk)
                        percep.get_output()

                    for percep in perceptrons:
                        if percep.output==1:
                            if percep.label in count.keys():
                                count[percep.label]=count[percep.label]+1
                            else:
                                count[percep.label]=1
                    try:
                        guess=max(count,key=count.get)
                    except:
                        guess=None

            if guess==line[0]:
                num_correct=num_correct+1

            for percep in perceptrons:
                percep.adjust_weight(line[0])
                percep.mod=random.choice([0,1])

        num_total=int(len(training_data))
        print("epoch: "+str(i+1)+"\tcorrect: "+str(num_correct)+"\ttotal: "+str(num_total)+"\taccuracy: "+str((num_correct/num_total)*100)+"%")
        i=i+1
        save_weights()
    return

def execute():
    counter=0
    streak=0
    time_start=time.time()
    while True:
        (targets, blob)=request()

        #set all outputs
        for percep in perceptrons:
            percep.input=compute_frequency(blob,percep.chunk)
            percep.get_output()

        count={}
        for percep in perceptrons:
            if percep.output==1 and targets.__contains__(percep.label):
                if percep.label in count.keys():
                    count[percep.label]=count[percep.label]+1
                else:
                    count[percep.label]=1

        try:
            guess=max(count,key=count.get)

            #if confidence low ie low fire rate .. raise and pull .. mess around with to create highest acc
            if int(count.get(guess)) <= confidence:
                print('low answer confidence...low fire['+str(int(count.get(guess)))+"]")
                raise('')

            print("Guess:\t"+guess)

            response=solve(guess)

            correct_resp=response.json()['correct']
            target=response.json()['target']
            accuracy=response.json()['accuracy']

            try:
                hash_resp=response.json()['hash']
                print("HASH COLLECTED!")
                time_stop=time.time()
                time_total=time_stop-time_start
                save_hash("Correct: "+str(correct_resp)+"\tAccuracy: "+str(accuracy)+"\tTotal Time: "+str(time_total)+"\nHash: "+hash_resp+"\n")
                ask_hash(email)
            except:
                hash_resp="None"

            print('Answer: '+target+'\tNumber: '+str(correct_resp)+"\tAccuracy: "+str(accuracy))

            if(target==guess):
                streak=streak+1
                print("streak: "+str(streak)+'\n')
            else:
                print('streak reset...\n')
                streak=0

            for percep in perceptrons:
                percep.adjust_weight(target)
                percep.mod=random.choice([0,1])

            counter=counter+1

            save_training_data(target,blob)

            #save weights every 10 cycles
            if counter % 10 == 0:
                print("Weights saved!")
                save_weights()

        except:
            #do nothing
            hello="world"
    return

##CLI##
#python3 scipio.py -alpha 0.000001  -epoch 5
#python3 scipio.py -alpha 0.00001 -time 0 -load weights.txt -conf 19

##GLOBAL VARS##
alpha=0.001       
threshold=0.5 
epochs=0  
speed=0
confidence=20
email=''
perceptrons=[]
session=start_session()
alphabet=string.ascii_lowercase[:6]
label=['avr', 'alphaev56', 'arm', 'm68k', 'mips', 'mipsel', 'powerpc', 's390', 'sh4', 'sparc', 'x86_64', 'xtensa']

base_url="https://mlb.praetorian.com/{}"

##PROGRAM START##
parser = argparse.ArgumentParser(description='Scipio Neural Net')
parser.add_argument('-a',action='store', dest='alpha',help='alpha perceptron learning rate | value b/w 0 and 1')
parser.add_argument('-thresh',action='store', dest='threshold',help='perceptron threshold value | default 0.5')
parser.add_argument('-e',action='store', dest='epochs',help='number of epochs to train > 0')
parser.add_argument('-l',action='store', dest='load',help='file name to load neural net weights')
parser.add_argument('-t',action='store', dest='speed',help='amount of time to pause between requesting and solving a challenge')
parser.add_argument('-c',action='store', dest='confidence',help='amount of confidence scipio needs to be sure of it\'s answer. default: 6')

args = parser.parse_args()

print_title()
[email,token]=get_user()
token = json.loads(token)
print("\nUSER DETAILS")
print("\tEmail:\t"+email.strip("\n"))
print("\tAuth:\t"+str(token['Authorization'])[:60]+"...")

print("\n~Neural Net Configuration~")
if(args.alpha==None):
    print("alpha:\t0.1\t[default]")
elif(float(args.alpha)<=0 or float(args.alpha)>1):
    print("alpha:\t0.1\t[default][invalid]")
elif(float(args.alpha)>0 or float(args.alpha)<1):
    print("alpha:\t"+str(args.alpha)+"\t[user]")
    alpha=float(args.alpha)
else:
    print("alpha:\t0.1\t[default][invalid]")

if(args.threshold==None):
    print("thresh:\t0.5\t[default]")
elif(float(args.threshold)<=0 or float(args.threshold)>1):
    print("thresh:\t0.5\t[default][invalid]")
elif(float(args.threshold)>0 or float(args.threshold)<1):
    print("thresh:\t"+str(args.threshold)+"\t[user]")
    threshold=float(args.threshold)
else:
    print("thresh:\t0.5\t[default][invalid]")

if(args.speed==None):
    speed=0.1
    print("time:\t"+str(speed)+"\t[default]")
else:
    speed=float(args.speed)
    print("time:\t"+str(speed)+"\t[user]")

if(args.epochs==None):
    print("epochs:\tnone\t[default]")
    training=False
else:
    epochs=int(args.epochs)
    print("epochs:\t"+str(epochs)+"\t[user]")
    training=True

if(args.confidence!=None):
    confidence=int(args.confidence)
    print('conf:\t'+str(confidence)+"\t[user]")
else:
    print('conf:\t'+str(confidence)+"\t[default]")

# if(input("continue? y/n: ")=='y'):
perceptron.init_percepts(perceptrons,alpha,label,threshold)

if(args.load!=None):
    load_weights(str(args.load))

if(training==True):
    train()
else:
    execute()

# else:
#     print('exiting scipio...')
    