
# System Architecture

## 1. Project Overview

This project develops an AI-powered anomaly detection system for a simulated water treatment plant.

The system will demonstrate how machine learning can help identify unusual communication patterns in an Industrial Control System (ICS).

## 2. System Purpose

The simulated water treatment plant will represent an industrial environment containing sensors, a Programmable Logic Controller (PLC), a SCADA/HMI system, pumps and valves.

A separate Python-based monitoring application will observe network traffic and identify potentially suspicious behaviour.

## 3. System Components

| Component | Purpose |
|---|---|
| Water-level sensor | Measures water level |
| Pressure sensor | Measures water pressure |
| Flow sensor | Measures water flow |
| PLC | Processes sensor readings and controls equipment |
| SCADA/HMI | Allows operators to monitor the process |
| Pump | Moves water through the system |
| Valve | Controls water flow |
| Industrial network | Connects industrial devices |
| AI monitoring system | Detects unusual network behaviour |

## 4. Communication

The PLC and SCADA/HMI will communicate using Modbus/TCP over an industrial network.

The AI monitoring application will independently observe network traffic and analyse communication patterns.

## 5. Security Boundary

The AI monitoring system will operate separately from the industrial control logic.

It will generate alerts and record detected anomalies. It will not automatically issue commands to the PLC, pumps or valves.

## 6. Network Architecture

The simulated industrial environment will contain a PLC, a SCADA/HMI station and a separate AI monitoring system.

The PLC and SCADA/HMI will communicate over an industrial Ethernet network using Modbus/TCP.

The AI monitoring system will passively observe a copy of network traffic. It will analyse communication patterns without interfering with the industrial control process.

## 7. Proposed Network Addressing

| Device | IP Address |
|---|---|
| PLC | 192.168.10.10 |
| SCADA/HMI | 192.168.10.20 |
| AI monitoring system | 192.168.10.30 |
| Gateway (if required) | 192.168.10.1 |

Subnet: 192.168.10.0/24

Modbus/TCP communication commonly uses TCP port 502.

These addresses are proposed for the isolated project simulation.

## 8. Network Monitoring Approach

The AI monitoring system will use passive network monitoring.

In a physical network, a managed switch can provide a mirrored copy of traffic to the monitoring system.

During the initial software simulation, Python may generate communication events directly. Actual packet capture can be introduced later.

The monitoring system will analyse traffic and generate alerts when unusual communication patterns are identified.

## 9. Security Design Principles

- Keep the simulation isolated from production networks.
- Do not allow the AI system to issue industrial control commands.
- Monitor network communication without disrupting the control process.
- Record suspicious events for investigation.
- Treat detected anomalies as potential threats requiring further investigation.
