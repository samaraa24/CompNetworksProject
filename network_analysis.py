import os
import datetime
import csv

def update_database(transfer_type, file_name, file_size, start_time, end_time):
    transfer_time = (end_time - start_time) / 1000000000
    file_size /= 1024

    if start_time != end_time:
        transfer_rate = file_size / transfer_time
    else:
        transfer_rate = 0

    start_time = datetime.datetime.fromtimestamp(start_time // 1000000000)
    
    data = {
        "File Name": file_name,
        "Transfer Type": transfer_type,
        "File Size (KB)": round(file_size, 1),
        "Start Time": start_time,
        "Elapsed Time (Seconds)": transfer_time,
        "Transfer Rate (KB/s)": transfer_rate
    }

    f = open("network_stats.csv", "a", newline = "")
    field_names = ["File Name", "Transfer Type", "File Size (KB)", "Start Time", "Elapsed Time (Seconds)", "Transfer Rate (KB/s)"]
    writer = csv.DictWriter(f, fieldnames = field_names)
    
    if os.path.getsize("network_stats.csv") == 0:
        writer.writeheader()

    writer.writerow(data)
