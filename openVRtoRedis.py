import sys
import time
import openvr
import redis
import math
import keyboard

Xoffset = 3.0
Yoffset = 2.2
openvr.init(openvr.VRApplication_Scene)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()

pool = redis.ConnectionPool(host='192.168.8.103', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
flag = 1
print("Press escape to start")
keyboard.wait('esc')

while flag:
    openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)


    hmd_pose = poses[1]
    print("Dyna X: {} Y: {}".format(hmd_pose.mDeviceToAbsoluteTracking[0][3],hmd_pose.mDeviceToAbsoluteTracking[2][3]))
    Dyna = str(hmd_pose.mDeviceToAbsoluteTracking[0][3]+Xoffset) +" "+ str(hmd_pose.mDeviceToAbsoluteTracking[2][3]+Yoffset)

    if hmd_pose.mDeviceToAbsoluteTracking[0][0] == 1.0:
        DynaHeading = math.atan2(hmd_pose.mDeviceToAbsoluteTracking[0][2],hmd_pose.mDeviceToAbsoluteTracking[2][3])
    elif hmd_pose.mDeviceToAbsoluteTracking[0][0] == -1.0:
        DynaHeading = math.atan2(hmd_pose.mDeviceToAbsoluteTracking[0][2],hmd_pose.mDeviceToAbsoluteTracking[2][3])
    else:
        DynaHeading = math.atan2(-hmd_pose.mDeviceToAbsoluteTracking[2][0],hmd_pose.mDeviceToAbsoluteTracking[0][0])
    DynaHeading =(DynaHeading +math.pi )/math.pi*180
    #print("dynaHeading: {}".format(DynaHeading))

    

    hmd_pose = poses[2]
    print("Hartvig X: {} Y: {}".format(hmd_pose.mDeviceToAbsoluteTracking[0][3],hmd_pose.mDeviceToAbsoluteTracking[2][3]))
    Hartvig = str(hmd_pose.mDeviceToAbsoluteTracking[0][3]+Xoffset) +" "+ str(hmd_pose.mDeviceToAbsoluteTracking[2][3]+Yoffset)+" "+ str(hmd_pose.mDeviceToAbsoluteTracking[1][3])

    if hmd_pose.mDeviceToAbsoluteTracking[0][0] == 1.0:
        HartvigHeading = math.atan2(hmd_pose.mDeviceToAbsoluteTracking[0][2],hmd_pose.mDeviceToAbsoluteTracking[2][3])
    elif hmd_pose.mDeviceToAbsoluteTracking[0][0] == -1.0:
        HartvigHeading = math.atan2(hmd_pose.mDeviceToAbsoluteTracking[0][2],hmd_pose.mDeviceToAbsoluteTracking[2][3])
    else:
        HartvigHeading = math.atan2(-hmd_pose.mDeviceToAbsoluteTracking[2][0],hmd_pose.mDeviceToAbsoluteTracking[0][0])
    HartvigHeading =(HartvigHeading +math.pi )/math.pi*180
    #print("hartvigHeading: {}".format(HartvigHeading))
    #print(hmd_pose.k_EButton_SteamVR_Touchpad)








    r.publish('dynaPos' , Dyna)
    r.publish('hartvigPos' , Hartvig)
    r.publish('dynaHeading' , DynaHeading)
    r.publish('hartvigHeading' , HartvigHeading)
    time.sleep(0.02)
    sys.stdout.flush()
    
    

openvr.shutdown()