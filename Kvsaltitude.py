import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


def main():
    gain = np.array([0.3, 0.55, 1])
    altitude = np.array([0.3, 0.5, 1])
    skgain = np.array([0.3, 0.55, 1], dtype=np.float64).reshape(-1, 1)
    skaltitude = np.array([0.3, 0.5, 1], dtype=np.float64).reshape(-1, 1)
    linreg = LinearRegression().fit(skgain, skaltitude)
    print("Least Square Line Intercept: ", linreg.intercept_)
    print("Least Square Line Coefficient: ", linreg.coef_)

    fig = plt.figure()
    plt.plot(gain, altitude, "ro", label="Points")
    plt.plot(gain, altitude, color="b", label="Line Plot")
    plt.plot(skgain, linreg.intercept_ + (linreg.coef_*skgain), color='g', linestyle="--", label="Least Square")
    plt.xlabel("Gain K")
    plt.ylabel("Altitude (m)")
    plt.title(f"Gain vs Altitude Plot")
    plt.grid(True)
    plt.legend(loc="best")
    plt.show()
    fig.savefig(f"gain_vs_altitude.png")


if __name__ == "__main__":
    main()