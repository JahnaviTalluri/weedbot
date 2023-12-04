import math
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import numpy as np
from tf.transformations import quaternion_from_euler

def move_robot(x, y, z, yaw):
    rospy.wait_for_service('/gazebo/set_model_state')

    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        model_state = ModelState()
        model_state.model_name = 'agribot'  # Replace with your actual model name
        model_state.pose.position.x = x
        model_state.pose.position.y = y
        model_state.pose.position.z = z

        # Convert yaw angle to quaternion
        quaternion = quaternion_from_euler(0, 0, yaw)

        model_state.pose.orientation.x = quaternion[0]
        model_state.pose.orientation.y = quaternion[1]
        model_state.pose.orientation.z = quaternion[2]
        model_state.pose.orientation.w = quaternion[3]

        response = set_state(model_state)
        return response.success

    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")
        return False



def interpolate_pose(start_pose, end_pose, num_steps):
    # Ensure the lengths of start_pose and end_pose are the same
    assert len(start_pose) == len(end_pose), "Start and end poses must have the same length"

    # Calculate the step size for interpolation
    step_size = [(end_val - start_val) / num_steps for start_val, end_val in zip(start_pose, end_pose)]

    # Perform interpolation
    interpolated_poses = []
    for step in range(1, num_steps + 1):
        # Interpolate the second term (y-coordinate) while keeping others constant
        current_pose = [start_val + step * step_size[index] if index == 1 else start_val for index, start_val in enumerate(start_pose)]
        interpolated_poses.append(current_pose)

    return interpolated_poses


if __name__ == '__main__':
    rospy.init_node('move_robot_node')

    # Specify the desired pose
    target_x = -3.80000   
    target_y = 8.746210
    target_z = 0.097987
    target_yaw = 1.6

    # Interpolate intermediate poses
    num_steps = 200  # Adjust this value to control the smoothness of the motion
#    intermediate_poses = interpolate_pose([-3.7375 ,-1.47633, 1.13156, 1.56832], [target_x, target_y, target_z, target_yaw], num_steps)
    start_pose = [-3.75445, -7.80736, 1.13155, 1.6]
    end_pose = [target_x, target_y, target_z, target_yaw]
    intermediate_poses = interpolate_pose(start_pose, end_pose, num_steps)


    # Move the robot to the intermediate poses gradually
    for pose in intermediate_poses:
        #print(pose)
        success = move_robot(*pose)
        rospy.sleep(0.1)  # Adjust the sleep duration to control the speed of the motion

    if success:
        print("Robot moved successfully!")
    else:
        print("Failed to move the robot.")

