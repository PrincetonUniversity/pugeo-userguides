# Raspberry shake installation

The following instructions are going to help you to install 
your raspberry shake on the Princeton campus from scratch.

---
***NOTE***:

The instructions still require you to go through the standard steps of the 
quick-start-guide: 
[https://manual.raspberryshake.org/quickstart.html](https://manual.raspberryshake.org/quickstart.html)
So don't just skip it!

---

## Installation locally and campus ethernet.

First connect the Shake to your computer using an ethernet cable. 
Make sure you have set your network setting to DHCP with manual 
IP. Choose something like

```
169.254.25.6
```

since the Shake's `IP` address is somewhere in `169.254.*.*`.
The stars can be `[0-255]`.

After setting the `IP` address on your computer, you'll be able to connect to
the raspberry shake using the command line. 

---

The raspberry shake is a computer itself, so to check whether it is visible 
in the network between you and the raspberry shake, we can "ping" it.

```bash
$ ping rs.local
```

The output hopefully looks somewhat like this:

```bash
PING rs.local (169.254.204.179): 56 data bytes
64 bytes from 169.254.204.179: icmp_seq=0 ttl=64 time=0.691 ms
64 bytes from 169.254.204.179: icmp_seq=1 ttl=64 time=0.816 ms
64 bytes from 169.254.204.179: icmp_seq=2 ttl=64 time=0.846 ms
...
```
---
Now that we know that we are connected, we use `ssh` to connect to it:

```bash
$ ssh myshake@rs.local
```

When asked for the fingerprint, answer `yes`. Use the default credentials to
login:

```
username: myshake
password: shakeme
```

After you logged in, keep the terminal window open, but use your browser to
connect to the main page of the Raspberry Shake 
[http://rs.local](http://rs.local). The first order of business should be
changing the password. Actions --> Actions --> Change Password. Note that this 
will change the login password, so write it down; it's very hard to get back.

My Shake right now:
```
username: myshake
password: GEO_RaspShake3346
```

---

Next, to make it work on campus wifi and/or dormnet, we have to register the 
device by making a request to OIT. 

Before, registering we need some info that we can only get from the command
line of the raspberry shake. So, go back to your terminal (ssh'ed to the 
raspberry shake) and type 

```bash
ifconfig
```

The output is fairly long, but we are specifically looking for two entries:

```
...
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 169.254.204.179  netmask 255.255.0.0  broadcast 169.254.255.255
        ether b8:27:eb:83:36:a5  txqueuelen 1000  (Ethernet)
...
wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        ether b8:27:eb:d6:62:f1  txqueuelen 1000  (Ethernet)
...
```

The numbers we are interested in are the ones with the colons.  `eth0` denotes
the ethernet entry and `wlan0` the Wifi one.

Eg.: `b8:27:eb:d6:62:f1` for the wifi

Register [Here](https://princeton.service-now.com/service?id=sc_cat_item&sys_id=27c256984f8a174018ddd48e5210c7a2&sysparm_category=0c0591f14f9d270c18ddd48e5210c79c).

Follow the instructions for `servicenet` and `wired` to add the device to both
wired and the wireless networks for devices that do not support `eduroam`.
Note that you can choose an alias for the device! The alias will enable you
to login to the raspberry shake using an alias instead of the full IP. E.g.
`rshake3346.princeton.edu`. 
The subnet network you should look for is `dormnet`.

Once the device is registered, you can connect it to campus ethernet through
most ethernet outlets. 

Address for my raspberry shake 3346 is 
[http://rshake3346.princeton.edu/](http://rshake3346.princeton.edu/)

## Trouble connecting to the internet even after registration

If it shows `Server: Not Connected` in the main menu of the Raspberry shake's 
GUI, change the DNS server in settings to `8.8.8.8`, and restart the machine
afterwards. This will change the way the machine is looking for addresses on the 
internet.