import sys
from lemur_stopwords import LEMUR_STOPWORDS 
from assignment_1 import read_url

def hash_value(word):
    m=(1<<64)-1
    p=53
    pval=1
    hash_val=0
    for c in word:
        hash_val=(hash_val+ord(c)*pval) & m
        pval=(pval*p) & m
    return hash_val

def tokenise_frequency(text):
    frequency_map={}
    word=[]
    for ch in text:
        if ch.isalnum():
            word.append(ch.lower())
        else:
            if word:
                key=''.join(word)
                if key not in LEMUR_STOPWORDS:
                    if key in frequency_map:
                        frequency_map[key]+=1
                    else:
                        frequency_map[key]=1
                word=[]
    if word:
        key=''.join(word)
        if key not in LEMUR_STOPWORDS:
            if key in frequency_map:
                frequency_map[key]+=1
            else:
                frequency_map[key]=1
    return frequency_map

def simhash(frequency_map):
    summed_weights=[0]*64
    for key ,value in frequency_map.items():
        hash_val=hash_value(key)
        for i in range(64):
            if (hash_val>>i)& 1:
                summed_weights[i]+=value
            else:
                summed_weights[i]-=value
    document_fingerprint=[1 if i>0 else 0 for i in summed_weights]
    return document_fingerprint

def count_common_bits(doc1_fingerprint,doc2_fingerprint):
    count=0
    for i in range(64):
        count+=1 if doc1_fingerprint[i]==doc2_fingerprint[i] else 0
    return count

def show_similarity(url1,url2):
    doc1=read_url(url1)
    doc2=read_url(url2)
    if not doc1 or not doc2:
        print("unable to parse page ")
        return None
    tokenise_doc1=tokenise_frequency(doc1["body"])
    doc1_fingerprint=simhash(tokenise_doc1)
    
    tokenise_doc2=tokenise_frequency(doc2["body"])
    doc2_fingerprint=simhash(tokenise_doc2)

    return count_common_bits(doc1_fingerprint,doc2_fingerprint)





if __name__ == "__main__":
    
    if len(sys.argv)==3:
        print("The count of similar bits is(out of 64): ", show_similarity(sys.argv[1],sys.argv[2]))

    else:
        print("Invalid input")
        sys.exit(1)


    