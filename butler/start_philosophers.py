import subprocess
import sys
#print(len(sys.argv))

myList = [0,1,2,3,4,5,6,7,8,9]
myList2 = ['a','b','c','d','e','f','g','h','i']


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

        if (i == int(sys.argv[1])-1):
           p = subprocess.Popen(["python", "phil.py", str(myList[i]) , str(myList2[i]), str(myList2[0])])
        else:
           p = subprocess.Popen(["python", "phil.py", str(myList[i]) , str(myList2[i]), str(myList2[i+1])])
        processwait.append(p)
        print("started " +  str(myList[i]) + " "+ str(myList2[i]) + " "+str(myList2[i+1]))
    except EnvironmentError as e:  
        sys.exit('failed to start %r, reason: %s' % (executable, e))
                                                                                    
#Wait for each process to end, for call control c and kill all child processes

while len(processwait)>1:
    try: # wait for the child process to finish
        for each in processwait:
            each.wait()
    except KeyboardInterrupt:
        sys.exit("interrupted")
