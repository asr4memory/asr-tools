"""
Exporter functions.
"""
import csv
import json
from datetime import datetime

def write_vtt_file(output_file, custom_segs):
    """
    Write the processed segments to a VTT file.
    This file will contain the start and end times of each segment along with
    the transcribed text.
    """
    with open(output_file + '.vtt', "w", encoding='utf-8') as vtt_file:
        vtt_file.write("WEBVTT\n\n")
        for i, seg in enumerate(custom_segs):
            start_time = datetime.utcfromtimestamp(seg["start"]).strftime('%H:%M:%S.%f')[:-3]
            end_time = datetime.utcfromtimestamp(seg["end"]).strftime('%H:%M:%S.%f')[:-3]
            vtt_file.write(f"{i + 1}\n")
            vtt_file.write(f"{start_time} --> {end_time}\n")
            vtt_file.write(f"{seg['sentence']}\n\n")


def write_text_file(output_file, custom_segs):
    """
    Write the processed segments to a text file.
    This file will contain only the transcribed text of each segment.
    """
    with open(output_file + '.txt', "w", encoding='utf-8') as txt_file:
        for seg in custom_segs:
            if "sentence" in seg:
                txt_file.write(f"{seg['sentence']}\n")


def write_csv_file(output_file, custom_segs, delimiter=",",
                   speaker_column=False, write_header=False):
    """
    Write the processed segments to a CSV file.
    This file will contain the start timestamps of each segment in the
    first column, optionally an empty "SPEAKER" column, and the
    transcribed text of each segment in the last column.
    """
    filename_suffix = "_speaker.csv" if speaker_column else ".csv"
    fieldnames = (['IN', 'SPEAKER', 'TRANSCRIPT'] if speaker_column
                  else ['IN', 'TRANSCRIPT'])

    with open(output_file + filename_suffix, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                delimiter=delimiter)

        if write_header: writer.writeheader()

        for seg in custom_segs:
            timecode = "{:02}:{:02}:{:06.3f}".format(int(seg['start'] // 3600),
                                                     int((seg['start'] % 3600) // 60),
                                                     seg['start'] % 60)
            text = seg['sentence']
            row = {'IN': timecode, 'TRANSCRIPT': text}
            # Leave the "SPEAKER" column empty
            if speaker_column: row['SPEAKER'] = ''
            writer.writerow(row)


def write_json_file(filename, data):
    """Write a dictionary as a JSON file."""
    with open(filename + ".json", "w") as f:
        json.dump(data, f, indent=4)
