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
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {page.status_code}: {e}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Failed to connect to {url}")
            return None
        except requests.exceptions.Timeout:
            print(f"Request timed out for {url}")
            return None
        except Exception as e:
                print(f"Unexpected error: {type(e).__name__}: {e}")
                return None
        soup=BeautifulSoup(page.text,"lxml")
        title=soup.title.get_text(strip=True) if soup.title else "No title"
        body=soup.body.get_text(strip=True) if soup.body else "No body"
        links=[link['href'] for link in soup.find_all('a',href=True)]
        

        return {"title": title, "body": body, "links": links}
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