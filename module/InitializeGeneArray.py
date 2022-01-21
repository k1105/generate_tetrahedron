import random


def InitializeGeneArray():
    weight_list = [random.uniform(0.8, 1.2) for i in range(32)]
    theta_list = [random.randint(1, 8) for i in range(32)]
    phi_list = [random.randint(1, 8) for i in range(32)]

    return {"weight": weight_list, "theta": theta_list, "phi": phi_list}
