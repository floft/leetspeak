from Spelling import Spelling

#set these
tests=[1,2,3,4,5,6,7,8]
limit_words=8

#necessary variables
corrections={}
s=Spelling()
flip=[2,3,7,8]

for num in tests:
    with open("/scripts/internet_jargon/oxford/test_"+str(num)+".txt") as infile:
        for line in infile:
            for entry in line.split(","):
                parts=entry.split(" ")
                
                if len(parts) >= 2:
                    if num in flip:
                        corrections[parts[1].strip()]=parts[0].strip()
                    else:
                        corrections[parts[0].strip()]=parts[1].strip()

correct=0
total=0

for key,entry in corrections.items():
    wrong=entry.lower()
    right=key.lower()
    
    if s.dictionary.Contains(wrong) == False and s.dictionary.Contains(right) == True:
        check=s.Check(wrong,dictionary=True)
        total+=1
        incorrect=True
        
        if check !=  False:
            for k,i in enumerate(check):
                if k < limit_words and i.lower() == right:
                    incorrect=False
                    correct+=1
                    break
        
        if incorrect==True:
            if check == False:
                print("FAIL",right,": ",wrong,"→ False")
            else:
                print("FAIL",right,": ",wrong,"→",[i for k,i in enumerate(check) if k < limit_words])
    #else:
    #    print("Not in dictionary:",right,"or",wrong)

print("Score:",str(correct)+"/"+str(total),"=",correct/total*100,"%")
