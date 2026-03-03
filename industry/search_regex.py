
import glob
from tqdm import tqdm
import re
import pandas as pd

#On parcours la liste des formes à rechercher et on la met dans un dictionnaire avec comme key le nom du cluster
#et comme value la requête
def queries_in_dictionnary(data, column_name_of_queries, list_of_regex):
    """data = a dataframe series containing the name of the queries. E.g. "Le vin" if we are looking for terms related to wine
    list_of_regex = a list of columns containing the regular expressions.
    return a dictionnary with the name of the queries and lists of regular expression
    """
    dict_queries = {}
    for i, x in enumerate(data[column_name_of_queries]):
        liste_regle = []
        for j, y in enumerate(list_of_regex):
            sq= data[y].iloc[i]
            if isinstance(sq, str):
                liste_regle.append(sq)
            else:
                pass
            dict_queries[x] = liste_regle
    return dict_queries


def texts_in_dictionnaries(list_text_id, list_text):
    """
    store list of text ids and texts in dictionnary. The aim is to apply regex on dictionnaries and not on dataframe (too long)
    list_text_id = a list of text
    list_text = a list of text (text should corresponds to its id)
    """
    dict_text= {}
    for n, x in tqdm(enumerate(list_text_id), total = len(list_text_id)):
        dict_text[x]= list_text[n]
    data = {"new_id": list_text_id, "text": list_text}
    df0 = pd.DataFrame(data)
    return dict_text, df0

def search_regex(dict_queries, dict_text, term_to_search = None):
    """
    Function which is used to look for regex.
    dict_queries : a dictionnary containing a list of queries, e.g. : {"Le vin" : ['vigne|viticult']}. You could get one with queries in dictionnary
    dict_text : a dictionnary with text id and id.
    term_to_search : a list of specific queries' name in dict_queries to search. Default : None (search all the queries in dictionnary)
    """
# La boucle pour recherche les expressions dans les textes
    dict_compteur = {}
    j = -1
    if term_to_search is not None:
        for n, x in tqdm(enumerate(term_to_search), total = len(term_to_search)):
            compteur  = 0
            queries = dict_queries[x]
            dict_test_queries = {}
            for y in dict_text:
                text = dict_text[y]
                compteur2 = 0
                for i, query in enumerate(queries):
                    p = re.compile(query, re.IGNORECASE)
                    sq = p.search(text)
                    if sq is not None:
                        compteur2 += 1
                    else:
                        pass
                if compteur2 >= len(queries):
                    dict_test_queries[y] = 1
                    compteur +=1
                else:
                    dict_test_queries[y] = 0
            j +=1
            if j == 0:
                df01 = pd.DataFrame.from_dict(dict_test_queries, orient='index', columns = [x])
                #df01["new_id"] = df01.index
            else:
                df01[x] = df01.index.map(dict_test_queries)
            print(f"{x} : {compteur}")
        return df01
    else:
        for n, x in tqdm(enumerate(dict_queries), total = len(dict_queries)):
            compteur  = 0
            queries = dict_queries[x]
            dict_test_queries = {}
            for y in dict_text:
                text = dict_text[y]
                compteur2 = 0
                for i, query in enumerate(queries):
                    p = re.compile(query, re.IGNORECASE)
                    sq = p.search(text)
                    if sq is not None:
                        compteur2 += 1
                    else:
                        pass
                if compteur2 >= len(queries):
                    dict_test_queries[y] = 1
                    compteur +=1
                else:
                    dict_test_queries[y] = 0
            j +=1
            if j == 0:
                df01 = pd.DataFrame.from_dict(dict_test_queries, orient='index', columns = [x])
                #df01["new_id"] = df01.index
            else:
                df01[x] = df01.index.map(dict_test_queries)
            print(f"{x} : {compteur}")
        return df01
