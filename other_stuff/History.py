class History():
    def __init__(self):
        self.history=[]
        
    def Add(self,user_statement,bot_statement):
        """
        Add an entry to the users's history while keeping at max 25 entries in the array.
        """
        
        #append the new data to the history
        self.history.append([user_statement,bot_statement])
        
        #reduce the length of the history to only 25 elements
        length = len(self.history)
        
        if length > 25:
            self.history.pop(0)
        
    def Get(self):
        return self.history
    
    def UserLastSaid(self,number):
        last_said=""
        length=len(self.history)
        
        if length > number:
            last_said=self.history[length-number-1]
            
        return last_said
    
    def UserRepeating(self,statement):
        repeat = 0
        if len(self.history) > 1 and statement == self.UserLastSaid(0)[0] == self.UserLastSaid(1)[0]:
            repeat = 1
            
        return repeat
