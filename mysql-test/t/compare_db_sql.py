
#!/usr/bin/env python

import os
import compare_db
from mysql.utilities.exception import MUTLibError, UtilDBError

class test(compare_db.test):
    """simple db diff
    This test executes a consistency check of two databases on
    separate servers generating transformation SQL statements. It uses the
    compare_db test as a base for all setup and teardown methods.
    """

    def check_prerequisites(self):
        return compare_db.test.check_prerequisites(self)

    def setup(self):
        return compare_db.test.setup(self)
        
    def run(self):
        self.server1 = self.servers.get_server(0)
        self.res_fname = "result.txt"
        
        s1_conn = "--server1=" + self.build_connection_string(self.server1)
        s2_conn = "--server2=" + self.build_connection_string(self.server2)
       
        cmd_str = "mysqldbcompare.py %s %s " % (s1_conn, s2_conn)

        comment = "Test case 1 - check a sample database generate SQL"
        res = self.run_test_case(0, cmd_str + "inventory:inventory -a "
                                 "--difftype=sql", comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
            
        self.alter_data()

        comment = "Test case 2 - check database with known differences " + \
                  "generate SQL direction = server1 (default)"
        res = self.run_test_case(1, cmd_str + "inventory:inventory -a "
                                 "--difftype=sql --format=CSV", comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
            
        comment = "Test case 3 - check database with known differences " + \
                  "generate SQL direction = server2"
        res = self.run_test_case(1, cmd_str + "inventory:inventory -a "
                                 "--difftype=sql --format=CSV "
                                 "--changes-for=server2", comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)

        comment = "Test case 4 - check database with known differences " + \
                  "generate SQL direction = server1 with reverse"
        res = self.run_test_case(1, cmd_str + "inventory:inventory -a "
                                 "--difftype=sql --format=CSV "
                                 "--changes-for=server1 --show-reverse",
                                 comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)

        comment = "Test case 5 - check database with known differences " + \
                  "generate SQL direction = server2 with reverse"
        res = self.run_test_case(1, cmd_str + "inventory:inventory -a "
                                 "--difftype=sql --format=CSV "
                                 "--changes-for=server2 --show-reverse",
                                 comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)

        self.do_replacements()

        return True
          
    def get_result(self):
        return self.compare(__name__, self.results)
    
    def record(self):
        return self.save_result_file(__name__, self.results)
    
    def cleanup(self):
        return compare_db.test.cleanup(self)




