#!/usr/bin/enc python
# -*- coding:utf-8 -*-

import os, sys, random
import matplotlib.pyplot as plt
import math

# Description: This python file aims to simulate the procedure of mixed content replication design on roadside units for vehicular networks

# Initialization of configurations
# The number of chunks of the file
m = 5000

# The number of RSUs
n = 5000

# The capacity of RSU depicted with chunks
B = 100

# The number of chunks the car can collect each time
d = 60

# the value of rho
rho = 2

# The overall versions of the file
whole_version = 3

# The replication of encoded chunks, which can be adjusted
w = 0

# The chunks of the original file, which can be adjusted
l = 0

# The bitmap to represent the missing/downloaded chunks
m_bit = [0] * m

# if whole_version = 3, B = 100M, then the bitrate of each chunk: (Mbps) (which can make sure that the number of encoded chunks would be equal, and these parameter can be adjusted)
bitrate_1 = 1
bitrate_2 = 0.7
bitrate_3 = 0.3


# Calculate the maximal step to download the whole file(Assume d is a maximum, >= 100)
def cal_maximal_step(w, l, m=5000):
    # initialization of placement of original chunks
    original_placement = []
    for i in range(m):
        o_temp = set()
        count = 0
        while count < l:
            value = random.randint(0, m - 1)
            if value not in o_temp:
                count = count + 1
                o_temp.add(value)
        original_placement.append(o_temp)
    # print(original_placement)

    m_bit = [0] * m

    max_step = 0

    all_downloaded = 0
    for i in range(m):
        o_temp = original_placement[i]
        for item in o_temp:
            m_bit[item] = 1
        all_downloaded = sum(m_bit) + (i + 1) * w

        if all_downloaded >= m:
            max_step = i + 1
            break

    return max_step


# simulation of the maximal step (d is limited)
def cal_limited_step(w, l, d):
    # initialization of placement of original chunks
    original_placement = []
    for i in range(m):
        o_temp = set()
        count = 0
        while count < l:
            value = random.randint(0, m - 1)
            if value not in o_temp:
                count = count + 1
                o_temp.add(value)
        original_placement.append(o_temp)
    # print(original_placement)

    m_bit = [0] * m

    max_step = 0

    return_list = [m] * m

    all_downloaded = 0
    for i in range(m):
        pre_sum_bit = sum(m_bit)
        o_temp = original_placement[i]
        count = 0
        for item in o_temp:
            if m_bit[item] == 0:
                m_bit[item] = 1
                count = count + 1
            if count >= d:
                break
        after_sum_bit = sum(m_bit)
        change_bit = after_sum_bit - pre_sum_bit

        if i == 0:
            return_list[i] = change_bit + d - change_bit
        else:
            return_list[i] = return_list[i - 1] + min(w, d - change_bit) + change_bit

        if return_list[i] >= m:
            return_list[i] = m
            max_step = i + 1
            break

    return return_list, max_step


# calculate the verifying result (simulation procedure. Equation (4), (5-6),(8-9),(10-11)) Fig.6,7,8
def partial_run():
    # Fig.6, w=0, l=100, d=60
    with open("partial_limited_origin.csv", 'w') as f_e:
        print("limited origin:")
        times = 100
        ED = [0] * 5000
        f_e.write(str(0) + '\n')
        for j in range(times):
            print("Times:", j)
            w = 0
            l = 100
            d = 60
            return_list, _ = cal_limited_step(w, l, d)
            for i in range(5000):
                ED[i] = ED[i] + return_list[i]
        for i in range(5000):
            ED[i] = ED[i] / float(times)
            f_e.write(str(ED[i]) + '\n')

    # Fig.7, w=30, l=40, d=60
    with open("partial_unlimited_encoded.csv", 'w') as f_e:
        print("limited mixed 1:")
        times = 100
        ED = [0] * 5000
        f_e.write(str(0) + '\n')
        for j in range(times):
            print("Times:", j)
            w = 30
            l = 40
            d = 60
            return_list, _ = cal_limited_step(w, l, d)
            for i in range(5000):
                ED[i] = ED[i] + return_list[i]
        for i in range(5000):
            ED[i] = ED[i] / float(times)
            f_e.write(str(ED[i]) + '\n')

    # Fig.8, w=20, l=60, d=50
    with open("partial_limited_encoded.csv", 'w') as f_e:
        print("limited mixed 2:")
        times = 100
        ED = [0] * 5000
        f_e.write(str(0) + '\n')
        for j in range(times):
            print("Times:", j)
            w = 20
            l = 60
            d = 50
            return_list, _ = cal_limited_step(w, l, d)
            for i in range(5000):
                ED[i] = ED[i] + return_list[i]
        for i in range(5000):
            ED[i] = ED[i] / float(times)
            f_e.write(str(ED[i]) + '\n')


# similar to last function, but we store the middle result.
def partial_run_new():
    # with open("partial_limited_encoded_1.csv",'w') as f_e:
    # with open("partial_unlimited_encoded_1.csv",'w') as f_e:
    with open("partial_limited_origin_1.csv", 'w') as f_e:
        # with open("partial_unlimited_pure_1.csv",'w') as f_e:
        times = 100
        for j in range(times):
            print("Times:", j)
            w = 0
            l = 100
            d = 60
            return_list, _ = cal_limited_step(w, l, d)
            for i in range(600):
                f_e.write(str(return_list[i]) + ',')
            f_e.write('\n')


# calculate the ED (theorectical Value of equation (4))
def partial_theory_1():
    with open("t_partial_unlimited_origin.csv", 'w') as f_e:
        ED = [0] * 5000
        w = 0
        l = 100
        d = 100
        f_e.write(str(0) + '\n')

        for j in range(0, 5000):
            base = 1 - l / float(m)
            ED[j] = m - (m - l) * pow(base, j)
            print(ED[j], base)
            f_e.write(str(ED[j]) + '\n')


# calculate the ED (theorectical Value of equation (5-6)) Fig.6 Theoretical
def partial_theory_2():
    # with open("t_partial_limited_encoded.csv",'w') as f_e:
    # with open("t_partial_unlimited_encoded.csv",'w') as f_e:
    with open("t_partial_limited_origin.csv", 'w') as f_e:
        ED = [0] * 5000
        w = 0
        l = 100
        d = 60

        f_e.write(str(0) + '\n')

        eta = (l - d) * (m / float(l)) / float(d)       # can be (l - d) / d, it doesn't matter
        eta = int(eta)
        print("eta:", eta)

        for j in range(0, 5000):
            if j <= eta:
                ED[j] = (j + 1) * d
            else:
                base = 1 - l / float(m)
                ED[j] = m + (ED[eta - 1] - m) * pow(base, j + 1 - eta)
                print(ED[j], base)
            f_e.write(str(ED[j]) + '\n')


# calculate the EH and ED (theorectical Value of equation (8-9)) Fig.7 Theoretical
def partial_theory_3():
    with open("t_partial_unlimited_encoded.csv", 'w') as f_e:
        ED = [0] * 5000
        EH = [0] * 5000
        E_all = [0] * 5000
        w = 30
        l = 40
        d = 60

        f_e.write(str(0) + '\n')

        for j in range(0, 5000):
            base = 1 - l / float(m)
            ED[j] = m - (m - l) * pow(base, j)      # equals to Eq.(3) (4)

            if j > 0:
                EH[j] = EH[j - 1] + min(w, d - l + ED[j - 1] * (l / float(m)))
            else:
                EH[j] = d - l

            E_all[j] = ED[j] + EH[j]
            if E_all[j] > m:
                E_all[j] = m
            f_e.write(str(E_all[j]) + '\n')


# calculate the EH and ED (theorectical Value of equation (10-11)) Fig.8 Theoretical
def partial_theory_4():
    with open("t_partial_limited_encoded.csv", 'w') as f_e:
        ED = [0] * 5000
        EH = [0] * 5000
        E_all = [0] * 5000
        w = 20
        l = 60
        d = 50

        f_e.write(str(0) + '\n')

        eta = (l - d) * (m / float(l)) / float(d)
        eta = int(eta)
        print("eta:", eta)

        for j in range(0, 5000):
            if j <= eta:
                ED[j] = (j + 1) * d         # equals to Eq.(5) (6)
            else:
                base = 1 - l / float(m)
                ED[j] = m + (ED[eta - 1] - m) * pow(base, j + 1 - eta)
                print(ED[j], base)
            if j > 0:
                EH[j] = EH[j - 1] + min(w, d - l + ED[j - 1] * (l / float(m)))
            else:
                EH[j] = 0
            E_all[j] = ED[j] + EH[j]
            if E_all[j] > m:
                E_all[j] = m
            f_e.write(str(E_all[j]) + '\n')


# similar to cal_maximal_step
def cal_new(l, w, I, m, d):
    ED = [0] * m
    EH = [0] * m
    E_all = [0] * m

    for j in range(0, m):
        base = 1 - l / float(m)
        ED[j] = m - (m - l) * pow(base, j)

        if j > 0:
            EH[j] = EH[j - 1] + min(w, d - l + ED[j - 1] * (l / float(m)))
        else:
            EH[j] = d - l

        E_all[j] = ED[j] + EH[j]
        if j >= I - 1:
            return E_all[j]


# Iterative Space Partition Algorithm (ISPA)
def ISPA(m=5000, B=100, rho=2, d=100):

    low = m / B
    high = m * rho / B
    I = int(m / (2 * B / (rho + 1)))
    w = 0
    l = 0

    while (high - low) > 1:
        l = (m * math.log(rho) / I)
        w = int((B - l) / rho)
        l = B - rho * w
        y_I_max = cal_new(l, w, I, m, d)
        if y_I_max > m:
            high = I
            I = ((I + low) / 2)
        else:
            low = I
            I = ((I + high) / 2)

    return w, l


# Enumeration procedure, w variations. Fig.9
def EP():
    low = 1
    high = 50
    max_steps = []
    for i in range(low, high):
        w = i
        l = B - w * rho
        print("Step:", i, l, w)
        temp_value = []
        times = 100
        for i in range(times):
            temp_step = cal_maximal_step(w, l)
            temp_value.append(temp_step)
        mean_step = sum(temp_value) / float(len(temp_value))
        max_steps.append(mean_step)
        print("Mean step:", mean_step)

    print(max_steps)
    with open("EP.csv", 'w') as f_ep:
        for i in range(low, high):
            print(i)
            f_ep.write(str(i) + "," + str(max_steps[i - low]) + "\n")


# simulation of the special cases (w = 0 and w = 50). Complement of EP and ISPA
def extreme_value():
    with open("extreme_value.csv", 'w') as f_extreme:
        for j in range(2):
            w = j * 50
            l = B - rho * w
            temp_2 = []
            times = 1000
            for i in range(times):
                print(i)
                temp_step = cal_maximal_step(w, l)
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            f_extreme.write(str(w) + "," + str(mean_step2) + "\n")


# simulation when rho varies(mixed content, d = 100), Fig.10
def rho_variation_d_unlimited():
    with open("ISPA_rho_d_unlimited.csv", 'w') as f_ispam:
        # rho range(2, 11)
        for i in range(2, 11):
            rho = i
            print("rho:", rho)
            tmp_w, tmp_l = ISPA(rho=rho, d=100)

            times = 100
            temp = []
            for j in range(times):
                temp_step = cal_maximal_step(tmp_w, tmp_l)
                temp.append(temp_step)
            mean_step = sum(temp) / float(len(temp))
            print("w:", tmp_w, "l:", tmp_l, "steps:", mean_step)
            f_ispam.write(str(rho) + "," + str(tmp_w) + "," + str(tmp_l) + "," + str(mean_step) + "\n")


# simulation when rho varies (only original content, only encoded content, d = 100) Fig.10
def rho_extreme_d_unlimited():
    times = 100
    with open("rho_extreme_encoded_d_unlimited.csv", 'w') as f_ispam:
        # the values of rho in [2, 10]
        for j in range(2, 11):
            rho = j
            print("rho:", rho)
            w = int(B / rho)
            l = 0
            temp_2 = []
            for i in range(times):
                temp_step = cal_maximal_step(w, l, m)
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            print("rho:", rho, "steps:", mean_step2)
            f_ispam.write(str(rho) + "," + str(mean_step2) + "\n")

    with open("rho_extreme_pure_d_unlimited.csv", 'w') as f_ispam1:
        for j in range(2, 11):
            rho = j
            print("rho:", rho)
            w = 0
            l = 100

            temp_2 = []
            for i in range(times):
                temp_step = cal_maximal_step(w, l, m)
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            print("rho:", rho, "steps:", mean_step2)
            f_ispam1.write(str(rho) + "," + str(mean_step2) + "\n")


# simulation when rho varies(mixed content, d = 60), Fig.11
def rho_variation_d_limited():
    with open("ISPA_rho_d_limited.csv", 'w') as f_ispam:
        # rho range(2, 11)
        for i in range(2, 11):
            rho = i
            print("rho:", rho)
            tmp_w, tmp_l = ISPA(rho=rho, d=60)      # d = 60

            times = 100
            temp = []
            for j in range(times):
                _, temp_step = cal_limited_step(tmp_w, tmp_l, 60)
                temp.append(temp_step)
            mean_step = sum(temp) / float(len(temp))
            print("w:", tmp_w, "l:", tmp_l, "steps:", mean_step)
            f_ispam.write(str(rho) + "," + str(tmp_w) + "," + str(tmp_l) + "," + str(mean_step) + "\n")


# simulation when rho varies (only original content, only encoded content, d = 60) Fig.11
def rho_extreme_d_limited():
    times = 100
    with open("rho_extreme_encoded_d_limited.csv", 'w') as f_ispam:
        # the values of rho in [2, 10]
        for j in range(2, 11):
            rho = j
            print("rho:", rho)
            w = int(B / rho)
            l = 0
            temp_2 = []
            for i in range(times):
                _, temp_step = cal_limited_step(w, l, 60)       # d = 60
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            print("rho:", rho, "steps:", mean_step2)
            f_ispam.write(str(rho) + "," + str(mean_step2) + "\n")

    with open("rho_extreme_pure_d_limited.csv", 'w') as f_ispam1:
        for j in range(2, 11):
            rho = j
            print("rho:", rho)
            w = 0
            l = 100

            temp_2 = []
            for i in range(times):
                _, temp_step = cal_limited_step(w, l, 60)       # d = 60
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            print("rho:", rho, "steps:", mean_step2)
            f_ispam1.write(str(rho) + "," + str(mean_step2) + "\n")


# simulation when m varies(mixed content), Fig.12
def M_variation():
    with open("ISPA_m.csv", 'w') as f_ispam:
        # m range(1000, 10500, 500)
        for i in range(1000, 10500, 500):
            m = i
            print("m:", m)
            tmp_w, tmp_l = ISPA(m=m)

            times = 100
            temp = []
            for j in range(times):
                temp_step = cal_maximal_step(tmp_w, tmp_l, m)
                temp.append(temp_step)
            mean_step = sum(temp) / float(len(temp))
            print("w:", tmp_w, "l:", tmp_l, "steps:", mean_step)
            f_ispam.write(str(m) + "," + str(mean_step) + "\n")


# simulation when m varies (only original content, only encoded content), Fig.12
def M_extreme():
    times = 100
    with open("m_extreme_encoded.csv", 'w') as f_ispam:
        print("encoded:")
        for j in range(1000, 10500, 500):
            print("m:", j)
            w = 50
            l = 0
            m = j
            temp_2 = []
            for i in range(times):
                temp_step = cal_maximal_step(w, l, m)
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            print("steps:", mean_step2)
            f_ispam.write(str(m) + "," + str(mean_step2) + "\n")

    with open("m_extreme_pure.csv", 'w') as f_ispam1:
        print("original:")
        for j in range(1000, 10500, 500):
            print("m:", j)
            w = 0
            l = 100
            m = j

            temp_2 = []
            for i in range(times):
                temp_step = cal_maximal_step(w, l, m)
                temp_2.append(temp_step)
            mean_step2 = sum(temp_2) / float(len(temp_2))
            print("steps:", mean_step2)
            f_ispam1.write(str(m) + "," + str(mean_step2) + "\n")


# for incorporating with NC (for improving_existing_algorithm.py) Section. 8.1.3
def ISPA_for_NC_with_B_variation():
    B_re = []
    w_re = []
    l_re = []
    # B range(100, 161, 5)
    for i in range(100, 161, 5):
        B = i
        print("B:", B)
        tmp_w, tmp_l = ISPA(B=B, d=100)
        print("w:", tmp_w, "l:", tmp_l)
        B_re.append(B)
        w_re.append(tmp_w)
        l_re.append(tmp_l)

    # saving for "improving_existing_algorithm.py"
    with open('ISPA_B.csv', 'w', newline='') as f:
        for i in range(len(B_re)):
            f.write(str(B_re[i]) + ',' + str(w_re[i]) + ',' + str(l_re[i]) + '\r\n')


# The main entry
if __name__ == "__main__":

    print("simulation start...")

    # calculate the verifying result (simulation procedure. Equation (4), (5-6),(8-9),(10-11)) Fig.6,7,8
    # partial_run()

    # partial theoretical analysis, Fig.6,7,8
    # partial_theory_1()
    # partial_theory_2()
    # partial_theory_3()
    # partial_theory_4()

    # Iterative Space Partition Algorithm (ISPA)
    # ISPA()

    # Enumeration procedure, w variations. Fig.9
    # EP()

    # simulation when rho varies(mixed content, d = 100), Fig.10
    # rho_variation_d_unlimited()

    # simulation when rho varies (only original content, only encoded content, d = 100) Fig.10
    # rho_extreme_d_unlimited()

    # simulation when rho varies(mixed content, d = 60), Fig.11
    # rho_variation_d_limited()

    # simulation when rho varies (only original content, only encoded content, d = 60) Fig.11
    # rho_extreme_d_limited()

    # simulation when m varies(mixed content), Fig.12
    # M_variation()

    # simulation when m varies (only original content, only encoded content), Fig.12
    # M_extreme()

    # for incorporating with NC (for improving_existing_algorithm.py) Section 8.1.3
    # ISPA_for_NC_with_B_variation()


