from enum import Enum
from multiprocessing import Queue
from datetime import datetime
from drops.helpers.HTTPTransceiver import HTTPTransceiver

class DodRobotWorkerStates(Enum):
    KEEP_ALIVE  = 0
    ROBOT_DO    = 1
    ERROR       = 2

class DodRobotEvent():
    def __init__(self, endpoint, blocking=True):
        self.endpoint = endpoint
        self.blocking = blocking
        self.time = datetime.now()
        self.robot_response = None

    def update_time(self):
        self.time = datetime.now()

class DodRobotWorker(Worker):
    CURRENT_STATE = DodRobotWorkerStates.KEEP_ALIVE
    LAST_REQ = None

    def __init__(self,
                 in_q : Queue(DodRobotEvent),
                 out_q : Queue(DodRobotEvent),
                 transceiver : HTTPTransceiver,
                 *args,
                 **kwargs):
        #super().__init__(*args, **kwargs)
        self.in_q = in_q
        self.out_q = out_q
        self.do_next = Value('i', False)
        self.transceiver = transceiver
        self.timeout = 100 # command timeout in seconds

    def work_func(self):
        while(self.do_work.value):
            if CURRENT_STATE == DodRobotWorkerStates.KEEP_ALIVE:
                # KEEP CONNECTION ALIVE
                # To keep connection alive, just prob status
                self.transceiver.send('/Dod/get/Status')
                time.sleep(0.1)
                r = self.transceiver.get_response() # Might be good to log

                if (self.LAST_REQ != None or self.LAST_REQ.blocking):
                    ## We are blocking
                    if(self.in_q.qsize() > 0 and self.do_next.value):
                        #we are blocking, but its ok to continue
                        self.do_next.value = False #reset flag, so we only do once
                        CURRENT_STATE = DodRobotWorkerStates().ROBOT_DO
                    else:
                        CURRENT_STATE = DodRobotWorkerStates().KEEP_ALIVE

                elif in_q.qsize() > 0:
                    # we are not blocking and we still got items in queue
                    CURRENT_STATE = DodRobotWorkerStates().ROBOT_DO

                time.sleep(1)

            elif CURRENT_STATE == DodRobotWorkerStates.ROBOT_DO:
                # A thought, We can add some functionality to retry the command
                # if something does not go as planned?
                event = self.in_q.get()

                self.transceiver.send(event.endpoint)
                time.sleep(0.1) # give robot some time?
                robot_response = self.transceiver.get_response()

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
                    CURRENT_STATE = DodRobotWorkerStates.ERROR
                    # DO the same as "IDLE FOR NOW" 
                    # TODO: Handle dialog
                    event.update_time() # update new time stamp
                    event.robot_response = inital_response
                    self.out_q.put(event)

                if robot_response.STATUS['Status'] == "Idle":
                    # All is good
                    CURRENT_STATE = DodRobotWorkerStates.KEEP_ALIVE
                    event.update_time() # update new time stamp
                    event.robot_response = inital_response
                    self.out_q.put(event)

            elif CURRENT_STATE == DodRobotWorkerStates.ERROR:
                # TODO
                if self.do_next.valu:
                    #Just keep going
                    CURRENT_STATE = DodRobotWorkerStates.KEEP_ALIVE

