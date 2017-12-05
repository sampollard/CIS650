# CIS 650
Group members: Prachi Desai, Robert Sappington, Sam Pollard
Assigmnents:
butler		leader		rollercoaster	traffic
## Group assignment - traffic
### Description
This manages a four-lane highway with 4 queuing zones acting as lanes in the following configuration
```
    |qz0|
    +---+---+----
    |l0 |l3 | qz3
----+---+---+----
qz1 |l1 |l2 |
----+---+---+
        |qz2|
```
There are the following scripts. To get this to work, they must be run in the following order:

- `python3 UI.py`: Starts the UI. This processes the messages and you can click through to see what happens at your leisure

- `python2 start_all.py`: This starts seven cars and four queues.

- `python2 cars_fluent.py`: This tracks how many cars are in each restricted zone. It also outputs this into a file called MONITOR.log. Note this is appended, so after each run you should delete the file. Every time something changes (i.e. a token passes, a car enters or exits a qz or a restricted zone) this adds a line consisting of a four-tuple, counting the number of cars in each restricted zone. For example, `(0,1,1,0)` indicates l1 and l2 have one car in them each. This can be used to track efficiency, though keep in mind this is not a measure of elapsed time but only prints when an event happens. An example is shown in `sample_MONITOR.log`.

- `python2 token_fluent.py`: Tracks which qz (lane) has the token. Only one should have it at at time!

- `python2 subtoken_fluent.py`: Tracks which qz (lane) has the subtoken. Only one should have it at time!


## Group assignment - Butler
### Description


## Group assignment - Leader
### Description
This assignment has 4 programs:
1. `client.py`. This runs the election process as described.
2. `cheater.py`. This starts out as the leader and just sends the leader.
3. `weak_until.py`. This tracks an assert `(!<l> W <r>) where `<l>` and `<r>` are command line arguments. These track whether the two messages have been received, and if `<l>` occurs before `<r>` then an error is flagged.
4. `UI.py`. This runs the GUI. It can take in 3 asserts and reads their status. It doesn't manage the logic, just displays their statuses.

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
