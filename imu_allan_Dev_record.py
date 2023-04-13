import pyrealsense2 as rs
import numpy as np
import csv
import time
import os

# Create a folder for the output data
output_folder = 'imu_output_allan_dev'
os.makedirs(output_folder, exist_ok=True)

# Open CSV file for writing IMU data
with open(os.path.join(output_folder, 'imu_data.csv'), 'w', newline='') as imu_csv:

    # Create CSV writer
    imu_writer = csv.writer(imu_csv)

    # Write CSV header
    imu_writer.writerow(['#timestamp [ns]', 'gyro_x', 'gyro_y', 'gyro_z', 'accel_x', 'accel_y', 'accel_z'])

    # Configure the T265 camera pipeline
    pipeline = rs.pipeline()
    config = rs.config()

    # Enable accelerometer and gyroscope streams
    config.enable_stream(rs.stream.accel)
    config.enable_stream(rs.stream.gyro)

    # Start the camera pipeline
    profile = pipeline.start(config)

    # Configure the recording duration (in seconds)
    record_duration = 30 * 60  # 30 minutes
    start_time = time.time()

    try:
        while time.time() - start_time < record_duration:
            # Get the frames from the T265 camera
            frames = pipeline.wait_for_frames()

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
        print("Recording complete")
