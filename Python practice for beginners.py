def Q1(n: int) -> None:
    for i in range(n):
        print(i)

def Q2(string: str) -> None:
    Newstring: str = string[::-1]
    print(Newstring)

def Q3(string: str) -> bool:
    NewString: str
    for i in range(len(string)):
        if string[i] == string[len(string) - i -1]:
            return True
    return False

def Q4(string: str) -> None:
    NewString: str = string[len(string) -1 ::]
    print(NewString)
    
    
