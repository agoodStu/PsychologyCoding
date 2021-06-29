# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 13:50:50 2021

This is a script for calculating position gain,
which was defineded as the ratio of eye postion 
to target postion [1].

[1] Nkam, I., Bocca, M. L., Denise, P., Paoletti, X., Dollfus, S., Levillain, D., & Thibaut, F. (2010). Impaired smooth pursuit in schizophrenia results from prediction impairment only. Biological psychiatry, 67(10), 992-997.

@author: YejiShan
"""

import pandas as pd


df = pd.read_table('14-fast.txt')

participantID = [int(i[0:2]) for i in df['RECORDING_SESSION_LABEL']]

df['participant'] = participantID

out_df = pd.DataFrame()

# convert str to float, set invalid parsing as NaN
df['RIGHT_GAZE_X'] = pd.to_numeric(df['RIGHT_GAZE_X'], errors='coerce')
df['RIGHT_GAZE_Y'] = pd.to_numeric(df['RIGHT_GAZE_Y'], errors='coerce')
df['TARGET_X_target'] = pd.to_numeric(df['TARGET_X_target'], errors='coerce')
df['TARGET_Y_target'] = pd.to_numeric(df['TARGET_Y_target'], errors='coerce')

for i in df['participant'].unique():
    for trial in df['TRIAL_INDEX'].unique():
        select_df = df[(df['participant'] == i) & (df['TRIAL_INDEX'] == trial)]
        
    
        
        # calculate postion gain
        gain_h = select_df['RIGHT_GAZE_X'] / select_df['TARGET_X_target'] 
        gain_v = select_df['RIGHT_GAZE_Y'] / select_df['TARGET_Y_target']
        
        temp_df = pd.concat([select_df['participant'], select_df['TRIAL_INDEX'],
                             gain_h, gain_v], axis=1)
        
        out_df = pd.concat([out_df, temp_df])
        

columns = ['participantID', 'trailIndex', 'gain_h', 'gain_v']
out_df.columns = columns

out_df.to_csv('position-gain-14fast.txt', sep='\t', index=False)