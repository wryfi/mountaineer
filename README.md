[![Build Status](https://www.travis-ci.org/wryfi/mountaineer.svg?branch=develop)](https://www.travis-ci.org/wryfi/mountaineer)

# Mountaineer: enumerate your operations

An anagram of `enumeration`, `mountaineer` is a Django application and API
for managing your operations inventory and environments, from rack to 
container. The idea behind mountaineer is that you should be able to 
manage all the things in your environment -- racks, switches, PDUs,
servers, virtual machines, networks, containers, and clusters --
in one place, whether you run on bare metal, in the cloud, or a hybrid.

Mountaineer aims to consolidate all of your systems inventory and
management into a single, unified API. Eventually, a rich graphical
interface will be written on top of this API to simplify the management
of your infrastructure.


## History and Background

Mountaineer is a rewrite of a project called Dewey, which
wryfi wrote for an employer, who has graciously agreed to allow its
release as open source. They remain nameless at management's request.
Because there is an existing Dewey project on PyPi, the project has been
renamed to Mountaineer. Besides, this is a major rewrite, so a new name
is justified.

Dewey was written in a hurry, without tests, and with some
database antipatterns that Django makes all too convenient (generic
foreign keys, for example). It was written in a monolithic way, to meet
the specific needs of a single organization. Its API and
frontend user interface are incomplete (the ops team relied heavily
on the Django admin, and used the API as a read-only data source).


## Project Goals

The goals of Mountaineer are several:

* Refactor the Dewey code base with an eye to style and quality
* Provide a high percentage of test coverage
* Remove database antipatterns to the greatest extent possible
* Focus on creating a full, rich API with complete read-write capabilities
* Modularize the application, with a "core" project (this one) and an
ecosystem of flexible add-on modules
* Support EC2 and other cloud providers
* Support Kubernetes clusters and resources
* Rewrite the frontend in a modern javascript framework (most likely
[cerebral](https://cerebraljs.com/) + [inferno](https://infernojs.org/))


# Planned Modules

* [mntnr_hardware](https://github.com/wryfi/mntnr_hardware) - track all
the hardware in your datacenter, including
connections between devices
* mntnr_hosts - manage hosts and clusters running on your hardware
* mntnr_networks - manage network blocks and address assignments,
and reserve address segments for your needs
* mntnr_powerdns - update PowerDNS entries based on address assignemts
in mntnr_networks
* mntnr_vault - integrating [Vault](https://www.vaultproject.io/)
transit-mode ciphertexts with host and role-based access controls
* mntnr_saltstack - send salt events to Mountaineer and surface in the API
* mntnr_ec2 - manage EC2 inventory and provisioning from Mountaineer
* mntnr_k8s - exposing [Kubernetes](https://kubernetes.io) resources
and management features in Mountaineer


# Status

The core Mountaineer glue module (this repo) is set up and generally
ready to be extended. Additional modules are in various states of
development, but none of them are currently ready for production use.
Please take a close look at the code before trying to use it, and feel
free to contribute!
