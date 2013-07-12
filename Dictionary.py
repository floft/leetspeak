class Dictionary():
    def __init__(self,dict_type):
        self.types={"usa":"american-english","british":"british-english","catalan":"catalan","cracklib":"cracklib-small","finnish":"finnish","french":"french","italian":"italian","german":"ogerman","spanish":"spanish","jargon":"jargon1.txt","guten":"gutenberg.txt","stopwords":"stopwords_en.txt","slang":"noslang.txt"}
        self.dictionary={}
        
        self.Load(dict_type)
    
    def Load(self,dict_type):
        if dict_type in self.types:
            filename=self.types[dict_type]
            
            with open('words/'+filename, encoding='utf-8') as dictionary_file:
                for line in dictionary_file:
                    words=line.replace("\n","").split("\t")
                    length=len(words)
                    
                    if length > 1:
                        self.dictionary[words[0]]=words[length-1]
                    else:
                        self.dictionary[words[0]]=""
        
        return self.dictionary
    
    def Contains(self,word):
        if word in self.dictionary:
            return True
        else:
            return False
    
    def Translate(self,phrase,dict_type="slang"):
        """
        implement the tab separated replacement thing in noslang.txt
        """
        translation=""
        
        if len(self.dictionary) == 0 and dict_type != "":
            self.Load(dict_type)
            
        if self.Contains(phrase):
            translation=self.dictionary[phrase]
        
        return translation
