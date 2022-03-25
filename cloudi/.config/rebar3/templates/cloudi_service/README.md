cloudi_service
--------------

* Install

Copy all template files to `${HOME}/.config/rebar3/templates`.

Check if `cloudi_service` is available:

```
$ rebar3 new --help
cloudi_service (custom): A basic service skeleton for CloudI
```

* Demo

Create a rebar3 project:

```bash
$ rebar3 new lib myservice
===> Writing myservice/src/myservice.erl
===> Writing myservice/src/myservice.app.src
===> Writing myservice/rebar.config
===> Writing myservice/.gitignore
===> Writing myservice/LICENSE
===> Writing myservice/README.md
```

```bash
$ cd myservice
$ ls
LICENSE  README.md  rebar.config  src
```

Run rebar3 for cloudi_service template:

```
# give SERVICE_NAME and CLOUDI_VERSION
$ rebar3 new cloudi_service myservice 2.0.4
===> Writing ./myservice.erl
===> Writing ./rebar.config.script
===> Writing ./priv/cloudi/myservice.conf
===> Writing ./priv/cloudi/myservice_test.sh
```

Move (!!overwrite!!) `myservice.erl` to `src` folder.

Compile the project.

```bash
$ rebar3 compile
```

If CloudI is running, you can test your service:

```
$ chmod +x priv/cloudi/myservice_test.sh
$ priv/cloudi/myservice_test.sh
{"status":"ok"}
```
