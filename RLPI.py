#  /usr/bin/python3.7
# 
#   Author: Virgil Hoover
#   License found in './License.txt'
# TODO: Add GUI to moderize and hide userpass

import pyodbc
import os
from shutil import copytree, rmtree
from pypsexec.client import Client
from socket import getfqdn


def queryrun(querystring):
    server = input('Enter the database server IP: ')
    username = input('Enter a username with access to the database: ')
    password = input('Enter the password: ')
    db = ('Enter the database name: ')
    c = pyodbc.connect("DRIVer={SQL Server}; \
                            SERVER=" + server + "; \
                            DATABASE=" + db + "; \
                            UID=" + username + "; \
                            PWD=" + password + "; \
                            readonly=True")
    query = c.cursor()
    result = query.execute(querystring).fetchval()
    return result


def query_printer(computer):
    clinic = ''
    host = getfqdn(computer)
    if not host.find('-', 0, 7):
        clinic = host[0:6]
    elif host.find('-', 0, 7) == 5:
        clinic = host[0:4]
    if len(clinic) > 6:
        print "Error, Invalid ID"
        return None None
        exit()
    what = "SELECT CONCAT(Clinic.Clinic_Subnet,'.',Printer_IP) AS Printer_IP "
    where = "FROM Clinic_Printers INNER JOIN Clinic ON Clinic.Clinic_ID=Clinic_Printers.Clinic_ID "
    condition = "WHERE Clinic.Clinic_ID = " + clinic + "AND Printer_Model = 'MX711';"
    querystring = (what + where + condition)
    printer = queryrun(querystring)
    if not printer:
        print("No printer found!!")
        man_print = input("What is the printer IP address: ")
        printer = man_print
    return printer, clinic


def file_copy(computer):
    result = query_printer(computer)
    printer = str.strip(str(result))
    src_path = "\\\\Server01\\Publicr\\PrintToolDrivers\\PrinterTool\\lexmarkuniversal\\x64"
    dst_path = "\\\\" + computer + "\\c$\\rlprinttool\\install.bat"
    path = "\\\\" + computer + "\\c$\\rlprinttool"
    print_drvr = "cscript //Nologo %__AppDir__%Printing_Admin_Scripts\\en-US\\prndrvr.vbs "
    print_port = "cscript //Nologo %__AppDir__%Printing_Admin_Scripts\\en-US\\Prnport.vbs "
    print_mngr = "cscript //Nologo %__AppDir__%Printing_Admin_Scripts\\en-US\\Prnmngr.vbs "
    if os.path.exists(path):
        rmtree(path)
    copytree(src_path, "\\\\" + computer + "\\c$\\rlprinttool\\LexmarkUniversal")
    access_mode = "a"
    with open(dst_path, access_mode) as vb:
        vb.write(print_drvr + '-a -m "Lexmark Universal v2 XL" -i "c:\\rlprinttool\\LexmarkUniversal\\LMUD1p40.inf"\n')
        vb.write(print_port + '-a -r IP_' + printer + ' -h ' + printer + ' -o raw -n 9100\n')
        vb.write(print_mngr + '-a -p "Lexmark @' + printer + '" -m "Lexmark Universal v2 XL" -r IP_' + printer + '\n')
    return


def timez(computer):
    time_set = ''
    clinic = str(query_printer(computer))
    what = "SELECT NOCOUNT ON; SELECT TZone "
    where = "FROM Clinic "
    condition = "WHERE Clinic.Clinic_ID = " + clinic + ";"
    querystring = (what + where + condition)
    zones = {"Pacific/Honolulu": '"Hawaiian Standard Time"',
             "America/Anchorage": '"Alaskan Standard Time"',
             "America/Los_Angeles": '"Pacific Standard Time"',
             "America/Denver": '"Mountain Standard Time"',
             "America/Pheonix": '"Mountain Standard Time_dstoff"',
             "America/Chicago": '"Central Standard Time"',
             "America/New_York": '"Eastern Standard Time"',
             "America/Detroit": '"Eastern Standard Time"',
             "America/Indiana/Indianapolis": '"Eastern Standard Time"',
             "America/Puerto_Rico": '"SA Western Standard Time"'}
    times = queryrun(querystring)
    tz = {"1": '"Hawaiian Standard Time"',
          "2": '"Alaskan Standard Time"',
          "3": '"Pacific Standard Time"',
          "4": '"Mountain Standard Time"',
          "5": '"Mountain Standard Time_dstoff"',
          "6": '"Central Standard Time"',
          "7": '"Eastern Standard Time"',
          "8": '"SA Western Standard Time"'}
    if not times:
        print(''' Select the timezone to use:
              1. Hawaii
              2. Alaska
              3. Pacific Time
              4. Mountain Time
              5. Arizona
              6. Central Time
              7. Eastern Time
              8. Puerto Rico
              ''')
        answer = input("Choose your timezone: ")
        if answer in tz:
            destination = "\\\\" + computer + "\\c$\\rlprinttool\\setTime.bat"
            with open(destination, "w") as time:
                time.write(r'%__appdir__%tzutil.exe /s ' + tz[answer])
            time_set = "c:\\rlprinttool\\setTime.bat"
    elif times in zones:
        destination = "\\\\" + computer + "\\c$\\rlprinttool\\setTime.bat"
        with open(destination, "w") as time:
            time.write(r'%__appdir__%tzutil.exe /s ' + zones[times])
        time_set = "c:\\rlprinttool\\setTime.bat"
    return time_set


def main():
    computer = input("Enter the computer IP Address: ")
    user = input("Enter your User name: ")
    userpass = input("Enter your password: ")
    file_copy(computer)
    install = "c:\\rlprinttool\\install.bat"
    connection(install, computer, user, userpass)
    connection(timez(computer), computer, user, userpass)
    rmtree("\\\\" + computer + "\\c$\\rlprinttool")
    return


def connection(exe, computer, user, userpass):
    c = Client(computer, username=user, password=userpass)
    c.connect()
    try:
        c.create_service()
        c.run_executable(exe)
    finally:
        c.cleanup()
        c.disconnect()
    return


# Call the main function if this is the application run
if __name__ == '__main__':
    main()
