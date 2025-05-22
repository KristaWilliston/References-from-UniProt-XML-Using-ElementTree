#Read through the ElementTree tutorials
#Write a program to pick out, and print, the references of a XML format UniProt
#entry, in a nicely formatted way.

import xml.etree.ElementTree as ET
import urllib.request
thefile = urllib.request.urlopen(
                         'http://www.uniprot.org/uniprot/Q9H400.xml')
document = ET.parse(thefile)
root = document.getroot()

ns = '{http://uniprot.org/uniprot}'
entry = root.find(ns+'entry')

def references(entry):
    references = []                                                     #store reference info
    for ref in entry.findall(ns+'reference'):                           #look through reference elements within entry
        citation = ref.find(ns+'citation')                              #find element citation within reference

        scopes = []
        for scope in ref.findall(ns+'scope'):
            if scope.text:
                scopes.append(scope.text)
        
        authors = []                                                    #stores authors of references
        author_list = citation.find(ns+'authorList')                    #find authorList within citation
        if author_list is not None:                                     #checks if authors are present
            for person in author_list.findall(ns+'person'):             #loops through each element person in authorList
                name = person.attrib.get('name')                        #gets name attribute of each person
                authors.append(name)                                    #adds name to authors list

        dbReferences = citation.findall(ns+'dbReference')
        dbRefs = []                                                     #stores dbReferences of references
        for dbReference in dbReferences:
            dbReferenceType = dbReference.attrib.get('type')
            dbReferenceID = dbReference.attrib.get('id')
            dbRefs.append((dbReferenceType, dbReferenceID))             #adds as tuple to list

        titleElem= citation.find(ns+'title')                            #finds title within citation
        title = titleElem.text if titleElem is not None else 'N/A'      #gets title text 
       
        citationType = citation.attrib.get('type')                      #gets attributes of citation
        citationDate = citation.attrib.get('date')
        citationName = citation.attrib.get('name')
        citationVolume = citation.attrib.get('volume')
        citationFirst = citation.attrib.get('first')
        citationLast = citation.attrib.get('last')
        citationDB = citation.attrib.get('db')
                    
        ref_dict = {                                                    #dictionary of all citation info
            'type':citationType,
            'authors':', '.join(authors),
            'title':title,
            'db':citationDB,
            'journal':citationName,
            'volume':citationVolume,
            'year':citationDate,
            'first':citationFirst,
            'last':citationLast,
            'scope':scopes,
            'dbReferences':dbRefs
        }
        references.append(ref_dict)                                     #adds citation dictionary to references list
    return references

reference = references(entry)                                           #store entry values and returned list into reference variable

for i, ref in enumerate(reference, start=1):                            #starts with index 1 and finds all the values of each reference
    print('Reference',i,':')
    if ref['authors']:
        print('Authors:',ref['authors'])
    else:
        print('Authors: N/A')
    print('Year:',ref['year'])
    print('Title:',ref['title'])
    if ref['db']:
        print('db:',ref['db'])
    else:
        print('db: N/A')
    print('Type:',ref['type'])
    if ref['journal']:
        print('Journal:',ref['journal'])
    else:
        print('Journal: N/A')
    if ref['volume']:
        print('Volume:',ref['volume'])
    else:
        print('Volume: N/A')
    if ref['first']:
        print('First:',ref['first'])
    else:
        print('First: N/A')
    if ref['last']:
        print('Last:',ref['last'])
    else:
        print('Last: N/A')
    if ref['scope']:
        print('Scope:')
        for scope in ref['scope']:
            print('--',scope)
    else:
        print('Scope: N/A')
    for dbType, dbID in ref['dbReferences']:
        print('dbReference Type:', dbType, 'ID:', dbID)
    print()
