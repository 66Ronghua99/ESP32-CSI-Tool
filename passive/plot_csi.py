import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from csi_reader_with_args import process_data

# Set subcarrier to plot
# subcarrier = 44


# Create figure for plotting
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
fig.canvas.draw()
plt.show(block=False)


def carrier_plot(data, output="plot.png", type="Amplitude"):
    plt.clf()
    df = np.asarray(data, dtype=np.int32)
    print(df.shape)
    num_data, num_subcarrier = df.shape
    # Can be changed to df[x] to plot sub-carrier x only (set color='r' also)
    plt.xlabel("Time")
    plt.ylabel(type)
    plt.xlim(0, len(data))
    plt.title(f"{type} plot of all subcarriers")
    for subcarrier in range(2, num_subcarrier):
        plt.plot(range(0, num_data), df[:, subcarrier])
    fig.canvas.flush_events()
    plt.show()
    plt.savefig(output)

args, perm_amp, perm_phase = process_data()
if args.amplitude:
    carrier_plot(perm_amp, f"{args.output_plot}_amp.png")
if args.phase:
    carrier_plot(perm_phase, f"{args.output_plot}_pha.png", type="Phase")