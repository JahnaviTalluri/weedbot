import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

def move_robot(x, y, z, yaw):
    rospy.wait_for_service('/gazebo/set_model_state')
    
    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        model_state = ModelState()
        model_state.model_name = 'agribot'  # Replace with your actual model name
        model_state.pose.position.x = x
        model_state.pose.position.y = y
        model_state.pose.position.z = z
        model_state.pose.orientation.z = yaw
        response = set_state(model_state)
        return response.success

    except rospy.ServiceException as e:
        print(f"Service call failed: {e}")
        return False

if __name__ == '__main__':
    rospy.init_node('move_robot_node')

    # Specify the desired pose
    target_x = -3.80000   
    target_y = 4.25572
    target_z = 0.097987
    target_yaw = 0.8

    # Move the robot to the desired pose
    success = move_robot(target_x, target_y, target_z, target_yaw)

    if success:
        print("Robot moved successfully!")
    else:
        print("Failed to move the robot.")
