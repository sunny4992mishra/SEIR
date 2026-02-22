import requests
from bs4 import BeautifulSoup
import sys
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


def read_url(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
    }
    
    try:
        page=requests.get(url,headers=headers,timeout=10)
        page.raise_for_status()

        soup=BeautifulSoup(page.text,"lxml")
        title=soup.title.get_text(strip=True) if soup.title else "No title"
        body=soup.body.get_text(strip=True) if soup.body else "No body"
        links=[link['href'] for link in soup.find_all('a',href=True)]
        
        return {"title": title, "body": body, "links": links}

    except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            return None
    
    

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
                if key not in stop_words:
                    if key in frequency_map:
                        frequency_map[key]+=1
                    else:
                        frequency_map[key]=1
                word=[]
    if word:
        key=''.join(word)
        if key not in stop_words:
            if key in frequency_map:
                frequency_map[key]+=1
            else:
                frequency_map[key]=1
    return frequency_map

def simhash(frequency_map):
    summed_weights=[0]*64
    for key ,frequency in frequency_map.items():
        hash_val=hash_value(key)
        for i in range(64):
            if (hash_val>>i)& 1:
                summed_weights[i]+=frequency
            else:
                summed_weights[i]-=frequency
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
    
    if len(sys.argv)==2:
        url=sys.argv[1]
        result=read_url(url)
        if result:
            print("Title:", result["title"])
            print()
            print("Body: " , result["body"])
            print()
            print("Links found:", len(result["links"]))
            print()
            for link in result["links"]:
                print(link)
    elif len(sys.argv)==3:
        print("The count of similar bits is(out of 64): ", show_similarity(sys.argv[1],sys.argv[2]))

    else:
        print("Invalid input")
        sys.exit(1)


    