import matplotlib.pyplot as plt
import numpy as np


def main():
    gain = 1.1
    altitude = 1
    success = 1
    oscillate_data = np.loadtxt(f"./altitude_{altitude}/data_gain{gain}_altitude{altitude}_success{success}.csv", delimiter=",")
    # print(oscillate_data)
    required_data = oscillate_data[:, [0, 4, 7, 8, 9]]
    # print(required_data)
    masked_data = required_data[required_data[:, 4] > 0]
    fig = plt.figure()
    plt.plot(masked_data[:, 0], masked_data[:, 1], label="v_hat (m/s)")
    plt.plot(masked_data[:, 0], masked_data[:, 2], label="omega_t")
    plt.plot(masked_data[:, 0], masked_data[:, 3], label="omega_t_smoothed")
    plt.xlabel("Time (s)")
    plt.ylabel("Optic Flow (rad/s)")
    plt.title(f"Optic Flow vs Time Plot for Gain={gain} and Alt={altitude}")
    plt.legend(loc="best")
    plt.show()
    fig.savefig(f"./altitude_{altitude}/data_gain{gain}_altitude{altitude}.png")


if __name__ == "__main__":
    main()
