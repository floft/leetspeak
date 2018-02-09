from ChatBot.User import User,Users

class Bot():
    def __init__(self):
        self.users=Users()
    def Respond(self,email,imid,statement):
        response=""
        
        #get user
        user=self.users.Get(email,imid)
        #generate response if the user isn't repeating pervious statements
        if user.history.UserRepeating(statement) == 0:
            response=self.generate(user,statement)
            #add to history
            user.history.Add(statement,response)

        return response
        
    def generate(self,user,statement):
        """
        Generate the response for what the user said.
        """
        #words=[dm(w) for w in tokenize(statement)]
        #response=words
        
        response="Why do you say \""+statement+"\"?"
        return response
