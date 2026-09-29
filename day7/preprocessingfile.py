with open("sample.txt","r") as file:
    text=file.read()
print(text)
print("No of characters:",len(text))
lc=len(open("sample.txt").readlines())
print(lc)