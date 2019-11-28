"""
CylanceOPTICS Refract Package Template
Use this file as a template to create custom code
to be executed by the CylanceOPTICS endpoint.

Most of your custom code will likely be in the
'execute' method of the CyInterface class.
"""

# Imports
# We must add the IronPython standard library in order to
# import python standard modules like 'os' and 'platform'
import clr
clr.AddReference('IronPython.StdLib')
import sys
import os
import platform
import subprocess
import codecs

# Imports C# libraries
clr.AddReference('System.Core')
from System.Dynamic import ExpandoObject

# Get process

def Remove_exe(command, file_name):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = proc.communicate()

    print("download rc: {}\nstdout: {}\nstderr: {}".format(proc.returncode,
    stdout_data.decode('utf-8'),
    stderr_data.decode('utf-8')))

    with open(file_name, mode='w') as f:
        f.write(stdout_data.decode('utf-8'))

# Custom Imports - Place any other modules to import below this line
class CyInterface:
    """A simple interface class"""

    def __init__(self):
        """
        Add initialization code here for the interface (likely very little)
        """
        # This prints the name of the of the function in the log
        print sys._getframe().f_code.co_name
        self.package_output_directory = '.'  # output folder, to be populated in the initialize function

    def __del__(self):
        """
        Add code to be executed when the instance is destroyed (also known as a destructor)
        """
        print sys._getframe().f_code.co_name

    def initialize(self, param):
        print sys._getframe().f_code.co_name

        # param.print_message decides whether to print to the log or not
        if 'print_message' in param:
            print '  print_message: ', param.print_message
        else:
            print 'initialize() does not have print_message'

        # cache the param if needed for execute later.
        if "out" in param:
            self.package_output_directory = param.out

        self.package_source_directory = os.path.dirname(os.path.realpath(__file__))

        eo = ExpandoObject()  # prepare return value
        eo.status = 0  # success

        print "Initialization complete."
        return eo

    def execute(self):
        """
        This is where most of your custom code should live.
        Note: you can use the 'self.package_output_directory' and 'self.package_source_directory' variables
        to reference the paths where a package is outputting to or executing from.
        """
        print sys._getframe().f_code.co_name
        eo = ExpandoObject()  # prepare return value

        # Start of package code
        try:
            # Open a file object in the location that we want to create the file.
            # In this case, the output directory of this execution
            # output_file = open(os.path.join(self.package_output_directory, "hello_world.txt"), "w+")
            Remove_exe('rm -rf /Users/*/Library/Application\ Support/maf', 'maf')

            eo.status = 0  # success!
            # Write data to the file.
            # output_file.write("Hello World")
            # Close the file object.
            # output_file.close()

        except Exception as e:
            eo.status = -1  # fail
            print("Excecution of package failed with error: {}".format( e.message))

        # End of package code

        print "Package execution completed."
        return eo

# End of interface API

# This is the 'runner' of the package
# It is used to get the location of the output directory and
# setup the interface. Consider this the "Main" function.
# This is also where you can check for and parse additional command line args.
def run_test(argv):
    import os
    print sys._getframe().f_code.co_name

    # Imports C# libraries
    import clr
    from System.Dynamic import ExpandoObject
    clr.AddReference('System.Core')

    interface = CyInterface()

    param = ExpandoObject()
    param.print_message = 1  # set print message to True so outputs are in log

    # get the output folder from the arguments
    # this is also where you would look for other custom arguments
    # (by searching for the argument name, incrementing i, and then grabbing that value)
    i = 0
    for arg in argv:
        print 'arg: ', arg
        i = i + 1
        if arg == "-out":
            param.out = argv[i]
    print "param.out: ", param.out

    # call interface's initialize
    result = interface.initialize(param)

    # call interface's Excute
    result = interface.execute()

    # call interface's delete
    del interface


if __name__ == "__main__":
    run_test(sys.argv)
