#!/usr/bin/env python

import os
import requests
import xlsxwriter
import xml.etree.ElementTree as ET

# Disable ssl warning
requests.packages.urllib3.disable_warnings()

def faultInfoParse():

    # APIC and credential
    apic = 'https://10.74.205.110/'
    username = 'admin'
    password = 'C1sc0123'
    
    # Login to APIC and get cookies
    apicSession = requests.Session()
    apicSession.verify = False
    
    loginUrl = apic+'api/aaaLogin.xml'
    loginData = '<aaaUser name="'+username+'" pwd="'+password+'" />'
    apicSession.post(loginUrl,data=loginData,verify=False)
    
    # Get faultInfo
    faultInfo = apicSession.get(apic+'api/node/class/faultInfo.xml').text

    # Set filename
    fabricName=ET.fromstring(apicSession.get(apic+'/api/node/mo/topology/pod-1/node-1.xml?query-target=children&target-subtree-class=topSystem').text)[0].get('fabricDomain')
    fileName = fabricName+' Fault Log Parse.xlsx'
    
    # Create excel workbook
    workbook = xlsxwriter.Workbook(fileName,{'strings_to_numbers': True})
    worksheet1 = workbook.add_worksheet('Fault Info Parse')
    worksheet2 = workbook.add_worksheet('Delegated Fault Info Parse')
    headline = workbook.add_format({'bold': True, 'color': 'blue', 'font_size': '13'})
    worksheetList = [worksheet1, worksheet2]

    if os.path.isfile(fileName):
        os.remove(fileName)

    # Parse faultInfo
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

faultInfoParse()
