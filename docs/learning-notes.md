
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

### Lesson 3: Water Treatment Plant Architecture

**Project scenario:**
Our project uses a simulated water treatment plant to demonstrate industrial control system cybersecurity.

**Physical process:**
The plant contains a water tank, pipes, pumps and valves.

**Sensors:**
- Water-level sensor: Measures the amount of water in the tank.
- Pressure sensor: Measures water pressure.
- Flow sensor: Measures the rate of water movement.

**Control system:**
- PLC: Receives sensor readings, executes control logic and operates pumps and valves.
- SCADA/HMI: Allows operators to monitor the process and send supervisory commands.
- Industrial network: Connects industrial devices and allows communication using Modbus/TCP.

**AI monitoring system:**
A separate Python-based monitoring system observes industrial network traffic and identifies unusual behaviour using machine learning.

**Important safety decision:**
The AI system will generate alerts and record suspicious activity. It will not automatically control or shut down industrial equipment.

**Example cybersecurity threat:**
An unauthorised device sending an unusually high number of Modbus requests to the PLC could indicate suspicious activity.

**Connection to our project:**
We will simulate normal and abnormal industrial network communication, collect traffic data and use machine learning to identify anomalies.
## Stage 4, Lesson 2: Resilience Strategy and Recovery Planning

- Resilience is the ability to prepare for, withstand, respond to, and recover from disruptions.
- Prevention reduces the likelihood of incidents.
- Detection identifies suspicious activity and equipment problems.
- Response limits the impact of incidents.
- Recovery restores normal operations safely.
- Backups provide copies of important data.
- Redundancy provides alternative components when primary components fail.
- Incident response plans define responsibilities and recovery procedures.
- AI anomaly detection supports the detection stage but does not automatically repair or control industrial equipment.