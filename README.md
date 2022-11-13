# ACEye

Business Ready Documents for Cisco ACI

## Current API Coverage

Application Profiles

Attachable Access Entity Profiles

Audit Log

Bridge Domains

Contexts (VRFs)

Contracts

Endpoints (All Connected Fabric Endpoints)

EPG (Endpoint Groups)

Fabric Nodes

Fault Summary

Filters

L2Outs

L3 Domains

L3Outs

Leaf Interface Profiles

Leaf Switch Profiles

Physical Domains

Physical Interfaces

QOS Classes

Spine Interface Profiles

Spine Switch Profiles

Subnets

Tenant

Top System

VLAN Pools


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