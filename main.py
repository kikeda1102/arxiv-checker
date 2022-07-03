# coding: UTF-8

import functions

def main():
    
    # set dates
    dateA_s, dateB_s = functions.recentDates() # 対象範囲の日付
    
    # get data
    df = functions.getdf(dateA_s, dateB_s)
    
    # search keywords
    kwds = ['Positivity',
            'Swampland',
            'Weak Gravity Conjecture',
            'distance conjecture',
            'completeness hypothesis',
            'Sugimoto',
            'quantum gravity',
           ] # 大文字小文字は区別なし
    
    # search and output
    functions.search(df, kwds) # df_hit.csvに書き出し
    
    return

if __name__ == '__main__':
    main()
