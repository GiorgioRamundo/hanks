import collections

from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import RegexpTokenizer

def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ' ' + ele
        # return string
    return str1

def preprocess(_w):
    tokens = word_tokenize(_w)
    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(listToString(tokens))
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    t = set(lemmatizer.lemmatize(w) for w in tokens if not w in stop_words)
    return t


def list_to_set(sentence):
    s = set()
    for w in sentence:
        s.add(w)
    return s


def wsd(term, sentence):
    context = list_to_set(sentence)
    bows = []
    bow = set()
    s = wn.synsets(term)
    max_sense = None
    for i in range(len(s)):
        bow = bow.union(preprocess(s[i].definition()))
        for e in s[i].examples():
            bow = bow.union(preprocess(e))
        bows.append((s[i],bow))
        bow = set()
    max_len = 0
    for i in range(len(bows)):
        overlap = bows[i][1] & context
        if len(overlap) > max_len:
            max_sense = bows[i][0]
            max_len = len(overlap)
    return max_sense

def retain(l,n):
    list = []
    for i in range(n):
        list.append(l[i])
    return list

def delete_none(list):
    res = []
    for (x, y) in list:
        if x is None and y is None:
            continue
        res.append((x, y))
    return res

def convert_to_set(l):
    s = set()
    for p in l:
        s.add(p)
    return s



verb = 'feel'
n = 211
sentences = retain([s for s in brown.sents() if verb in s],n)
fillers = []
lemmatizer = WordNetLemmatizer
for s in sentences:
    for i in range(len(s)):
        if s[i] == verb:
            try:
                _senses = [s[i-1],s[i+1]]
            except:
                continue
            senses = []
            for i in range(len(_senses)):
                senses.append(wsd(_senses[i],s))
            fillers.append(senses)
c = 0
pairs = []
frequences = []

for (x,y) in delete_none(fillers):
    res = ''
    res2 = ''
    if x is not None:
        semtype1 = wn.synset(x.name()).lexname()
        res += str(x) + ' '
        res2 += str() + str(semtype1) + ' '
    else:
        semtype1 = 'empty'
        res += 'empty '
        res2 += 'empty '
    if y is not None:
        semtype2 = wn.synset(y.name()).lexname()
        res += str(y) + ' '
        res2 += str(semtype2)
    else:
        semtype2 = 'empty'
        res += 'empty'
        res2 += 'empty'
    print(res)
    print(res2+'\n')
    pairs.append((semtype1,semtype2))
    c = c + 1

print('found ' + str(c) + ' semantic types on ' + str(n) + ' sentences')
pairs_set = convert_to_set(pairs)
frequences = {}
for p in pairs:
    if p in frequences.keys():
        frequences[p] = frequences[p] + 1
    else:
        frequences[p] = 1
print(frequences)
print(collections.OrderedDict(sorted(frequences.keys(),reverse=True)))