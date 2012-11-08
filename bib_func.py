import re
from invenio.search_engine import perform_request_search
from invenio.bibformat_elements import bfe_INSPIRE_bibtex
from invenio.bibformat_engine import BibFormatObject
from invenio.bibformat_elements import bfe_INSPIRE_bibtex

def main():
    inputTeX = open('file.tex')
    lines = inputTeX.readlines()
    inputTeX.close()
    
    bibFile = open('file.bib', 'w')
    bibtxt = bibtex_service(lines)
    bibFile.write(bibtxt)
    bibFile.close()

def bibtex_service(lines):
    citeString = '\cite{'
    citeStringMatch = r"\\cite\{(.*?)\}"
    references = []
    for line in lines:
        if citeString in line:
            for a in list(re.finditer(citeStringMatch,line)):
                r = a.groups()[0].split(',')
                for x in r:
                    x = re.sub('\s','',x)
                    if not x in references:
                        references.append(x) 
  
    for x in references:
        index = None
        btxt_str = ''
        if re.search('.*\:\d{4}\w\w\w?',x) : index = 'texkey'
        elif re.search('.*\/\d{7}',x)      : index = 'eprint'
        elif re.search('\d{4}\.\d{4}',x)   : index = 'eprint'
        elif re.search('\w\.\w+\.\w',x) : 
            index = 'j'
            x = re.sub('\.',',',x)
        elif re.search('\w\-\w',x) : index = 'r'
        if index :
            #print 'find',index,x,'in INSPIRE'
            recid_list = perform_request_search(p=x)
            if recid_list:
                bfo = BibFormatObject(recid_list[0])
                btxt_str = btxt_str + bfe_INSPIRE_bibtex.format_element(bfo)

        else :
            print '***************************************'
            print '*** I do not know what',x,'is. ***'
            print '***************************************'
        return btxt_str

if __name__ == "__main__":
    main()
