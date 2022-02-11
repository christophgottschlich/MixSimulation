Developed with following Versions:
    - Python 3.9
    - numpy 1.17.4
    - simpy 3.0.11

SETUP:
    1) install every package that is required
    2) just start the main script and the UI will appear

Information for Code-Execution:
    - the duration of the simulation should always be set higher than 60000 milliseconds, otherwise no messages will
    be generated. This is because of the definition of the lamda values that describe the number of messages to be
    sent per minute (calculated with a poisson-distribution based on lamda)
    - Please consider your input in the UI to be the right format, as displayed by the standard values on the right side
    - In order to execute the hitting set analysis a simulation must be performed beforehand
    - The time window that must be defined for the hitting set analysis is defined as the interval that starts after
    a message, that is monitored, arrives at a mix node. After the arrival every message that is sent by the mix node
    is then saved and gets monitored as well. This procedure is done until every monitored message has arrived at the
    egress provider.


Notice:
    If the screen is too small, the UI-window may exceed the lower edge of the screen, when the analytics are displayed.