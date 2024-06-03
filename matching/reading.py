import os
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

def preprocess_line(line):
    while not line[0].isalpha():
        line = line[1:]
    while not line[-1].isalpha():
        line = line[:-1]

    tokens = mystem.lemmatize(line.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token not in (" ", "«", "»") \
              and token.strip() not in punctuation]
    
    line = " ".join(tokens)
    
    return line

def read_dishes(DISHES_PATH, n_clusters):
    dishes = []
    targets = []
    dishes_files = os.listdir(DISHES_PATH)[:n_clusters]

    for target, file in enumerate(dishes_files):
        with open(os.path.join(DISHES_PATH,file)) as f:
            lines = f.readlines()

            dishes.append(preprocess_line(lines[0]))
            targets.append(target)

            for line in lines[1:]:
                if line[0].isnumeric():
                    dishes.append(preprocess_line(line))
                    targets.append(target)

    return dishes, targets
