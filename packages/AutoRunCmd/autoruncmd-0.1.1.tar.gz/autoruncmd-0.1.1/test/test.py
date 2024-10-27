from autoruncmd import *

# INIT
name = ".autoruncmd.test"
createConfig(name)

# ADD SCRIPT
name = ".autoruncmd.test"
header = "tests"
script = "test=running test - addtoScript"
addtoScript(name, header, script)

# RUN SCRIPT
name = ".autoruncmd.test"
header = "tests"
runScript(header, name)


# FIND SCRIPT
name = ".autoruncmd.test"
line = "test"
header = "tests"
findLine(name, line, header)