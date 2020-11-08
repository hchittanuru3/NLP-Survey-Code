import glob
import pandas as pd

def main(anno_path: str, text_path: str):
    anno_files = glob.glob(anno_path + "*")
    for anno in anno_files:
        with open(anno, "r") as f:
            print(f.read())
        break

if __name__ == "__main__":
    anno_path = "Annotations/"
    text_path = "Text/"
    main(anno_path, text_path)
