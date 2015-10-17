#!/usr/bin/env python
'''
    Copyright (C) 2013-2015 xtr4nge [_AT_] gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import os
import time
import select
import readline
import glob
from lib.Webclient import Webclient
from configobj import ConfigObj

config = ConfigObj("init.conf")

__VERSION__ = "1.0"

server = config["api"]["server"]
token = config["api"]["token"]

def call_api(execute):
    out =  w.submitGet("api=" + str(execute))
    try:
        return out.json()
    except:
        pass

class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERL = '\033[4m'
    ENDC = '\033[0m'

def load_commands():
    data = ["show", "modules", "options", "use", "set", "help", "start", "stop", "status", "clear"]
    return data

def load_config():
    data = ["config/io/in", "config/io/out", "config/io/action"]
    return data

def load_modules():
    return modules

def complete(text, state):

    data = []
    data.extend(load_commands())
    data.extend(load_config())
    data.extend(load_modules())

    for line in data:
        if line.startswith(text):
            if not state:
                return line
            else:
                state -= 1

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def search_str(data):
    
    datafile = []
    datafile.extend(modules)
    
    out = []
    for line in datafile:
        if data in line:
            out.append(line.strip())

    return out

# Message output
def show_error(message):
    print bcolors.RED + bcolors.BOLD + "[-] " + bcolors.ENDC + str(message)

def show_alert(message):
    print bcolors.YELLOW + bcolors.BOLD + "[!] " + bcolors.ENDC + str(message)

def show_msg(message):
    print bcolors.GREEN + bcolors.BOLD + "[+] " + bcolors.ENDC + str(message)

def show_info(message):
    print bcolors.BLUE + bcolors.BOLD + "[*] " + bcolors.ENDC + str(message)

# Start module
def set_module_start(module):
    show_info("Starting module " + module[1])
    execute = "/module/" + module[1] + "/start"
    out =  w.submitGet("api=" + str(execute))
    
    execute = "/module/" + module[1]
    out =  w.submitGet("api=" + str(execute))
    
    if out.json()[0] == True:
        show_msg("Module started.")
    else:
        show_error("The module cannot be started.")

# Stop module
def set_module_stop(module):
    show_info("Stopping module " + module[1])
    execute = "/module/" + module[1] + "/stop"
    out =  w.submitGet("api=" + str(execute))
    
    execute = "/module/" + module[1]
    out =  w.submitGet("api=" + str(execute))
    
    if out.json()[0] == False:
        show_info("Module stopped.")
    else:
        show_error("Fail")

# Show module status
def get_module_status(module):
    execute = "/module/" + module[1]
    out =  w.submitGet("api=" + str(execute))
    
    if out.json()[0] == True:
        show_info(module[1] + " is enabled")
    else:
        show_info(module[1] + " is disabled")

# USE MODULE
def use_module(module):
        
    module = module.split("/")
    
    while 1:
        
        prompt = raw_input(bcolors.BOLD + "shell " + bcolors.ENDC + module[0] +"(" + bcolors.RED + "%s" % module[1] + bcolors.ENDC + ") > ")
        
        if prompt == "back": break
        
        if prompt == "quit" or prompt == "exit": sys.exit()
        
        if prompt == "help" or prompt == "?":
            print
            print " Command          Description"
            print " -------          -----------"
            print bcolors.BOLD + " ?" + bcolors.ENDC + "                Help menu"
            print bcolors.BOLD + " back" + bcolors.ENDC + "             Move back from current context"
            print bcolors.BOLD + " clear" + bcolors.ENDC + "            Clear the console"
            print bcolors.BOLD + " exit" + bcolors.ENDC + "             Exit the console"
            print bcolors.BOLD + " start" + bcolors.ENDC + "            Starts current module"
            print bcolors.BOLD + " stop" + bcolors.ENDC + "             Stops current module"
            print bcolors.BOLD + " status" + bcolors.ENDC + "           Show current module status"
            print bcolors.BOLD + " show options" + bcolors.ENDC + "     Show module options [to be implemented...]"
            print
            
        if prompt == "show options":
            print "[to be implemented...]"
        
        # to use module
        if prompt.startswith("use"):
            prompt = prompt.split(" ")
            
            if prompt[1] in search_str(prompt[1]):
                use_module(prompt[1])
            else:
                show_error("Failed to load module: " + prompt[1])
                
            prompt = ""

        # start module        
        if prompt == "start":
            set_module_start(module)
            
        # stop module
        if prompt == "stop":
            set_module_stop(module)
        
        # status module
        if prompt == "status":
            get_module_status(module)
            pass
        
        # clear screen            
        if prompt == "clear":
            os.system('clear')

# USE CONFIG
def use_config(config):
    data = config.split("/")
    name = config.replace(data[0] + "/", "")
    while 1:
        prompt = raw_input(bcolors.BOLD + "shell " + bcolors.ENDC + data[0] +"(" + bcolors.RED + "%s" % name + bcolors.ENDC + ") > ")
        
        if prompt == "back": break
        
        if prompt == "quit" or prompt == "exit": sys.exit()
        
        if prompt == "help" or prompt == "?":
            print
            print " Command          Description"
            print " -------          -----------"
            print bcolors.BOLD + " ?" + bcolors.ENDC + "                Help menu"
            print bcolors.BOLD + " back" + bcolors.ENDC + "             Move back from current context"
            print bcolors.BOLD + " clear" + bcolors.ENDC + "            Clear the console"
            print bcolors.BOLD + " exit" + bcolors.ENDC + "             Exit the console"
            print bcolors.BOLD + " show options" + bcolors.ENDC + "     Show config options"
            print bcolors.BOLD + " set" + bcolors.ENDC + "              Set config options //set {property} {value}"
            print
        
        if prompt == "show options":
            
            try:
                print 
                print " Name      Current Setting       Description"
                print " ----      ----------------      -----------"
                
                if config == "config/io/in" or config == "config/io/out":
    
                    out = call_api("/" + config)
                    
                    print " IFACE     " + out[0]
                    print " TYPE      " + out[1] + "                     0 [Current], 1 [Manual]"
                    if out[1] == "1":
                        print " IP        " + out[2]
                        print " MASK      " + out[3]
                        print " GW        " + out[4]
                    else:
                        ip = call_api("/interface/" + out[0])[0]
                        print " IP        {" + ip + "}"
                
                elif config == "config/io/action":
                    IFACE = call_api("/" + config)[0]
                    
                    print " IFACE     " + IFACE
                
                print
            
            except IndexError:
                print
                show_error("Error: Ensure that IFACE exists or change TYPE to 1")
                print
                
            except:
                print
                show_error("Unexpected error: " + str(sys.exc_info()[0]))
                print
        
        if prompt.startswith("set"):
            prompt = prompt.split(" ")
            
            options = ["IFACE", "TYPE", "IP", "MASK", "GW"]
            
            if prompt[1].upper() in options:
                if config == "config/io/action":
                    execute = "/" + config + "/" + prompt[2].lower()
                else:
                    execute = "/" + config + "/" + prompt[1].lower() + "/" + prompt[2].lower()
                print prompt[1].upper() + " => " + prompt[2].lower()
                call_api(execute)
            
        if prompt == "clear":
            os.system('clear')

# Show modules list
def show_modules():
    print
    print " Modules"
    print " -------"
    for line in search_str("module"):
        print " " + line
    
    print

# Show banner
def show_banner():
    banner = """
 ___         _ _      __      ___ ___ _   ___ _        _ _ 
| __| _ _  _(_) |_ _  \ \    / (_) __(_) / __| |_  ___| | |
| _| '_| || | |  _| || \ \/\/ /| | _|| | \__ \ ' \/ -_) | |
|_||_|  \_,_|_|\__|\_, |\_/\_/ |_|_| |_| |___/_||_\___|_|_|
                   |__/
                                               version """ + bcolors.BOLD + __VERSION__ + bcolors.ENDC

    print banner
    print "Site: " + bcolors.BOLD + "http://www.fruitywifi.com" + bcolors.ENDC
    print "Twitter: " + bcolors.BOLD + "@fruitywifi @xtr4nge" + bcolors.ENDC
    print

show_banner()

# START FRUITYWIFI SESSION [API]
show_msg("Establishing session with FruityWiFi server...")
try:
    w = Webclient(server, token)
    w.login()
    w.loginCheck()
    show_msg("Session established. Have fun ;)")
    print 
except:
    time.sleep(1)
    show_error("The session cannot be established. Check the connection details.")
    print 
    sys.exit()

show_info("FruityShell v" + __VERSION__)
print

execute = "/module"
out =  w.submitGet("api=" + str(execute))

modules = []
for line in out.json():
    modules.append("module/" + line)

# START CORE
while 1:
    try:
        prompt = raw_input(bcolors.BOLD + "shell" + bcolors.ENDC + " > ")
    
        if prompt == "quit" or prompt == "exit": sys.exit()
    
        if prompt == "help" or prompt == "?":
            print
            print " Command          Description"
            print " -------          -----------"
            print bcolors.BOLD + " ?" + bcolors.ENDC + "                Help menu"
            print bcolors.BOLD + " exit" + bcolors.ENDC + "             Exit the console"
            print bcolors.BOLD + " clear" + bcolors.ENDC + "            Clear the console"
            print bcolors.BOLD + " show modules" + bcolors.ENDC + "     Show modules list"
            print bcolors.BOLD + " set" + bcolors.ENDC + "              Sets module status //set module/{name} start|stop"
            print bcolors.BOLD + " use" + bcolors.ENDC + "              Uses config|module //use module/{name}"
    
            print
        
        if prompt == "show modules":
            show_modules()
    
        # use module
        if prompt.startswith("use"):
            prompt = prompt.split(" ")
            
            if "module/" in prompt[1] :
                if prompt[1] in search_str(prompt[1]):
                     use_module(prompt[1])
                else:
                    show_error("Failed to load module: " + prompt[1])
            
            elif "config/" in prompt[1] :        
                
                if str(prompt[1]) == "config/io/in":
                    use_config(prompt[1])
                    
                elif str(prompt[1]) == "config/io/out":
                    use_config(prompt[1])
                
                elif str(prompt[1]) == "config/io/action":
                    use_config(prompt[1])
                
                else:
                    show_error("Failed to load config: " + prompt[1])
                
            prompt = ""
    
        # set module [start|stop]
        if prompt.startswith("set"):
            prompt = prompt.split(" ")
            
            if prompt[1] in search_str(prompt[1]) and len(prompt) >= 3:
                
                module = prompt[1].split("/")
                
                if prompt[2] == "start":
                    set_module_start(module)
                    
                if prompt[2] == "stop":
                    set_module_stop(module)
            else:
                show_error("Failed to set module: " + prompt[1])
                
            prompt = ""
        
        if prompt == "clear":
            os.system('clear')

    except KeyboardInterrupt:
        print "exit"
        sys.exit()
        
    except EOFError:
        print "exit"
        sys.exit()
