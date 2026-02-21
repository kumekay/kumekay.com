---
title: "Starting services on WSL2 with systemd"
date: 2020-07-12 11:12:04
draft: false
slug: "wsl2-and-systemd"
tags: ["wsl2", "systemd", "linux", "windows"]
author: "Sergei Silnov"
image: "bill-jelen-woWf_VJ7dNs-unsplash.jpg"
---

Updated 28.10.2021: Corrected installation flow, init way + notes on VScode server

![](image.jpg)

[WSL2](https://docs.microsoft.com/en-us/windows/wsl/wsl2-index) is a great way to run Linux alongside Windows 10/11. However, systemd [doesn't work](https://github.com/microsoft/WSL/issues/994) in it yet.

Luckily, there is a 3rd-party solution - [genie](https://github.com/arkane-systems/genie).  It creates a PID namespace, so systemd can run with PID 1 in it. Ther  While it's not a full replacement with a number of known [issues](https://github.com/arkane-systems/genie#bugs), it allows running some common Linux daemons on your WSL2 instance, for example, docker or [Syncthing](https://syncthing.net/).

<!--more-->

Here are the steps for Ubuntu 20.04 or Debian bullseye, if you use another distro, please, check docs in the [project's repo](https://github.com/arkane-systems/genie)

In super user shell (`sudo -s`) run:

```bash
# add Microsoft repo and install dotNet 5.0 runtime
wget https://packages.microsoft.com/config/ubuntu/21.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

apt update
apt install -y apt-transport-https

# add repo with genie
curl -s https://packagecloud.io/install/repositories/arkane-systems/wsl-translinux/script.deb.sh | sudo bash

# Install both of them
apt update
apt install -y dotnet-sdk-5.0 systemd-genie
```

## Entering the bottle (PID-namespace) on every launch of the terminal

It's convenient to be in the bottle all the time, so this snippet inside `~/.zprofile` or `~/.bash_profile` will start it every time you open a new shell:

```bash
# Start genie
if [[ ! -v INSIDE_GENIE ]]; then
  exec /usr/bin/genie -s
fi
```

## Fix VS Code

There are 2 issues with VS Code

1. The `code` command doesn't work from the terminal in the bottle. The simplest fix is to add function to `~/.zshrc` or `~/.bashrc`. Don't forget to replace `[[username]]` with your actual Windows username.

```bash
# Genie bottle magic
code() {
  /mnt/c/Users/[[username]]/AppData/Local/Programs/Microsoft\ VS\ Code/bin/code "$@"
}
```

2. VS Code doesn't start its server inside the bottle. The only way at the moment is to patch the `Remote - WSL` plugin launcher. Add to the `/mnt/c/Users/[[username]]/.vscode/extensions/ms-vscode-remote.remote-wsl-0.58.4/scripts/wslServer.sh` after the `#!` line this snippet:

```bash
# Check if inside bottle
if command -v genie > /dev/null && ! genie -b > /dev/null; then
        # Rerun current script inside bottle
        exec genie -c "$0" "$@"
fi
```

Your version may be other than `0.58.4`, and there may be more than one version in the directory. Update the most recent one. And yes, it will be necessary to repeat it after every update of the plugin.

If something doesn't work for you, check the [WIKI](https://github.com/arkane-systems/genie/wiki) or open [issues](https://github.com/arkane-systems/genie/issues)
