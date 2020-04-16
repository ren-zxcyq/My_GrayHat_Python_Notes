from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32     #   function itself is ?responsible? o.O
                                        #   cdlL(dllname) -> caller is responsible

class debugger():
    def __init__(self):
        self.h_process          =   None
        self.pid                =   None
        self.debugger_active    =   False

    def load(self, path_to_exe):

        #   dwCreation flag determines how to create the process
        #   set creation_flags = CREATE_NEW_CONSOLE if you want
        #   to see the calculator GUI
        creation_flags = DEBUG_PROCESS

        #   instantiate the structs
        startupinfo         = STARTUPINFO()
        process_information = PROCESS_INFORMATION()


        #   The following two options allow the started process
        #   to be shown as a separate window
        #   This also illustrates how different settings in the
        #   STARTUPINFO struct can affect the debuggee.
        startupinfo.dwflags     = 0x1
        startupinfo.wShowWindow = 0x0


        #   We then initialize the cb variable in the STARTUPINFO struct
        #   which is just th esize  of the struct itself
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                    None,
                                    None,
                                    None,
                                    None,
                                    creation_flags,
                                    None,
                                    None,
                                    byref(startupinfo),
                                    byref(process_information)
        ):
            print("[*] We have successfully launched the process!")
            print("[*] PID: %d", process_information.dwProcessId)
        else:
            print("[*] Error: 0x%08x.", kernel32.GetLastError())

# To prepare a process to attach to   -   obtain a handle to the process itself.
# Most of the function we will be using require a valid process handle

# Access the Process before we attampt to debug it


# This is done with           kernel32.dll.OpenProcess()

# HANDLE WINAPI OpenProcess(
#     DWORD       dwDesiredAccess,      #   What type of access rights are we requesting for the process object?    for debugging -> PROCESS_ALL_ACCESS
#     BOOL        bInheritHandle,       #   always False for our purposes
#     DWORD       dwProcessId           #   
# );
#       upon success ->     RETURNS handle to the Process Object



# We attach to the process using      DebugActiveProcess()
#
# BOOL WINAPI DebugActiveProcess(
#     DWORD   dwProcessId
# );
#
#
#
#   system determines if we have permissions required
#   target process assumes that the attaching process(the debugger) is ready to
#       handle debug events   ->            Relinquishes control to the debugger
#
#       The debugger traps these debugging events by calling
#           WaitForDebugEvent() in a loop
#
#                   loop over this:
# BOOL WINAPI WaitForDebugEvent(
#     LPDEBUG_EVENT lpDebugEvent,       #   pointer to the DEBUG_EVENT struct
#     DWORD dwMilliseconds              #   INFINITE so that the WaitForDebugEvent() call doesn't return until an event occurs
# );
#
#
#   For each event the debugger catches, there are
#       associated event handlers that perform some type of action
#       before letting the process continue
#
#   
#   Once the handlers are finished executing, we want the process to continue executing.
#   This is achieved using          ContinueDebugEvent()
#
# BOOL WINAPI ContinueDebugEvent(
#     DWORD   dwProcessId,              #
#     DWORD   dwThreadId,               #   fields in DEBUG_EVENT struct
#     DWORD   dwContinueStatus          #   DBG_CONTINUE    or  DBG_EXCEPTION_NOT_HANDLED -> Continue Processing the Exception
# );
#
#
#   
#
#
#   The only thing left to do is Detaching from the process.
#
#   DebugActiveProcessStop()        <-  PID that you wish to detach from as its only param
#
#
#   Let's put all of this together:
#
#
#
#
        print('[*] We have successfully launched the process!')
        print('[*] PID: %d', process_information.dwProcessId)

        #   Obtain a valid handle to the newly created process
        #   & store it for future access
        self.h_process = self.open_process(process_information.dwProcessId)

    def open_process(self, pid):
        
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)    # update #2
        return h_process
#     DWORD       dwDesiredAccess,      #   What type of access rights are we requesting for the process object?    for debugging -> PROCESS_ALL_ACCESS
#     BOOL        bInheritHandle,       #   always False for our purposes
#     DWORD       dwProcessId

    def attach(self, pid):
        
        self.h_process = self.open_process(pid)
        print("Successfully attached!")
        #   We attempt to attach to the process
        #   if this fails => exit the call
        if kernel32.DebugActiveProcess(pid):
            print('[*] Calling kernel32.DebugActiveProcess - ',pid)
            self.debugger_active    =   True
            self.pid                =   int(pid)
            #self.run()          #   update #1       is to remove this call
                                #   BUT: if i remove it the process & the debugger exit
        else:
            print("[*] Unable to attach to the process")

    def run(self):
        
        #   Now we have to poll the debuggee for debugging events
        while self.debugger_active == True:
            self.get_debug_event()

    def get_debug_event(self):

        debug_event         =   DEBUG_EVENT()
        continue_status     =   DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            
            #   WE AREN'T going to build any event handlers
            #   just yet. Let's just resume the process for now.
             
            #   if everything else works comment out the following:
            #input('Press a key to continue')
            #self.debugger_active = False
            #


            #   This line creates an infinite loop:
            #print('[*] Calling kernel32.ContinueDebugEvent')
            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status
            )
            #
            #   perhaps this loop needs to handle if the process is still running, because if i close the window
            #   it keeps on looping forever
            #

    def detach(self):

        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished Debugging. Exiting")
            return True
        else:
            print("there was an error")
            return False


    #   Obtaining CPU Register State
    #
    #       #   1. Obtain a handle to the currently executing thread in the debuggee
    #
    #                   OpenThread()

                        # HANDLE WINAPI OpenThread(
                        #     DWORD dwDesiredAccess,
                        #     BOOL bInheritHandle,              #   sister func to OpenProcess()
                        #     DWORD dwThreadId                  #   <- Process ID everything else is the same
                        # );
    #                                                           #   except this one takes a thread Identifier
    #       #   - Obtain a list of all the threads currently executing inside the process
    #       #   - select the thread we want
    #       #   - obtain a valid handle using OpenThread()
    def open_thread(self, thread_id):
        print('open_thread')

        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread is not None:
            return h_thread
        else:
            print('[*] Could not obtain a valid thread handle.')
            return False


    def enumerate_threads(self, thread_id=None, h_thread=None):
        


        print('enumerate_threads')

        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:
            #   Have to set size of the struct
            #   or the call will fail
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))     #   pass obj THREADENTRY32 by reference

                            # contains relevant info for the first thread that was
                            #                                             found.


                            #                                             typedef struct THREADENTRY32 {
                            #                                                 DWORD dwSize;                       <-----
                            #                                                 DWORD cntUsage;
                            #                                                 DWORD th32ThreadID;                 <-----
                            #                                                 DWORD th32OwnerProcessID;           <-----
                            #                                                 LONG tpBasePri;
                            #                                                 LONG tpDeltaPri;
                            #                                                 DWORD dwFlags;
                            #                                             };
            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot, byref(thread_entry))

            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False


    def get_thread_context(self, thread_id=None, h_thread=None):

        print('get_thread_Context')
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        #   Obtain a handle to the thread
        if not h_thread:
            self.open_thread(thread_id)

        if kernel32.GetThreadContext(h_thread, byref(context)):     #   if it actually retrieves Context of the thread, just close
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False    #None                                   #   @TODO it jumps here -> 64 bit?! https://stackoverflow.com/a/18622123
                                                                                                #       https://stackoverflow.com/a/18814507