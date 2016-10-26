import operator
import sys
import csv
import json

def by_size(words, size):#Returns all words that match a specific length
    return [word for word in words if len(word) == size]

def getSuccessors(temp,word):#Checks if two words differ by a single character
    return [word1 for word1 in temp if(sum([word1[i] != word[i] for i in range(len(word1))]) == 1)]

def getMax_Successors(temp): #returns the word with the maximum number of successors
    temp1=[];
    for word in temp:
        temp1.append(len(getSuccessors(temp,word)));
    return temp[temp1.index(max(temp1))];

def Exists(temp ,word):
    for words in temp:
        if word in words[0]:
            print "hi";
            return word;
    return False
        
def recurse(temp,word1,word2,depth):
    sol = []
    print depth;
    for word in temp:
        if (not sol and depth == 0) or len(word[4])<depth:
            if word1 in word[4]:
                if word2 in word[4]:
                    sol=list(word[4]);
                    print sol," ",sol.index(word1)," ",sol.index(word2)
                    if(sol.index(word1)< sol.index(word2)):
                        temp = list(sol[sol.index(word1):sol.index(word2)+1])
                    else:
                        temp = list(sol[sol.index(word2):sol.index(word1)+1])
                    depth=len(sol)
                    sol = list(temp)
                    del temp[:]
                else:
                    if word[5]== False:
                        temp = list(sol[sol.index(word1):sol.index(word[4][-1])+1])
                        if depth > len(temp):
                            temp = temp + recurse(temp,word[4][-1],word2,(depth-);
                            if word1 in temp and word2 in temp and len(temp)<len(sol):
                                sol=list(temp);
                                                  
    return sol;
def findChain(temp,word,word2):#The word ladder problem i.e. if a word can be made from another word
    sol = [];
    print word,word2
    if Exists(temp,word) and Exists(temp,word2):
            sol = list(recurse(temp,word,word2,1000));
    

container = []; #contains graphs of all 1,2,3,4 letter words and so on.
keep = []; #A container for holding the graph of a word of particular size
Explored = [];#Keeps track of all words that have been explored (i.e. were linked with another word) and thus will not be explored again (Their reference will be kept) 
x = 2; #A variable for storing key length(starts from 2)
fname = open("dictionary.json").read()
mydictionary = json.loads(fname)
keys = mydictionary.keys()
keys = sorted(keys, key=len); 
temp = by_size(keys,x);
temp_word = getMax_Successors(temp);
temp1 = getSuccessors(temp,temp_word);
#print temp1;
while temp:
    temp_word = getMax_Successors(temp);
    temp1 = getSuccessors(temp,temp_word);
    keep.append((temp_word,None,temp1,0,[temp_word],True));
    frontier = list(keep);#copying keep into frontier
    while(frontier):
        gs = frontier.pop();
        Explored.append(gs[0]);
        for word in gs[2]:
            if word not in Explored:
                tempC = list(gs[4]); #Keeps track of chains
                tempC.append(word);
                i = (word,gs[0],getSuccessors(temp,word),gs[3]+1,tempC,True);
                frontier.append(i); keep.append(i);
            else:
                tempC = list(gs[4]); #Keeps track of chains
                tempC.append(word);
                i = (word,gs[0],getSuccessors(temp,word),gs[3]+1,tempC,False);
                keep.append(i);
    with open("Explored"+str(x)+".csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(Explored) 
##    with open("output"+str(x)+".csv", "wb") as f:
##        writer = csv.writer(f)
##        writer.writerows(keep)
    #findChain(keep,"FAR","LAP");
    #container.append(temp2);
    #print "Keep elements: ", len(container[x-2][0])
    del keep[:];del Explored[:];x+=1;
    temp = by_size(keys,x);
#print "Container made!", len(container); 
