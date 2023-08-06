import random
from random_greetings.constants import greetings

def say_hello():
    language, greeting = random.choice(list(greetings.items()))
    print(f"In {language}, we greet with {greeting}")
    