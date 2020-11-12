import glob
import json
import pandas as pd
import requests

BASE_URL = "https://ncr.ccm.sickkids.ca/curr/annotate/"
DATA_PATH = "Text/"


def get_hpo(text):
    resp = requests.get(BASE_URL, params={"text": text}).json()
    matches = resp["matches"]
    symptoms = []
    codes = []
    starts = []
    ends = []
    matches = sorted(matches, key=lambda x: x["start"])
    for match in matches:
        symptoms.append(match["names"][0])
        hpo_id = match["hp_id"].replace("HP:", "")
        codes.append(hpo_id)
        starts.append(match["start"])
        ends.append(match["end"])
    return symptoms, codes, starts, ends


def generate_dataset_from_GSC(data_path):
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
    generate_dataset_from_GSC("data/NCR_GSC.csv")
