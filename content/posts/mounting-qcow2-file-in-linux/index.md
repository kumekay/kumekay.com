---
title: "How to Mount a QCOW2 Disk to a Linux Machine"
date: 2025-06-08 16:48:24
draft: false
slug: "mounting-qcow2-file-in-linux"
tags: []
author: "Sergei Silnov"
---

This guide explains how to mount a `qcow2` disk image to a Linux machine. While the initial command might differ for other distributions, the core steps remain consistent. This example is tailored for Debian 12.

<!--more-->

### 1. Install QEMU Tools

First, install the necessary QEMU utilities, which provide the `qemu-nbd` tool.

```
sudo apt install qemu-utils
```

### 2. Load the NBD Kernel Module

Load the **NBD (Network Block Device)** kernel module. The `max_part` parameter specifies the maximum number of partitions the NBD device can expose. Set it to a value suitable for your needs, for example, `2` if you expect up to two partitions.

```
sudo modprobe nbd max_part=2
```

### 3. Connect QCOW2 as a Network Block Device

Now, connect your `qcow2` image as a network block device. Replace `/path/to/snap-vol-20GB.qcow2` with the actual path to your `qcow2` file. This command makes the `qcow2` image accessible via `/dev/nbd0`.

```
sudo qemu-nbd --connect=/dev/nbd0 /path/to/snap-vol-20GB.qcow2
```

### 4. List Partitions

To identify the partition you want to mount, list the partitions available on the connected NBD device:

```
lsblk /dev/nbd0
```

This command will show you the partition layout of your `qcow2` image (e.g., `nbd0p1`, `nbd0p2`).

### 5. Mount the Partition

Create a mount point (if it doesn't already exist) and then mount the desired partition. In this example, we're mounting `/dev/nbd0p1` to `/mnt/data/`. Adjust the partition name (`nbd0p1`) and mount point (`/mnt/data/`) as needed.

```
sudo mkdir -p /mnt/data/
sudo mount /dev/nbd0p1 /mnt/data/
```

### 6. Teardown

Once you're finished accessing the disk, it's crucial to unmount it and disconnect the NBD device to free up resources. Follow these steps in reverse order:

```
sudo umount /mnt/data/
sudo qemu-nbd --disconnect /dev/nbd0
sudo rmmod nbd
```