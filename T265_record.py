import pyrealsense2 as rs
import numpy as np
import cv2
import time
import csv
import os

import shutil



# Create a folder for the output data
# output_folder = 'euroc_output'
output_folder = 'allan_Dev_T265'
# Function to delete the contents of a folder
def delete_folder_contents(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

# Delete the contents of the output folders
# delete_folder_contents(os.path.join(output_folder, 'mav0', 'cam0', 'data'))
# delete_folder_contents(os.path.join(output_folder, 'mav0', 'cam1', 'data'))
# delete_folder_contents(os.path.join(output_folder, 'mav0', 'imu0', 'data'))

os.makedirs(output_folder, exist_ok=True)
os.makedirs(os.path.join(output_folder, 'mav0', 'cam0', 'data'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'mav0', 'cam1', 'data'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'mav0', 'imu0', 'data'), exist_ok=True)
# Open CSV files for writing camera and IMU data
with open(os.path.join(output_folder, 'mav0', 'cam0', 'data.csv'), 'w', newline='') as cam0_csv, \
        open(os.path.join(output_folder, 'mav0', 'cam1', 'data.csv'), 'w', newline='') as cam1_csv, \
        open(os.path.join(output_folder, 'mav0', 'imu0', 'data.csv'), 'w', newline='') as imu_csv:

    # Create CSV writers
    cam0_writer = csv.writer(cam0_csv)
    cam1_writer = csv.writer(cam1_csv)
    imu_writer = csv.writer(imu_csv)

    # Write CSV headers
    cam0_writer.writerow(['#timestamp [ns]', 'filename'])
    cam1_writer.writerow(['#timestamp [ns]', 'filename'])
    imu_writer.writerow(['#timestamp [ns]', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z'])

    # Configure the T265 camera pipeline
    pipeline = rs.pipeline()
    config = rs.config()

    # Enable streams from the T265 camera
    config.enable_stream(rs.stream.pose)
    config.enable_stream(rs.stream.fisheye, 1)  # Left fisheye camera
    config.enable_stream(rs.stream.fisheye, 2)  # Right fisheye camera

    # Enable accelerometer and gyroscope streams
    config.enable_stream(rs.stream.accel)
    config.enable_stream(rs.stream.gyro)

    # Start the camera pipeline
    profile = pipeline.start(config)

    # Configure the recording duration (in seconds)
    record_duration = 60*30
    start_time = time.time()
    print("recording start!")

    try:
        while time.time() - start_time < record_duration:
            # Get the frames from the T265 camera
            frames = pipeline.wait_for_frames()

            # Get the pose data
            pose_frame = frames.get_pose_frame()

            # Get the fisheye images
            left_fisheye_frame = frames.get_fisheye_frame(1)
            right_fisheye_frame = frames.get_fisheye_frame(2)

            # Save the fisheye images to separate folders
            if left_fisheye_frame and right_fisheye_frame:
                timestamp_ns = int(left_fisheye_frame.get_timestamp() * 1e6)

                left_filename = f"{timestamp_ns}_left.png"
                right_filename = f"{timestamp_ns}_right.png"

                left_image_path = os.path.join(output_folder, 'mav0', 'cam0', 'data', left_filename)
                right_image_path = os.path.join(output_folder, 'mav0', 'cam1', 'data', right_filename)
                left_fisheye_image = np.asanyarray(left_fisheye_frame.get_data())
                right_fisheye_image = np.asanyarray(right_fisheye_frame.get_data())

                cv2.imwrite(left_image_path, left_fisheye_image)
                cv2.imwrite(right_image_path, right_fisheye_image)

                # Write the timestamps and filenames to the CSV files
                cam0_writer.writerow([timestamp_ns, left_filename])
                cam1_writer.writerow([timestamp_ns, right_filename])

            # Get the IMU data
            accel_frame = frames.first_or_default(rs.stream.accel)
            gyro_frame = frames.first_or_default(rs.stream.gyro)

            if accel_frame and gyro_frame:
                accel_data = accel_frame.as_motion_frame().get_motion_data()
                gyro_data = gyro_frame.as_motion_frame().get_motion_data()

                imu_timestamp_ns = int(accel_frame.get_timestamp() * 1e6)
                imu_writer.writerow([imu_timestamp_ns,
                                    gyro_data.x, gyro_data.y, gyro_data.z,
                                    accel_data.x, accel_data.y, accel_data.z])
                
    finally:
        # Stop the camera pipeline and release resources
        pipeline.stop()
        print("recording complete")

