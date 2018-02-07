#!/usr/bin/python

# import packages
import numpy as np
import pandas as pd
import sys
import math


def main():
    input_fn = sys.argv[1]
    output_q1_fn = sys.argv[2]
    output_q2_fn = sys.argv[3]

    data = pd.read_table(input_fn, header=None, sep='|', usecols=[0,10,13,14,15], 
                         dtype={10: str, 13: str})

    # set column names
    data.columns = ["CMTE_ID","ZIP_CODE","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID"]

    # # create dictionary
    d1 = {}
    # CMTE_ID|ZIP_CODE|MEDIAN|#OFRECORDS(length of list)|SUMOFAMOUNT(sum of list)
    result1 = pd.DataFrame(columns=['CMTE_ID', 'ZIP_CODE','MEDIAN','COUNT','SUM'])   
    row_index = 0
    for i in range(len(data)): # read in one line
        # check if it is valid row or not: the length and the format of CMTE_ID,
        # the lenght of ZIP_CODE, if TRANSACTION_AMT is empty, if OTHER_ID is not empty
        if len(data.iloc[i,][0])!=9 or data.iloc[i,][0][:3]!='C00' or \
                str(data.iloc[i,][1])=='nan' or len(data.iloc[i,][1])<5 or \
                (data.iloc[i,][3] is None) or not str(data.iloc[i,][4])=='nan':
            continue
        else:
            # get name,zipcode,date, amount from this row
            name = data.iloc[i,][0]
            zipcode = data.iloc[i,][1][:5]
            amount = data.iloc[i,][3]
            
            # put new line into the data structure
            if name not in d1.keys():
                d1[name] = {}
                d1[name][zipcode] = [amount]
            else:
                if zipcode not in d1[name].keys():
                    d1[name][zipcode] = [amount]
                else:
                    d1[name][zipcode].append(amount)

            # compute result and save into df
            result1.loc[row_index] = [name, zipcode, math.ceil(np.median(d1[name][zipcode])),
                                        len(d1[name][zipcode]),sum(d1[name][zipcode])]
            row_index += 1

    # write into file for one line
    np.savetxt(output_q1_fn, result1.values, fmt='%s|%s|%d|%d|%d', delimiter='|')


    # 2nd question
    d2 = {}
    # CMTE_ID|ZIP_CODE|MEDIAN|#OFRECORDS(length of list)|SUMOFAMOUNT(sum of list)
    result2 = pd.DataFrame(columns=['CMTE_ID', 'TRANSACTION_DT','MEDIAN','COUNT','SUM'])
    for i in range(len(data)):
        # check if it is valid row or not
        # check the length and the format of CMTE_ID
        # check the lenght of TRANSACTION_DT
        # check if TRANSACTION_AMT is empty
        # check if OTHER_ID is not empty
        if len(data.iloc[i,][0])!=9 or data.iloc[i,][0][:3]!='C00' or \
                len(data.iloc[i,][2])>8 or (data.iloc[i,][3] is None) or \
                not str(data.iloc[i,][4])=='nan':
            continue
        else:
            # get name,zipcode,date, amount from this row
            name = data.iloc[i,][0]
            date = data.iloc[i,][2]
            amount = data.iloc[i,][3]
            
            # put new line into the data structure
            if name not in d2.keys():
                d2[name] = {}
                d2[name][date] = [amount]
            else:
                if date not in d2[name].keys():
                    d2[name][date] = [amount]
                else:
                    d2[name][date].append(amount)
    
    # prepare output file
    # sort d2.keys(), and for every value, re-sort based on date
    # then prepare output files
    j = 0
    for name in sorted(d2):
        for date in sorted(d2[name]):
            result2.loc[j] = [name, date, math.ceil(np.median(d2[name][date])),
                                  len(d2[name][date]),sum(d2[name][date])]
            j += 1
    
    # save as txt file
    np.savetxt(output_q2_fn, result2.values, fmt='%s|%s|%d|%d|%d', delimiter='|')

if __name__ == '__main__':
    main()

