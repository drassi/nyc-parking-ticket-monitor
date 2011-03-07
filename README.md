# NYC parking ticket monitor

This is a simple python script to watch your vehicles' plates for new NYC parking tickets, using the nyc.gov "[eService Center](http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain)".  It keeps track of tickets it's already seen, so it can be run as a cron job in the spirit of [urlwatch](http://thpinfo.com/2008/urlwatch/) to e-mail you new tickets periodically.

![parking ticket](http://i.imgur.com/mKQTf.jpg "parking ticket")

## Dependencies

* python (2.6 works)
* mechanize (python-mechanize in ubuntu)
* lxml (python-lxml in ubuntu)

## How to run

Run the script with two file arguments, like so:

`python ticketmonitor.py plates.txt tickets.txt`

`plates.txt` is a newline-separated list of your New York license plates to watch, for example:

    ABC123
    FLYGURL2

`tickets.txt` is a path to a file that the script should use to remember tickets it's seen in the past.  This file will be created the first time a ticket is found, so it doesn't need to exist when the script is run.

Running the script will print out a formatted list of new tickets it's found:
    --------------------------------
    Plate: FLYGURL2
    State: New York
    Type: Passenger
    Make: HONDA

    Ticket #: 123456789
    Issued On: 09/18/2010
    Description: FAILURE TO STOP AT RED LIGHT
    Code: 07
    Location: At the intersection of
              W 25FT S/OF DELANCEY S
              Manhattan
    Fine: $87.87
    --------------------------------
    Plate: ABC123
    State: New York
    Type: Motorcycle
    Make: KAWAS

    Ticket #: 1234567810
    Issued On: 09/17/2010
    Description: SIDEWALK
    Code: 51
    Location: In front of
              301 81ST ST
              Brooklyn
    Fine: $115.00
    --------------------------------

The script saves the ticket numbers it finds in the specified tickets file, and re-running the script will produce no output unless it finds a new ticket.

## Running under cron
You can run this script under cron using some bash logic to e-mail you if the script produces any output.  This assumes that you have your `mail` command all set up.  Here's a cron entry to run the script at midnight:
    0 0 * * * python /path/to/ticketmonitor.py /path/to/plates.txt /path/to/tickets.txt > /tmp/ticketmon && if test -s /tmp/ticketmon; then mail -s "new parking ticket!" your@email.com < /tmp/ticketmon;fi
The NYCServ page claims to have maintenance hours 1:00 AM - 2:15 AM nightly and Sundays 5:00AM - 10:00 AM, so probably best to not run it during then.

## FAQ
Q: Why make this?

A: I wanted to learn how to use `mechanize`, but also thought it might be useful to help avoid being quadruple-ticketed or towed if you leave your vehicle in sketchy locations for indeterminate lengths of time.  Uh, hypothetically.  But I'm not exactly sure how long it takes new tickets to show up in the system, so don't blame me if that happens to you.

Q: How can I get the 2011 alternate side parking calendar to show up in my google calendar?

A: Add By URL: http://www.nyc.gov/html/dot/downloads/excel/asp2011.ics
The calendar is published in other formats [here](http://www.nyc.gov/html/dot/html/motorist/disclaimer.shtml).

Q: May I use this application for unauthorized purposes?

A: Unfortunately not, the NYCServ [FAQ](http://nycserv.nyc.gov/NYCServWeb/FAQ.html) states that the website may only be used for authorized purposes.
