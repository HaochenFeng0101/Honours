import os
import time
import cv2
import numpy as np
import pyrealsense2 as rs

# Set up directories
output_path = 'output_euroc'
os.makedirs(os.path.join(output_path, 'mav0', 'cam0', 'data'), exist_ok=True)
os.makedirs(os.path.join(output_path, 'mav0', 'cam0', 'depth'), exist_ok=True)
os.makedirs(os.path.join(output_path, 'mav0', 'imu0'), exist_ok=True)

# Configure D435 camera
pipeline_d435 = rs.pipeline()
config_d435 = rs.config()
config_d435.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config_d435.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Configure T265 camera
pipeline_t265 = rs.pipeline()
config_t265 = rs.config()
config_t265.enable_stream(rs.stream.pose)

# Start pipelines
pipeline_d435.start(config_d435)
pipeline_t265.start(config_t265)

# Open IMU file
imu_file = open(os.path.join(output_path, 'mav0', 'imu0', 'data.csv'), 'w')

# Record data
print("recording start!")
try:
    frame_count = 0
    start_time = time.time()
    while time.time() - start_time < 40:  # Record for 40 seconds
        # Get D435 frames
        frames_d435 = pipeline_d435.wait_for_frames()
        color_frame = frames_d435.get_color_frame()
        depth_frame = frames_d435.get_depth_frame()
        
        if not color_frame or not depth_frame:
            continue
        
        # Get T265 IMU data
        frames_t265 = pipeline_t265.wait_for_frames()
        pose_frame = frames_t265.get_pose_frame()
        pose_data = pose_frame.get_pose_data()
        
        timestamp = int(round(time.time() * 1e9))

        # Save color and depth images
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        
        cv2.imwrite(os.path.join(output_path, 'mav0', 'cam0', 'data', '{}.png'.format(timestamp)), color_image)
        cv2.imwrite(os.path.join(output_path, 'mav0', 'cam0', 'depth', '{}.png'.format(timestamp)), depth_image)

        # Save IMU data
        imu_file.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}\n'.format(timestamp, pose_data.acceleration.x, pose_data.acceleration.y, pose_data.acceleration.z, pose_data.angular_velocity.x, pose_data.angular_velocity.y, pose_data.angular_velocity.z))

        frame_count += 1
        print('Frame: {}'.format(frame_count), end='\r')

except KeyboardInterrupt:
    print('Recording stopped.')

finally:
    imu_file.close()
    pipeline_d435.stop()
    pipeline_t265.stop()
    print('\nRecording finished.')
