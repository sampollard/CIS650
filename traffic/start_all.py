import subprocess
import sys
#print(len(sys.argv))



processwait =[]
for i in range(4):
    try:
        p = subprocess.Popen(['python2', 'CARS.py',str(i),str(i),'Straight'] )
        processwait.append(p)
        print("started car" + str(i))
    except EnvironmentError as e:
        sys.exit('failed to start %r, reason: %s' % (executable, e))
# Add a second car to queue 0
p = subprocess.Popen(['python2', 'CARS.py',str(4),str(0),'Right'] )
processwait.append(p)
print("started car" + str(4))

p = subprocess.Popen(['python2', 'CARS.py',str(5),str(0),'Straight'] )
processwait.append(p)
print("started car" + str(5))

p = subprocess.Popen(['python2', 'CARS.py',str(6),str(1),'Straight'] )
processwait.append(p)
print("started car" + str(6))

y=0
for i in range(4):
    try:
        
        if i == 1:
            y=1
        else:
            y=0
        p = subprocess.Popen(['python2', 'QUEUE.py',str(i),str(y)] )
        processwait.append(p)
        print("started queue" + str(i))
    except EnvironmentError as e:
        sys.exit('failed to start %r, reason: %s' % (executable, e))



#Wait for each process to end, for call control c and kill all child processes
while len(processwait)>1:
    try: # wait for the child process to finish
        for each in processwait:
            each.wait()
    except KeyboardInterrupt:
        sys.exit("interrupted")
