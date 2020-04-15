import my_debugger

debugger = my_debugger.debugger()

#   test case 1: included only the following line
#
#   debugger.load("C:\\WINDOWS\\system32\\calc.exe")

pid = input("enter the PID of the process to attach to: ")

debugger.attach(int(pid))


'''
To use:

        CNTRL+R:        tasklist | findstr Calculator.exe
'''