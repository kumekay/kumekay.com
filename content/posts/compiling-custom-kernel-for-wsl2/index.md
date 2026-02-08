---
title: "Compiling custom kernel for WSL2 + USB-IP support"
date: 2021-04-01 20:26:16
draft: false
slug: "compiling-custom-kernel-for-wsl2"
tags: []
author: "Sergei Silnov"
---

**Updated** 19.11.2021: Add note on runnins usbipd from WSL

**Updated** *08.11.2021:*  Add metntion [usbipd-win](https://github.com/dorssel/usbipd-win )

**Updated** *28.10.2021*: The most recent kernel 5.10.60.1 has enabled USB-IP support, but only a few drivers for USB devices are enabled, so these instructions still make sense.

Now it's possible to [Windows Subsystem for Linux](https://www.microsoft.com/store/productId/9P9TQF7MRM4R) from the Microsoft Store, and it's recommended way since it brings new features faster.

I would like to use USB devices inside WSL2, however, it doesn't support USB pass-through yet. [VirtualHere](https://www.virtualhere.com/) allows to pass USB devices from windows to WSL2 through the network but it requires USBIP support from the Linux kernel. Also, all the drivers should be built into it or built as modules. As of 5.10.60.1, it includes support for USB-IP and FTDI USB-UART converters, but missing support for others, including the popular SiLabs CP210\* series. So let's build our own kernel with this driver.

All instructions are given for Ubuntu 20.04 or Debian bullseye on the WSL side and Windows 11 as a host. Windows 10 21h2 should work too, but I didn't try.

To build the kernel first install a compiler and required libs:

```
sudo apt update -y
sudo apt install -y \
  autoconf \
  bison \
  build-essential \
  flex \
  libelf-dev \
  libncurses-dev \
  libssl-dev \
  libtool \
  libudev-dev \
  bc
```

Check your kernel version with `uname -r`. In my case, it's `5.10.60.1-microsoft-standard-WSL2+` so the relevant branch is `linux-msft-wsl-5.10.y`. As for now, it's the default one, but this may change later.

```
git clone https://github.com/microsoft/WSL2-Linux-Kernel.git ~/kernel
```

And copy the default Microsoft kernel config to the working directory. It will be a good starting point.

```
cd ~/kernel && cp Microsoft/config-wsl .config
```

Let's configure the kernel:

```
make menuconfig
```

The driver that I need hides under `Device Drivers --->` > `[*] USB support --->` > `<*> USB Serial Converter support --->`  >  `< > USB CP210x family of UART Bridge Controllers`.

Press the `space` to select it. First, it will be marked as `M`. It means it will be built as a separate file, a loadable module, that has to be loaded manually later. But for simplicity I would suggest to built everything in, then the driver will the part of the kernel binary. So press the `space` bar one more time and it will be marked with `*`.

If you are working with hobby dev-kits, they often contain `CH341` serial converters, so select `USB Winchiphead CH341 Single Port Serial Driver` too.

It will be also nice to modify the local version in the kernel name. You can find it in `General setup --->` > `Local version`. I would set it to `-kumekay-standard-WSL2`

Save the changes and exit, now it's time to build the kernel:

```
make -j $(nproc)
```

Copy kernel to windows partition where it can be loaded by WSL2:

```
cp arch/x86/boot/bzImage /mnt/c/Users/<UserName>/kernel
```

And create a WSL config file: `/mnt/c/Users/<UserName>/.wslconfig` with the content:

```
[wsl2]
kernel=C:\\Users\\<UserName>\\kernel
```

The last step is to restart the WSL:

```
wsl.exe --shutdown
```

Now you can install [usbipd-win](https://github.com/dorssel/usbipd-win ) and follow Microsoft's [tutorial on USBIP](https://aka.ms/wsl-usbip).

Note: If you want to run USBIPd from WSL, you can do it like this, with elevated permissions`powershell.exe Start-Process -FilePath usbipd.exe -Verb runas -Args wsl,attach,-b,6-1,-d,Ubuntu`

One feature usbipd missing is the automatic reconnection of the USB device to the Linux VM. If it's something you need, then [VirtualHere USB Server](https://www.microsoft.com/store/productId/9PK805V256R6) for windows and [GUI Linux client](https://virtualhere.com/sites/default/files/usbclient/vhuit64) can be used. GUI client works out of the box on Windows 11. VirtualHere can be used for free for exporting 1 USB device.

However, to have proper permissions `udevd` should run. Normally it starts with the `systemd`, so follow [these instructions](https://kumekay.com/wsl2-and-systemd/) on how to enable it on WSL2.