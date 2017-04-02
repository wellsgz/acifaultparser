#!/usr/bin/env python

'''
Written by Wei Zixi (ziwei@cisco.com)
'''

import os
import argparse
import requests
import xlsxwriter
import xml.etree.ElementTree as ET

# Disable ssl warning
requests.packages.urllib3.disable_warnings()

def main():
    if os.path.isfile('faultInfo.xml'):
        print "Found 'faultInfo.xml' in current path, creating fault parse spreadsheet'"
        faultInfo = open('faultInfo.xml','r').read()
        faultInfoParse(None,None,None,faultInfo)
    else:
        print 'Can not find faultInfo in current path, please specify APIC information to retrieve it...'
        args = get_args()
        apic = 'https://'+args.host+'/'
        username = args.user
        password = args.password
        if args == None:
            print "'faultInfo' is missing from current path, please specify APIC to connect to"
        faultInfoParse(apic,username,password,None)

def get_args():
    parser = argparse.ArgumentParser(
        description='Connect to APIC controller')

    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='APIC controller to connect to')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='APIC username')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='APIC password')

    args = parser.parse_args()

    return args

def faultInfoParse(apic=None,username=None,password=None,faultInfo=None):
    
    print apic,username,password,faultInfo

    if faultInfo == None:
        # Login to APIC and get cookies
        print 'Logging into APIC to retrieve faultInfo...'
        apicSession = requests.Session()
        apicSession.verify = False
        
        loginUrl = apic+'api/aaaLogin.xml'
        loginData = '<aaaUser name="'+username+'" pwd="'+password+'" />'
        apicSession.post(loginUrl,data=loginData)
        
        # Get faultInfo
        faultInfo = apicSession.get(apic+'api/node/class/faultInfo.xml').text

        # Set filename
        fabricName=ET.fromstring(apicSession.get(apic+'/api/node/mo/topology/pod-1/node-1.xml?query-target=children&target-subtree-class=topSystem').text)[0].get('fabricDomain')
        fileName = fabricName+' Fault Log Parse.xlsx'
    else:
        fileName = 'Fault Log Parse.xlsx'
    
    # Create excel workbook
    workbook = xlsxwriter.Workbook(fileName,{'strings_to_numbers': True})
    worksheet1 = workbook.add_worksheet('Fault Info Parse')
    worksheet2 = workbook.add_worksheet('Delegated Fault Info Parse')
    headline = workbook.add_format({'bold': True, 'color': 'blue', 'font_size': '13'})
    worksheetList = [worksheet1, worksheet2]

    if os.path.isfile(fileName):
        os.remove(fileName)

    # Parse faultInfo
    print 'Parsing faultInfo...'
    root = ET.fromstring(faultInfo)
    
    # Create index
    faultFields = ('code', 'occur', 'type', 'subject', 'cause', 'descr', 'rule', 'domain', 'dn', 'changeset', 'childAction', 'created', 'delegated', 'severity', 'origSeverity', 'prevSeveirty', 'highestSeverity', 'lastTransition', 'ack')

    delegatedFaultFields = ('code', 'occur', 'affected', 'type', 'subject', 'cause', 'descr', 'rule', 'domain', 'dn', 'changeset', 'childAction', 'created', 'delegated', 'severity', 'origSeverity', 'highestSeverity', 'lastTransition')

    fieldList = (faultFields, delegatedFaultFields)

    indexList = ('faultInst', 'faultDelegate')
    
    # Write faultInfo into spreadsheet
    for i in (0,1):
        row = 0
        for faultField in fieldList[i]:
            worksheetList[i].write(0,row,faultField,headline)
            row += 1

        col = 1
        for faults in root.findall(indexList[i]):
            row = 0
            for faultField in fieldList[i]:
                worksheetList[i].write(col,row,faults.attrib.get(faultField))
                row += 1
            col += 1
        
            #print code+','+occur+','+faultType+','+subject+','+cause+','+descr+','+rule+','+domain+','+dn+','+changeset+','+childAction+','+created+','+delegated+','+severity+','+origSeverity+','+highestSeverity+','+lastTransition+','+ack
    print "Fault parsed as '"+fileName+"'."

if __name__ == "__main__":
    main()