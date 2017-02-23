# loadwatch
`loadwatch` tracks the health of a server, and logs information if conditions are met.

* Output is logged to `/var/log/loadwatch`.
* The checklog is at `/var/log/loadwatch.log`.
* The configuration is at `/etc/loadwatch.conf`.

There are three requirements for this script:

* It cannot cause load
* It has to run quickly
* It must provide useful information

This script currently does not support email notifications, it is purely passive.
The intention is that this should gather information to be reviewed if other issues are noticed.
