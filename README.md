# CIS 650
Group members: Prachi Desai, Robert Sappington, Sam Pollard
## Group assignment - Rollercoaster

### Description
Each process is on its own edision. Each process is described below. The groupings are as follows:
1. TURNSTILE and MONITOR
2. CONTROL
3. All CARs

#### TURNSTILE AND MONITOR
The turnstile counts up to 3 people on the platform. The monitor logs everything to a file. No lights.

#### CONTROL
Control keeps track of how many passengers are on the platform and allows only 3 at
 a time, until they load on the card. It is shown by LED lights.

#### CAR
A care has 3 passengers on it. From this, passengers can make friends. There can be
 multiple cars on the track at once. We have an led light for each car.


### Some Subtleties
- Right now we are sending the messages then parsing them. It seems like a better idea would be to have different sub-topics in the cis650 larger topic. For examle, cis650prs/passengers would just say how many passengers there are.

- Another thing we should consider is when not everything starts at the exact same time. We don't want to have a passenger enter the turnstile until we're sure the control will allow it. Thus, I think we want to have logic so that turnstile publishes "ATTEMPT TO ENTER" or something, then when it gets the goahead from CONTROL it will say "arrive" so that CONTROL can update the passenger (lights, and sending to the cis650prs/passengers topic). This is one of those things where having a state machine in each one is really useful (and the modeling we did, right?)
