from clinphen_src import get_phenotypes, src_dir
import glob

def load_common_phenotypes(commonFile):
    returnSet = set()
    for line in open(commonFile): returnSet.add(line.strip())
    return returnSet

def get_names():
    srcDir = src_dir.get_src_dir()
    hpo_main_names = srcDir + "/data/hpo_term_names.txt"
    returnMap = {}
    for line in open(hpo_main_names):
      lineData = line.strip().split("\t")
      returnMap[lineData[0]] = lineData[1]
    return returnMap

def main(text_path):
    hpo_names = get_names()
    text_files = glob.glob(text_path + "*")
    for text in text_files:
        input_text = ""
        for line in open(text): input_text += line
        returnString = get_phenotypes.extract_phenotypes(input_text, hpo_names)
        print(text)
        print(returnString)
        break

if __name__ == "__main__":
    text_path = "Text/"
    main(text_path)