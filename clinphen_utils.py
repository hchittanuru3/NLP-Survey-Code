from clinphen_src import get_phenotypes, src_dir
import glob
import pandas as pd

DATA_PATH = "Text/"


def load_common_phenotypes(commonFile):
    returnSet = set()
    for line in open(commonFile):
        returnSet.add(line.strip())
    return returnSet


def get_names():
    srcDir = src_dir.get_src_dir()
    hpo_main_names = srcDir + "/data/hpo_term_names.txt"
    returnMap = {}
    for line in open(hpo_main_names):
        lineData = line.strip().split("\t")
        returnMap[lineData[0]] = lineData[1]
    return returnMap


def main(data_path):
    hpo_names = get_names()
    text_files = sorted(glob.glob(DATA_PATH + "*"))
    data_df = {"file": [], "text": [], "HPO_symptoms": [], "HPO_codes": []}
    for text in text_files:
        input_text = ""
        for line in open(text):
            input_text += line
        returnString = get_phenotypes.extract_phenotypes(input_text, hpo_names)
        items = returnString.split("\n")
        codes = []
        symptoms = []
        for item in items[1:]:
            cols = item.split("\t")
            codes.append(cols[0].replace("HP:", ""))
            symptoms.append(cols[1])
        data_df["file"].append(text.replace(DATA_PATH, ""))
        data_df["text"].append(input_text)
        data_df["HPO_symptoms"].append(symptoms)
        data_df["HPO_codes"].append(codes)
    df = pd.DataFrame(data_df, columns=["file", "text", "HPO_symptoms", "HPO_codes"])
    df.to_csv(path_or_buf=data_path)


if __name__ == "__main__":
    main("data/clinphen_gsc.csv")
