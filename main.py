# coding: UTF-8

import functions
import pandas as pd

def main():
    
    # set dates
    now = functions.now()
    
    dateA_s, dateB_s = functions.recentDates(now=now, A=4, B=1) # 4日前から1日前
    
    # get data
    df = functions.getdf(dateA_s, dateB_s)
    
    # search keywords
    kwds = ['Positivity',
            'Swampland',
            'Weak Gravity Conjecture',
            'distance conjecture',
            'holographic QCD',
           ] # 大文字小文字は区別なし
    
    # search and output
    df_hit = functions.search(df, kwds) # df_hit.csvに書き出し
    
    # log
    df_hit.to_csv('log.csv', index=False, header=False, mode='a') # 追記モード
    
    return

if __name__ == '__main__':
    main()
