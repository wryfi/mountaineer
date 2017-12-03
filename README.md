# mountaineer: enumerate your gear

An anagram of `enumeration`, `mountaineer` is an application and API
for managing your operations inventory and environments. The idea behind
mountaineer is that you should be able to enumerate all the things in
your environment, from a single, canonical, authoritative source.

This iteration is an open source port of work that started at one of my
employers (with their blessing), but I have built some verison of a
system like this almost everywhere I have worked as an ops engineer.

##  inventory-driven infrastructure

Mountaineer is a tool for inventory-driven infrastructure. The basic
philosophy behind inventory-driven infrastructure is that there should
never be any guess work or discovery required to find out what systems
are running on your network and what they're doing. Instead, you should
declare what you're building in an inventory and lifecycle management
system, and use the inventory to drive your infrastructure.

## configuration management

Mountaineer is designed to be used with configuration management and
monitoring systems like Saltstack and Prometheus. Mountaineer was
developed alongside these tools, which use the Mountaineer API to
get their host inventories, among other things. While developed
alongside Saltstack and Prometheus, Mountaineer's rich API should be
adaptable to many other software systems.

