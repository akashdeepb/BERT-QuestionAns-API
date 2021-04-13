import string
import random

N = 32

def generate_token():
	return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))