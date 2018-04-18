---
layout: default
---

# Quad Copters
## Fast and dangerous

Before starting VNovus, Bill and I spent a lot of time building, flying, crashing and fixing mini quads.
No, not the big fat ones you can find at BestBuy that basically fly themselves and act as flying tripods.
They are ferocious little buggers which are essentially four motors strapped together and are capable of acceleration over 8G.
Just to give an example, a camera drone carries a big battery and usually fly for 15-20 minutes.
A mini quad could suck a 4S (15v) 1300 mah battery dry in under 3 minutes, if you do the math that works out to an average amperage draw of 25 amps, with a max amperage in the range of 50-80 amps!
From an aerodynamics perspective, there is ... almost none. You can think of it as acting like a free floating thrust vector, which is actually aerodynamically unstable so we need to stabilize it digitally.
All I'm trying to say is, they are powerful, fast, and so nimble that are close to uncontrollable. That's why we drove miles to find place to fly them where there is absolutely nobody around, and don't call it a bad day because when there has been crashes, but call it a bad day when we can't find all the pieces after the crash.

So they are little monsters cost us a lot of time and money, but they are also extremely fun to fly.
What we do is we put cameras on them and fly them in first person view, and that is just awesome.

Naturally, that got me thinking, how can I make it even more exciting?

We usually just fly them around and try not to crash into the ground. What we find very challenging but fun is to chase after each other.
Now, what if we can shoot at each other?
Think about it for a second, that's real life air-to-air combat.
Would anyone think that's not cool?

So that is an interesting project right there.
Right off the bat I ruled out physically shooting projectiles. It's almost impossible to build and it's not sustainable.
So it's decided that it has to be done electronically.

The logic is, when quad A fires at quad B, to get a vector pointing from A to B, and compare this vector to the forward vector of A. If the angle is small enough, then we say A successfully hit B.

blabla details regarding how to get the aiming vector.

One of the ideas is that if B knows about its accurate location, and broadcast it to A, then A can easily calculate the aiming vector.
The really difficult part to do, is to get an accurate 3D spatial location, I haven't really found a solution yet.
But a part of it, the part where B talks to A should be fairly straight forward to implement.
Besides, it can be quite useful in a lot of ways in itself.

To put it into proper terms this is called Vehicle to Vehicle communication.

For this function, I thought it would be more useful if it is a separate, self contained system, so it would run on a separate controller.
I bought some minimized adurino chips from Banggood and there is that, fairly obvious choice.

Now for the actual communication
There are a wide range of choices for this, from Wifi, to bluetooth, to XeeBee, pretty much anything would work since it only needs to work in close range, and bandwidth is no issue since we are talking about bytes of data per transmission
Ultimately I've decided on SI4663 RF chips. I've found a custom board that would work with Arduino, and it's dirt cheap, so I can buy loads of them and not really worry about breakage

The tricky part is SI4663 is a RF chip, and that's all it is. You give it some signals to send, and it sends it. So I need to write a communication protocol for it.

It breaks down to:

Synchronization
The RF chip can either receive or send signal, but not both at the same time. And since it's just broadcasting, we need to make sure at anytime there is only one client that's sending the signal, and all other parties are in receiving mode and wait for their turn to send

Solution is simple, all clients were put into receiving mode when boot up. After a given time without receiving a sync signal, starts to send sync signals on a interval that is smaller than the initial wait time

Another client wakes up later and would receive the sync signal from the first client, and adds a slight offset and start sending sync signals on the same interval

The time between the two sync signals becomes the transmission window for the first client. Again, we are only sending dozens of bytes of data, so this window should provide ample time for the data to get through

Data Packet
We are only sending a minimal amount of data on each transmission, and the data packets are very small.
The design is that each packet starts with a timestamp, followed by a sender id, then a simple identifier saying the type of data, then the payload

Error Checking
The most annoying part of writing a custom com protocol is to ensure the integrity of the data packets.
Keep in mind this is RF transmission, a lot things could happen that would invalidates the data, for example the signal could get weakened in the middle of transmission and result in noise based errors, or two nodes are somehow transmitting at the same time and totally scramble the data packets.

I've took the lazy route here and only implemented very simple error checking
The payload would repeat a couple of times during each transmission
And added to each payload is a hash that would be used to validate the whole data packet

After I started VNovus this project has been put in storage for a very long time now.
I still think this is a very cool idea so I'll try to revive it and push it a bit further.
