
import re 
import xml.etree.ElementTree as ET


def get_variation_archive_info(s, fh, query_end):
    info = []
    slist = [s]
    while True:
        s = fh.readline()
        slist.append(s)
        if (not s) or (re.search(query_end, s)):
            break
            
    root = ET.fromstringlist(slist)
    
    accession = root.get("Accession")
    
    # find all variant infos 
    for hgvs_record in root.findall('.//HGVS'):
        if hgvs_record.get("Type") == "coding":
            
            # only consider missense mutations 
            mut_type = hgvs_record.find('MolecularConsequence')
            if mut_type is None or mut_type.get('Type') != 'missense variant':
                continue 
            
            # get the protein expression record 
            protein_elem = hgvs_record.find('ProteinExpression')
            nuc_elem = hgvs_record.find("NucleotideExpression")
            
            if protein_elem is None:
                continue
            
            mane_select = bool(nuc_elem.get("MANESelect", False))
            
            # record the changes 
            info.append({'seq_accession': protein_elem.get('sequenceAccessionVersion'),
                         'change': protein_elem.get('change'),
                         'mane_select': mane_select})        
            
    return accession, info

