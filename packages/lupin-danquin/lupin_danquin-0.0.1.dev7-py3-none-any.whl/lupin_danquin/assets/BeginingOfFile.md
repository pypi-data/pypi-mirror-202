# Revision

| Rev. | Description | Date | Author |
|------|-------------|------|--------|
| A | First version | 05-DEC-2022 | MF. Aouachria |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

# Signature

| Role | Name | Title | Signature |
|------|------|-------|-----------|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

[[_TOC_]]

# Robot Application software item presentation

The Robot Application software item runs on the CS9 controller and is programed in VAL3. It has three main functions:

- Receive commands from the LupinPrep software item, and send back responses and data about the robot.
- Get data and status from the F/T sensor. ...

## VAL3 scripting language

## Analogy with C++

VAL3 is the scripting language developed by Stäubli. It enables the user to control the robot through API calls. A software in VAL3 is organized in applications. The following analogy between VAL3 and C++ can be made:

| C++ | VAL3 | Comments |
|-----|------|----------|
| class | application | An application contains data and programs. |
| method | program | List of VAL3 commands. |
| attribute | data | A data has a type (the existing types are listed below and can be a single instance, an array of a collection (dictionary). |

An application can also be used by another application as an external library of data and programs. Thus, data and programs can be defined as public (accessible by other applications) or private.

### Type of Data in VAL3

The existing type of data in VAL3 are:

| Type | Meaning | Comments |
|------|---------|----------|
| aio | analogic I/O |  |
| bool | boolean |  |
| configRx | Staubli TX robot configuration | Configuration of the shoulder, elbow and wrist |
| dio | digitalI/O | A data has a type (the existing types are listed below and can be a single instance, an array of a collection (dictionary). |
| frame | pose | Expressed relatively to another frame. “World” is the global frame. |
| jointRx | Stäubli TX robot joint configuration | Angular value of the 6 joints of the robot. |
| mdesc | motion description | Define the acceleration, deceleration and maximal speed for a robot move. |
| num | numerical | In VAL3, there is no difference between integer or float |
| pointRx | Stäubli TX robot pose and configuration | Uniquely defines the robot position, orientation and branch of configuration(Shoulder left or right, elbow positive or negative, wrist positive or negative |
| sio | socket I/O |  |
| string | character string |  |
| tool | parameter defining a tool geometry |  |
| trsf | geometric transformation | Array of 6 num. |

### Executing an application

At start, the CS9 firmware automatically calls a program named start() in the application configured with the “AutoStart” flag. In our case, the application “RobotMainApp” is the entry point of the Robot Application software item. This application will in turn, start other programs in parallel tasks (See chapter 2).

In VAL3, a task can be synchronous or asynchronous. Synchronous means that the execution of the task is scheduled at a fixed period, while asynchronous means that the task will be executed in the remaining available CPU time. The time sharing between several asynchronous tasks in determined according to their priority.

# Applications documentation

## Architecture

### UML Diagram

```plantuml
@startuml
@startuml
interface ITcpCommunication
{
+intialize
+tcpListen
+tcpSend
}
class TcpCommunication
class TcpCommunicationMock
ITcpCommunication <|-- TcpCommunication
ITcpCommunication <|-- TcpCommunicationMock


interface IStateMachine
{
}
class StateMachine
class StateMachineMock
IStateMachine <|-- StateMachine
IStateMachine <|-- StateMachineMock

interface IMessageHandler
{
+initialize 
+sendResponse 
+startListening 
+ackClient 
+decodeBody 
+decodeHeader 
+encodeJointMsg 
+fromArraytoJointRx 
}
class MessageHandler
class MessageHandlerMock
IMessageHandler <|-- MessageHandler
IMessageHandler <|-- MessageHandlerMock
MessageHandler o-- ITcpCommunication

interface ITrajectoryManager
{
+ initialize
+ run
+ getTimeStamp
+ getTaskParams
}
class TrajectoryManager
class TrajectoryManagerMock
ITrajectoryManager <|-- TrajectoryManager
ITrajectoryManager <|-- TrajectoryManagerMock
TrajectoryManager o-- IStateMachine
TrajectoryManager o-- IMessageHandler

class Utilities << (S,#FF7700) >>

interface ITaskManager
{
+ initialize
+ run
+ getTaskParams
}
class TaskManager
class TaskManagerMock
ITaskManager <|-- TaskManager
ITaskManager <|-- TaskManagerMock
TaskManager o-- ICommandExecutor
TaskManager o-- ITrajectoryManager
TaskManager o-- IForceSensorDriver
TaskManager o-- IWatchdog

interface IWatchdog
{
+ initialize
+ run
+ getTaskParams
+ getTaskStatus
+ setTaskParams
+ setTimeStamp
}
class Watchdog
class WatchdogMock
IWatchdog <|-- Watchdog
IWatchdog <|-- WatchdogMock
Watchdog o-- IStateMachine



interface ICommandExecutor
{
+ initialize
+ run
+ getTimeStamp
+ getTaskParams
}
class CommandExecutor
class CommandExecutorMock
ICommandExecutor <|-- CommandExecutor
ICommandExecutor <|-- CommandExecutorMock
CommandExecutor o-- IStateMachine
CommandExecutor o-- IMessageHandler

interface IForceSensorDriver
{
+ initialize
+ run
+ getTimeStamp
+ getTaskParams
}
class ForceSensorDriver
class ForceSensorDriverMock
IForceSensorDriver <|-- ForceSensorDriver
IForceSensorDriver <|-- ForceSensorDriverMock
ForceSensorDriver o-- IStateMachine
ForceSensorDriver o-- IMessageHandler

class RobotMainApp
{ 
+start
+stop
}

RobotMainApp o-- ITaskManager
@enduml
```

### Sequence Diagram

### State Machine

```plantuml
@startuml
!theme mars
[*] -> DISCONNECTED 
DISCONNECTED --> CONNECTED : CONNECT

CONNECTED --> DISCONNECTED : DISCONNECT
CONNECTED --> INIT : INITIALIZE

INIT --> IDLE_READY : START
INIT --> ERROR_OCCURED : ERROR

IDLE_READY --> ERROR_OCCURED : ERROR
IDLE_READY --> POWERED : ON_POWER

IDLE_READY --> DISCONNECTED : DISCONNECT

POWERED --> BRAKE : ON_BRAKE
POWERED --> MOVING : START_MOVEMENT

BRAKE --> POWERED : ON_POWER

MOVING --> POWERED : CANCEL_MOVEMENT
MOVING --> COLLIDED : START_COLLISION
MOVING --> MOVEMENT_STOPPED : STOP_MOVEMENT
MOVING --> ERROR_OCCURED : ERROR

MOVEMENT_STOPPED --> MOVING : RESUME_MOVEMENT
MOVEMENT_STOPPED --> POWERED : CANCEL_MOVEMENT
MOVEMENT_STOPPED --> ERROR_OCCURED : ERROR

COLLIDED --> MOVING : RESUME_MOVEMENT
COLLIDED --> MOVING : START_MOVEMENT
COLLIDED --> ERROR_OCCURED : ERROR

ERROR_OCCURED --> INIT : MANAGE_ERROR
@enduml
```

## Application List
