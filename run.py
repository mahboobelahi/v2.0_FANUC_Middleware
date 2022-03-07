from FANUC.workstation import RobotCell
from FANUC.configurations import ROBOT_ID,ROBOT_NAME
import threading,time


if __name__ == '__main__':
    _fanuc = RobotCell(ROBOT_ID,ROBOT_NAME)
    #access token
    _fanuc.getAccessToken()
    #refresh token



    """
        Register robot to ZDMP-DAQ component. It is one time API call and can be
        done using any REST-client like Postman etc. 
    """
    registerRobot=threading.Timer(1, _fanuc.register_device)
    registerRobot.daemon=True
    registerRobot.start()
    """
        This API call allows a data source to publish it data to
        ZDMP-Service and Message Bus when ever a measurement from device is recorded 
        on ZDMP-DAQ component. For disabling this feature omit last parameter
    """
    subscribeToAsync = threading.Timer(0.5, _fanuc.sub_or_Unsubscribe_DataSource)
    subscribeToAsync.daemon = True
    subscribeToAsync.start()
    
    # start Flask server for robot
    #wait for execution of previous functions
    time.sleep(5)
    _fanuc.runApp()