import pandas as pd
import chess.pgn

pgn = open('lidatafiltered', 'r')

gamedata = []

while True:
    game = chess.pgn.read_game(pgn)
    if not game:
        break
    gamedata.append({k: v for k, v in game.headers.items() if k in {'TimeControl', 'UTCDate'}})

def timeControlToClass(string):
    if string == "-":
        return "daily" # use chess.com names for consistency
    (start, inc) = map(int, string.split('+'))
    total = start + (40*inc)
    if total <= 29:
        return "ultraBullet"
    if total <= 179:
        return "bullet"
    if total <= 479:
        return "blitz"
    if total <= 1499:
        return "rapid"
    return "classical"

for game in gamedata:
    game['time_class'] = timeControlToClass(game['TimeControl'])

df = pd.DataFrame.from_dict(gamedata)
df.to_csv('lidataanalysed')
