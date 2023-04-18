import sys
import allantools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

imu_csv_file = "/home/haochen/Honours/imu_allan_ros"
T265_imu_csv_file = '/home/haochen/Honours/allan_Dev_T265/mav0/imu0/data.csv'

def read_imu_csv(filename):
    df = pd.read_csv(filename, header=1, names=['timestamp', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z'])
    timestamps = np.array(df['timestamp']) * 1e-9
    gyro_data = np.array(df[['gyro_x', 'gyro_y', 'gyro_z']])
    accel_data = np.array(df[['accel_x', 'accel_y', 'accel_z']])
    return timestamps, gyro_data, accel_data

def compute_allan_deviation(data, taus):
    taus, adevs, _, _ = allantools.adev(data, rate=200, data_type="freq", taus=taus)
    return taus, adevs

def find_N_at_tau_1(ax, labels, data, taus, unit, linestyle='-'):
    for axis in range(3):
        taus, adevs = compute_allan_deviation(data[:, axis], taus)

        tau_1_index = np.argmin(np.abs(taus - 1))
        adev_at_tau_1 = adevs[tau_1_index]

        N = np.sqrt(adev_at_tau_1 * taus[tau_1_index])

        print(f"{labels[axis]} Angle Random Walk Coefficient (N) at Tau=1: {N:.2e} {unit}")

    ax.legend()

def find_bias_instability(ax, labels, data, taus, unit, linestyle='-'):
    scaling_factor = np.sqrt(2 * np.log(2) / np.pi)
    
    for axis in range(3):
        taus, adevs = compute_allan_deviation(data[:, axis], taus)

        min_adev = np.min(adevs)

        B = min_adev / scaling_factor

        print(f"{labels[axis]} Bias Instability Coefficient (B): {B:.2e} {unit}")

    ax.legend()

def plot_allan_deviation(ax, title, labels, data, taus, unit, linestyle='-'):
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Tau (s)')
    ax.set_ylabel('Allan Deviation')
    ax.grid(which='both')

    plot_data_on_axis(ax, labels, data, taus, linestyle)
    find_N_at_tau_1(ax, labels, data, taus, unit, linestyle)
    find_bias_instability(ax, labels, data, taus, unit, linestyle)
    
def plot_data_on_axis(ax, labels, data, taus, linestyle='-'):
    for axis in range(3):
        taus, adevs = compute_allan_deviation(data[:, axis], taus)
        ax.plot(taus, adevs, linestyle, label=f"{labels[axis]}")
        
    ax.legend()

def main(args):
    timestamps1, gyro_data1, accel_data1 = read_imu_csv(imu_csv_file)
    timestamps2, gyro_data2, accel_data2 = read_imu_csv(T265_imu_csv_file)
    taus = np.logspace(-2, 5, num=100)

    fig, axs = plt.subplots(2, 2, figsize=(12, 16))
    labels_accel = ['Accel X', 'Accel Y', 'Accel Z']
    labels_gyro = ['Gyro X', 'Gyro Y', 'Gyro Z']

    print("ROS IMU:")
    plot_allan_deviation(axs[0, 0], 'Allan Deviation - Accelerometer (ROS)', labels_accel, accel_data1, taus, 'm/s²/sqrt(Hz)', '-')
    plot_allan_deviation(axs[0, 1], 'Allan Deviation - Gyroscope (ROS)', labels_gyro, gyro_data1, taus, 'rad/s/sqrt(Hz)', '-')
    
    print("T265 IMU:")
    plot_allan_deviation(axs[1, 0], 'Allan Deviation - Accelerometer (T265)', labels_accel, accel_data2, taus, 'm/s²/sqrt(Hz)', '-')
    plot_allan_deviation(axs[1, 1], 'Allan Deviation - Gyroscope (T265)', labels_gyro, gyro_data2, taus, 'rad/s/sqrt(Hz)', '-')

    plt.show()

if __name__ == '__main__':
    main(sys.argv)

