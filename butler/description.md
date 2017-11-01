## Part a.
Please add a new process to your butler system that tracks this assert.
```assert TESTING = (!phil[0].eat W phil[0].arise)```
You probably notice that it should fail. I wanted this so you can see if you catch the failure.

My ideal is for you to write a "weak-until" program that takes the left and right operands in on the command line.

## Part b.
This one is a bit harder, I believe. I'd like you to build a program for this property.

```property TESTING2 =(phil[0].sitdown->phil[1].arise->TESTING2).  //should fail```

You can run both part a and part b on a laptop. Use some simple python GUI library to show a mini-dashboard. Give the state of the assert and of the property. Note you now have more than leds to play with. Think about giving the user as much info as possible. Maybe an error trace?

I think I would like to see this one in action. Turn in a link to your code but demo it for me. I can arrange to meet up with your group Saturday and Sunday if we can find a reasonable time.
