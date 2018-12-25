import platform
import re
import subprocess
def get_default_gateway():
    if platform.system() == "Darwin":
        route_default_result = subprocess.check_output(["route", "get", "default"])
        gateway = re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", route_default_result).group(0)

    elif platform.system() == "Linux":
        route_default_result = re.findall(r"([\w.][\w.]*'?\w?)", subprocess.check_output(["ip", "route"]))
        gateway = route_default_result[2]

    if route_default_result:
        return(gateway)
    else:
        print("(x) Could not default gateway.")

print(get_default_gateway())
