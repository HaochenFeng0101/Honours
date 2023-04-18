import csv
import matplotlib.pyplot as plt

# imu_csv_file = '/home/fhc/ANU/2023 S1/honours/camera_calibration/imu_plot/data.csv'
# ros_csv_file = '/home/fhc/ANU/2023 S1/honours/camera_calibration/imu_plot/imu_ros.csv'

imu_csv_file = "/home/haochen/Honours/imu_comare/mav0/imu0/data.csv"
ros_csv_file = "/home/haochen/Honours/imu_ros"
'''
firstly steady at 20s, pull out to certain position, up and down twice, horizontal move then push back
'''
def read_imu_csv(filename):
    timestamps = []
    gyro_data = []
    accel_data = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        for col in reader:
            timestamps.append(int(col[0]))
            gyro_data.append([float(col[1]), float(col[2]), float(col[3])])
            accel_data.append([float(col[4]), float(col[5]), float(col[6])])

    # Normalize timestamps to start at 0
    start_timestamp = timestamps[0]
    timestamps = [(t - start_timestamp) * 1e-9 for t in timestamps]  # Convert timestamps to seconds

    gyro_data = list(zip(*gyro_data))  # Transpose the data
    accel_data = list(zip(*accel_data))  # Transpose the data

    return timestamps, gyro_data, accel_data


# Read data from both CSV files
fisheye_timestamps, fisheye_gyro_data, fisheye_accel_data = read_imu_csv(imu_csv_file)
ros_timestamps, ros_gyro_data, ros_accel_data = read_imu_csv(ros_csv_file)

# Plot gyroscope data for fisheye
plt.figure()
plt.plot(fisheye_timestamps, fisheye_gyro_data[0], label='Fisheye Gyro X')
plt.plot(fisheye_timestamps, fisheye_gyro_data[1], label='Fisheye Gyro Y')
plt.plot(fisheye_timestamps, fisheye_gyro_data[2], label='Fisheye Gyro Z')
plt.xlabel('Time (s)')
plt.ylabel('Gyroscope (rad/s)')
plt.title('IMU Gyroscope Data-T265_imu')
plt.legend()
plt.grid()

#Plot gyroscope data for ros
plt.figure()
plt.plot(ros_timestamps, ros_gyro_data[0], label='ROS Gyro X')
plt.plot(ros_timestamps, ros_gyro_data[1], label='ROS Gyro Y')
plt.plot(ros_timestamps, ros_gyro_data[2], label='ROS Gyro Z')
plt.xlabel('Time (s)')
plt.ylabel('Gyroscope (rad/s)')
plt.title('IMU Gyroscope Data-ros')
plt.legend()
plt.grid()

# Plot accelerometer data for both datasets
plt.figure()
plt.plot(fisheye_timestamps, fisheye_accel_data[0], label='Fisheye Accel X')
plt.plot(fisheye_timestamps, fisheye_accel_data[1], label='Fisheye Accel Y')
plt.plot(fisheye_timestamps, fisheye_accel_data[2], label='Fisheye Accel Z')
plt.xlabel('Time (s)')
plt.ylabel('Accelerometer (m/s²)')
plt.title('IMU Accelerometer Data-T265_imu')
plt.legend()
plt.grid()

plt.figure()
plt.plot(ros_timestamps, ros_accel_data[0], label='ROS Accel X')
plt.plot(ros_timestamps, ros_accel_data[1], label='ROS Accel Y')
plt.plot(ros_timestamps, ros_accel_data[2], label='ROS Accel Z')
plt.xlabel('Time (s)')
plt.ylabel('Accelerometer (m/s²)')
plt.title('IMU Accelerometer Data-ros')
plt.legend()
plt.grid()

plt.show()
