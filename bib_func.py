import re
from invenio.search_engine import perform_request_search
from invenio.bibformat_elements import bfe_INSPIRE_bibtex
from invenio.bibformat_engine import BibFormatObject
from invenio.bibformat_elements import bfe_INSPIRE_bibtex

def main():
    print 'in main\n'
    
    inputTeX = open('file.tex')
    lines = inputTeX.readlines()
    inputTeX.close()
    
    bibtex_service(lines)

def bibtex_service(lines):
    print 'in bibtex'
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
  
    bibFile = open('file.bib', 'w')
    for x in references:
        index = None
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
                btxt_str = bfe_INSPIRE_bibtex.format_element(bfo)
                print btxt_str

        else :
            print '***************************************'
            print '*** I do not know what',x,'is. ***'
            print '***************************************'
    bibFile.close()

if __name__ == "__main__":
    main()
