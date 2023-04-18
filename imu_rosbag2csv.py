import rosbag
from sensor_msgs.msg import Imu
import csv
import sys

if len(sys.argv) < 3:
    print("Usage: imu_data_from_rosbag_to_csv.py <input_rosbag_file> <output_csv_file>")
    sys.exit(1)

input_rosbag_file = sys.argv[1]
output_csv_file = sys.argv[2]

# Initialize empty lists to store IMU data
imu_data = []

with rosbag.Bag(input_rosbag_file, 'r') as bag:
    for topic, msg, t in bag.read_messages(topics=['/carlie/imu']):
        #print(f"Processing message at time: {t}")  # Add this line to print the message timestamp
        #print(msg)
       
        imu_data.append([
            msg.header.stamp.to_nsec(),
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z,
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z
        ])
print(imu_data)
# Sort the IMU data by timestamp
imu_data.sort(key=lambda x: x[0])

# Write the IMU data to the output CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['timestamp_ns', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z'])
    csv_writer.writerows(imu_data)

print('conversion done!')