def add_entry(data):
    with open("database.csv", "a") as f:
        f.write(data[0] + ";" + data[1] + ";" + data[2] + ";" + data[3] + ";" + data[4])
