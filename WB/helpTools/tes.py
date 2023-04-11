import pandas as pd

df = pd.DataFrame(pd.read_excel(r"E:\Downloads\Караханян от 03.04.2023.xlsx"))
df = df.groupby(['Артикул'])['Продажи'].sum().reset_index()
df.to_excel(r"E:\Downloads\cons2.xlsx", index=False)