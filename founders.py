import zipfile
import os 
import pandas as pd

filepath = 'Python/KS/Exports/'
final_csv_path = 'Python/KS/founderlist.csv'

os.listdir()

files = [entry.name for entry in os.scandir(filepath)]
#print(files)

rolelist = ['founder, director'] # , 'chief','executive','officer', 'partner','entrepreneur','pioneer','board']
for letter in 'ABCDEFGIJKLMNOPQRSTUVWXYZ': 
    rolelist.append(f'C{letter}O')
#print(rolelist)
all_roles = '|'.join(rolelist)


#### Toggle for finding presidents 
# all_roles = 'president'

#### Toggle for VCs 
#all_roles = 'vc|venture|capital| '

all_filtered_dfs = []

for file in files:
    if file.endswith('.zip'): 
        zip_path = os.path.join(filepath, file)
        with zipfile.ZipFile(str(zip_path), 'r') as zip_file:
            file_list = zip_file.namelist()  # Get all files inside the ZIP
            print(f'Contents of {file}: {file_list}')
            if file_list[0].endswith('.csv'):
                #print(file_list[0])
                with zip_file.open(file_list[0], 'r') as csv_file:
                    #print(type(csv_file))
                    unfiltered_df=pd.read_csv(csv_file, sep=None,engine='python', skiprows=3,encoding='utf-8')
                    df = unfiltered_df[unfiltered_df.apply(lambda row: row.count() + row.isna().sum() == 7, axis=1)]
                    
                    #### Toggle for all connections 
                    filtered_df = df[df['Position'].str.contains(all_roles, case=False, na=False)]
                    #filtered_df = df
                    
                    filtered_df['PersonFile'] = file
                    all_filtered_dfs.append(filtered_df)
                    print(f'Total Number of Connectios: {len(unfiltered_df)}')
                    print(f'Total Number of Valid Rows : {len(df)}') # right number of columns 
                    print(f'Total Number of Founders: {len(filtered_df)}')
                    print(f'Added to list - length: {len(all_filtered_dfs)}')


                    # filtered_lines = [line.strip().split(',') for line in raw_text if line.count(',') == 6]
                    # print(len(filtered_lines))
                    # print(type(filtered_lines))
                    # print(filtered_lines[0])
                    # filtered_lines.pop(0)
                    # df = pd.DataFrame(filtered_lines, columns=['First Name','Last Name','URL','Email Address','Company','Position','Connected On'])
                    # filtered_df = df[df['Position'].str.contains(all_roles, case=False, na=False)]
                    # all_filtered_dfs.append(filtered_df)



        # Convert the filtered lines into a DataFrame
        # df = pd.read_csv(pd.io.common.StringIO('\n'.join(filtered_lines)), sep=',', skiprows=3, encoding='utf-8', engine='python')
        
        #df=pd.read_csv(csv_path, sep=None,engine='python', skiprows=3,encoding='utf-8')
                    
        #filtered_df['PersonFile'] = file #allocated name of file as column
                    

                    #print(filtered_df.head())
                    #print(filtered_df.columns)
                    # print(len(df))
                    # print(len(filtered_df))
                    # print(len(all_filtered_dfs))
    if file.endswith('.csv'):
        csv_path = os.path.join(filepath, file) 
        print(f'\n{csv_path}')

        with open(csv_path, 'r', encoding='utf-8') as raw_text:
            filtered_lines = [line.strip().split(',') for line in raw_text if line.count(',') == 6]
            print(f'Total Number of Connectios: {len(filtered_lines)}')
            #print(type(filtered_lines))
            #print(filtered_lines[0])
            filtered_lines.pop(0)
            df = pd.DataFrame(filtered_lines, columns=['First Name','Last Name','URL','Email Address','Company','Position','Connected On'])

        # Convert the filtered lines into a DataFrame
        # df = pd.read_csv(pd.io.common.StringIO('\n'.join(filtered_lines)), sep=',', skiprows=3, encoding='utf-8', engine='python')
        
        #df=pd.read_csv(csv_path, sep=None,engine='python', skiprows=3,encoding='utf-8')
        
        #### Toggle for all connections 
        filtered_df = df[df['Position'].str.contains(all_roles, case=False, na=False)]
        #filtered_df = df
        
        filtered_df['PersonFile'] = file
        #filtered_df['PersonFile'] = file #allocated name of file as column
        all_filtered_dfs.append(filtered_df)
        #print(filtered_df.head())
        #print(filtered_df.columns)
        print(f'Total Number of Valid Rows : {len(df)}') # right number of columns 
        print(f'Total Number of Founders: {len(filtered_df)}')
        print(f'Added to list - length: {len(all_filtered_dfs)}')
    # if file.endswith('l.csv'): 
    #     csv_path = os.path.join(filepath, file)
    #     print(csv_path)
    #     df=pd.read_csv(csv_path, sep=None,engine='python', skiprows=3,encoding='utf-8')
    #     filtered_df = df[df['Position'].str.contains(all_roles, case=False, na=False)]
    #     #filtered_df['PersonFile'] = file #allocated name of file as column
    #     #all_filtered_dfs.append(filtered_df)
    #     #print(filtered_df.head())
    #     #print(filtered_df.columns)
    #     print(len(df))
    #     print(len(filtered_df))
    #     print(len(all_filtered_dfs))

final_df = pd.concat(all_filtered_dfs, ignore_index=True)

print(f'Total number of founders (with duplicates): {len(final_df)}')

final_df = final_df.drop_duplicates(subset=['URL'], keep='first')


print(f'Total number of founders (w/o duplicates): {len(final_df)}')

with open(final_csv_path, "w", encoding='utf-8') as file:
    #file.write('First Name,Last Name,URL,Email Address,Company,Position,Connected On,,\n')
    for index, row in final_df.iterrows():
        file.write(','.join(map(str, row.values)) + '\n')
