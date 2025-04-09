user1=int(input("enter the number"))
user2=int(input("enter the number"))
for i in range(user1,user2+1):
    a=open(f"{i}.txt","w")
    for j in range(1,11):
        a.write(f"{i}*{j}={i*j}\n")