# ACEye

Business Ready Documents for Cisco ACI

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