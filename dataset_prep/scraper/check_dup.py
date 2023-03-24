
import requests, sys, time, os, argparse, csv
from datetime import date


def check_dup(file_name1, file_name2):

    id_set = set()

    with open(file_name1) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        row_count = 0
        output_count = 0
        
        for row in csv_reader:
            if (row[0] in id_set):
                print(row[0])
            
            
            id_set.add(row[0])


    with open(file_name2) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        row_count = 0
        output_count = 0
        
        for row in csv_reader:
            if (row[0] in id_set):
                print(row[0])
            
            
            id_set.add(row[0])
        

    #print(id_set)
        

if __name__ == "__main__":
    #api_key = setup("api_key.txt")

    check_dup("US_youtube_trending_data_trim.csv", "US_youtube_nontrending_data_trim.csv")


