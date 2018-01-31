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


## History and Background

Mountaineer is an open-source port of a project called Dewey, which I
wrote for one of my employers, who has graciously agreed to allow me
to open-source the code. They remain nameless at management's request.
Because there is an existing Dewey project on PyPi, I have renamed the
port to Mountaineer.

Dewey was written in a rush, without tests, and with some
database antipatterns that Django makes all too convenient (generic
foreign keys, for example). It was written in a monolithic way, to meet
the specific needs of my employer and its ecosystem. Its API and
frontend user interface are incomplete (the ops team relied heavily
on the Django admin, and used the API as a read-only data source).


## Project Goals

The goals of Mountaineer are several:

* Refactor the Dewey code base with an eye to style and quality
* Provide a high percentage of test coverage
* Remove database antipatterns to the greatest extent possible
* Focus on creating a full, rich API with complete read-write capabilities
* Modularize the application, with a "core" project (this one) and an
ecosystem of flexible add-ons (coming soon)
* Rewrite the frontend in a modern javascript framework (most likely
[cerebral](https://cerebraljs.com/) + [inferno](https://infernojs.org/))




##  Inventory-Driven Infrastructure

Mountaineer is a tool for inventory-driven infrastructure. The basic
philosophy behind inventory-driven infrastructure is that there should
never be any guess work or discovery required to find out what systems
are running on your network and what they're doing. Instead, you should
declare what you're building in an inventory and lifecycle management
system, and use the inventory to drive your infrastructure.


## Configuration Management

Mountaineer is designed to be used with configuration management and
monitoring systems like Saltstack and Prometheus. Mountaineer was
developed alongside these tools, which use the Mountaineer API to
get their host inventories, among other things. While developed
alongside Saltstack and Prometheus, Mountaineer's rich API should be
adaptable to many other software systems.


## What Mountaineer is NOT

### Service Discovery System

While you could hobble together something resembling a service discovery
mechanism from Hosts and Roles, this is currently inadvisable. There are
many benefits to using a proper, distributed service discovery mechanism,
like [Consul](https://www.consul.io).
