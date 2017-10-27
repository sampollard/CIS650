import subprocess
import sys
#print(len(sys.argv))

myList = ['a','b','c','d','e','f','g','h','i']

if len(sys.argv) < 2:
    print("Need to pass in a number as an arg")
    sys.exit(1)

try:
    if not isinstance(int(sys.argv[1]), int):
        print("Pass in a int")
        sys.exit(1)
except:
    print("Pass in a int")
    sys.exit(1)

processwait =[]
for i in range(int(sys.argv[1])):
    try:
        p = subprocess.Popen(['python', 'fork.py', str(myList[i])])
        processwait.append(p)
        print("started " + str(myList[i]))
    except EnvironmentError as e:  
        sys.exit('failed to start %r, reason: %s' % (executable, e))
        
#Wait for each process to end, for call control c and kill all child processes
while len(processwait)>1:
    try: # wait for the child process to finish
        for each in processwait:
            each.wait()
    except KeyboardInterrupt: 
        sys.exit("interrupted")
