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

# Create subplots with shared x and y axes
# Plot gyroscope data
fig1, ax1 = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Shift the ROS IMU data by a fixed time offset (in seconds)
time_offset = 3.2  # Adjust this value based on the actual time difference
ros_timestamps = [t + time_offset for t in ros_timestamps]


for i in range(3):
    ax1[i].plot(fisheye_timestamps, fisheye_gyro_data[i], label=f'T265 Gyro {["X", "Y", "Z"][i]}')
    ax1[i].plot(ros_timestamps, ros_gyro_data[i], label=f'car Gyro {["X", "Y", "Z"][i]}')
    ax1[i].set_title(f'Gyroscope {["X", "Y", "Z"][i]} Axis')
    ax1[i].legend()
    ax1[i].grid()

ax1[0].set(ylabel='Gyroscope (rad/s)')
ax1[1].set(ylabel='Gyroscope (rad/s)')
ax1[2].set(ylabel='Gyroscope (rad/s)')
for ax in ax1.flat:
    ax.set(xlabel='Time (s)')

# Plot accelerometer data
fig2, ax2 = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

for i in range(3):
    ax2[i].plot(fisheye_timestamps, fisheye_accel_data[i], label=f'T265 Accel {["X", "Y", "Z"][i]}')
    ax2[i].plot(ros_timestamps, ros_accel_data[i], label=f'car Accel {["X", "Y", "Z"][i]}')
    ax2[i].set_title(f'Accelerometer {["X", "Y", "Z"][i]} Axis')
    ax2[i].legend()
    ax2[i].grid()

ax2[0].set(ylabel='Accelerometer (m/s²)')
ax2[1].set(ylabel='Accelerometer (m/s²)')
ax2[2].set(ylabel='Accelerometer (m/s²)')
for ax in ax2.flat:
    ax.set(xlabel='Time (s)')

# # Show the plots
# plt.show()

# Plot gyroscope data
fig1, (ax1_1, ax1_2) = plt.subplots(1, 2, figsize=(15, 5), sharex=True)

# T265 Gyroscope data
ax1_1.plot(fisheye_timestamps, fisheye_gyro_data[0], label='T265 Gyro X')
ax1_1.plot(fisheye_timestamps, fisheye_gyro_data[1], label='T265 Gyro Y')
ax1_1.plot(fisheye_timestamps, fisheye_gyro_data[2], label='T265 Gyro Z')
ax1_1.set_title('T265 IMU Gyroscope Data')
ax1_1.legend()
ax1_1.grid()

# ROS Gyroscope data
ax1_2.plot(ros_timestamps, ros_gyro_data[0], label='car Gyro X')
ax1_2.plot(ros_timestamps, ros_gyro_data[1], label='car Gyro Y')
ax1_2.plot(ros_timestamps, ros_gyro_data[2], label='car Gyro Z')
ax1_2.set_title('ROS IMU Gyroscope Data')
ax1_2.legend()
ax1_2.grid()

ax1_1.set(ylabel='Gyroscope (rad/s)')

for ax in (ax1_1, ax1_2):
    ax.set(xlabel='Time (s)')
    
# Plot accelerometer data
fig2, (ax2_1, ax2_2) = plt.subplots(1, 2, figsize=(15, 5), sharex=True)

# T265 Accelerometer data
ax2_1.plot(fisheye_timestamps, fisheye_accel_data[0], label='T265 Accel X')
ax2_1.plot(fisheye_timestamps, fisheye_accel_data[1], label='T265 Accel Y')
ax2_1.plot(fisheye_timestamps, fisheye_accel_data[2], label='T265 Accel Z')
ax2_1.set_title('T265 IMU Accelerometer Data')
ax2_1.legend()
ax2_1.grid()

# ROS Accelerometer data
ax2_2.plot(ros_timestamps, ros_accel_data[0], label='car Accel X')
ax2_2.plot(ros_timestamps, ros_accel_data[1], label='car Accel Y')
ax2_2.plot(ros_timestamps, ros_accel_data[2], label='car Accel Z')
ax2_2.set_title('ROS IMU Accelerometer Data')
ax2_2.legend()
ax2_2.grid()

ax2_1.set(ylabel='Accelerometer (m/s²)')

for ax in (ax2_1, ax2_2):
    ax.set(xlabel='Time (s)')

# Show the plots
plt.show()
