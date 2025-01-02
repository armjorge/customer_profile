import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
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
                'PublishedAt': comment['publishedAt']
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

def C_Jobs(csv_folder, working_folder, output_jobs):
    """
    Process CSV files to extract comments classified as 'Jobs'.

    Args:
        csv_folder (str): Path to the folder containing CSV files.
        working_folder (str): Path to the working directory.
        output_jobs (str): Name of the output Excel file.

    Returns:
        DataFrame: Master DataFrame containing classified comments.
    """
    output_xlsx = os.path.join(working_folder, output_jobs)
    df_master = pd.DataFrame()  # Initialize an empty master DataFrame

    # Iterate through all CSV files in the folder
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith('.csv'):
            file_path = os.path.join(csv_folder, csv_file)
            input_df = pd.read_csv(file_path)

            # Classify comments
            input_df['Job'] = input_df['Comment'].apply(C1_classify_jobs)
            
            # Filter rows with 'Job'
            classified_df = input_df[input_df['Job'] == 'Job'].copy()
            classified_df['filename'] = csv_file  # Add filename column
            
            # Append to master DataFrame
            df_master = pd.concat([df_master, classified_df], ignore_index=True)

    # Save the master DataFrame to Excel
    df_master.to_excel(output_xlsx, index=False)
    print(f"Jobs analysis saved to {output_xlsx}")
    return df_master

def C1_classify_jobs(comment):
    """
    Analyze if a comment describes a task to be done, a problem to be solved,
    or a need to be satisfied (Jobs in Value Proposition Design).

    Args:
        comment (str): The comment text to analyze.

    Returns:
        str: 'Job' if the comment matches the criteria, otherwise an empty string.
    """
    keywords = ['task', 'problem', 'solve', 'need', 'requirement', 'goal', 'objective']
    if any(keyword in comment.lower() for keyword in keywords):
        return 'Job'
    return ''


def main():
    # Define working folder
    working_folder = r'G:\My Drive\Projects\Pen Clip'
    # Define the file name
    input_xlsx = os.path.join(working_folder, 'Key_videos.xlsx')
    
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

    csv_folder = os.path.join(working_folder, 'OutputCSV1')
    output_jobs = 'Jobs.xlsx'

    # Run the jobs extraction
    df_jobs = C_Jobs(csv_folder, working_folder, output_jobs)
        
if __name__ == "__main__":
 main()