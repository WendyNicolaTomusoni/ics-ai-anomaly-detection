
# Reliability-Cybersecurity Matrix

## 1. Introduction

This document compares cybersecurity incidents and operational reliability failures in the simulated water treatment plant.

The purpose is to understand how different incidents affect industrial operations, safety and system availability.

## 2. Reliability and Cybersecurity Incidents

| ID | Incident | Category | Affected Asset | Operational Impact |
|---|---|---|---|---|
| I01 | Unauthorised PLC commands | Cybersecurity | PLC | Incorrect equipment operation |
| I02 | Ransomware affecting SCADA | Cybersecurity | SCADA/HMI | Loss of operator visibility |
| I03 | Excessive Modbus requests | Cybersecurity | Industrial network | Communication disruption |
| I04 | Pump motor failure | Reliability | Pump | Water movement stops |
| I05 | Sensor malfunction | Reliability | Sensor | Incorrect process measurements |
| I06 | Network switch failure | Reliability | Industrial network | Loss of device communication |
| I07 | PLC hardware failure | Reliability | PLC | Loss of automated control |

## 3. Impact Analysis

| Incident | Availability Impact | Integrity Impact | Potential Safety Impact |
|---|---|---|---|
| Unauthorised PLC commands | High | High | High |
| SCADA ransomware | High | Medium | Medium |
| Excessive Modbus requests | High | Medium | Medium |
| Pump motor failure | High | Low | Medium |
| Sensor malfunction | Medium | High | High |
| Network switch failure | High | Medium | Medium |
| PLC hardware failure | High | Medium | High |

These are preliminary qualitative assessments for the simulated environment.

## 4. Detection and Recovery

| Incident | Detection Method | Proposed Recovery |
|---|---|---|
| Unauthorised PLC commands | Network monitoring and access logs | Isolate affected access, verify PLC configuration |
| SCADA ransomware | Endpoint alerts and system monitoring | Restore from verified backups |
| Excessive Modbus requests | Network traffic analysis | Investigate source and restrict unauthorised traffic |
| Pump motor failure | Equipment alarms and inspection | Repair or replace pump |
| Sensor malfunction | Sensor validation and diagnostics | Calibrate or replace sensor |
| Network switch failure | Connectivity monitoring | Repair or replace switch |
| PLC hardware failure | Controller diagnostics | Replace hardware and restore configuration |

## 5. Mean Time To Repair (MTTR)

MTTR measures the average time required to repair a failed component or restore a system.

Formula:

MTTR = Total repair time / Number of repairs

The project will record recovery times during controlled simulations to evaluate whether improved detection and response procedures reduce restoration time.

## 6. Connection to the AI Anomaly Detection System

The AI monitoring system will primarily support the detection of suspicious network behaviour.

It may help identify excessive Modbus requests and unusual communication patterns.

However, it cannot independently repair mechanical failures, replace defective sensors or restore damaged hardware.

Additional recovery measures, including backups, maintenance procedures and incident response plans, will be required.

## 7. Conclusion

Cybersecurity incidents and reliability failures can both disrupt industrial operations.

The proposed resilience strategy combines network monitoring, anomaly detection, access controls, maintenance and recovery procedures to improve the reliability and security of the simulated water treatment plant.
