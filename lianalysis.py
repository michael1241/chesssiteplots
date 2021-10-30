import re
import bz2
from tqdm import tqdm
import sys
#data from https://database.lichess.org/ September 2021

gm = re.compile(r'\[(?:White|Black)Title "GM"\]')

#with bz2.open('lichesssep21.pgn.bz2', 'rb') as f:
f = sys.stdin
with open('lidatafiltered', 'w') as w:
    stored_lines = []
    gm_flag = False
    for line in tqdm(f, total=88133339*20): #number of games times row estimate
        stored_lines.append(line)
        if gm.match(line):
            gm_flag = True
        if line == '\n' and gm_flag:
            w.write(''.join(stored_lines))
            w.write('\n')
            stored_lines = []
            gm_flag = False
        elif line == '\n':
            stored_lines = []

