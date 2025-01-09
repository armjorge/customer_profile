import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import re

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

def B_extractcomments(links_dictionary, working_folder, output_folder, youtube):
    # Function to process multiple links and save comments
    # Create the output folder if it doesn't exist
    output_path = os.path.join(working_folder, output_folder)
    os.makedirs(output_path, exist_ok=True)

    for index, link in links_dictionary.items():
        try:
            # Extract video ID from the YouTube URL
            video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else link.split("/")[-1].split("?")[0]
            print(f"Processing video ID: {video_id} for link: {link}")
            
            # Extract comments
            comments_df = B1_get_comments(video_id, youtube)
            
            # Save the comments to a CSV file
            output_file = os.path.join(output_path, f"{index}.csv")
            comments_df.to_csv(output_file, index=False)
            print(f"Comments for video {index} saved to {output_file}")
        except Exception as e:
            print(f"Failed to process link {link}: {e}")

def B1_get_comments(video_id, youtube, max_results=10000):
    # Function to extract comments from a single video
    comments = []

    # Fetch the video title
    video_request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    video_response = video_request.execute()
    video_title = video_response['items'][0]['snippet']['title'] if video_response['items'] else "Unknown Title"    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )

    while request:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'Author': comment['authorDisplayName'],
                'Comment': comment['textDisplay'],
                'Likes': comment['likeCount'],
                'PublishedAt': comment['publishedAt'],
                'VideoTitle': video_title  # Add the video title to each row                
            })

        # Check if there's another page of comments
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                pageToken=response['nextPageToken'],
                textFormat="plainText"
            )
        else:
            break

    return pd.DataFrame(comments)

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

def D1_Job_Class(csv_folder):
    print("\nA customer job could be:\n" )
    print("- The tasks they are trying  to perform and complete")
    print("the problems they  are trying to solve")
    print("the needs they are trying  to satisfy.\n")
    
def D2_Job_type(csv_folder):
    print("\nThe main types of  customer jobs to be done")
    print("1. Functional jobs  When your customers try to perform or complete  a specific task or solve a specific problem")
    print("2. Social jobs  When your customers want to look good or gain  power or status")
    print("3. Personal/emotional jobs  When your customers seek a specific emotional  state, such as feeling good or secure")
    print("\n...and supporting jobs:\n")
    print("1. BUYER OF VALUE: jobs related to buying  value, such as comparing offers")
    print("2. COCREATOR OF VALUE: jobs related to  cocreating value with your organization")
    print("3. TRANSFERRER OF VALUE: jobs related to the  end of a value proposition’s life cycle\n3")
def D3_Job_context(csv_folder):
    print("Job context To be developped")

def main():
    # Define working folder
    script_directory = os.path.dirname(os.path.abspath(__file__))
    working_folder = os.path.abspath(os.path.join(script_directory, '..'))
    # Define the file name and paths
    input_xlsx = os.path.join(working_folder, 'Key_videos.xlsx')
    output_csv = 'OutputCSV1'
    csv_folder = os.path.join(working_folder, output_csv)
    outputfilename = 'PenClip'
    #Ask the user    
    print("¿Qué deseas hacer?\n1. Extraer comentarios de la lista de archivos {input_xlsx}")
    print("2. Fusionar archivos CSV y generar un dataframe\n3. Procesar el CSV  \n")

    user_input = input("Ingrese el número de la opción: ")
    if user_input == "1":    
        # Generate the links dictionary
        links_dictionary = A_generateDictionary(input_xlsx)
        
        # Print the resulting dictionary
        print("Generated Links Dictionary:")
        print(links_dictionary)
            # Define the service account JSON key file path
        SERVICE_ACCOUNT_FILE = os.path.join(working_folder, 'armjorge.json')

        # Authenticate and build the YouTube API client
        SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        try:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            youtube = build("youtube", "v3", credentials=credentials)
        except FileNotFoundError:
            print(f"Service account file not found at {SERVICE_ACCOUNT_FILE}")
        except google.auth.exceptions.MalformedError as e:
            print(f"Malformed service account file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        B_extractcomments(links_dictionary, working_folder, 'OutputCSV1', youtube)
    if user_input == "2":    
        # Run the jobs extraction
        df_input = C_Commondataframe(csv_folder, outputfilename, working_folder)
    if user_input == "3":  
        D1_Job_Class(csv_folder)
        D2_Job_type(csv_folder)

    print("*******\nFinalizamos con éxito la script\n")
        
if __name__ == "__main__":
 main()