# Mountaineer: enumerate your gear

An anagram of `enumeration`, `mountaineer` is a Django application and API
for managing your operations inventory and environments, from rack to 
container. The idea behind mountaineer is that you should be able to 
enumerate all the things in your environment -- racks, switches, PDUs,
servers, virtual machines, networks, containers, and clusters -- from a 
single, canonical, authoritative source.

Once you have a well-defined enumeration of these objects, you can begin
to build orchestration and management tools around them, in a single, 
unified interface. Mountaineer provides a framework for building this
kind of system, and includes some add-on packages for using Mountaineer
with SaltStack.

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

## service discovery

While you could hobble together something resembling a service discovery
mechanism from Hosts and Roles, this is currently inadvisable. There are
many benefits to using a proper, distributed service discovery mechanism,
like [Consul](https://www.consul.io).
 