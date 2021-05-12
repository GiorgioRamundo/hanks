from nltk.parse.corenlp import CoreNLPDependencyParser

parser = CoreNLPDependencyParser(url='http://localhost:9000')
parse = parser.raw_parse('Smith jumps over the lazy dog')
for governor,dep,dependent in parse.triples():
    print(governor,dep,dependent)