# felog
# Description
Felog is yet another simple logging library to quickly and simply deploy logging with projects.
The aim with this library is to have a simple to import and uniform logging system across several projects.
Felog allows such and even gives the option to enable/disable debug mode which allows for more verbose debugging.
# Dependencies
 Felog only has one dependency: logging
 # Installation
 ```
 pip install felog
 ```
 # Usage
 ## Setup a Logger
 ```
 import felog.core as felog

 log = felog.log(<project or module name>)
 ```
 ## Log Levels
 There are several log levels and you can switch between them at any time, including debug mode.
 The levels are as follows:
 - Debug
 - Info
 - Warning
 - Error
 - Critical

 To switch between these levels, you can simply call the function to facilitate as follows:
 ```
 import felog.core as felog

 log = felog.log(<project or module name>)
 log.setLevel(<level name>)
 ```
 ## Send an INFO Log
 ```
 import felog.core as felog

 log = felog.log("TEST123")

 log.info("THIS IS WHATEVER INFO YOU WANT TO LOG.")
 ```
 ## Send a WARNING Log
 ```
 import felog.core as felog

 log = felog.log("TEST123")

 log.warning("THIS IS WHATEVER INFO YOU WANT TO LOG.")
 ```
 ## Send an ERROR Log
 ```
 import felog.core as felog

 log = felog.log("TEST123")

 log.error("THIS IS WHATEVER INFO YOU WANT TO LOG.")
 ```
 ## Send a CRTICAL Log
 ```
 import felog.core as felog

 log = felog.log("TEST123")

 log.critical("THIS IS WHATEVER INFO YOU WANT TO LOG.")
 ```
 ## Setting up and using DEBUG MODE
 You can setup DEBUG MODE in one of two ways:
  ```
 import felog.core as felog

 log = felog.log(<project or module name>,debug=True)
 ```
 OR
 ```
 import felog.core as felog

 log = felog.log(<project or module name>)
 log.setLevel("debug")
 ```
 From this point forward, the logger will display debug messages as well as all others.
 To Debug you would simply send debug logs as follows:
 ```
 import felog.core as felog

 log = felog.log("TEST123",debug=True)

 log.debug("THIS IS WHATEVER INFO YOU WANT TO LOG.")
 ```
 To disable DEBUG MODE, you would simply set the log level back to INFO as follows:
  ```
 import felog.core as felog

 log = felog.log("TEST123",debug=True)

 log.debug("THIS IS WHATEVER INFO YOU WANT TO LOG.")
 log.setLevel("info")
 log.info("THIS IS OTHER INFO YOU WANT TO LOG.")
 ```