import random
import string


def createImg(length):
    return ''.join(random.choice(string.digits) for i in range(length))
