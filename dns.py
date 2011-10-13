#!/usr/bin/env python
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#       If you have any questions or inquiries please feel free to email at
#       eugene@jinocloud.com

import sys
import MySQLdb
import os.path

#### START VARIABLES ####
TIMESPAN = 500
DBHOST = "127.0.0.1"
DBPORT = 3306
DBUSER = "dnsuser"
DBPASSWORD = "dnspassword"
DBNAME = "dns"
DNSCONFPATH = ""
#### END VARIABLES ####

class fetchdata():
    global DBHOST, DBUSER, DBPASSWORD, DBNAME, DBPORT, TIMESPAN
    
    def __dbconnect(self, request):
        try:
            conn = MySQLdb.connect (host = DBHOST,
                            user = DBUSER,
                            passwd = DBPASSWORD,
                            db = DBNAME,
                            port = DBPORT)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        cursor = conn.cursor()
        cursor.execute(request)
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return rows
    
    def __zonefile(self, domain_id):
        soa = self.__dbconnect("SELECT `domain`, DATE_FORMAT(`date`, '%%Y%%m%%d%%H%%i%%S'),`soa`,`admin`,`ttl`,`refresh`,`retry`,`expiry`,`min` FROM zones WHERE zoneid = %s" % domain_id)
        records = self.__dbconnect("SELECT `subdomain`, `ttl`,`type`,`target` FROM records WHERE zoneid = %s" % domain_id)
        srv = self.__dbconnect("SELECT `service`,`proto`,`ttl`,`priority`,`weight`,`port`,`target` FROM srv WHERE zoneid = %s" % domain_id)
        spf = self.__dbconnect("SELECT `ttl`,`record` FROM spf WHERE zoneid = %s" % domain_id)
        with open(DNSCONFPATH + str(soa[0][0]) + ".zone",'w+') as f:
            f.write("$ORIGIN\t%s.\n" % soa[0][0])
            f.write("$TTL\t\t%s\n" % soa[0][4])
            f.write("%s.\tIN\tSOA\t%s. %s (\n" % (soa[0][0], soa[0][2], soa[0][3]) )
            f.write("\t"*3 + str(soa[0][1]) + "\n")
            f.write("\t"*3 + str(soa[0][5]) + "\n")
            f.write("\t"*3 + str(soa[0][6]) + "\n")
            f.write("\t"*3 + str(soa[0][7]) + "\n")
            f.write("\t"*3 + str(soa[0][8]) + " )\n")
            for i in records:
                f.write("%s\t\t%s\tIN %s\t%s\n" % i)
            if len(srv) > 0:
                f.write("%s._%s\t%s\tIN SRV\t%s\t%s\t%s\t%s\n" % srv[0] )
            if len(spf) > 0:
                f.write('\t\t%s\tIN TXT\t"%s"\n' % spf[0])

    
    def run_updates(self):
        domains = self.__dbconnect("SELECT `zoneid` FROM zones WHERE `date` >= (NOW() - INTERVAL %s MINUTE)" % TIMESPAN)
        if len(domains) > 0:
            for i in domains:
                self.__zonefile(i[0])
        else:
            sys.exit(0)


data = fetchdata()
data.run_updates()
