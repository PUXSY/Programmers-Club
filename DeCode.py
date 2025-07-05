import hashlib

def DeCodeMD5(hash_string = "") -> str:
    '''Decode a hash string using brute force.'''
    for i in range(000000,999999):
        guess = str(i).zfill(6)
        guess_hash = hashlib.md5(guess.encode()).hexdigest()
        if guess_hash == hash_string:
            return guess
    return "Not Found"



if __name__ == '__main__':
    md5_hash: str = "3cc6520a6890b92fb55a6b3d657fd1f6"
    result = DeCodeMD5(md5_hash)
    print(f"Decoded string: {result}")
