# a = open("3.txt","r")
# char,word,line = 0,0,0
# for i in a.read():
#     if (i == "\n"):
#         line += 1
#     if (i == " "):
#         word +=1
#     if (i != " "):
#         char +=1
# print("word count :" ,word)
# print("line count :" ,line)
# print("char count :" ,char)
text = open("first.txt").read()
print("word count:", len(text.split()), "line count:", len(text.splitlines()), "char count:", len(text))
