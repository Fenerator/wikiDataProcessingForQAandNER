import pandas as pd
import requests
from requests import utils
from collections import defaultdict
import os


# function provided by Odunayo Ogundepo
def get_wikipedia_url_from_wikidata_id(wikidata_id, lang="en", debug=False):
    url = "https://www.wikidata.org/w/api.php" "?action=wbgetentities" "&props=sitelinks/urls" f"&ids={wikidata_id}" "&format=json"
    json_response = requests.get(url).json()
    if debug:
        print(wikidata_id, url, json_response)

    entities = json_response.get("entities")
    if entities:
        entity = entities.get(wikidata_id)
        if entity:
            sitelinks = entity.get("sitelinks")
            if sitelinks:
                if lang:
                    # filter only the specified language
                    sitelink = sitelinks.get(f"{lang}wiki")
                    if sitelink:
                        wiki_url = sitelink.get("url")
                        if wiki_url:
                            return requests.utils.unquote(wiki_url)
                else:
                    # return all of the urls
                    wiki_urls = {}
                    for key, sitelink in sitelinks.items():
                        wiki_url = sitelink.get("url")
                        if wiki_url:
                            wiki_urls[key] = requests.utils.unquote(wiki_url)
                    return wiki_urls
    return None


def read_text(filenam):
    with open(filenam) as f:
        text_lines = f.read().splitlines()
    return text_lines


if __name__ == "__main__":
    os.makedirs("lang_biography", exist_ok=True)

    list_ids = read_text("id_list.csv")

    # keep only first 100000 ids
    list_ids = list_ids[:100000]

    list_langs = ["en", "tr", "az", "id", "als", "uz", "yo", "ig", "kk"]

    lang_wiki = dict([(l + "wiki", l) for l in list_langs])

    print("length of langs and ids", len(list_langs), len(list_ids))

    dict_lang = defaultdict(list)

    for i, id in enumerate(list_ids):
        val = None
        try:
            val = get_wikipedia_url_from_wikidata_id(id, lang=None, debug=True)
        except:
            pass

        if val != None:
            # list_qid_url.append([id, val])
            for l in val:
                if l in lang_wiki:
                    # print(l, val[l])
                    dict_lang[l].append([id, val[l]])

        # if i % 1000 == 0:
        print(i)

    for l in lang_wiki:
        df = pd.DataFrame(dict_lang[l], columns=["qid", "wiki_url"])
        lang = lang_wiki[l]
        print(l, lang, df.shape)
        df.to_csv("lang_biography/" + lang + ".csv", sep=",", index=None)
