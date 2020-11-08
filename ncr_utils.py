import json
import requests

BASE_URL = "https://ncr.ccm.sickkids.ca/curr/annotate/"


def get_hpo(text):
    resp = requests.get(BASE_URL, params={"text": text}).json()
    print(resp['matches'][0])

if __name__ == "__main__":
    get_hpo(
        "A pedigree of branchio-oto-renal dysplasia (the BOR syndrome) is reported, including the documentation by serial audiometric studies of the onset and rapid progression of hearing loss in the twin sister of an affected child. The literature on this syndrome is analyzed to derive some figures for use in genetic counseling of such families. Branchio-oto-renal dysplasia is an autosomal dominant disorder in which affected individuals may have preauricular pits, lachrymal duct stenosis, hearing loss, branchial fistulas or cysts, structural defects of the outer, middle, and inner ear, and renal anomalies, which may range from mild hypoplasia to complete absence. Not all features of the syndrome are expressed in all carriers of the gene, but few carriers lack all the features, and the pits, branchial clefts, and hearing loss, are frequently expressed. Those offspring of affected persons who have pits or fistulas are likely (about 80%) to have hearing loss of varying degrees of severity. A minority of heterozygotes (about 7%) may have hearing loss without pits or fistulas. The risk of severe renal malformation is probably fairly low. Whether families that show dominant inheritance of pits, clefts, and deafness without renal anomalies represent variants of the BOR syndrome or a separate entity (the BO syndrome), is still not clear. At present, any individual with preauricular pits and branchial clefts deserves both otologic and renal investigation."
    )