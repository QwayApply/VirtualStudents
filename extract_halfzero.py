import tabula

df = tabula.read_pdf('halfzero.pdf', pages='7')
print(type(df))
print(df[0].iloc[1])
print(df[0].iloc[2])
