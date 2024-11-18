import pandas as pd

read_file = pd.read_excel ("SiC.xlsx")

read_file.to_csv ("sic.csv",
                  index = None,
                  header=True)
