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

for i in range(int(sys.argv[1])):
    subprocess.call(["python", "forks.py", str(myList[i])])
