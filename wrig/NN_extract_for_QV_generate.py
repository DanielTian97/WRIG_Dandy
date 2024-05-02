import sys
import xml.etree.ElementTree as ET
import re
from tqdm import tqdm
from nltk.stem import PorterStemmer

import gensim

if len(sys.argv) < 4:
    # print('Needs 2 arguments - \n1. TREC original query file (.xml format)\n'
    #       '2. word2vec file (.txt)\n'
    #       '3. <query-term \t NN-list> output file path')
    print('Needs 3 arguments - \n1. TREC original query file (a txt file)\n'
          '2. word2vec file (.txt)\n'
          '3. <query-term \t NN-list> output file path')
    exit(0)

arg_trec_query_file = sys.argv[1]
arg_w2v_file = sys.argv[2]
arg_nn_out_file = sys.argv[3]

fw_NN_terms = open(f'./output/{arg_nn_out_file}', 'w+')

# read stop words
stopwords = []
try:
    file = open('../resources/smart-stopwords', 'r', encoding='utf-8')

except FileNotFoundError:
    print(f"Results about stopwords are not found.")

with file:
    
    Lines = file.readlines()
        
    for line in Lines:
        stopwords.append(line[:-1])
    file.close()
stopwords = set(stopwords)
print(stopwords)

# start ...
original_query_list = []
qterm_NN_dict = {}

stemmer = PorterStemmer()

# rootElement = ET.parse(arg_trec_query_file).getroot()
# for subElement in rootElement:
#     query = re.sub('[^a-zA-Z0-9 \n\.]', '', subElement[1].text.lower().strip())
#     for term in query.split(' '):
#         original_query_list.append(stemmer.stem(term))
# print(original_query_list)
try:
    file = open(arg_trec_query_file, 'r', encoding='utf-8')

except FileNotFoundError:
    print(f"Results about {arg_trec_query_file} are not found.")

with file:
    
    Lines = file.readlines()
        
    for line in Lines:
        query = line.split('\t')[1][:-1].lower().strip()
        for term in query.split(' '):
            original_query_list.append(stemmer.stem(term))    
    file.close()
print(original_query_list)

model = gensim.models.KeyedVectors.load_word2vec_format(arg_w2v_file, binary=False)
for term in tqdm(original_query_list):
    # if term not in ['am', '103', 'three', 'u.s.']:
    print('query term : ', term)
    # if(term in stopwords):
    #     continue
    try:
        vector = model.most_similar(positive=[term], topn=5)
    except KeyError:
        continue
    qterm_NN_dict[term] = vector
    print(vector)
    nn_list = []
    for nn_term in vector:
        nn_list.append(nn_term[0])
    qterm_NN_dict[term] = nn_list
print('dictionary ready...')

for key in qterm_NN_dict:
    fw_NN_terms.writelines(str(key) + '\t')
    for nn in qterm_NN_dict[key]:
        fw_NN_terms.writelines(str(nn) + ',')
    fw_NN_terms.write('\n')


