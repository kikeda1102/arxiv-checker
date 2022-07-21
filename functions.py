# coding: UTF-8

import arxiv
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


def now():
    '''
    return datetime on now
    '''
    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差
    now = datetime.datetime.now(JST)
    
    return now

def recentDates(now, A,B):
    '''
    return two recent dates from today's date (JST)
    '''
    
    # recent dates
    dateA = now + datetime.timedelta(days=-A) # A日前
    dateB = now + datetime.timedelta(days=-B) # B日前
    
    dateA_s = str(dateA.year) + str(dateA.month).zfill(2) + str(dateA.day).zfill(2)
    dateB_s = str(dateB.year) + str(dateB.month).zfill(2) + str(dateB.day).zfill(2)
    
    return dateA_s, dateB_s
    
def getdf(dateA_s, dateB_s):
    '''
    get data by arxiv package
    '''
    
    search = arxiv.Search(
        query = f'cat:hep-th AND submittedDate:[{dateA_s} TO {dateB_s}235959]',
        max_results = 200,
        sort_by = arxiv.SortCriterion.SubmittedDate,
    )
    
    # pack into df
    link = []
    title = []
    publishedDate = []
    authors = []
    abstract = []
    
    for result in search.results():
        link.append(result.entry_id)
        title.append(result.title)
        publishedDate.append(result.published)
        authors.append(result.authors)
        abstract.append(result.summary)
    
    # make df
    df = pd.DataFrame(columns=['link','title','publishedDate','authors','abstract'])
    df['link'] = link
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
            df2[f'Key_{kwds[i]}'] = df['abstract'].str.contains(kwds[i], case=False) # 大文字小文字区別無しで検索

    # make flag
    flag = []
    for i in range(len(df2)):
        flag.append( any( df2.iloc[i, :] ) ) # 1つでもtrueならtrue

    df3 = pd.concat([df,df2], axis=1)
    df3['anyKey'] = flag

    df_hit = df3[ df3['anyKey'] ] # filter    
    df_hit2 = df_hit.drop({'anyKey','abstract'},axis=1)
    
    return df_hit2


