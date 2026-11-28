# Learning Notes

## Stage 1: Project Setup
- Git: Version control system used to track project changes.
- GitHub: Platform for hosting Git repositories.
- Commit: Saves a snapshot of changes.
- Push: Uploads commits to GitHub.
- Pull: Downloads and integrates remote changes.

## Stage 2: Industrial Control Systems
### Lesson 1: Introduction to ICS
- ICS monitors and controls physical industrial processes.
- IT manages information and business systems.
- OT manages physical equipment and industrial processes.
- Main components: sensors, PLC, SCADA, actuators and industrial networks.

### Lesson 2: PLC, SCADA and Modbus/TCP
- PLC executes control logic and operates equipment.
- SCADA provides supervisory monitoring and control.
- Modbus is an industrial communication protocol.
- Modbus/TCP communicates over TCP/IP, commonly using port 502.

### Lesson 3: Water Treatment Plant
- Sensors measure water level, pressure and flow.
- PLC processes sensor readings.
- SCADA/HMI allows operators to monitor the plant.
- AI monitoring observes network traffic and identifies anomalies.

## Stage 3: System Analysis and Threat Modelling
### Lesson 1: System Architecture
- System architecture describes components and their connections.
- Network segmentation separates systems to limit unauthorised access.

### Lesson 2: Asset Inventory
- Asset inventory identifies important system components and their criticality.

### Lesson 3: Threat Modelling
- Threat modelling identifies potential attackers, threats and consequences.
- CIA means Confidentiality, Integrity and Availability.
- Safety is an additional priority in industrial systems.

### Lesson 4: Vulnerability and Risk Assessment
- A vulnerability is a weakness that could be exploited.
- Risk Score = Likelihood × Impact.
- Risk assessment helps prioritise security measures.

## Stage 4: Reliability and Resilience
### Lesson 1: Reliability and Cybersecurity
- Reliability is the ability to perform a required function over time.
- Cyber incidents involve malicious activity; reliability failures involve technical or equipment problems.
- MTTR measures average repair or restoration time.

### Lesson 2: Resilience Strategy
- Prevention reduces the likelihood of incidents.
- Detection identifies suspicious activity and failures.
- Response limits the impact of incidents.
- Recovery restores normal operations.
- Backups and redundancy support recovery.
- AI anomaly detection supports detection, not automatic repair.
## Stage 5: Simulated Water Treatment Plant
### Lesson 1: Basic Simulation
- A simulation represents an industrial process without requiring physical equipment.
- Sensors provide measurements such as water level, pressure and flow.
- A PLC uses control logic to operate equipment.
- Hysteresis uses separate ON and OFF thresholds to prevent frequent switching.