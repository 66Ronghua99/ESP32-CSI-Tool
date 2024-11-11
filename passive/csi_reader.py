import math
import collections
from typing import List, Tuple, Any
def process_line(res):
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

    return amplitudes, phases


def process_data() -> Tuple[Any, List[int], List[int]]:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="input data")
    parser.add_argument("-o", "--output", help="save file")
    parser.add_argument("-a", "--amplitude", action="store_false", help="save file")
    parser.add_argument("--mac", default="54:EF:44:5D:59:27", help="target mac address")
    args = parser.parse_args()
    # target_mac = "54:EF:44:5D:59:27"
    # Deque definition
    perm_amp = collections.deque(maxlen=200)
    perm_phase = collections.deque(maxlen=200)
    with open(args.data, "r") as f:
        for line in f:
            line = line.replace('\x00', '').strip()
            if "CSI_DATA" in line and args.mac in line and "task_wdt" not in line:
                amplitudes, phases = process_line(line)
                perm_phase.append(phases)
                perm_amp.append(amplitudes)
    return args, perm_amp, perm_phase

    