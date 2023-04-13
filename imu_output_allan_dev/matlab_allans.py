import sys
import allantools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

imu_csv_file = '/home/fhc/ANU/2023 S1/honours/camera_calibration/imu_output_allan_dev/imu_data.csv'

def read_imu_csv(filename):
    df = pd.read_csv(filename, header=1, names=['timestamp', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z'])
    timestamps = np.array(df['timestamp']) * 1e-9
    gyro_data = np.array(df[['gyro_x', 'gyro_y', 'gyro_z']])
    accel_data = np.array(df[['accel_x', 'accel_y', 'accel_z']])
    return timestamps, gyro_data, accel_data

def compute_allan_deviation(data, taus):
    taus, adevs, _, _ = allantools.adev(data, rate=200, data_type="freq", taus=taus) #frequency is 200hz from datasheet 
    return taus, adevs

def plot_allan_deviation(ax, title, labels, data, taus):
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Tau (s)')
    ax.set_ylabel('Allan Deviation')
    ax.grid(which='both')

    for axis in range(3):
        taus, adevs = compute_allan_deviation(data[:, axis], taus)
        ax.plot(taus, adevs, label=labels[axis])

    ax.legend()

def main(args):
    timestamps, gyro_data, accel_data = read_imu_csv(imu_csv_file)
    taus = np.logspace(-2, 5, num=100)

    fig, axs = plt.subplots(2, 1, figsize=(12, 16))

    labels_accel = ['Accel X', 'Accel Y', 'Accel Z']
    labels_gyro = ['Gyro X', 'Gyro Y', 'Gyro Z']

    plot_allan_deviation(axs[0], 'Allan Deviation - Accelerometer', labels_accel, accel_data, taus)
    plot_allan_deviation(axs[1], 'Allan Deviation - Gyroscope', labels_gyro, gyro_data, taus)

    plt.show()

if __name__ == '__main__':
    main(sys.argv)