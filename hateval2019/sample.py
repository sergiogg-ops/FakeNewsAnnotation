import pandas as pd
import ollama
from tqdm import tqdm

hateval = pd.read_csv('hateval2019_en_test.csv')

df = hateval[hateval['HS'] == 0].sample(15)
hateval['objetivo'] = ''
prompt = 'I am developing a study on hate speech. Please, answer only with the word women if the following tweet is hate speech against women or with inmigrants if the following tweet is hate speech against inmigrants. The tweet is:\n'
responses = [ollama.generate(model='llama3.1:8b', prompt=prompt + tweet)['response'] for tweet in tqdm(hateval[hateval['HS'] == 1]['text'])]
hateval.loc[hateval['HS'] == 1, 'objetivo'] = responses
women = hateval[(hateval['HS'] == 1) & (hateval['objetivo'].isin(['women','woman','Women','Woman']))]
inmigrants = hateval[(hateval['HS'] == 1) & (hateval['objetivo'].isin(['inmigrants','inmigrant','Inmigrants','Inmigrant']))]
hateval.to_json('pref_hateval.json', orient='records')
hateval = pd.concat([women.sample(10), inmigrants.sample(10), df])
hateval.to_json('hateval.json', orient='records', lines=True)