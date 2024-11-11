from csi_reader_with_args import process_data
import numpy as np
import matplotlib.pyplot as plt

def calc_variance(data: np.ndarray, window_size=30) -> np.ndarray:
    variance = []
    if len(data) <= window_size:
        variance.append(data.var())
        return variance
    for i in range(0, len(data)-window_size):
        window = np.array(data[i:i+window_size])
        variance.append(window.var())
    return variance


def main():
    args, amplitudes, phases = process_data()
    data = np.asarray(amplitudes)
    num_data, num_subcarrier = data.shape
    plt.clf()
    # Can be changed to df[x] to plot sub-carrier x only (set color='r' also)
    plt.xlabel("Time")
    plt.ylabel("Variance")
    plt.title(f"Variance plot of all subcarriers")
    variance_dict = {}
    for subcarrier in range(2, num_subcarrier):
        variance = calc_variance(data[:, subcarrier])
        plt.plot(range(0, len(variance)), variance)
        # variance_dict[subcarrier]= variance_dict
    # plt.show()
    plt.savefig(f"{args.output_dir}/{args.data.split("/")[-1].split(".")[0]}_variance.png")


if __name__ == "__main__":
    main()