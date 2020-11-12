import glob
import json
import requests
import pandas as pd

BASE_URL = "https://api.monarchinitiative.org/api/nlp/annotate/entities"
DATA_PATH = "Text/"


def get_hpo(text):
    resp = requests.get(BASE_URL, params={"content": text}).json()
    symptoms = []
    codes = []
    starts = []
    ends = []
    for match in resp["spans"]:
        for token in match['token']:
            if "HP:" in token["id"]:
                symptoms.append(token["terms"][0])
                codes.append(token["id"].replace("HP:", ""))
                starts.append(match['start'])
                ends.append(match['end'])
    return symptoms, codes, starts, ends

def extract_info_biolink(data_path):
    files = sorted(glob.glob(DATA_PATH + "*"))
    df_dict = {
        "file": [],
        "text": [],
        "HPO_symptoms": [],
        "HPO_codes": [],
        "starts": [],
        "ends": [],
    }
    for file in files:
        file_name = file.replace(DATA_PATH, "")
        df_dict["file"].append(file_name)
        with open(file, "r") as f:
            input_text = f.read()
        f.close()
        df_dict["text"].append(input_text)
        symptoms, codes, starts, ends = get_hpo(input_text)
        df_dict["HPO_symptoms"].append(symptoms)
        df_dict["HPO_codes"].append(codes)
        df_dict["starts"].append(starts)
        df_dict["ends"].append(ends)
    df = pd.DataFrame(
        df_dict, columns=["file", "text", "HPO_symptoms", "HPO_codes", "starts", "ends"]
    )
    df.to_csv(path_or_buf=data_path)


if __name__ == "__main__":
    extract_info_biolink("data/biolink_GSC.csv")
