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



#       obtaining thread context and register contents test
list = debugger.enumerate_threads()

#       For each thread in the list we want to
#       grab the value of each of the registers

for thread in list:

        thread_context = debugger.get_thread_context(thread)

        #       echo
        print('[*] Dumping Registers for thread ID: 0x%08x', thread)
        print('[**] EIP:\t0x%08x',thread_context.Eip)
        print('[**] ESP:\t0x%08x',thread_context.Esp)
        print('[**] EBP:\t0x%08x',thread_context.Ebp)
        print('[**] EAX:\t0x%08x',thread_context.Eax)
        print('[**] EBX:\t0x%08x',thread_context.Ebx)
        print('[**] ECX:\t0x%08x',thread_context.Ecx)
        print('[**] EDX:\t0x%08x',thread_context.Edx)
        print('[*] End Dump')

debugger.detach()       #       closes the app as well