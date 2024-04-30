# Droplet on Demand HTTP API Specification


## Connect to API
### Connect

/DoD/Connect?ClientName={value}

Required to send ‘Do’ requests. Software has to be enabled on its UI (button ‘Enable API Control’).

 

### Disconnect

/DoD/Disconnect

The client can end the connection with access to ‘Do’ requests. Clicking the button ‘Disable API Control’ on the UI has the same effect.

 

### Status (get)

/DoD/get/Status

A collection of information as requested by SLAC: ‘Position’ (actual coordinates), ‘LastProbe’, ‘Humidity’, ‘Temperature’, ‘BathTemp’.

 

### NozzleStatus (get)

/DoD/get/NozzleStatus

Returns the activated and selected nozzles an the parameters for all activated nozzles. The parameter ‘Trigger’ (true/false) is not linked to a nozzle.
Note: Nozzle parameters ‘ID’ (number), ‘Volt’, ‘Pulse’ (name or number), ‘Freq’ and ‘Volume’ appear as an array of strings (JSON).

 

###PulseNames (get)

/DoD/get/PulseNames

Returns the list of available pulse shapes for the sciPULSE channels.

 

###Position Names (get)

/DoD/get/PositionNames

Returns the list of positions that are stored in the software by name.

 

###Current Position (get)

/DoD/get/CurrentPosition

Returns the name and properties of the last selected position, together with the real current position coordinates. (The drives can have been stepped away from the stored position or they include small dispenser related offsets.)

 

### Task Names (get)

/DoD/get/TaskNames

Returns the list of tasks that are stored in the software by name.

 

### SelectNozzle (do)

/DoD/do/SelectNozzle?Channel={value}

Set the selected nozzle for dispensing and task execution etc. Returns a reject if the channel value is not one of the ‘Activated Nozzles’ (see ‘NozzleStatus’).

 

### Dispensing (do)

/DoD/do/Dispensing?State={value}

Switches between the dispensing states ‘Trigger’ (includes ‘Stat Continuous Dispensing’), ‘Free’ (‘Continuous Dispensing’ without trigger) and ‘Off’. Returns a reject if the value is not one of the three strings. (Some tasks can set the state to ‘Off’ without restarting dispensing afterwards.)

 

### SetLED (do)

/DoD/do/SetLED?Duration={value}&Delay={value}

Sets the two strobe LED parameters ‘Delay’ (0 to 6500) and Duration (1 to 65000). Returns a reject if one of the values is out of range.

 

### Move (do)

/DoD/do/Move?PositionName={value}

Move the drives to a position taken from the list ‘PositionNames’. This kind of moves is safe in general. It simulates the analog action on the UI.

 

### Move X (do)

/DoD/do/MoveX?X={value}

The X drive can be sent to any absolute coordinate (the value’s unit is µm) within the allowed range.

NOTE: This does not include a Z move up to the safe height nor any other safety feature checking whether the move from the current position to the selected coordinate can lead to collision or breaking of a dispenser Tip.

 

### Move Y (do)

/DoD/do/MoveY?Y={value}

Same as for X.

 

### Move Z (do)

/DoD/do/MoveZ?Z={value}

Same as for X.

 

### Execute Task (do)

/DoD/do/ExecuteTask?TaskName={value}

Runs a task from the list of ‘TaskName’. This operation is safe in general. It simulates the analog action on the UI.

 

### TakeProbe (do)

/DoD/do/TakeProbe?Channel={value}&ProbeWell={value}&Volume={value}

This endpoint requires the presence of the task ‘ProbeUptake’ (attached). If that is not given, the return is not a reject, but nothing happens.
The parameters are ‘Channel’ (number of nozzle, includes effect as ‘SelectNozzle’), ‘ProbeWell’ (e.g. A1), Volume (µL). Returns a reject  if ‘Channel’ is not among ‘Active Nozzles’, Volume is > 250 or ‘ProbeWell’ is not one of the allowed wells for the selected nozzle.

 

### AutoDrop (do)

/DoD/do/AutoDrop

Runs the particular task that is linked to the UI button. Its name is ‘AutoDropDetection’. In principal this endpoint is not needed. ‘ExecuteTask’ can be used instead.

 

### Interaction Point (do)

/DoD/do/InteractionPoint

The moving to the predefined position of the interaction point corresponds to the use of the endpoint ‘Move’. But only with this endpoint the UI elements for the dispensers’ position adjustment become visible on the UI. The request simulates the button (beam symbol) on the UI.

