import operator,os,pickle
from phonetics import metaphone
from Dictionary import Dictionary
#look at: http://www.korokithakis.net/node/87 (useful page talking about levenshtein distance... and has a link to http://norvig.com/spell-correct.html, very useful)
#for a better, in-context algorithm: http://l2r.cs.uiuc.edu/~danr/Papers/Abstracts/spellJ.html

class Spelling:
    def __init__(self):
        self.alphabet='abcdefghijklmnopqrstuvwxyz'
        self.guten="data/gutenburg_small.txt"
        self.guten_pickle="data/gutenburg_small.pickle"
        #self.american="words/american-english"
        self.gutenburg={}
        self.learned={}
        self.dictionary=Dictionary("usa")
        self.stopwords=Dictionary("stopwords")
        
        #self.Load_dictionary()
        self.Load_gutenburg()
        self.Load_learned()
    
    def Load_gutenburg(self):
        with open(self.guten,encoding='utf-8') as dictionary_file:
            for line in dictionary_file:
                words=line.strip().split(" ")
                length=len(words)
                
                if length == 2:
                    self.gutenburg[words[1]]=words[0]
    
    #def Load_dictionary(self):
    #    with open('words/american-english', encoding='utf-8') as dictionary_file:
    #        for line in dictionary_file:
    #            word=line.strip()
    #            length=len(word)
    #            
    #            if length > 1:
    #                self.dictionary.append(word)
    
    def Load_learned(self):
        """
        Load the metaphone array, and if it doesn't exist, create it.
        """
        if len(self.learned) == 0:
            if os.path.exists(self.guten_pickle):
                with open(self.guten_pickle, 'rb') as infile:
                    self.learned=pickle.load(infile)
            else:
                if len(self.gutenburg) == 0:
                    self.Load_dict()
                
                for word,times in self.gutenburg.items():
                    meta=metaphone(word.replace("'",""))
                    
                    #add and up the frequency of the words
                    if meta not in self.learned:
                        self.learned[meta]={word:int(times)}
                    elif word not in self.learned[meta]:
                        self.learned[meta][word]=int(times)
                        
                if len(self.learned) > 0:
                    with open(self.guten_pickle, 'wb') as outfile:
                            pickle.dump(self.learned, outfile)
    
    def slight_edits(self,word):
        """
        Find all edits within one character of the word.
        """
        splits=[(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes=[a + b[1:] for a, b in splits if b]
        transposes=[a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces=[a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts=[a + c + b for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)
    
    def letters_off(self,word):
        """
        Find all edits within two characters of the word.
        """
        return set(e2 for e1 in self.slight_edits(word) for e2 in self.slight_edits(e1))
        
    def known_guten(self,words):
        """
        Determine if the word is in the gutenburg dictionary file.
        """
        return set(w for w in words if w in self.gutenburg and int(self.gutenburg[w]) > 100)
        
    def known_usa(self,words):
        """
        Determine if the word is in the USA dictionary file.
        """
        return set(w for w in words if self.dictionary.Contains(w) == True)
    
    def highest_likely(self,words):
        """
        Find the word out of 'words' with the highest frequency in the 'self.gutenburg' array Used in max_look_like and Check
        """
        values={}
        likely=[]
        
        #get the frequency of the word
        for i in words:
            if i in self.gutenburg:
                values[i]=int(self.gutenburg.get(i))
        
        #sort by the frequency
        sort=sorted(values.items(),key=operator.itemgetter(1),reverse=1)
        
        #create an array of the sorted words
        for value in sort:
            if len(value) == 2:
                likely.append(value[0])
        
        #return the array
        if len(likely) > 0:
            return likely
        else:
            return False
    
    def max_look_like(self,word,fast=False):
        """
        Find all the words that are likely to be mistakes from when the user knows how to spell it but accidently types it in wrong.
        """
        if fast==True:
            words=self.known_usa([word]) or self.known_usa(self.slight_edits(word)) or self.known_usa(self.letters_off(word)) or [word]
        else:
            words=self.known_usa([word]) or self.known_usa(self.slight_edits(word)) or self.known_usa(self.letters_off(word)) or self.known_guten(self.slight_edits(word)) or self.known_guten(self.letters_off(word)) or [word]
        
        return self.highest_likely(words)
            
    def max_sound_like(self,word):
        """
        Find all the words that are likely to be mistakes from the user not knowing how to spell it but knowing how it sounds.
        """
        meta=metaphone(word)
        rewords=[]
        
        if meta in self.learned:
            words=sorted(self.learned[meta].items(),key=operator.itemgetter(1),reverse=1)
            
            if word not in [i[0] for i in words]:
                if len(words) == 1:
                    rewords.append(words[0][0])
                else:
                    rewords+=[i[0] for i in words]
        
        if len(rewords) > 0:
            return rewords
        else:
            return False
        
    def Check(self,word,dictionary=False,fast=False):
        """
        Figure out what the user probably is looking for.
        
        word - the word to check if it is spelled correctly, and if it isn't, return the correct word
        dictionary - if True, return a dictionary or list of possible corrections
        """
        result=""
        
        if len(word) > 0:
            look=self.max_look_like(word.lower(),fast=fast)
            sound=self.max_sound_like(word)
            
            #if one of them is the only option, return the first one
            if look == False and sound == False:
                if dictionary==True:
                    result={}
                else:
                    result=""
            elif look == False:
                if dictionary==True:
                    result=sound
                else:
                    result=sound[0]
            elif sound == False:
                if dictionary==True:
                    result=look
                else:
                    result=look[0]
            #if both have options, find the words in both or find the highest_likely out of all the combined ones
            else:
                #see if the same word is in both lists
                likely=[]
                intersection=set(look)&set(sound)
                
                if len(intersection) > 0:
                    likely=self.highest_likely(intersection)
                else:
                    likely=self.highest_likely(look+[ent for key,ent in enumerate(sound) if key < 10 and self.dictionary.Contains(ent) == True and self.stopwords.Contains(ent) == False])
                
                #if there is a likely word, return that word, otherwise let result = "", thus returning False
                if dictionary == True:
                    result=likely
                else:
                    if len(likely) > 0:
                        result=likely[0]
                
        if result == "" or result == {}:
            return False
        else:
            return result
        
    def Frequency(self,word):
        result=0
        length=len(self.gutenburg)
        
        if word in self.gutenburg and length > 0:
            result=int(self.gutenburg.get(word))/length
        
        return result
        
if __name__ == '__main__':
    s=Spelling()
    print(s.Check("thrue"))
    print(s.Check("williage"))
    print(s.Check("weedend"))
    #works: print(s.Check("through"))
    #works: print(s.Check("qwickly"))
