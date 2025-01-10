import pandas as pd

def A_generateDictionary(xlsx_file):
    """
    Load an Excel file and create a dictionary from the 'Link' column.

    Args:
        xlsx_file (str): Path to the Excel file.

    Returns:
        dict: Dictionary with indices as keys and links as values.
    """
    try:
        # Load the file as a DataFrame
        df_file = pd.read_excel(xlsx_file)
        print("File loaded successfully. Here's a preview of the data:")
        print(df_file.head())
        
        # Create a dictionary from the 'Link' column
        if 'Link' in df_file.columns:
            links_dictionary = {idx: link for idx, link in enumerate(df_file['Link'])}
            print("Links dictionary created successfully.")
        else:
            raise KeyError("The column 'Link' does not exist in the DataFrame.")
    except FileNotFoundError:
        print(f"Error: The file {xlsx_file} was not found.")
        return {}
    except KeyError as e:
        print(f"Error: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

    return links_dictionary


