import os,operator,pickle
from DoubleMetaphone import metaphone

class GutenBooks:
    def __init__(self):
        self.learned={}
        self.load_location="words/gutenberg.txt"
        self.save_location="words/gutenberg.pickle"
        self.Learn()
        
    def Learn(self):
        #verify the variable hasn't already been set        
        if len(self.learned) == 0:
            
            #load from disk
            if os.path.exists(self.save_location):
                with open(self.save_location, 'rb') as infile:
                    self.learned=pickle.load(infile)
            
            #if it isn't on disk, make it and then save it to disk
            else:
                with open(self.load_location) as infile:
                    for i,line in enumerate(infile):
                        word=line.strip()
                        meta=metaphone(word)
                        
                        #add and up the frequency of the words
                        if meta not in self.learned:
                            self.learned[meta]={word:1}
                        elif word not in self.learned[meta]:
                            self.learned[meta][word]=1
                        else:
                            self.learned[meta][word]+=1
                        
                        #for debugging... print the percentage done
                        if i%1000000 == 0:
                            print(round(i/51478714*100),"%")
                    
                self.Save()
    
    def Save(self):
        if len(self.learned) > 0:
            with open(self.save_location, 'wb') as outfile:
                    pickle.dump(self.learned, outfile)

    def DidYouMean(self,word):
        """
        Find words that sound like the given word. Idea taken from: http://www.biais.org/blog/index.php/2007/01/31/25-spelling-correction-using-the-python-natural-language-toolkit-nltk
        Another idea: http://norvig.com/spell-correct.html
        """
        meta=metaphone(word)
        rewords=[]
        
        if meta in self.learned:
            words=sorted(self.learned[meta].items(),key=operator.itemgetter(1),reverse=1)
            
            if word in [i[0] for i in words]:
                pass
            else:
                if len(words) == 1:
                    rewords.append(words[0][0])
                else:
                    rewords+=[i[0] for i in words]
            
        return rewords
    
    def Number(self,word):
        """
        Determine the number of times a word is in the dictionary.
        """
        number=0
        meta=metaphone(word)
        
        if meta in self.learned and word in self.learned[meta]:
            number=self.learned[meta][word]
        
        return number

    def Frequency(self,word):
        """
        Determine the percentage of this word out of all the words in the dictionary.
        """
        frequency=0
        length=len(self.learned)
        
        if length > 0:
            frequency=self.Number(word)/len(self.learned)                                
        
        return frequency

if __name__ == '__main__':
    g=GutenBooks()
    
    #for word in ["birdd","oklaoma","emphasise","bird","carot","garrett","bufalo","dictinary","oparatur","linux"]:
    #    print(word,"-",str([i for l,i in enumerate(g.DidYouMean(word)) if l < 1]))
    print(g.DidYouMean("thrue"))
    print(g.DidYouMean("through"))
    print(g.DidYouMean("qwickly"))
