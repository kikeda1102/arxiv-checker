# coding: UTF-8

import arxiv
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


def recentDates():
    '''
    return two recent dates from today's date (JST)
    '''
    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差
    now = datetime.datetime.now(JST)
    
    dateA = now + datetime.timedelta(days=-4) # 4日前
    dateB = now + datetime.timedelta(days=-1) # 1日前
    
    dateA_s = str(dateA.year) + str(dateA.month).zfill(2) + str(dateA.day).zfill(2)
    dateB_s = str(dateB.year) + str(dateB.month).zfill(2) + str(dateB.day).zfill(2)
    
    return dateA_s, dateB_s
    
def getdf(dateA_s, dateB_s):
    '''
    get data by arxiv package
    '''
    search = arxiv.Search(
        query = f'cat:hep-th AND submittedDate:[{dateA_s} TO {dateB_s}235959]',
        max_results = 100,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )
    
    # pack into df
    title = []
    publishedDate = []
    authors = []
    abstract = []
    
    for result in search.results():
        title.append(result.title)
        publishedDate.append(result.published)
        authors.append(result.authors)
        abstract.append(result.summary)
    
    # make df
    df = pd.DataFrame(columns=['title','publishedDate','authors','abstract'])
    df['title'] = title
    df['publishedDate'] = publishedDate
    df['authors'] = authors
    df['abstract'] = abstract
    
    return df

    
def search(df, kwds):
    '''
    search by keywords
    '''
    
    df2 = pd.DataFrame()
    
    # search
    if len(df) != 0: # 土日は更新なしなのでHitしない
        for i in range(len(kwds)):
            df2[i] = df['abstract'].str.contains(kwds[i], case=False) # 大文字小文字区別無しで検索

    # make flag
    flag = []
    for i in range(len(df2)):
        flag.append( any( df2.iloc[i, :] ) ) # 1つでもtrueならtrue

    df['flag'] = flag

    df_hit = df[ df['flag'] ] # filter

    df_hit.to_csv('df_hit.csv', index=False)
    
    return


