import operator
import sys
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

def findChain(temp,word,word2):#Checks if two words differ by a single character
    return [word1 for word1 in temp if(sum([word1[i] != word[i] for i in range(len(word1))]) == 1)]


container = []; #contains graphs of all 1,2,3,4 letter words and so on.
keep = []; #A container for holding the graph of a word of particular size
Explored = [];#Keeps track of all words that have been explored (i.e. were linked with another word) and thus will not be explored again (Their reference will be kept) 
fname = open("dictionary.json").read()
mydictionary = json.loads(fname)
keys = mydictionary.keys()
keys = sorted(keys, key=len); x = 2; #A temp variable for storing key length(starts from 2)
temp = by_size(keys,x);
temp_word = getMax_Successors(temp);
temp1 = getSuccessors(temp,temp_word);
#print temp1;
while temp:
    temp_word = getMax_Successors(temp);
    temp1 = getSuccessors(temp,temp_word);
    keep.append((temp_word,None,temp1,0,True));
    frontier = list(keep);#copying keep into frontier
    while(frontier):
        gs = frontier.pop();
        Explored.append(gs[0]);
        for word in gs[2]:
            if word not in Explored:
                i = (word,gs[0],getSuccessors(temp,word),gs[3]+1,True);
                frontier.append(i); keep.append(i);
            else:
                i = (word,gs[0],getSuccessors(temp,word),gs[3]+1,False);
                keep.append(i);
    temp2 = list(keep);
    container.append(temp2);
    print "Keep elements: ", len(container[x-2][0])
    del keep[:];del Explored[:];x+=1;
    temp = by_size(keys,x);
print "Container made!", len(container); 
