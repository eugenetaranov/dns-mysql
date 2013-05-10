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
import os.path
import MySQLdb
import json

class dbConnect():
    
    def __init__(self, config):
        self.config = config

        try:
            conn = MySQLdb.connect(host = config['db']['dbhost'], user = config['db']['dbuser'],
                                    passwd = config['db']['dbpassword'], db = config['db']['dbname'],
                                    port = config['db']['dbport'])
            self.cursor = conn.cursor()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e[0], e[1])
            sys.exit (1)
    
    def __del__(self):
        self.cursor.close()
    
    def getdata(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class dns(dbConnect):
    def __zonefile(self, domain_id):
        soa = self.getdata("SELECT `domain`, DATE_FORMAT(`date`, '%Y%m%d%H%i%S'),`soa`,`admin`,`ttl`,`refresh`,`retry`,`expiry`,`min` FROM zones WHERE zoneid =" + str(domain_id))
        records = self.getdata("SELECT `subdomain`, `ttl`,`type`,`target` FROM records WHERE zoneid = %s" % domain_id)
        srv = self.getdata("SELECT `service`,`proto`,`ttl`,`priority`,`weight`,`port`,`target` FROM srv WHERE zoneid = %s" % domain_id)
        spf = self.getdata("SELECT `ttl`,`record` FROM spf WHERE zoneid = %s" % domain_id)
        with open(self.config['others']['dnsconfpath'] + str(soa[0][0]) + ".zone",'w+') as f:
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
        domains = self.getdata("SELECT `zoneid` FROM zones WHERE `date` >= (NOW() - INTERVAL %s MINUTE)" % self.config['others']['timespan'])
        if len(domains) > 0:
            for i in domains:
                self.__zonefile(i[0])
        else:
            sys.exit(0)


if os.path.dirname(__file__):
    config_file = os.path.dirname(__file__) + '/dns.conf'
else:
    config_file = os.path.dirname(__file__) + 'dns.conf'

with open(config_file, 'r+') as config_fd:
    config = json.load(config_fd)


data = dns(config)
data.run_updates()
