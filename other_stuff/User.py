from ChatBot.History import History

class User():
    def __init__(self):
        self.email=""
        self.imid=""
        self.topic=[]
        self.history=History()
        
        self.status=""
        self.name=""
        self.age=""
        self.birthday=""
        self.father=""
        self.mother=""
        self.brother=""
        self.sister=""
        self.gender=""
        self.friend=""
        self.pet=""
        self.location=""
        self.job=""
        self.husband=""
        self.wife=""
        self.phone=""
        self.favorite_movie=""
        self.favorite_song=""
        self.favorite_website=""
        self.favorite_show=""
        self.favorite_color=""
        self.girlfriend=""
        self.boyfriend=""
        self.he=""
        self.she=""
        self.it=""
        self.they=""
        self.we=""
        self.want=""
        self.haircolor=""
        self.zipcode=""
        self.topic=""
        self.language=""

class Users():
    def __init__(self):
        self.users=[]
        
    def GetAll(self):
         return self.users
         
    def Add(self,email,imid):
         user=User()
         user.email=email
         user.imid=imid
         self.users.append(user)
         
         return user
         
    def Get(self,email,imid):
        return_user=None
        
        #find the user
        for user in self.users:
            if user.email == email:
                return_user=user
                break
            
        #if there was no user, make one
        #if there was a user, set the imid (jid)
        if return_user == None:
            return_user=self.Add(email,imid)
        else:
            if return_user.imid != imid:
                return_user.imid = imid
            
        return return_user
