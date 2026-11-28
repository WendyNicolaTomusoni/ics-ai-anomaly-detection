
# Threat Model

## 1. Introduction

This document identifies potential threats against the simulated water treatment plant.

The purpose is to understand possible attack scenarios, affected assets and their operational consequences.

## 2. System Under Consideration

The system consists of sensors, a PLC, SCADA/HMI, pumps, valves and an industrial network using Modbus/TCP.

A separate Python-based AI monitoring system observes network traffic and identifies unusual behaviour.

## 3. Potential Threat Actors

| Threat Actor | Description |
|---|---|
| Cybercriminal | May attempt ransomware or operational disruption |
| Malicious insider | May misuse legitimate system access |
| External attacker | May attempt unauthorised network access |
| Accidental user | May cause disruption through human error |

## 4. Identified Threat Scenarios

| ID | Threat | Target | Potential Consequence |
|---|---|---|---|
| T01 | Unauthorised Modbus commands | PLC | Incorrect equipment operation |
| T02 | Sensor data manipulation | Sensors | Incorrect process measurements |
| T03 | Excessive network requests | Industrial network | Communication disruption |
| T04 | Ransomware | SCADA/HMI | Loss of operator access |
| T05 | Unauthorised access | SCADA/HMI | Unapproved monitoring or control |
| T06 | Network equipment failure | Industrial network | Loss of communication |

## 5. CIA Security Analysis

**Confidentiality:**
Protect industrial information and configuration from unauthorised access.

**Integrity:**
Ensure sensor readings and control information are accurate and protected against unauthorised changes.

**Availability:**
Ensure industrial systems and communication remain available when required.

**Safety:**
Ensure failures or cyber incidents do not create unsafe physical conditions.

## 6. Preliminary Threat Modelling Conclusion

The PLC, industrial network and SCADA/HMI are important targets because they support industrial control and monitoring.

Unauthorised Modbus commands, manipulated sensor readings, excessive network traffic and ransomware are relevant scenarios for further investigation.

The proposed AI monitoring system will help identify unusual network behaviour and generate alerts for investigation.
