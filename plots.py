import pandas as pd
import matplotlib.pyplot as plt

# chess.com data reformating
ccdf = pd.read_csv('ccdataanalysed')
ccdf['day'] = pd.to_datetime(ccdf['end_time'], unit='s').dt.date
ccdf.drop_duplicates(subset=['url'])
ccdf = ccdf.drop(columns=['end_time', 'url'])
cc_pivot = ccdf.pivot_table(index='day', values='time_control', columns='time_class', aggfunc='count')

# lichess.org data reformating
lidf = pd.read_csv('lidataanalysed')
lidf['day'] = pd.to_datetime(lidf['UTCDate']).dt.date
lidf = lidf.rename(columns={'TimeControl': 'time_control'})
lidf = lidf.drop(columns=['UTCDate'])
li_pivot = lidf.pivot_table(index='day', values='time_control', columns='time_class', aggfunc='count')

# time estimates
# I used the lichess time controls https://lichess.org/faq#time-controls and assumed that 1/2 time used on average
# rapid time estimate used for daily/correspondence
def timeConvert(df):
    time_conversions = {'ultraBullet': 30, 'bullet': 180, 'blitz': 480, 'rapid': 1500, 'classical': 3000, 'daily': 1500}
    new_df = df.copy()
    for column in new_df:
        new_df[column] = (time_conversions[column] * new_df[column]) / (60*60) # hours
    return new_df

def plotData(df1, df1source, df2, df2source, title):
    fig, axs = plt.subplots(2, sharex=True, sharey=True)

    color_dict = {'ultraBullet': 'tab:orange', 'bullet':'tab:blue', 'blitz': 'tab:red', 'rapid':'blue', 'classical': 'tab:olive', 'daily': 'purple'}
    df1.plot.bar(ax=axs[0],stacked=True, color=color_dict, legend=None)
    axs[0].title.set_text(df1source)
    df2.plot.bar(ax=axs[1],stacked=True, color=color_dict, legend=None)
    axs[1].title.set_text(df2source)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys())
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

#plotData(cc_pivot, 'chess.com', li_pivot, 'lichess.org', 'Grandmaster games on chess.com vs lichess.org')
plotData(timeConvert(cc_pivot), 'chess.com', timeConvert(li_pivot), 'lichess.org', 'Grandmaster hours on chess.com vs lichess.org')
