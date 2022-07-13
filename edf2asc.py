# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 16:03:32 2022

@author: Ye JiShan
"""

import os ; import subprocess ; 


def edfConvert(convert_path, edf_folder):
    """
    
    Parameters
    ----------
    convert_path : string
        The path of 'edfconverterW.exe'.
        e.g. r'C:\Program Files\SR Research\edfconverter'
    edf_folder : string
        The path of EDF folder.
        e.g. r'F:\Ye\data\adhd\test'

    Returns
    -------
    None.

    """
    cmd = convert_path + r'\edfconverterW.exe'
    for root, dirs, files in os.walk(edf_folder) :
        for file in files:
            if file.endswith('.EDF'):
                asc_file = file.split('.')[0] + '.asc'
                asc_file_path = os.path.join(root, asc_file)
                edf_path = os.path.join(root, file)
                if not os.path.isfile(asc_file_path):
                    print("-------- " + file + ' is converting. --------')
                    subprocess.run([cmd, edf_path])
                else:
                    print("-------- " + file + ' is already exist. --------')
                    
     

if __name__ == '__main__':
e    edfConvert(r'C:\Program Files\SR Research\edfconverter', r'F:\Ye\data\adhd\eyeData\\fixationStability')
