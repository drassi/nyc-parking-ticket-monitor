import os
import sys
import mechanize
from lxml.html import fromstring

template = """
Plate: %s
State: %s
Type: %s
Make: %s

Ticket #: %s
Issued On: %s
Description: %s
Code: %s
Location: %s
          %s
          %s
Fine: $%s
"""

sep = '--------------------------------'

if len(sys.argv) != 3:
    print 'Error: must pass plate and ticket file arguments\nExample: python %s /tmp/plates.txt /tmp/tickets.txt' % sys.argv[0]
    sys.exit(1)

platefile = sys.argv[1]

if not os.path.exists(platefile):
    print 'Error: plates file %s does not exist' % platefile
    sys.exit(1)

platehandle = open(platefile)
plates = platehandle.read().split()
platehandle.close()

ticketfile = sys.argv[2]

if os.path.exists(ticketfile):
    tickethandle = open(ticketfile)
    knowntickets = tickethandle.read().split()
    tickethandle.close()
else:
    knowntickets = []

newtickets = []
results = ''

for search_plate in plates:

    b = mechanize.Browser()
    b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    b.open('http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain')
    b.select_form(name='NycservProtocolForm')
    b.form.set_all_readonly(False)
    b.form['ServiceName'] = 'PVO_QUERY_SETUP'
    b.form['SearchType'] = 'T'
    b.form['NycservRequest'] = """ChannelType=ct/Browser|RequestType=rt/Business|SubSystemType=st/Payments|AgencyType=at/PVO|ServiceName=PVO_QUERY_SETUP|MethodName=NONE|ParamCount=undefined|pvodropdownmenu=javascript:PVO_Violation_Search('T')|redlightdropdownmenu=javascript:PVO_Violation_Search('T')|propertydropdownmenu=javascript:findPropertyTaxes('TAX_QUERY_SETUP','B')|waterdownmenu=javascript:waterChargeQuerySetup('DEP_WATER_CHARGE_QUERY_SETUP')|ecbdropdownmenu=javascript:environmentalBoardViolationsquerySetup('GET_ECB_VIOLATION_SEARCH_QUERY_SETUP')|dohdcadropdownmenu=javascript:healthViolationsQuerySetup('GET_HEALTH_VIOLATION_SEARCH_QUERY_SETUP')|dcadropdownmenu=javascript:consumerAffairsViolationsQuerySetup('GET_CONSUMER_AFFAIRS_VIOLATION_SEARCH_QUERY_SETUP')|businesstaxdropdownmenu=javascript:findBusinessTaxes('BUSINESS_TAX_QUERY_SETUP')|requestahearingdropdownmenu=javascript:setServiceName('PVO_HEARING_QUERY_SETUP');submitProtocolForm();|AgencySelect=PVO|PageID=NYCSERVHome|SearchType=T|LinkType=EMPTY"""
    b.submit()

    b.select_form(name='NycservProtocolForm')
    b.form.set_all_readonly(False)
    b.form['PVO_PLATE_ID'] = search_plate
    b.form['PVO_STATE_NAME'] = 'NY'
    b.form['PVO_SEARCH_FOR_TOW'] = 'false'
    b.form['PVO_PLATE_TYPE'] = '  '
    b.form['PVO_COLLATERAL'] = 'TRUE'
    b.form['ServiceName'] = 'PVO_VIO_BY_PLATE'
    b.form['NycservRequest'] = """ChannelType=ct/Browser|RequestType=rt/Business|SubSystemType=st/Payments|AgencyType=at/PVO|ServiceName=PVO_VIO_BY_PLATE|MethodName=NONE|ParamCount=undefined|searchticket=|searchplate=ABC123|towcheck=on|collateralcheck=on|selState=NY|selPlateType= |PageID=PVO_Search|PVO_VIOLATION_NUMBER=|PVO_PLATE_ID=ABC123|PVO_SEARCH_FOR_TOW=false|PVO_COLLATERAL=TRUE|PVO_PLATE_TYPE= |PVO_STATE_NAME=NY|PVO_PLATE_EFFECTIVE_DATE=|PVO_PLATE_EXPIRATION_DATE=""".replace('ABC123', search_plate)
    b.submit()

    html = b.response().read()
    
    if 'No unpaid parking violations' not in html:
        
        doc = fromstring(html)
        tickets = doc.cssselect('form[name=NycservProtocolForm]')[0].cssselect('tr[bgcolor="#336633"]~tr')
        for ticket in tickets:
            tds = ticket.cssselect('td')
            details = tds[6].cssselect('a')[0].get('href').partition('(')[2].rpartition(')')[0].split("'")
            ticketnum = details[9]
            if ticketnum not in knowntickets:
                newtickets.append(ticketnum)
                plate = tds[2].text.strip()
                issued = tds[4].text.strip()
                desc = tds[5].text.strip()
                amt = tds[8].text.strip()
                vehicletype = details[3]
                state = details[5]
                make = details[7]
                code = details[15]
                modifier = details[37]
                address = details[39]
                county = details[41]
                results = results + sep + template % (plate,state,vehicletype,make,ticketnum,issued,desc,code,modifier,address,county,amt)

if results:
    print results + sep

if newtickets:
    tickethandle = open(ticketfile, 'a')
    tickethandle.write('\n'.join(newtickets) + '\n')
    tickethandle.close()

