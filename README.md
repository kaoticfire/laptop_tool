# RLPI

RLPI is a batch program for finishing setup of rounding laptops  
This program will install the local clinic Lexmark printer onto the computer,  
wipe-out the last logged in user, and set the timezone for where the laptop is destined for.

## Requirements

This tool requires the following:
 1. [Microsoft SQL Server Management Studio](https://go.microsoft.com/fwlink/?linkid=2043154) or
 2. [Microsoft SQL Command Line Utility](https://go.microsoft.com/fwlink/?linkid=2043518) installed on the local system.
 3. Access to the corporate network
 4. Domain Admin rights on said network
 5. The remote system is attached to the domain
 6. [PSExec](https://download.sysinternals.com/files/PSTools.zip) by Mark Russinovich installed in the C:\Windows\System32\ directory
 7. The rounding laptop to be setup is using a 64-bit version of Windows 10 or later
 8. The local system is Windows 10 or later.
 9. The remote system is destined for somewhere in the United States Territory

## Support

For technical support regarding this program send emails to Virgil.Hoover@fmc-na.com

## Roadmap

Eventually this tool will be moved to a more efficient language.

## Contributions

Contributions are welcome, but all changes and contributors must abide by the license for this software.

## License

This tool is licensed under the GNU AGPLv3.  
A copy of this license can be found in the same directory as this file,  
or found at [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)

## Copyright

Copyright (c) June 6, 2018 and was modified by creator on January 3, 2019.  
Author: Virgil Hoover

## Changelog

Version 5.5 - Modified to move all variables to the top for easy organization.  
Version 5.6 - Added ability to extract clinic id from Host-name for use in queries.  
Version 5.7 - Extract Clinic from the hostname  
Version 5.8 - Add future code for when hostnames no longer contain '-'.  
Version 5.9 - Bug fix - Fixed timezone setting function.