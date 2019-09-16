# imporving existing algorithm

import random
import math

# The number of chunks
m = 5000

# the cache size of RSu, range(100, 161, 5)
B = 100

# download at most d chunks from an rsu during one step
d = 100

# Mbps
avg_data_rate = 2

# Mbps
v2v_data_rate = 6

# the number of vihecles, as a group, accoding to the paper of NC
K = 6

# The overall versions of the file
v = 3

# bitrate versions, Mbps
bitrate_options = [1, 0.7, 0.3]

# the chunk sizes for each vehicle is different with different bitrates
chunk_sizes = []
for _ in range(K):
    chunk_sizes.append(bitrate_options[random.randint(0, v - 1)])

# Mb
avg_data_size = sum(chunk_sizes) / len(chunk_sizes)

times = 100

# accoding to the paper of NC
passing_phase = 30

# the download time
result_time = []

# the number of rounds/steps
result_round = []

# read the w and l with different B, calculated by ISP algorithm of simulation.py, with d = 100
with open('ISPA_B.csv', 'r') as f:
    line = f.readline().strip()
    while line:

        line = line.split(',')

        B = int(line[0])

        w = int(line[1])

        l = int(line[2])

        if w + l > d:       # limited d
            l = 100
            w = 0

        R2V_phase_NC = math.ceil(avg_data_size / avg_data_rate) * w * K

        download_times = []

        rounds = []

        for t in range(times):
            chunk_sizes = []
            for k in range(K):
                chunk_sizes.append(bitrate_options[random.randint(0, v - 1)])
            avg_data_size = sum(chunk_sizes) / len(chunk_sizes)
            received_count = 0
            download_time = 0
            download_round = 0
            while received_count < m:
                download_round += 1
                valid_origin = int(l * (1 - random.uniform(0, 0.2)))     # (1-random.uniform(0, 0.2) is optional, considering repeated chunks

                R2V_phase_Origin = math.ceil(avg_data_size / avg_data_rate) * K * valid_origin

                V2V_phase = (R2V_phase_NC + R2V_phase_Origin) * avg_data_rate / v2v_data_rate * K

                received_count = received_count + (w + l) * K

                download_time = download_time + R2V_phase_NC + R2V_phase_Origin + V2V_phase + passing_phase

            download_times.append(download_time)
            rounds.append(download_round)

        # print(sum(download_times)/times)
        result_time.append(str(sum(download_times)/times))
        result_round.append(str(sum(rounds)/times))

        line = f.readline().strip()

# save result
with open('ImprovingExistingAlgorithm.csv', 'a+', newline='') as wf:
    wf.write(','.join(result_round) + '\r\n')


# the download time
result_time = []

# the number of rounds/steps
result_round = []

for i in range(0, 13):
    # accoding to the paper of NC, download d chunks each step
    w = d

    l = 0

    download_times = []

    rounds = []

    print("w: {}".format(w))

    R2V_phase_NC = math.ceil(avg_data_size / avg_data_rate) * w * K

    for t in range(times):
        chunk_sizes = []
        for k in range(K):
            chunk_sizes.append(bitrate_options[random.randint(0, v - 1)])
        avg_data_size = sum(chunk_sizes) / len(chunk_sizes)
        download_time = 0
        received_count = 0
        download_round = 0
        while received_count < m:
            download_round += 1
            valid_origin = l * (
                        1 - random.uniform(0, 0.2))  # (1-random.uniform(0, 0.2) is optional, considering repeated chunks

            R2V_phase_Origin = math.ceil(avg_data_size / avg_data_rate) * K * l

            V2V_phase = (R2V_phase_NC + R2V_phase_Origin) * avg_data_rate / v2v_data_rate * K

            received_count = received_count + (w + valid_origin) * K

            download_time = download_time + R2V_phase_NC + R2V_phase_Origin + V2V_phase + passing_phase
            print("R2V_phase_NC: {} V2V_phase: {}".format(R2V_phase_NC, V2V_phase))

        download_times.append(download_time)
        rounds.append(download_round)

    print(sum(download_times) / times)
    result_time.append(str(sum(download_times) / times))
    result_round.append(str(sum(rounds) / times))

# save result
with open('ImprovingExistingAlgorithm.csv', 'a+', newline='') as wf:
    wf.write(','.join(result_round) + '\r\n')
