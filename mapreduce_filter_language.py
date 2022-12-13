# import files one by one
# filter the language of the file based on the argument n°1
# eval column viewer
# explode column viewer
# group by ['viewer', 'langage']

# python mapreduce_filter_language.py <language>
# python mapreduce_filter_language.py fr
# python mapreduce_filter_language.py en

import pandas as pd
import sys

for i in range(1, 31):
    df = pd.read_csv('data\World2022-04-' + str(i) + '.csv', header=None)
    df.columns = ['viewers', 'streamer', 'date', 'category', 'viewership', 'language']
    df = df[df['language'] == sys.argv[1]]
    # eval column viewers
    df['viewers'] = df['viewers'].apply(eval)
    # explode column viewers
    df = df.explode('viewers')
    # group by ['viewer', 'langage']
    df = df.groupby(['viewers', 'streamer', 'category']).size().reset_index(name='counts')
    # reject viewers with less than 10 viewers
    df = df[df['counts'] > 10]
    # save the file
    df.to_csv('output\World2022-04-' + str(i) + '-' + sys.argv[1] + '.csv', index=False)

# clear memory
del df

# load the files
# map reduce them
# save the file

import pandas as pd
import glob
import sys

# load the files
path = r'output'
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
df = pd.concat(li, axis=0, ignore_index=True)

# map reduce them
df = df.groupby(['viewers', 'streamer', 'category']).sum().reset_index()

# save the file
df.to_csv('graph\\final_' + sys.argv[1] + '.csv', index=False)