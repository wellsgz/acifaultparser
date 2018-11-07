aci-fault-parser
=============
Author: Wei Zixi (ziwei@cisco.com)

# Description
Script to parse ACI faults into excel spreadsheet

## Environment
Required
* Python 2.7+
* argparse
* xlsxwriter

# Usage
You can eitehr put exported 'faultInfo.xml' into the same path with the script or access to APIC to query current fault and get the parsesd spreadsheet.

<pre>
usage: usage: faultparser_apic.py [-h] -s HOST -u USER [-p PASSWORD]

positional arguments if 'faultInfo.xml' is not existed:

HOST              APIC IP Address (https is desired)
USER              Username of APIC
PASSWORD          Password of APIC

</pre>
# Example

Online data collection

<pre>
[user@localhost ~]$ ./faultparser_apic.py -s 10.10.10.10 -u admin -p Pas$w0rd

Logging into APIC to retrieve faultInfo...
Parsing faultInfo...
Fault parsed as 'ACI Fault Log Parse.xlsx'.

</pre>

Offline data collection

<pre>
apic1# icurl 'http://localhost:7777/api/class/faultInfo.xml' > faultInfo.xml
</pre>

</pre>
