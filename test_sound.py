import winsound
import threading
import time





def thread_test():
    print("I am a thread")
    winsound.Beep(2000, 500)
    return


#threads = []
for i in range(4):
    t = threading.Thread(target=thread_test)
    #threads.append(t)
    t.start()