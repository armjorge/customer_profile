
import pandas as pd
import os


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