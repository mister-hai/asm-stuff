    '''
    SIGBREAK (Unix), CTRL_BREAK_EVENT (Windows):
        When CTRL + BREAK is pressed on the keyboard
    SIG_DFL: 
        Perform the default function for the signal
    SIG_IGN: 
        Ignore the given signal. As an instance, we can do signal.signal(signal.SIGBREAK, signal.SIG_IGN) to ignore the break signal.
    SIGABRT: 
        Abort signal
    SIGALRM:
        Timer signal
    SIGBUS: 
        Bad memory access signal
    SIGCHILD/SIGCLD: 
        Child processes stopped or terminated
    SIGCOUNT: 
        Continue the process if it is currently stopped
    SIGFPE: 
        If a floating-point exception is raised
    SIGHUP: 
        If hangup/death is detected on controlling terminal/process
    SIGILL: 
        When illegal instruction is encountered
    SIGINT (Unix), CTRL_C_EVENT(Windows): 
        CTRL+ C is pressed on the keyboard (keyboard interrupt)
    SIGKILL: 
        When the signal to kill is raised
    SIGPIPE: 
        When we are writing to a broken pipe without any readers
    SIGSEGV:
        Invalid memory reference
    SIGTERM: 
        When the termination signal is raised


Signal Functions

There are a number of functions implemented in the signal module. I will outline the must-know functions amongst them.

    signal.alarm(time):

If you want to raise the SIGALRM signal , set the 
    signal.alarm(time) 
function with the specified time in seconds.
If the time is set to 0, then it disables the alarm
Setting a new alarm cancels any previously scheduled alarms.

2. signal.pause()
The process sleeps until a signal is received. And then the signal handler is called.

3. signal.raise_signal(number of signal):
It sends a signal to the calling process

4. signal.setitimer(which, seconds, interval)
This function accepts float number of seconds which we can use to raise a signal. Also after that, for each interval, the signal is sent to the process.

5. signal.siginterrupt(signalnum, flag):
It changes system call restart behaviour.
If the flag is False then the system calls are restarted when they are interrupted by signal signalnum
If the flag is True then the system calls are interrupted

6. signal.getsignal(signalnum)

It takes the signal and returns the handler.

7. signal.signal(signalnum, handler):
Lastly and most importantly, I wanted to cover the functional signal()
This function sets the handler whenever the signal signalnum is received.
The handler is essentially a Python function/callable that takes in either two of the arguments:

    The signal number
    Current stack frame (or signal.SIG_IGN or signal.SIG_DFL) as arguments.

In a multi-threaded application, it can only be called from the main thread
3. Platform-Specific Signals

In Linux, we can pass in any of the acceptable enum values which I have mentioned above as argument to the signal function.

In Windows, the acceptable values for signal() are SIGABRT, SIGFPE, SIGINT, SIGILL, SIGSEGV, SIGTERM, SIGBREAK. A ValueError is raised for any other case.
4. Signal Programming Example

Let’s quickly go over an example to demonstrate how signaling works:
Use case

    We are going to set the alarm for 10 seconds.
    We are also going to listen to the SIGALM signal which is raised when an alarm is signaled.
    When the alarm is signaled after the 10 seconds time then the custom signal handler my_handler will raise TimeoutError

signal.signal(signal.SIGALM, my_handler)
signal.alarm(10)def my_handler(signum, frame):
 print(‘Took too long’)
 raise TimeoutError(‘took too long’)

    We are then going to call a long-running function which is going to sleep for 20 seconds.

def get_data():
 import time
 time.sleep(20)get_data()

After 10 seconds of waiting, the alarm signal will be raised. It will be handled by the my_handler which will raise the TimeoutError.

The signals are asynchronous in nature and can also be used as decorators.
5. Best Practises

Lastly, I wanted to outline the best practices for signals.

    Do not use signals for inter-thread communication. 
    The signals are always executed in the main Python thread.
    If we want inter-thread communication then use the synchronisation 
    primitives from the threading module.
    Long-running operations such as a regular expression that attempts 
    to find patterns in a large text run until it completes its 
    execution. They are not interrupted by the signals. The signals 
    are called after it finished its computation.
    If there is an error raised by C code then it is not optimum to 
    catch those synchronous errors. Such examples are SIGFPE or SIGSEGV.
    This is because Python will return the signal handler to the C code
    which will raise the same signal again. Thus it will hang the code.
    We can use the faulthandler module in Python to report on synchronous
    errors.
'''
import sys
from ..Utils import redprint
import signal
from signals import *

def sigintEvent(sig, frame):
    redprint('[!] CTRL + C PRESSED! Exiting program!')
    exit(0)
signal(SIGINT, sigintEvent)
