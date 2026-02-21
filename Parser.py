import requests
from bs4 import BeautifulSoup

class url_parser:

    def parse(url):
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0 Safari/537.36"
        }
        
        try:
            page=requests.get(url,headers=headers,timeout=10)
            page.raise_for_status()
        except Exception as e:
                print(f"Unexpected error: {type(e).__name__}: {e}")
                return None
        
        soup=BeautifulSoup(page.text,"lxml")
        title=soup.title.get_text(strip=True) if soup.title else "No title"
        body=soup.body.get_text(strip=True) if soup.body else "No body"
        links=[link['href'] for link in soup.find_all('a',href=True)]
        

        return {"title": title, "body": body, "links": links}
    def hash(word):
        m=(0b1<<64)-1
        p=53
        p_val=1
        hash_value=0
        for c in word:
            hash_value=(hash_value+ord(c)*p_val) & m
            p_val=(p_val*p) & m
        return hash_value
if __name__ == "__main__":
    url=input("Enter the url :  ")
    print()
    result=url_parser.parse(url)
    if result:
        print("Title:", result["title"])
        print()
        print("Body: " , result['body'])
        print()
        print("Links found:", len(result["links"]))
        print()
        print(result["links"])