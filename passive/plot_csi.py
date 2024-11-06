import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import numpy as np
import collections

# Set subcarrier to plot
subcarrier = 44
target_mac = "42:43:76:34:CF:CD"

# Variables to store CSI statistics
packet_count = 0
total_packet_counts = 0

# Deque definition
perm_amp = collections.deque(maxlen=1000)
perm_phase = collections.deque(maxlen=1000)

# Create figure for plotting
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
fig.canvas.draw()
plt.show(block=False)


def carrier_plot(data, output="plot.png", type="Amplitude"):
    plt.clf()
    df = np.asarray(data, dtype=np.int32)
    # Can be changed to df[x] to plot sub-carrier x only (set color='r' also)
    plt.plot(range(0, len(data)), df[:, subcarrier], color='r')
    plt.xlabel("Time")
    plt.ylabel(type)
    plt.xlim(0, len(data))
    plt.title(f"{type} plot of Subcarrier {subcarrier}")
    # TODO use blit instead of flush_events for more fastness
    # to flush the GUI events
    fig.canvas.flush_events()
    # plt.show()
    plt.savefig(output)


def process(res):
    # Parser
    all_data = res.split(',')
    csi_data = all_data[25].split(" ")
    csi_data[0] = csi_data[0].replace("[", "")
    csi_data[-1] = csi_data[-1].replace("]", "")

    csi_data.pop()
    csi_data = [int(c) for c in csi_data if c]
    imaginary = []
    real = []
    for i, val in enumerate(csi_data):
        if i % 2 == 0:
            imaginary.append(val)
        else:
            real.append(val)

    csi_size = len(csi_data)
    amplitudes = []
    phases = []
    if len(imaginary) > 0 and len(real) > 0:
        for j in range(int(csi_size / 2)):
            amplitude_calc = math.sqrt(imaginary[j] ** 2 + real[j] ** 2)
            phase_calc = math.atan2(imaginary[j], real[j])
            amplitudes.append(amplitude_calc)
            phases.append(phase_calc)

        perm_phase.append(phases)
        perm_amp.append(amplitudes)


with open("csi-raw.csv", "r") as f:
    for line in f:
        line = line.replace('\x00', '').strip()
        if "CSI_DATA" in line and target_mac in line and "task_wdt" not in line:
            process(line)
            packet_count += 1
            total_packet_counts += 1

carrier_plot(perm_amp, "amplitude.png")
carrier_plot(perm_phase, "phase.png")