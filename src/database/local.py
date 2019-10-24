def add_entry(data):
    with open("database.csv", "a") as f:
        f.write(str(data[0]) + ";" + str(data[1]) + ";" + str(data[2]) + ";" + str(data[3]) + ";" + str(data[4]))
