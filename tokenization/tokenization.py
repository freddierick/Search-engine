import spacy
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import unquote
import time


hostName = "localhost"
serverPort = 8080

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

def tokenize(text):
    start = time.time() * 1000
    # text = text.lower()
    #  "nlp" Object is used to create documents with linguistic annotations.
    doc = nlp(text)

    # Create list of word tokens
    # Analyze syntax
    nouns = [chunk.text for chunk in doc.noun_chunks]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    adverbs = [token.lemma_ for token in doc if token.pos_ == "ADV"]

    for token in doc:
        print(token.lemma_, token.pos_)

    specialFinds = []
    # Find named entities, phrases and concepts
    for entity in doc.ents: 
        specialFinds.append((entity.text, entity.label_)) 

    return json.dumps({'noun-phrases': nouns, 'verbs': verbs, 'adverbs': adverbs, 'special': specialFinds, 'tokenised-text': [token.lemma_ for token in doc], 'time-to-run': (time.time() * 1000) - start})

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        urlparsed = urlparse(self.path)
        print(urlparsed)
        query_components = dict(qc.split("=") for qc in urlparsed.query.split("&"))

        print(self.request)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(tokenize(unquote(query_components['string'])), encoding='utf8'))


webServer = HTTPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))
try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass




# print(tokenize("how do i find a girlfriend?"))