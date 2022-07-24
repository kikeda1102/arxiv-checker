# coding: UTF-8

import functions
import pandas as pd
import datetime

def main():
    
    # set date
    
    now = functions.now()
    
    dateA_s, dateB_s = functions.recentDates(now=now, A=7, B=0) # A日前からB日前で検索
    
    # get data
    df = functions.getdf(dateA_s=dateA_s, dateB_s=dateB_s, max_results=300)
    
    # search keywords
    kwds = [
        'dispersion relation',
        'distance conjecture',
        'EFT',
        'holographic QCD',
        'landscape',
        'Positivity',
        'Regge',
        'Swampland',
        'Weak Gravity',
    ] # 大文字小文字は区別せず検索される
    
    # search
    df_hit = functions.search(df, kwds)
    
    # attach current date
    df_hit.insert(loc = 0, column= 'AcquisitionDate', value = functions.now().date())
    
    # read log
    df_log = pd.read_csv('log.csv')
    
    # concat log and df_hit
    df_out = pd.concat( [ df_hit, df_log ], axis=0 )
    
    # resolve duplications
    df_out2 = df_out[~df_out.duplicated(subset=['title','authors'])] # タイトルと著者が一致する論文は重複とみなしdrop
    
    # output
    df_out2.to_csv('log.csv', index=False, header=True, mode='w') # 上書きモード, headerあり
    # df_out2.to_csv('log.csv', index=False, header=False, mode='a') # 追記モード, headerなし
    
    
    return

if __name__ == '__main__':
    main()
