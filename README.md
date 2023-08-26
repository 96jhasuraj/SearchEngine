# SearchEngine
simple search implementation | inverted index | ranking with tfidf 
## Requirements

I'm using Python 3.8 , no library dependency
## Usage

Run from the command line (this program will exit afterwards):
```bash
$ pip install -r requirements.txt
$ python run.py
```

## Functions / interface

### 0. Note :
```
  a. Document class : 
    a.1 attributes : path , text , term_frequencies
      a.1.1. path  ( path of the document indexed ) 
      a.1.2. text ( text in the document )
      a.1.3. term_frequencies ( TF of the tokens in document)

    a.2 methods :  fulltext , path , term_frequency
```
### 1. buildIndex(path):
```
  takes path/folder from where it will pick up files for indexing , as a string input
  a. sample usage : index.buildIndex('data')
```

### 2. search ( query , search_option , rank ) : 
```
  performs boolean search

  a. sample usage : index.search("query" , "AND" , True)
  b. returns list of Document objects meeting search criteria
  b. search_option can be "AND" "OR" or "NOT" 
  d. rank = True / False ( do you want results to ranked acc to TFIDF)
```
### 3. delete_document( filepath ): 
```
  takes filepath as string input & deletes file from index

  a. sample usage : index.delete_document('data/mit.txt')
  b. returns void
  c. Note : code expects data in root directory ./data
```

### 4. update_document ( filepath ): 
```
  takes filepath as string input & updates it in index

  a. sample usage : index.update_document ('data/mit.txt')
  b. returns void
  c. Note : code expects data in root directory ./data
```
### 5. phrase_search ( phrase ):
```
  a. sample usage : index.phrase_search ('phrase to be searched')
  b. returns list of Document objects meeting search criteria
```
### 6. add_folder ( folder_path ):
```
  Adds files of a folder to index . takes folder_path as string input

  a. sample usage : index.add_folder('data2')
  b. returns void
```
