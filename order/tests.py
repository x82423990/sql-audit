from django.test import TestCase


# Create your tests here.
def read_in_chunks(file_obj, chunk_size=2048):

    while True:
        data = file_obj.read(chunk_size) 
        if not data:
            break
        yield data


with open('filename', 'r', encoding='utf-8') as f:
    for chuck in read_in_chunks(f):
       pass
