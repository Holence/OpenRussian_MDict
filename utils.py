def addStress(c):
    return c+chr(769)

def convertStress(word: str):
    return word.replace("'", chr(769))
