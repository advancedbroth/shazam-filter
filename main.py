import asyncio
import os
import shutil
from shazamio import Shazam

async def recognize_mp3(file_path, recognized_folder, unrecognized_folder, output_file):
    shazam = Shazam()
    try:
        out = await shazam.recognize_song(file_path)
        recognized_info = f"Recognized song in '{os.path.basename(file_path)}': {out['track']['title']} - {out['track']['subtitle']}\n"
        print(recognized_info)
        output_file.write(recognized_info)
        # Move recognized files to recognized_folder
        shutil.move(file_path, os.path.join(recognized_folder, os.path.basename(file_path)))
    except Exception as e:
        error_info = f"Error recognizing '{os.path.basename(file_path)}': {e}\n"
        print(error_info)
        output_file.write(error_info)
        # Move unrecognized files to unrecognized_folder
        shutil.move(file_path, os.path.join(unrecognized_folder, os.path.basename(file_path)))

async def process_folder(folder_path, recognized_folder, unrecognized_folder, output_file):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        return

    if not os.path.exists(recognized_folder):
        os.makedirs(recognized_folder)

    if not os.path.exists(unrecognized_folder):
        os.makedirs(unrecognized_folder)

    files = os.listdir(folder_path)
    mp3_files = [file for file in files if file.lower().endswith('.mp3')]

    tasks = []
    for mp3_file in mp3_files:
        file_path = os.path.join(folder_path, mp3_file)
        tasks.append(recognize_mp3(file_path, recognized_folder, unrecognized_folder, output_file))

    await asyncio.gather(*tasks)

async def main():
    folder_path = 'songs'  # Replace with the path to your folder containing MP3s
    recognized_folder = 'recognized'  # Replace with path to store recognized songs
    unrecognized_folder = 'unrecognized'  # Replace with path to store unrecognized songs
    output_file_path = 'output.txt'  # Replace with the path where you want to save the output file

    with open(output_file_path, 'w') as output_file:
        await process_folder(folder_path, recognized_folder, unrecognized_folder, output_file)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
