from llama_index.core import SimpleDirectoryReader
import re

def read_my_docs(input_dir: str = "./data"):
    reader = SimpleDirectoryReader(input_dir=input_dir, recursive=True)
    extracted = []
    for docs in reader.iter_data():
        body = ''.join([chunk.text for chunk in docs])
        cleaned_text = re.sub(' +', ' ', body.replace('\n', ' '))
        yield {'title':f'{docs[0].metadata['file_name'].rsplit('.', 1)[0]}.txt',
               'body':cleaned_text} 
