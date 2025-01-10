
import os
import pandas as pd
import re

def C_Commondataframe(csv_folder, filename, outputfolder):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the folder.")
        return None
    
    # Initialize the dataframe with the first file
    first_file = csv_files[0]
    dataframe = pd.read_csv(os.path.join(csv_folder, first_file))
    all_headers = dataframe.columns.tolist()
    
    # Iterate through the rest of the CSV files
    for csv_file in csv_files[1:]:
        file_path = os.path.join(csv_folder, csv_file)
        temp_df = pd.read_csv(file_path)
        
        # Check headers
        if temp_df.columns.tolist() != all_headers:
            print(f"Warning: Headers in {csv_file} do not match {first_file}. Exiting.")
            return None
        
        # Append to the dataframe without headers
        dataframe = pd.concat([dataframe, temp_df], ignore_index=True)
    
    # Add new columns
    dataframe['Job_Class'] = ''
    dataframe['Job_Types'] = ''
    dataframe['Job_Context'] = ''
    def remove_empty_line_breaks(comment):
        # Replace two or more line breaks with a single line break
        return re.sub(r'\n\s*\n', '\n', comment)

    # Apply the function to the 'Comment' column
    dataframe['Comment'] = dataframe['Comment'].apply(remove_empty_line_breaks)

    # Save the dataframe
    output_path = os.path.join(outputfolder, f"{filename}_workingdata.csv")
    dataframe.to_csv(output_path, index=False)
    
    # Print the first few rows of the dataframe
    print(dataframe.head())
    
    return dataframe
