import random,copy,operator
from multiprocessing import Process,Pipe
from Dictionary import Dictionary
from Spelling import Spelling
#from GutenBooks import GutenBooks

#thread info: http://jessenoller.com/2009/02/01/python-threads-and-the-global-interpreter-lock/

#def synchronized():
#    the_lock = Lock()
#    def fwrap(function):
#        def newFunction(*args, **kw):
#            with the_lock:
#                return function(*args, **kw)
#        return newFunction
#    return fwrap

class LeetSpeak:
    def __init__(self,processes=1):
        #number of threads
        if processes > 0:
            self.processes=processes
        else:
            self.processes=1
        #load word frequency and spell checker
        self.spelling=Spelling()
        #load the dictionaries
        self.jargon = Dictionary("slang")
        self.dictionary = self.spelling.dictionary
        self.stopwords = self.spelling.stopwords
        
        self.a=["a","4","@","/-\\","/\\","/_\\","^","aye","ci","λ","∂","//-\\\\","/=\\","ae"]
        self.b=["b","8","|3","6","13","l3","]3","|o","1o","lo","ß","]]3","|8","l8","18","]8"]
        self.c=["c","(","<","[","{","sea","see","k","©","¢","€"]
        self.d=["d","|]","l]","1]","|)","l)","1)","[)","|}","l]","1}","])","i>","|>","l>","1>","0","cl","o|","o1","ol","Ð","∂","ð"]
        self.e=["e","3","&","[-","€","ii","ə","£","iii"]
        self.f=["f","|=","]=","}","ph","(=","[=","ʃ","eph","ph"]
        self.g=["g","6","9","&","(_+","C-","gee","jee","(Y,","cj","[","-","(γ,","(_-"]
        self.h=["h","|-|","#","[-]","{-}","]-[",")-(","(-)",":-:","}{","}-{","aych","╫","]]-[[","aech"]
        self.i=["!","1","|","l","eye","3y3","ai","i"]
        self.j=["j","_|","_/","]","</","_)","_l","_1","¿","ʝ","ul","u1","u|","jay","(/","_]"]
        self.k=["k","x","|<","|x","|{","/<","\\<","/x","\\x","ɮ","kay"]
        self.l=["l","1","7","|_","1_","l_","lJ","£","¬","el"]
        self.m=["m","/\/\\","|\\/|","em","|v|","[v]","^^","nn","//\\\\//\\\\","(V)","(\/)","/|\\","/|/|",".\\\\","/^^\\","/V\\","|^^|","JVL","][\\\\//][","[]\/[]","[]v[]","(t)"]
        self.n=["n","|\\|","/\\/","//\\\\//","[\\]","<\\>","{\\}","//","[]\\[]","]\\[","~","₪","/|/","in"]
        #the ω is because Ω is mistakenly taken as that character sometimes...
        self.o=["o","0","()","oh","[]","{}","¤","Ω","ω","*","[[]]","oh"]
        self.p=["p","|*","l*","1*","|o","lo","1o","|>","l>","1>","|\"","l\"","1\"","?","9","[]d","|7","l7","17","q","|d","ld","1d","℗","|º","1º","lº","þ","¶","pee"]
        self.q=["q","0_","o_","0,","o,","(,)","[,]","<|","<l","<1","cue","9","¶","kew"]
        self.r=["r","|2","l2","12","2","/2","I2","|^","l^","1^","|~","l~","1~","lz","[z","|`","l`","1`",".-","®","Я","ʁ","|?","l?","1?","arr"]
        self.s=["s","5","$","z","es","2","§","š",",,\\``"]
        self.t=["t","7","+","-|-","-l-","-1-","1","']['","†"]
        self.u=["u","|_|","l_l","1_1","(_)","[_]","{_}","y3w","m","\\_/","\\_\\","/_/","µ","yew","yoo","yuu"]
        self.v=["v","\\/","\\\\//","√"]
        self.w=["w","\\/\\/","vv","'//","\\\\'","\\^/","(n)","\\x/","\\|/","\\_|_/","\\_l_/","\\_1_/","\\//\\//","\\_:_/","]i[","uu","Ш","ɰ","1/\\/","\\/1/","1/1/"]
        self.x=["x","%","><","><,","}{","ecks","x","*",")(","ex","Ж","×"]
        self.y=["y","j","`/","`(","-/","'/","\\-/","Ψ","φ","λ","Ч","¥","``//","\\j","wai"]
        self.z=["z","2","~/_","%","7_","ʒ","≥","`/_"]
        self.zero=["0","o","zero","cero","()"]
        self.one=["1","won","one","l","|","]["]
        self.two=["two","to","too","2","z"]
        self.three=["e","3","three"]
        self.four=["4","four","for","fore","a"]
        self.five=["5","five","s"]
        self.six=["6","six","g"]
        self.seven=["7","seven","t","l"]
        self.eight=["8","eight","b"]
        self.nine=["9","nine","g"]
        
        #"0":self.zero,"1":self.one,"2":self.two,"3":self.three,"4":self.four,"5":self.five,"6":self.six,"7":self.seven,"8":self.eight,"9":self.nine
        self.alphabet={"a":self.a, "b":self.b, "c":self.c, "d":self.d, "e":self.e, "f":self.f, "g":self.g, "h":self.h, "i":self.i, "j":self.j, "k":self.k, "l":self.l, "m":self.m, "n":self.n, "o":self.o, "p":self.p, "q":self.q, "r":self.r, "s":self.s, "t":self.t, "u":self.u, "v":self.v, "w":self.w, "x":self.x, "y":self.y, "z":self.z}

    def ConvertToLeet(self,text):
        """
        This is fairly straightforward. Randomly select letters from the array of letters and output it.
        """
        leet=""
        
        for letter in list(text):
            if letter.isalpha() and self.alphabet[letter.lower()]:
                values=self.alphabet[letter.lower()]
                random.seed()
                number=random.randint(1,len(values))
                leet+=values[number-1]
            else:
                leet+=letter
        
        return leet

    def rec_parse(self,text,previous=[]):
        """
        Input: 
        Output: 
        """
        possibilities=[]
        text_length=len(list(text))
        
        if text_length > 7:
            length=8
        else:
            length=text_length
        
        for q in range(1,length):
            if q < len(text):
                possibilities.append(previous+[text[0:q],text[q:text_length]])
                possibilities+=self.rec_parse(text[q:text_length],previous+[text[0:q]])
        
        return possibilities

    def rec_scan_array(self,array,previous=[]):
        """
        Input: [['h'], ['e'], ['i', 'l', 't'], ['i', 'l', 't'], ['d', 'o']]
        Output:
         ['h','e','i','i','d'],
         ['h','e','i','i','o'],
         ['h','e','i','1','d'],
         ['h','e','i','1','o'],
         ...
        """
        
        words=[]
        
        passon=copy.copy(array)
        passon.pop(0)
        
        if len(array) > 0:
            for let in array[0]:
                letters=copy.copy(previous)
                letters.append(let)
                
                if len(passon) > 0:
                    words+=self.rec_scan_array(passon,letters)
                if len(array) == 1:
                    words.append("".join(letters))
                
                del letters

        del passon

        return words

    def ConvertFromLeet(self,text):
        """
        Convert leet to readable English text. Find all possible words, check which are English, check for misspellings, etc.
        
        Uses self.processes, so when creating the LeetSpeak() object, you can specify the number of threads to use: l=LeetSpeak(threads=3)
        """
        #figure out how many words each thread should work on
        split=text.split(" ")
        thread_count={}
        thread_words={}
        thread_num=1
        
        for word in split:
            #add word to the array for the current thread
            if thread_num in thread_count:
                thread_count[thread_num]+=1
            else:
                thread_count[thread_num]=1
                thread_words[thread_num]=[]
            
            #up the thread_num unless it is currently at the number of threads we want, then set it to 1 to start over again
            if self.processes > thread_num:
                thread_num+=1
            else:
                thread_num=1
        
        #compute what words each thread should decode
        for num,word in enumerate(split):
            for thread,words in thread_words.items():
                if len(words) < thread_count[thread]:
                    thread_words[thread].append(word)
                    break
        
        #INFORMATION:
        #if self.processes = 3 and text = "cows are cool or not", thread_words={1: ['cows', 'are'], 2: ['cool', 'or'], 3: ['not']}
        
        #create the processes
        threads={}
        num_threads=len(thread_words)
        result_english=""
        thread_results={}
        receive_pipe,send_pipe=Pipe()
        
        for i in range(self.processes):
            if num_threads >= i+1:
                threads[i]=Process(target=self.ConvertFromLeet_thread,args=(thread_words[i+1],i,send_pipe))
                threads[i].start()
        
        #start and wait for threads
        for i in range(self.processes):
            if num_threads >= i+1:
                threads[i].join()
                result=receive_pipe.recv()
                thread_results[result[0]]=result[1]
        
        #close the pipe
        send_pipe.close()
        
        #sort the results
        thread_results=sorted(thread_results.items())
        
        #make a string out of the results
        for thread,string in thread_results:
            result_english+=string+" "
        
        return result_english.strip()
    
    def ConvertFromLeet_thread(self,text,thread_id,pipe):
        """
        The function that ConvertFromLeet() calls for each thread.
        """
        english=[]
        
        #convert each word
        for word in text:
            #get all the character locations less than 8 (e.g. "c,ow", "co,w", and "cow" for "cow")
            #this uses some recursive substringing
            possibilities=self.rec_parse(word.lower())
            
            #append the actual "word" if it is less than 8 characters, since it might be a single letter (e.g. "n" for "and")
            if len(word) <= 8:
                possibilities.append([word.lower()])
            
            #calculate what this could be in leet (if it can be anything)
            validwords=[]
            for possibility in possibilities:
                letters=[]
                valid=1
                for char in possibility:
                    chars=[]
                    for let,val in self.alphabet.items():
                        if char in val:
                            chars.append(let)
                    if len(chars) == 0:
                        valid=0
                        break
                    else:
                       letters.append(chars)
                   
                    del chars
                if valid==1 and len(letters) > 0:
                    #generate possible words from given letters
                    words=self.rec_scan_array(letters)
                    validwords+=words
                    del words
            
            #print(validwords)
            
            #check which valid words are english if there's more than one option
            #go with the most frequently used english word
            if len(validwords) > 0:
                englishwords={}
                
                for valid in validwords:
                    score=1+5/len(valid)
                    
                    #computer talk
                    if self.jargon.Contains(valid) == True:
                        value=2
                        jargon=self.jargon.Translate(valid)
                        
                        if self.dictionary.Contains(jargon) == True:
                            value=4
                        
                        score+=value
                        
                        if len(jargon) > 0:
                            if jargon in englishwords:
                                englishwords[jargon]+=value
                            else:
                                englishwords[jargon]=score
                        
                            score=0
                    #valid english
                    if len(valid) > 1 and self.dictionary.Contains(valid) == True:
                        score+=5
                    #frequency words
                    if self.stopwords.Contains(valid):
                        score+=self.spelling.Frequency(valid)
                    else:
                        score+=5*self.spelling.Frequency(valid)
                    #same length
                    if len(word) == len(valid):
                        score+=0.1
                    #no numbers
                    if valid.isalpha() == True:
                        score+=1
                    
                    englishwords[valid]=score
                
                #figure out what word is the most likely to be correctable
                check=[]
                skip=0
                for valid in englishwords:
                    if valid.isalpha():
                        #if there is already a good word in the list, then don't bother with looking up spell corrections
                        if self.dictionary.Contains(valid) and len(valid) >= len(word)/2:
                            skip=1
                            check=[]
                            break
                        else:
                            check.append(valid)
                if len(check)==0 and skip == 0:
                    check.append(englishwords[0])
                #append the corrected version, hopefully
                for item in check:
                    corrected=self.spelling.Check(item,dictionary=True,fast=True)
                    if corrected != False and len(corrected) > 0:
                        word=corrected[0]
                        
                        if word not in englishwords:
                            frequency=self.spelling.Frequency(word)
                            #if it is on the stop list, don't add as much weight
                            if self.stopwords.Contains(word):
                                value=frequency+1
                            else:
                                value=5*frequency+1
                            #add weight if in the dictionary
                            if self.dictionary.Contains(word) == True:
                                value+=1
                            #add weight if not numbers
                            if word.isalpha() == True:
                                value+=1
                            englishwords[word]=value
                        else:
                            #if one of the corrected words list is in the englishwords list then up that value by 0.1
                            for correct in corrected:
                                if correct in englishwords:
                                    englishwords[correct]+=0.1
                        
                #get the most likely word
                final=sorted(englishwords.items(),key=operator.itemgetter(1),reverse=True)[0]
                #add word
                english.append(final[0])
        
        #send the result
        pipe.send([thread_id," ".join(english)])
