Kerl + Ubuntu 20.04
===================

* Download and setup kerl

* Install deps

```bash
sudo apt-get install libgtk-3-dev build-essential
sudo apt-get install libssl-dev automake autoconf libncurses5-dev
sudo apt-get install libwxgtk3.0-gtk3-dev libwxgtk-webview3.0-gtk3-dev
sudo apt install default-jre default-jdk
sudo apt-get install xsltproc fop libxml2-utils
```

* Build & install Erlang with Kerl

```bash
KERL_CONFIGURE_OPTIONS="--with-wx --enable-webview" ./kerl build 25.0-rc1
./kerl install 25.0-rc1 ~/workspace/env/erlang/25.0-rc1
```

* Activate Erlang installation

```bash
. ~/workspace/env/erlang/25.0-rc1/activate
```

* Deactivate

```bash
kerl_deactivate
```