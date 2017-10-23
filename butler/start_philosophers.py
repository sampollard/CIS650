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

for i in range(int(sys.argv[1])):
    if (i == int(sys.argv[1])-1):
        subprocess.call(["python", "phils.py", str(myList[i]) , str(myList2[i]), str(myList2[0])])
    else:
        subprocess.call(["python", "phils.py", str(myList[i]) , str(myList2[i]), str(myList2[i+1])])
