from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ahocorasick
import pprint, os, json, sys
import logging

uri = "mongodb+srv://medifind:medifind@medifind.uezyqvq.mongodb.net/?retryWrites=true&w=majority"

logging.basicConfig(filename="extract.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

logging.info("Pinged your deployment. You successfully connected to MongoDB!")
try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logging.exception("An exception occurred while trying to ping MongoDB")

db = client["MediFind"]
collection = db["Drug"]

dir_path = os.getcwd()
nlp_path = os.path.dirname(os.path.realpath(__file__))
ocr_path = os.path.join(dir_path, "./")

def load(collection):
    data = collection.find({})
    names = [item["tenThuoc"] for item in data]
    return names

def build_trie(names):
    trie = ahocorasick.Automaton()
    for index, drugName in enumerate(names):
        trie.add_word(drugName, (index, drugName))
    trie.make_automaton()
    return trie

def extract(text, trie):
    medName = set()
    for _, (_, drugName) in trie.iter(text):
        medName.add(drugName)
    return medName

def print_info(name, collection):
    data = collection.find_one({"tenThuoc": name})
    # pprint.pprint(data)
    print(json.dumps(data, default=str))

def list(input, collection):
    names = load(collection)
    trie = build_trie(names)
    with open(input, "r", encoding="utf-8",errors="ignore") as file:
        docText = file.read()

    medNames = extract(docText, trie)
    return medNames

if __name__ == "__main__":
    input = os.path.join(ocr_path, "output_ocr.txt")
    output = os.path.join(nlp_path, "output_nlp.txt")
    sys.stdout = open(output, "w")
    pred_names = list(input, collection)

    for medicine in pred_names:
        print_info(medicine, collection)
    
    sys.stdout.close()
    sys.stdout = sys.__stdout__