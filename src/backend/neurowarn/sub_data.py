from cortex import Cortex
import math
import time
import json
import threading
import numpy as np



class Subcribe():
    """
    A class to subscribe data stream.

    Attributes
    ----------
    c : Cortex
        Cortex communicate with Emotiv Cortex Service

    Methods
    -------
    start():
        start data subscribing process.
    sub(streams):
        To subscribe to one or more data streams.
    on_new_data_labels(*args, **kwargs):
        To handle data labels of subscribed data 
    on_new_eeg_data(*args, **kwargs):
        To handle eeg data emitted from Cortex
    on_new_mot_data(*args, **kwargs):
        To handle motion data emitted from Cortex
    on_new_dev_data(*args, **kwargs):
        To handle device information data emitted from Cortex
    on_new_met_data(*args, **kwargs):
        To handle performance metrics data emitted from Cortex
    on_new_pow_data(*args, **kwargs):
        To handle band power data emitted from Cortex
    """
    def __init__(self, app_client_id, app_client_secret,command, **kwargs):
        """
        Constructs cortex client and bind a function to handle subscribed data streams
        If you do not want to log request and response message , set debug_mode = False. The default is True
        """
        print("Subscribe __init__")
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=False, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(new_mot_data=self.on_new_mot_data)
        self.c.bind(inform_error=self.on_inform_error)
        self.c.bind(new_com_data=self.on_new_com_data)
    
        self.serial_lock = threading.Lock()  # Lock to ensure thread-safe access
        self.command_lock = threading.Lock()  # Lock to ensure thread-safe access
        
        self.action = 's'
        self.motion = None
        self.motion_prev = 0
        self.prev_value = False
        self.lidar1 = True
        self.servo1 = 0
        self.lidar2 = True
        self.servo2 = 0   
        self.data_is_set = False
        self.rotation_center = None   
        self.command = command

    def start(self, streams, headsetId='', profile_name = ''):
        """
        To start data subscribing process as below workflow
        (1)check access right -> authorize -> connect headset->create session
        (2) subscribe streams data
        'eeg': EEG
        'mot' : Motion
        'dev' : Device information
        'met' : Performance metric
        'pow' : Band power
        'eq' : EEQ Quality

        Parameters
        ----------
        streams : list, required
            list of streams. For example, ['eeg', 'mot']
        headsetId: string , optional
             id of wanted headet which you want to work with it.
             If the headsetId is empty, the first headset in list will be set as wanted headset
        Returns
        -------
        None
        """
        if profile_name == '':
            raise ValueError('Empty profile_name. The profile_name cannot be empty.')

        self.profile_name = profile_name
        self.c.set_wanted_profile(profile_name)
        
        self.streams = streams

        if headsetId != '':
            self.c.set_wanted_headset(headsetId)

        self.c.open()



    def sub(self, streams):
        """
        To subscribe to one or more data streams
        'eeg': EEG
        'mot' : Motion
        'dev' : Device information
        'met' : Performance metric
        'pow' : Band power

        Parameters
        ----------
        streams : list, required
            list of streams. For example, ['eeg', 'mot']

        Returns
        -------
        None
        """
        self.c.sub_request(streams)
        

    def unsub(self, streams):
        """
        To unsubscribe to one or more data streams
        'eeg': EEG
        'mot' : Motion
        'dev' : Device information
        'met' : Performance metric
        'pow' : Band power

        Parameter
        ----------
        streams : list, required
            list of streams. For example, ['eeg', 'mot']

        Returns
        -------
        None
        """
        self.c.unsub_request(streams)

   


    def on_new_mot_data(self, *args, **kwargs):
        """
        To handle motion data emitted from Cortex

        Returns
        -------
        data: dictionary
             The values in the array motion match the labels in the array labels return at on_new_data_labels
        For example: {'mot': [33, 0, 0.493859, 0.40625, 0.46875, -0.609375, 0.968765, 0.187503, -0.250004, -76.563667, -19.584995, 38.281834], 'time': 1627457508.2588}
        """
        data = kwargs.get('data')
        if not self.data_is_set:
            self.rotation_center = self.quaternion_to_euler(data['mot'][2:6])
            self.data_is_set = True
        
        self.motion = self.quaternion_to_euler(data['mot'][2:6])

           
 

    def on_new_com_data(self, *args, **kwargs):
        data = kwargs.get('data')
        
        if data:
            
            
            diff = self.motion - self.rotation_center
            # print(f"diff: {diff}")
            # print(self.rotation_center)
                     
            if abs(diff) > 0.3:
                if diff < 0:
                    self.set_command('r') # Move forward with speed 100 
                  
                 
                else:
                    self.set_command('l')  # Move forward with speed 100
               
                   
                    
            elif data['action'] == "pull":
                self.set_command('f')  # Move forward with speed 100
           
    
            
            elif data['action'] == "push":
                self.set_command('b')  # Move forward with speed 100
                # print(self.action)
                # time.sleep(0.1)
            
                
                
        
            else:
                self.set_command('s')  # Move forward with speed 100
                # print(self.action)
                # time.sleep(0.1)

     
        
            # print(self.motion)

            # print(self.extract_rotations(self.quaternion_rotation_matrix(self.motion)))
            # print(self.motion)
            


        else:
            print("No data received")
            
            
            

    # callbacks functions
    def on_create_session_done(self, *args, **kwargs):
        print('on_create_session_done')

        # subscribe data 
        self.sub(self.streams)

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        print(error_data)




            
        
    def set_lidar1(self, new_data):
        # Use the lock to prevent race conditions
        with self.command_lock:
            self.lidar1 = new_data

    def get_lidar1(self):
        
        with self.serial_lock:
            return self.lidar1
    
    def get_servo1(self):
        
        with self.serial_lock:
            return self.servo1
    
    def set_servo1(self, new_data):
        with self.command_lock:
            self.servo1 = new_data
        
        
    
    def set_lidar2(self, new_data):
        with self.command_lock:
            self.lidar2 = new_data

    def get_lidar2(self):
        
        with self.serial_lock: 
            return self.lidar2
        
    def get_servo2(self):
        
        with self.serial_lock:
            return self.servo2
    
    def set_servo2(self, new_data):
        
        with self.command_lock:
            self.servo2 = new_data
        
    def set_command(self, new_data):
        with self.command_lock:
            self.command.value = new_data
        
    def get_command(self):
        with self.command_lock:
            return self.command.get()
            
        
    
    def quaternion_to_euler(self,rotation):
        """
        Convert a quaternion to Euler angles (roll, pitch, yaw).
        
        :param rotation: A list or array of 4 elements representing the quaternion (x, y, z, w)
        :return: A NumPy array containing the roll, pitch, and yaw angles
        """
        # Ensure the input is a NumPy array for easy manipulation
        rotation = np.array(rotation)
        # Extract quaternion components
        x, y, z, w = rotation
        # Calculate roll, pitch, and yaw
        roll = np.arctan2(2 * y * w - 2 * x * z, 1 - 2 * y**2 - 2 * z**2)
        pitch = np.arctan2(2 * x * w - 2 * y * z, 1 - 2 * x**2 - 2 * z**2)
        yaw = np.arcsin(2 * x * y + 2 * z * w)
        return roll



