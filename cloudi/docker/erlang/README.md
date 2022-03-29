# CloudI Erlang Docker Example

## USAGE

To build Erlang from source, use:

    docker build -f Dockerfile.build.erlang -t erlang .

To build CloudI and run the image, use:

    docker build -f Dockerfile.build.cloudi -t cloudi_erlang .

    docker run -d -it -p 6464:6464 \
               # -v ${HOST_DIR}:${CONTAINER_DIR} \
               --net host \
               --cap-add NET_ADMIN \
               --name cloudi_erlang cloudi_erlang
    docker exec -it cloudi_erlang bash

For development, you may want to set extras:

    docker build -f Dockerfile.build.cloudi -t cloudi_erlang .
    # docker create --rm -i \
    docker run -d -it \
                --hostname cloudi-erlang \
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
                -p 6464:6464 \
                # --net host \
                --cap-add NET_ADMIN \
                --name cloudi_erlang \
                cloudi_erlang
    # docker start cloudi_erlang
    docker exec -it cloudi_erlang bash

To run CloudI from source, use `Dockerfile.build.cloudi-git`.

The CloudI dashboard is then accessible at
[http://localhost:6464/cloudi/](http://localhost:6464/cloudi/).


## Connect to node

If you need to use the Erlang shell while CloudI is running,
remember to detach with a CTRL+P,CRTL+Q key sequence:

    docker container attach cloudi_erlang

Alternativelly, you can connect from a remote node.

    erl -sname n1 -setcookie cloudi

    > net_adm:ping('cloudi@<HOSTNAME>').
    pong

    <CTRL-G>
    User switch command
    --> r 'cloudi@<HOSTNAME>'
    --> c
    Eshell V12.2.1  (abort with ^G)
    (cloudi@<HOSTNAME>)1>

Or:

    erl -sname n1 -setcookie cloudi -remsh 'cloudi@<HOSTNAME>'

## Connect Observer (host) to CloudI (local container)

Assuming the container port mapping:

```
  -p 6464:6464 \  # cloudi web
  #-p 3470:3469 \ # epmd
  -p :4374-4474 \ # inets
```

Add to `/etc/hosts` (host):

```
<CONTAINER IP>  <CONTAINER HOSTNAME>
172.17.0.2    cloudi-erlang
```

Run `observer` from host Erlang installation:

```
erl -sname obs -setcookie cloudi -run observer
```

Go to Nodes -> Connect node: `cloudi@cloudi-erlang`.


## Connect to simulator network

The subnet name is "ne.<X>":

    docker network ls

Create a network if it does not exist:

    docker network create --driver=bridge ne.<X>

Connect to:

    docker network connect ne.<X> cloudi_erlang
    docker exec cloudi_erlang /bin/bash -c "ifconfig eth1 \"169.254.0.36\""

## CloudI/containers

[https://github.com/CloudI/containers](https://github.com/CloudI/containers)


## Throubleshooting

Installing pkgs with 'apt install': dpkg: unrecoverable fatal error, aborting:

* Remove unused entries from `/var/lib/dpkg/statoverride`

Graphics does not work from container:

* At host, run:

  `xhost +`
