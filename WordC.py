def openTextFile() -> list:
    '''Open a text file and return the contents as a string.'''
    with open(r"./text.txt", 'r') as f:
        return f.read().split()
    
def Words() -> None:
    text: list = openTextFile()
    text.sort(key=lambda x: x[0].lower())
    words: dict = {}
    for word in text:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
        
    return words

def sortWords(words: dict ) -> list:
    sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
    return sorted_words

def printWordsToN(n:int, sorted_words:list) -> None:   
    for i in range(n):
        print("key:", sorted_words[i][0] + ",", "value: ", sorted_words[i][1])
        
def main() -> None:
    '''Main function.'''
    printWordsToN(3, sortWords(Words()))
    
if __name__ == '__main__':
    main()