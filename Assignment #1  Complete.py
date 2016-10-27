import operator
import sys
import copy
import csv
import json
import os.path

def by_size(words, size):#Returns all words that match a specific length
    return [word for word in words if len(word) == size]

def getSuccessors(temp,word):#Checks if two words differ by a single character
    return [word1 for word1 in temp if(sum([word[i] != word1[i] for i in range(len(word))]) == 1)]

def getMax_Successors(temp): #returns the word with the maximum number of successors
    temp1=[];
    for word in temp:
        temp1.append(len(getSuccessors(temp,word)));
    return temp[temp1.index(max(temp1))];

def Exists(temp ,word):#Check if a word exists in the specified dictionary
    for words in temp:
        if word in words[0]:
            return word;
    return False

        
def heuristic(word1,word2):#Heurisitic computes the hamming distance between words and decides if two words are closer, thus reducing computation time
    return sum (word1[i] != word2[i] for i in range(len(word1)) )

def recurse(temp,word1,word2):
    frontier=[];Explored = [];words = [];list1 =[]
    frontier.append(([word1],0));
    while frontier:
        gs = frontier.pop();
        Explored.append(gs[0][-1])
        #print gs[0]
        if gs[1] > 170:
            print "HI";
            break;
        if gs[0][-1] != word2:
           words = getSuccessors(temp,gs[0][-1]);
           for word in words:
               total = len(gs[0])+ heuristic(word,word2);
               temp1 = list(gs[0]); temp1.append(word);
               if word not in Explored:
                   frontier.append((temp1,total));
               else:
                    frontier = list(sorted(frontier,key=lambda x: x[1]))                                                
                    for x in frontier:
                        if word in x[0][-1] and (x[1]>total):
                            frontier.append((temp1,total));
                            break;
        else:
           return gs[0]        
        frontier = list(sorted(frontier,key=lambda x: x[1],reverse = True))
    return [];

def findChain(temp,word,word2):#The word ladder problem i.e. if a word can be made from another word
    sol = list(recurse(temp,word,word2));
    if not (recurse(temp,word,word2)):
        recurse(temp,word2,word);
    if sol:
        print "Solution is: ", sol;
    else:
        print "No solution!"; 

def countChains(dict1,length):#Increment each entry in a dictionary including the current length by one
    count = 2;
    if(length> 1):
        if length not in dict1:
            dict1.update({length:0});
        while count <= length :
            dict1[count] +=1;
            count+=1;
    return dict1;   

def notExplored(keys):#Increment each entry in a dictionary including the current length by one
    count = 2; temp = [];
    dict1 = by_size(keys,count);#Dict1 will now only contain those words of length = x;
    while dict1:
        for word in dict1:
            if not getSuccessors(dict1,word):
                temp.append(word);
        with open("NoChains"+str(count)+".csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerow(temp)
        del temp[:]; count+=1
        dict1 = by_size(keys,count);#Dict1 will now only contain those words of length = x;

def dictWriter(string,dict1):#Writes the dictionary into a csv file
    with open(string, "wb") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dict1.items():
           writer.writerow([key, value])     

def makeGraph(keys,temp):
    dict1={}
    keep = []; #A container for holding the graph of a word of particular size
    Explored = [];#Keeps track of all words that have been explored (i.e. were linked with another word) and thus will not be explored again (Their reference will be kept) 
    x = 2; #A variable for storing key length(starts from 2)
    while temp:#Makes graphs for words of all lengths (from 2-26);
        temp_word = getMax_Successors(temp);
        temp1 = getSuccessors(temp,temp_word);
        keep.append((temp_word,None,temp1,0,[temp_word],True));
        frontier = list(keep);#copying keep into frontier
        while(frontier):
            gs = frontier.pop();#The first element from the frontier is removed; its successors and chain lengths are computed
            if(gs[0] not in Explored):
                Explored.append(gs[0]);
            for word in gs[2]:
                count = 2;
                if word not in Explored:
                    tempC = list(gs[4]); #Keeps track of chains
                    dict1 = countChains(dict1,len(gs[4]))#Increment the number of chains produced
                    tempC.append(word);
                    i = (word,gs[0],getSuccessors(temp,word),gs[3]+1,tempC,True);
                    frontier.append(i); keep.append(i);
                else:
                    tempC = list(gs[4]); #Keeps track of chains
                    tempC.append(word);
                    i = (word,gs[0],getSuccessors(temp,word),gs[3]+1,tempC,False);
                    keep.append(i);
        print "Graph being made for word of length: ",x;
        with open("output"+str(x)+".csv", "wb") as f:#Writes entire graph onto a csv file.
                writer = csv.writer(f)
                writer.writerows(keep)
        dictWriter("LengthX"+str(x)+".csv",dict1)#Sends dictionary writer all lengths of words
        del keep[:];del Explored[:];x +=1
        temp = by_size(keys,x);#Temp will now only contain those words of length = x;



fname = open("dictionary.json").read()#Opening the file in read mode
mydictionary = json.loads(fname)
keys = mydictionary.keys()
keys = sorted(keys, key=len);
usr_input = "";

while(1):
    while (usr_input >= '1') or (usr_input <= '3'):
        usr_input = raw_input("Input choice:\n1)Draw graph of the word with most successors \n2)Find chain between two words of your choosing\n3)Find all words with no chains\n ")
        if usr_input == '1':
            temp = by_size(keys,2);#Temp will now only contain those words of length = x;
            makeGraph(keys,temp)
        elif usr_input == '2':
            var = raw_input("Please enter word#1: ").upper()
            var1 = raw_input("Please enter word#2: ").upper()
            if(len(var) == len(var1)):
                temp = by_size(keys,len(var));
                if var in temp and var1 in temp:
                    findChain(temp,var,var1);
                else:
                    print "Word\words not in dictionary!\n"
            else:
               print "Error! Lengths do not match!";
        elif usr_input == '3':
            notExplored(keys)#Will make a graph of all words that have no chain.
       

