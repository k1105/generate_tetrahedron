import csv


def InitializeGeneArrayViaCSV(file_path):
    weight_list = []
    theta_list = []
    phi_list = []
    with open(file_path) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                weight_list.append(float(row[1]))
                theta_list.append(int(row[2]))
                phi_list.append(int(row[3]))
            i += 1

    return {"weight": weight_list, "theta": theta_list, "phi": phi_list}
