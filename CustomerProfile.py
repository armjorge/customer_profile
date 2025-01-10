
import os
import sys  # Required to modify the Python path dynamically.pd
script_directory = os.path.dirname(os.path.abspath(__file__))
working_folder = os.path.abspath(os.path.join(script_directory, '..'))
function_library = os.path.abspath(os.path.join(script_directory, 'Library'))
sys.path.append(function_library)  # Add the library folder to the path.
# Librerías internas
from A_Generate_dicts import A_generateDictionary
from B_extract_youtube_comments import B_extractcomments
from C_Common_dataframe import C_Commondataframe
from D_jobs import D1_Job_Class, D2_Job_type, D3_Job_context
from Youtube_API_load import youtube_load

def main():
    #Youtube client. 
    youtube = youtube_load(working_folder)
    if youtube:
        print("\nYouTube API client loaded successfully!\n")
    else:
        print("Failed to load YouTube API client.")
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
        
        
        B_extractcomments(links_dictionary, working_folder, 'OutputCSV1', youtube)
    if user_input == "2":    
        # Run the jobs extraction
        df_input = C_Commondataframe(csv_folder, outputfilename, working_folder)
    if user_input == "3":  
        D1_Job_Class(csv_folder)
        D2_Job_type(csv_folder)
        D3_Job_context(csv_folder)

    print("*******\nFinalizamos con éxito la script\n")
        
if __name__ == "__main__":
 main()