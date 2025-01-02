import os
import pandas as pd

def main():
    # Define folder prefix
    folder_prefix = r'G:\My Drive\Projects\Pen Clip'
    
    # Define the file name
    file_xlsx = os.path.join(folder_prefix, 'Key_videos.xlsx')
    
    # Load the file as a DataFrame
    try:
        df_file = pd.read_excel(file_xlsx)
        # Display the head of the DataFrame
        print(df_file.head())
    except FileNotFoundError:
        print(f"Error: The file {file_xlsx} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
