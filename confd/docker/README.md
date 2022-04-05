ConfD image
===========

Source

  https://github.com/ConfD-Developer/ConfD-Demos/blob/master/confd-and-docker/ubuntu-confd/README

Build a ConfD docker container based on Ubuntu 20.04.

Prerequisites
-------------

The ConfD artifacts folder must be available in `resources` folder.
I've used confd-7.7.2.

Steps
-----
1. Drop the ConfD artifacts into the resources directory.
2. Create the ConfD image

  docker build -f Dockerfile.confd -t confd:7.7.2 .

3. Run the docker image and expose the NETCONF, CLI and internal IPC ports.

  $ docker run -it --rm -p 2022:2022 -p 2024:2024 -p 4565:4565 --name confd_7.7.2 --init confd:7.7.2
  confd[7]: - Starting ConfD vsn: 7.7.2
  confd[7]: - Loading file confd.fxs
  confd[7]: - Loading file ietf-yang-types.fxs
  confd[7]: - Loading file ietf-inet-types.fxs
  confd[7]: - Loading file confd_cfg.fxs
  confd[7]: - Loading file config.fxs
  confd[7]: - Loading file netconf.fxs
  ...

For development, you may want to set extras:

  docker run -d -it \
    --hostname confd-7.7.2 \
    --privileged \
    --env LOGNAME="${USER}" \
    --env USER="${USER}" \
    --env USER_ID_GID="`id -u ${USER}`:`id -g ${USER}`" \
    --env DISPLAY="${DISPLAY}" \
    --env HOME="${HOME}" \
    -v /etc/group:/etc/group:ro \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/shadow:/etc/shadow:ro \
    -v ${HOME}/.ssh:${HOME}/.ssh \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v ${HOME}/workspace:${HOME}/workspace \
    -w ${HOME}/workspace \
    -p 2022:2022 \
    -p 2024:2024 \
    -p 4565:4565 \
    --cap-add NET_ADMIN \
    --name confd_7.7.2 \
    confd:7.7.2

4. Access the container and run confd

```bash
#confd --foreground [--verbose]

confd -c ${CONFD_CONF_FILE} --addloadpath ${CONFD_DIR}/etc/confd --addloadpath ${FXS_DIR} --verbose
```

5. Test the NETCONF interface.

  $ netconf-console --hello
  <?xml version="1.0" encoding="UTF-8"?>
  <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
      <capability>urn:ietf:params:netconf:base:1.0</capability>
      <capability>urn:ietf:params:netconf:base:1.1</capability>
      <capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>

      ...

      <capability>urn:ietf:params:xml:ns:yang:ietf-yang-types?module=ietf-yang-types&amp;revision=2013-07-15</capability>
      <capability>urn:ietf:params:xml:ns:netconf:base:1.0?module=ietf-netconf&amp;revision=2011-06-01</capability>
      <capability>urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults?module=ietf-netconf-with-defaults&amp;revision=2011-06-01</capability>
    </capabilities>
    <session-id>12</session-id>
  </hello>

6. Test the CLI interface

```
$ ssh -p 2024 admin@localhost
admin@localhost's password:
Welcome to the ConfD CLI
admin connected from 172.17.0.1 using ssh on confd-7.7.2
admin@confd-7 17:33:58> ?
Possible completions:
  clear          - Clear parameter
  commit         - Confirm a pending commit
  compare        - Compare running configuration to another configuration or a file
  configure      - Manipulate software configuration information
  describe       - Display transparent command information
  exit           - Exit the management session
  file           - Perform file operations
  help           - Provide help information
  id             - Show user id information
  leaf-prompting - Automatically query for leaf values
  monitor        - Real-time debugging
  ping           - Ping a host
  quit           - Exit the management session
  request        - Make system-level requests
  script         - Script actions
  set            - Set CLI properties
  set-path       - Set relative show path
  show           - Show information about the system
  source         - File to source
  top            - Exit to top level and optionally run command
  traceroute     - Trace the route to a remote host
  up             - Exit one level of configuration
admin@confd-7 17:33:58>
```

Note 1: the default CLI is Juniper style.  This can be changed in
confd.conf, see confd.conf(5) man-page.

Note 2: In order to make it easy to run a quick test as I did here,
this container use default locations for CDB
($CONFD_DIR/var/confd/cdb) and $CONFD_DIR/etc/confdconfd.conf.  This
is obviously not realistic and in production both should reside in
separate volumes outside the running container.  This is easily
achieved by passing a different confd.conf location when starting
ConfD.

netconf-console2
----------------

  $ python3 -m venv ~/workspace/env/python/v3
  $ source ~/workspace/env/python/v3/bin/activate

  (v3) pip install netconf-console2
  (v3) netconf-console2 --user=admin --password=admin --host=localhost --port=2022 --db candidate --get=/aaa