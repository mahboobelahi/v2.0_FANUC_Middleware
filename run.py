from FANUC.workstation import RobotCell
from FANUC.configurations import ROBOT_ID,ROBOT_NAME
import threading,time
from FANUC.UtilityFunction import start_camera_cycle


if __name__ == '__main__':
    _fanuc = RobotCell(ROBOT_ID,ROBOT_NAME)
    #access token
    _fanuc.getAccessToken()
    #refresh token
    refreshToken=threading.Thread(target= _fanuc.refreshToken)
    refreshToken.daemon=True
    refreshToken.start()

    """
        Register robot to ZDMP-DAQ component. 
    """
    registerRobot=threading.Timer(0.5, _fanuc.register_device)
    registerRobot.daemon=True
    registerRobot.start()
    """
        This API call allows a data source to publish it data to
        ZDMP-Service and Message Bus when ever a measurement from device is recorded 
        on ZDMP-DAQ component. For disabling this feature omit last parameter
    """
    subscribeToAsync = threading.Timer(0.5, _fanuc.sub_or_Unsubscribe_DataSource, args=(True,))
    subscribeToAsync.daemon = True
    subscribeToAsync.start()
    """
        Connect to robot socket server and get Positional data
        start FTP connect to download latest picture of workspace
        publish data to MsgBus as well as sends to DAQ    
    """
    SocketComm = threading.Timer(0.5, _fanuc.start_socket_server)
    SocketComm.daemon = True
    SocketComm.start()

    #start camera cycle

    camCycle = threading.Timer(2, start_camera_cycle, args=(_fanuc,))
    camCycle.daemon = True
    camCycle.start()
 
    # start Flask server for robot
    #wait for execution of previous functions
    runApp = threading.Timer(.1, _fanuc.runApp())
    runApp.daemon = True
    runApp.start()

    