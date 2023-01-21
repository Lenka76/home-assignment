import glob
import pandas as pd


folder_path = 'C:\\your\\path\\to\\folder'
for file_name in glob.glob(folder_path +'\*.csv'):

    #assuming that all .csv files have headers
    df = pd.read_csv(file_name, usecols=['ColumnA', 'ColumnB'])
    
    #sum values of ColumnA if requirement for ColumnB is met
    sum_of_columnA = df.loc[df['ColumnB'] == 'needed_value', 'ColumnA'].sum()
    print(sum_of_columnA)
