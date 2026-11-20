Guard:     
if phase == "WAIT_READY" and kind == "READY":
        return "release"
Meaning: robot releases the cup only when both conditions are true: when robot is ready to release the cup (it has a cup, and it is in the right position) and when the person is ready to accept the cup (person said ready)
Event: (normal transfer): last row READY -> release, WAIT_READY -> COMPLETE. 