import random 
import string

word_length = 18

components = [string.ascii_letters, string.digits, "!@#$%&"]

chars = []
for clist in components:
    for item in clist:
        chars.append(item)
def generate_password():
    """
    The function generates a random password of a specified length using a given set of characters.
    :return: a randomly generated password as a string.
    """
    passoword = []
    for i in range(word_length):
        rchar = random.choice(chars)
        passoword.append(rchar)
    return "".join(passoword)
print(generate_password())



#simplified version
import random
import string

word_length = 18

components = [string.ascii_letters, string.digits, '!@#$%&']

chars = [char for clist in components for char in clist]

def generate_password():
    """
    The function generates a random password of a specified length using a given set of characters.
    :return: The function `generate_password()` is returning a randomly generated password as a string.
    The password is generated using the `random.choices()` function, which selects characters randomly
    from the `chars` list with a length of `word_length`. The selected characters are then joined
    together using the `join()` method and returned as a string.
    """
    password = random.choices(chars, k=word_length)
    return ''.join(password)
print(generate_password())