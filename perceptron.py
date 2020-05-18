#valtyr

import random

class perceptron():
    def __init__(self):
        self.input=[]               #raw input
        self.output=0               #0 or 1
        self.alpha=0                #learning rate
        self.label=""               #perceptron label
        self.weight=[]              #individual channels for a-f 0-9 frequencies       
        self.chunk=''
        self.threshold=0.5

    def adjust_weight(self,correct):
        #custom weight adjustment algorithm adding small random mutation
        if self.label==correct:
            correct=1
        else:
            correct=0
        i=0
        for item in self.weight:
            self.weight[i]=item+(self.alpha*(correct-self.output)*self.input[i]) + (random.uniform(0,0.00001)*(correct-self.output))
            i=i+1

    def get_output(self):
        #mult weights and input then sum all
        i=0
        summation=[]

        for item in self.input:
            summation.append(int(item)*self.weight[i])
            i=i+1
        summation=sum(summation)

        #fire if over threshold 
        if summation < self.threshold:
            self.output=0
        else:
            self.output=1
        return

def init_percepts(perceptrons,alpha,label,threshold):
    #init perceptron groups into various input chunk sizes
    #multiple parallel groups are used to create a neural net consensus
    #combined with random mutation - creates more reliable network output
    #32 chunk
    j=0
    while j < 2:
        i=0
        while i != 12:
            tmp=perceptron()
            tmp.label=label[i]
            tmp.alpha=alpha
            tmp.threshold=threshold
            tmp.chunk='................................................................'
            tmp.weight=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
            perceptrons.append(tmp)
            i=i+1
        j=j+1

    #16 chunk
    j=0
    while j < 10:
        i=0
        while i != 12:
            tmp=perceptron()
            tmp.label=label[i]
            tmp.alpha=alpha
            tmp.threshold=threshold
            tmp.chunk='................'
            tmp.weight=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
            perceptrons.append(tmp)
            i=i+1 
        j=j+1

    #8 chunk
    j=0
    while j < 9:
        i=0
        while i != 12:
            tmp=perceptron()
            tmp.label=label[i]
            tmp.alpha=alpha
            tmp.threshold=threshold
            tmp.chunk='........'
            tmp.weight=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,
                        0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
            perceptrons.append(tmp)
            i=i+1
        j=j+1
 
    print("Total Nodes: "+str(len(perceptrons))+"\nParallel Net Groups: "+str(int(len(perceptrons)/12)))
    return 