from search.index import Index
import pprint as pp

def getIndex(path='data'): 
    '''
        utility function to make a inverted index data structure
    '''
    index = Index()
    index.buildIndex(path)
    return index


if __name__ == '__main__':
    
    index = getIndex()
    
    print(f'Index contains {len(index.documents)} documents' , end='\n')
    if(len(index.documents)<1):
        print("ERROR , no documents indexed , check if files present in indexed folder")
        quit()
    #index.add_folder('data2')

    '''
        test cases
    '''
    print("TESING search NOT" , end='\n')
    res = index.search('Suraj', search_type='NOT')
    res = [x.path for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()
    

    print("TESING search")
    res = index.search('suraj', search_type='AND')
    res = [x.path for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()

    print("TESING delete DOC")
    index.delete_document('data/mit.txt')
    res = index.search('suraj', search_type='AND')
    res = [x.path for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()


    print("TESING update DOC")
    index.update_document('data/mit.txt')
    res = index.search('suraj', search_type='AND')
    res = [x.path for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()
    
    print("TESING search OR")
    res = index.search('suraj appropriate', search_type='OR')
    res = [x.path for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()

    print("TESING search AND with rank")
    res = index.search('suraj appropriate', search_type='AND', rank=True)
    res = [(x[0].path,x[1]) for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()

    print("TESING search OR with rank")
    res = index.search('suraj appropriate', search_type='OR', rank=True)
    res = [(x[0].path,x[1]) for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()


    print("TESING phrase search")
    res = index.phrase_search('Free Software Foundation')
    res = [x.path for x in res]
    print(f"numbers of filed found : '{len(res)}'")
    pp.pprint(res)
    print()
