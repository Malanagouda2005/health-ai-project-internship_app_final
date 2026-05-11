import pandas as pd
df = pd.read_csv('data/raw/Training.csv')
diseases = sorted(df['prognosis'].unique())
print('Total diseases:', len(diseases))
print('Diseases:', diseases)