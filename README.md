# URL Similarity Checker using SimHash

A Python tool that takes two URLs and compares how similar their content is using **SimHash** with a **64-bit Polynomial Rolling Hash**. The result is the number of matching bits (out of 64) in their document fingerprints.

---

## 📁 Project Structure

```
├── assignment_1.py       # URL fetcher and parser (uses requests + BeautifulSoup)
├── parser.py             # SimHash pipeline — hashing, tokenising, fingerprint comparison
├── lemur_stopwords.py    # Lemur stopword set for filtering common words
└── requirements.txt      # Project dependencies
```

---

## 🔍 How It Works

1. **Fetch** — `assignment_1.py` fetches the HTML of each URL and extracts the body text using `requests` and `BeautifulSoup`
2. **Tokenise** — `parser.py` splits the body text into lowercase tokens, filters out stopwords from `lemur_stopwords.py`, and builds a word frequency map
3. **Hash** — Each token is hashed using a **64-bit Polynomial Rolling Hash** with base `p = 53`:
   ```
   hash = sum(ord(c) * p^i) mod (2^64 - 1)
   ```
4. **SimHash** — A 64-bit fingerprint is built by summing weighted bit contributions across all tokens. Each bit is set to `1` if its weighted sum is positive, else `0`
5. **Compare** — The two fingerprints are compared bit by bit. The output is the count of **matching bits out of 64**

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

```bash
git clone https://github.com/sunny4992mishra/SEIR.git
cd SEIR
pip install -r requirements.txt
```

---

## ▶️ Usage

### Parse a single URL
```bash
python assignment_1.py <url>
```

### Compare two URLs
```bash
python parser.py <url1> <url2>
```

**Example:**
```bash
python parser.py https://en.wikipedia.org/wiki/Python_(programming_language) https://en.wikipedia.org/wiki/Java_(programming_language)
```

**Output:**
```
The count of similar bits is (out of 64): 58
```

A higher number means the two pages are more similar in content. A score of 64 means identical fingerprints.
---

## 🧠 Key Concepts

**Polynomial Rolling Hash** — Converts each word into a 64-bit integer based on the position and ASCII value of each character.

**SimHash** — A locality-sensitive hashing technique where similar documents produce fingerprints close to each other in [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance). Word frequencies are used as weights, making the fingerprint robust to minor content differences.

**Lemur Stopwords** — A standard stopword list from the [Lemur Project](http://www.lemurproject.org/) used to filter out common words (e.g. "the", "is", "and") that carry no semantic meaning.

---

## 📚 References

- [SimHash — Detecting Near-Duplicates for Web Crawling (Manku et al., 2007)](https://dl.acm.org/doi/10.1145/1242572.1242592)
- [Lemur Project](http://www.lemurproject.org/)
- [Polynomial rolling Hash Function](https://cp-algorithms.com/string/string-hashing.html)
