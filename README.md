[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/automateyournetwork/ACEye)

# ACEye

Business Ready Documents for Cisco ACI

## Current API Coverage

Access Control Entities

Access Control Instances

Access Control Rules

Aggregate Interfaces

Application Profiles

Attachable Access Entity Profiles

*Audit Log

BGP Route Reflectors

Bridge Domains

Cluster Health

Contexts (VRFs)

Contracts

Contract Subjects

Device Packages

Endpoints (All Connected Fabric Endpoints)

EPG (Endpoint Groups)

*Events

Fabric Membership

Fabric Node SSL Certifcates

Fabric Nodes

Fabric Paths

Fabric Pods

Fault Summary

Filters

Health

Interface Policies

Interface Profiles

IP Addresses

License Entitlements

L2Outs

L3 Domains

L3 Interfaces

L3Outs

Leaf Interface Profiles

Leaf Switch Profiles

Physical Domains

Physical Interfaces

Prefix List

Prefix List Detailed

QOS Classes

Security Domains

Spine Interface Profiles

Spine Switch Profiles

Subnets

Tenant

Tenant Health

Top System

Users

VLAN Pools

* Both Audit Log and Events are commented out of the base package due to the potentially huge number of records; should you want the Audit Log / Events please uncomment out lines 72-73 (Audit Log) and 76-77 (Events)


## Installation

```console
$ python3 -m venv ACI
$ source ACI/bin/activate
(ACI) $ pip install aceye
```

## Usage - Help

```console
(ACI) $ aceye --help
```

![ACEye Help](/images/help.png)

## Usage - In-line

```console
(ACI) $ aceye --url <url to APIC> --username <APIC username> --password <APIC password>
```

## Usage - Interactive

```console
(ACI) $ aceye
APIC URL: <URL to APIC>
APIC Username: <APIC Username>
APIC Password: <APIC Password>
```

## Usage - Environment Variables

```console
(ACI) $ export URL=<URL to APIC>
(ACI) $ export USERNAME=<APIC Username>
(ACI) $ export PASSWORD=<APIC Password>
```

## Recommended VS Code Extensions

Excel Viewer - CSV Files

Markdown Preview - Markdown Files

Markmap - Mindmap Files

Open in Default Browser - HTML Files

## Contact

Please contact John Capobianco if you need any assistance
