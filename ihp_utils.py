import pandas as pd
import requests 

FILE_PATH = "results_hpo_train_report.txt"
STARTING_LINE = 33
TEXT_PATH = "Text/"
ANNO_PATH = "Annotations/"
HPO_URL = "https://hpo.jax.org/api/hpo/search/?q="

def get_hpo_code(text):
    resp = requests.get(HPO_URL + text).json()
    try:
        hpo_code = resp["terms"][0]["id"].replace("HP:", "")
        return hpo_code
    except:
        return


def parse_ihp_results(data_path):
    f = open(FILE_PATH, "r")
    text = f.read()
    items = text.split("\n")
    items = items[STARTING_LINE:]
    item_dict = {}
    for item in items:
        try:
            file_num = int(item)
            item_dict[item] = {}
            text_file = open(TEXT_PATH + item, 'r')
            item_dict[item]["text"] = text_file.read()
            item_dict[item]["symptoms"] = []
            item_dict[item]["starts"] = []
            item_dict[item]["ends"] = []
            item_dict[item]["codes"] = []
        except:
            vals = item.split("\t")
            if "TP" not in vals[0]:
                continue
            file_name = vals[0].split(":")[1]
            start, end = vals[1].split(":")
            item_dict[file_name]["starts"].append(start)
            item_dict[file_name]["ends"].append(end)
            item_dict[file_name]["symptoms"].append(vals[2])
            item_dict[file_name]["codes"].append(get_hpo_code(vals[2]))
    sorted_keys = sorted(item_dict.keys())
    df_dict = {
        "file": [],
        "text": [],
        "HPO_symptoms": [],
        "HPO_codes": [],
        "starts": [],
        "ends": [],
    }
    for k in sorted_keys:
        df_dict["file"].append(k)
        df_dict["text"].append(item_dict[k]["text"])
        df_dict["HPO_symptoms"].append(item_dict[k]["symptoms"])
        df_dict["HPO_codes"].append(item_dict[k]["codes"])
        df_dict["starts"].append(item_dict[k]["starts"])
        df_dict["ends"].append(item_dict[k]["ends"])
    df = pd.DataFrame(
        df_dict, columns=["file", "text", "HPO_symptoms", "HPO_codes", "starts", "ends"]
    )
    df.to_csv(path_or_buf=data_path)

        

if __name__ == "__main__":
    parse_ihp_results("IHP_GSC.csv")