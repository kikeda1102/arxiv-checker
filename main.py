# coding: UTF-8

import functions
import pandas as pd
import datetime

def main():
    
    # set date
    
    now = functions.now()
    
    dateA_s, dateB_s = functions.recentDates(now=now, A=3, B=0) # 3日前から0日前で検索
    
    # get data
    df = functions.getdf(dateA_s, dateB_s)
    
    # search keywords
    kwds = [
        'Regge',
        'EFT',
        'Positivity',
        'Swampland',
        'Weak Gravity Conjecture',
        'distance conjecture',
        'holographic QCD',
        'landscape',
    ] # 大文字小文字は区別せず検索される
    
    # search
    df_hit = functions.search(df, kwds)
    
    # attach current date
    df_hit.insert(loc = 0, column= 'AcquisitionDate', value = functions.now().date())
    
    # output log
    # df_hit.to_csv('log.csv', index=False, header=True, mode='w') # 上書きモード, headerあり
    df_hit.to_csv('log.csv', index=False, header=False, mode='a') # 追記モード, headerなし
    
    # resolve duplication of log
    df = pd.read_csv('log.csv')
    df2 = df[~df.duplicated()]
    df2.to_csv('log.csv', index=False, header=True, mode='w')
    
    return

if __name__ == '__main__':
    main()
