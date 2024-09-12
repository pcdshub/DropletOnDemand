from enum import Enum
from multiprocessing import Queue
from multiprocessing.sharedctypes import Value
from datetime import datetime
import time
from drops.helpers.HTTPTransceiver import HTTPTransceiver

class DodRobotWorkerStates(Enum):
    KEEP_ALIVE  = 0
    ROBOT_DO    = 1
    ERROR       = 2

class DodRobotEvent():
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.time = datetime.now()
        self.robot_response = None

    def update_time(self):
        self.time = datetime.now()
    
    def __str__(self):
        return f" Endpoint: {self.endpoint}\nTime: {self.time}\n Response: {self.robot_response}"
class DodRobotWorker():

    def __init__(self,
                 in_q : Queue(),
                 out_q : Queue(),
                 transceiver : HTTPTransceiver,
                 *args,
                 **kwargs):
        #super().__init__(*args, **kwargs)
        self.in_q = in_q
        self.out_q = out_q
        self.do_next = Value('i', False)
        self.do_work = Value('i', True)
        self.transceiver = transceiver
        self.timeout = 100 # command timeout in seconds
        self.CURRENT_STATE = DodRobotWorkerStates.KEEP_ALIVE
        self.LAST_REQ = None
        self.timer_start = time.perf_counter()

    def work_func(self):
        while(self.do_work.value):
            if self.CURRENT_STATE == DodRobotWorkerStates.KEEP_ALIVE:
                # KEEP CONNECTION ALIVE
                # To keep connection alive, just prob status

                delta = time.perf_counter() - self.timer_start
                
                if delta >= 1: # keep alive request every second
                    self.timer_start = time.perf_counter()
                    delta = 0
                    self.transceiver.send('/DoD/get/Status')
                    r = self.transceiver.get_response() # Might be good to log

                if self.in_q.qsize() > 0:
                    # we still got items in queue
                    self.CURRENT_STATE = DodRobotWorkerStates.ROBOT_DO


            elif self.CURRENT_STATE == DodRobotWorkerStates.ROBOT_DO:
                # A thought, We can add some functionality to retry the command
                # if something does not go as planned?
                event = self.in_q.get()

                self.transceiver.send(event.endpoint)
                try:
                    robot_response = self.transceiver.get_response()
                except Exception as e:
                    self.CURRENT_STATE = DodRobotWorkerStates.ERROR

                # DO some busy waiting for robot to finish
                start = time.time()
                delta = 0
                inital_response = robot_response # save original response
                while(robot_response.STATUS['Status'] == "Busy"):
                    if delta > self.timeout:
                        # Timeout in case something went wront
                        self.timeout = True
                        return #exit loop

                    time.sleep(0.1) #Wait a ms to stop spamming robot
                    robot_response = client.get_status()
                    delta = time.time() - start

                if robot_response.STATUS['Status'] == "Dialog":
                    # Something went wrong
                    self.CURRENT_STATE = DodRobotWorkerStates.ERROR
                    # DO the same as "IDLE FOR NOW" 
                    # TODO: Handle dialog
                    event.update_time() # update new time stamp
                    event.robot_response = inital_response
                    self.out_q.put(event)

                if robot_response.STATUS['Status'] == "Idle":
                    # All is good
                    self.CURRENT_STATE = DodRobotWorkerStates.KEEP_ALIVE
                    event.update_time() # update new time stamp
                    event.robot_response = inital_response
                    self.out_q.put(event)

                self.LAST_REQ = event

            elif self.CURRENT_STATE == DodRobotWorkerStates.ERROR:
                # TODO
                print("IN EROR")
                if self.do_next.valu:
                    #Just keep going
                    self.CURRENT_STATE = DodRobotWorkerStates.KEEP_ALIVE

