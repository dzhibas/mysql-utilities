#!/usr/bin/env python

import os
import check_index
from mysql.utilities.exception import MUTLibError

class test(check_index.test):
    """check parameters for the check_index utility
    This test executes the check index utility parameters on a single server.
    It uses the check_index test as a parent for setup and teardown methods.
    """

    def check_prerequisites(self):
        return check_index.test.check_prerequisites(self)

    def setup(self):
        return check_index.test.setup(self)

    def run(self):
        self.res_fname = "result.txt"
        from_conn = "--server=" + self.build_connection_string(self.server1)

        cmd_str = "mysqlindexcheck.py %s " % from_conn

        comment = "Test case 1 - do the help"
        res = self.run_test_case(0, cmd_str + "--help", comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)

        comment = "Test case 2 - show drops for a table with dupe indexes"
        res = self.run_test_case(0, cmd_str + "util_test_a.t1 --show-drops "
                                 "-vv", comment)
        if not res:
            raise MUTLibError("%s: failed" % comment)

        comment = "Test case 3 - show drops for a table with dupe indexes"
        res = self.run_test_case(0, cmd_str + "util_test_a.t1 -d",
                                 comment)
        if not res:
            return False

        comment = "Test case 4 - show drops for a table without dupe indexes"
        res = self.run_test_case(0, cmd_str + "util_test_c.t6 --show-drops "
                                 "-vv", comment)
        if not res:
            return False

        comment = "Test case 5 - same as test case 2 but quiet"
        res = self.run_test_case(0, cmd_str + "util_test_a.t1 --show-drops ",
                                 comment)
        if not res:
            return False

        comment = "Test case 6 - same as test case 4 but quiet"
        res = self.run_test_case(0, cmd_str + "util_test_c.t6 -d ",
                                 comment)
        if not res:
            return False

        comment = "Test case 7 - show indexes"
        res = self.run_test_case(0, cmd_str + "util_test_a.t1 --show-indexes",
                                 comment)
        if not res:
            return False

        comment = "Test case 8 - show indexes with -i"
        res = self.run_test_case(0, cmd_str + "util_test_a.t1 -i ",
                                 comment)
        if not res:
            return False


        return True

    def get_result(self):
        return self.compare(__name__, self.results)

    def record(self):
        return self.save_result_file(__name__, self.results)

    def cleanup(self):
        return check_index.test.cleanup(self)
