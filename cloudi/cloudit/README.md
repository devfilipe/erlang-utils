# cloudit

Create a virtual environment
----------------------------

```
# requires python3.X-venv
python3 -m venv ${VENV_PATH}
```

i.e. 'python3.10 -m venv ~/workspace/env/python/v3.10'

* Activate

```
source '${VENV_PATH}/bin/activate'
```

* Install requirements

```
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

* Run/quit python

```
python3
# Ctrl-D
```

* Deactivate venv

```
deactivate
```

Usage
-----

```
import cloudit
```

Main utilities
--------------

* Get/Set `current work dir`

```python
cloudit.get_cwd()
cloudit.set_cwd('<SERVICE PARENT DIR>')
```

* Single service

```python
cloudit.rebar3('<SERVICE_NAME>')
cloudit.code_path_add('<SERVICE_NAME>')
cloudit.service_add('<SERVICE_NAME>')
cloudit.service_remove('<SERVICE_NAME>')
```

* Multiple services

Depends on `modules_code_path` and `services_init`.

```python
cloudit.compile_all()
cloudit.init()
cloudit.clear()
```

Troubleshooting
---------------

* UDP initialization failed

```
>>> cloudit.init()
{'pad_service_udp': '{error,{service_internal_start_failed,{error,eaddrnotavail}}}'
```

*Check if `ip` argument in `pad_service_udp.conf` belongs to a network interface.*

Example: set interface 169.254.0.36 to communicate in 169.254.0.0 network.

```
# (optional) set container network (if it does not exist) and connecto to
docker network create --driver=bridge ne.<X>
docker network connect ne.<X> <CONTAINER_NAME>

# configure an interface
docker exec <CONTAINER_NAME> /bin/bash -c "ifconfig eth1 \"169.254.0.36\""
```

Edit `pad_service_udp.conf`:

```
# set ip argument
{args,
    [{ip, {169,254,0,36}},
```

Run `cloudit.init()`.


* Create a distribution

```
  python3 setup.py sdist
```
