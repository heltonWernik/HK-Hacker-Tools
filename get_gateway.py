#!/usr/bin/env python

import subprocess
import re

route_result = subprocess.check_output("route -n")
gateway = re.search(r"", route_result)



