#!/usr/bin/env python

import os
import clone_db
from mysql.utilities.exception import MUTLibError, UtilDBError

class test(clone_db.test):
    """check errors for clone db
    This test ensures the known error conditions are tested. It uses the
    clone_db test as a parent for setup and teardown methods.
    """

    def check_prerequisites(self):
        return clone_db.test.check_prerequisites(self)

    def setup(self):
        self.server1 = self.servers.get_server(0)
        try:
            self.server1.exec_query("DROP DATABASE IF EXISTS util_clone")
            self.server1.exec_query("CREATE DATABASE util_clone")
        except MUTLibError, e:
            raise MUTLibError("Failed to create test database.")
        return True
        
    def run(self):
        self.server1 = self.servers.get_server(0)
        self.res_fname = "result.txt"
       
        from_conn = "--source=" + self.build_connection_string(self.server1)
        to_conn = "--destination=" + self.build_connection_string(self.server1)

        test_num = 1        
        # Check --rpl option errors        
        cmd_str = "mysqldbcopy.py %s %s util_clone:util_clone2 " % \
                  (to_conn, from_conn)
        comment = "Test case %s - error: %s but no --rpl" % \
                  (test_num, "--rpl-user=root")
        res = self.run_test_case(2, cmd_str + "--rpl-user=root", comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        test_num += 1

        # Attempt to use --rpl while cloning
        cmd_str = "mysqldbcopy.py %s %s util_clone:util_clone2 --rpl=slave" % \
                  (to_conn, from_conn)
        comment = "Test case %s - error: using --rpl with cloning" % test_num
        res = self.run_test_case(2, cmd_str, comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)
        test_num += 1

        return True
  
    def get_result(self):
        return self.compare(__name__, self.results)
    
    def record(self):
        return self.save_result_file(__name__, self.results)
    
    def cleanup(self):
        try:
            self.server1.exec_query("DROP DATABASE util_clone")
            self.server1.exec_query("DROP DATABASE util_clone2")
        except:
            pass
        return True




