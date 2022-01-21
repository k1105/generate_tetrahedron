import math


def GetState(theta, phi):
    pi = math.pi

    if 0 <= theta < 2*pi:  # 定義域内であることの確認
        theta_num = int(theta / (pi / 4)) + 1
    else:
        print("theta error!")
        print(str(theta / pi) + "pi")

    if -pi/2 <= phi < pi/2:  # 定義域内であることの確認
        phi_num = int((phi + pi / 2) / (pi / 4)) + 1
    else:
        print("phi error!")

    if not 1 <= theta_num <= 8:
        print("theta_num error!")

    if not 1 <= phi_num <= 4:
        print("phi_num error!")

    state = theta_num + 8 * (phi_num - 1)  # 1 < state < 32

    return state
