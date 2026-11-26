
# Learning Notes

This file records the concepts and technical knowledge learned during the project.

## Stage 1: Project Setup

### Git
Git is a version control system. It tracks changes made to project files.

### GitHub
GitHub is an online platform for hosting Git repositories and collaborating on projects.

### Repository
A repository is a project storage location containing files and their change history.

### Clone
Cloning downloads a remote GitHub repository onto a local computer.

### Commit
A commit saves a snapshot of project changes in Git.

### Push
Push uploads local commits to GitHub.

### Pull
Pull downloads and integrates changes from GitHub.

## Stage 2: Understanding Industrial Control Systems

### Lesson 1: Introduction to ICS

**Industrial Control System (ICS):**
A combination of hardware and software used to monitor and control physical industrial processes.

**IT (Information Technology):**
Technology used to manage information, computers, databases and business systems.

**OT (Operational Technology):**
Technology used to monitor and control physical equipment and industrial processes.

### Main ICS Components

1. Sensors: Measure physical conditions such as water level, pressure and flow.
2. PLC: Processes sensor information and controls industrial equipment using programmed instructions.
3. SCADA: Allows operators to monitor and supervise industrial processes.
4. Actuators: Perform physical actions, such as operating pumps and valves.
5. Industrial Network: Allows industrial devices to exchange information.

### Why ICS Cybersecurity Matters

Cyberattacks against industrial systems can disrupt physical operations, affect equipment and threaten safety.

Industrial cybersecurity must consider confidentiality, integrity, availability and safety.

### Connection to Our Project

Our project will monitor communication in a simulated water treatment plant and use machine learning to identify unusual network behaviour.
git add docs/learning-notes.md
### Lesson 2: PLC, SCADA and Modbus/TCP

**PLC (Programmable Logic Controller):**
An industrial computer that receives sensor information, executes programmed logic and controls equipment.

**SCADA (Supervisory Control and Data Acquisition):**
A system that allows operators to monitor and supervise industrial processes.

**Difference between PLC and SCADA:**
The PLC handles local control operations, while SCADA provides supervisory monitoring and control.

**Modbus:**
An industrial communication protocol used by devices to exchange information.

**Modbus/TCP:**
A version of Modbus that communicates over TCP/IP networks, commonly using TCP port 502.

**Client:**
The device that initiates a communication request.

**Server:**
The device that receives a request and sends a response.

**Cybersecurity relevance:**
Unauthorised Modbus requests, unusual communication frequency and manipulated register values may indicate suspicious activity.

**Connection to our project:**
Our simulated water treatment plant will use industrial communication concepts to generate normal and abnormal network behaviour for our AI anomaly detection system.