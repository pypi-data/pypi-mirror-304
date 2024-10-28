# `molecule-qemu`

Molecule QEMU driver for testing Ansible roles.

Supported platforms:

- MacOS 13.x (arm64)
- MacOS 14.x (arm64)
- Ubuntu 22.04 LTS (amd64) (tested on GitHub Actions)

Support guest OS:

- Debian 11 (arm64, amd64)
- Debian 12 (arm64, amd64)
- Ubuntu 20.04 LTS (arm64, amd64)
- Ubuntu 22.04 LTS (arm64, amd64)
- Ubuntu 24.04 LTS (arm64, amd64)

Supported Ansible versions:

- 8.x
- 9.x

Supported Molecule versions:
- 0.5.x

`molecule-qemu` does not provide support for `molecule` of version `0.6.x` and higher. Support is unfortunately not planned. Molecule `0.6.x` has a completely different architecture and is not compatible with the current implementation. Molecule of version `0.5.x` is still supported and works well. Future versions of `molecule-qemu` will be released only for `molecule` of version `0.5.x` which means that at some point `molecule-qemu` becomes obsolete.

Support of other platforms and guest OS is possible, but not tested. Please, open an issue if you want to add support for other platforms.

Supported network modes:

- `user` - QEMU's user networking mode
- `vmnet-shared` - QEMU's `vmnet-shared` networking mode (MacOS only)

Supported disk types:

- `virtio` - QEMU's virtio disk type
- `virtio-scsi` - QEMU's virtio-scsi disk type

Supported BIOS types:

- `uefi` - QEMU's uefi used for image with uefi configured
- `bios` - QEMU's bios used for image with bios configured

## Quick start

Install `molecule-qemu` python package:

```bash
pip install molecule-qemu
```

Create a new Molecule scenario using `molecule init` command:

```bash
molecule init scenario default --driver-name molecule-qemu --verifier-name testinfra
```

Edit `molecule.yml` and add platforms:

```yaml
---
dependency:
  name: galaxy
driver:
  name: molecule-qemu
platforms:
  - name: debian-bookworm-arm64
    image_arch: aarch64
    image_url: https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-arm64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
    network_mode: vmnet-shared
provisioner:
  name: ansible
  inventory:
    host_vars:
      debian-bullseye-arm64: {}
verifier:
  name: testinfra
```

Full list of supported options:

```yaml
platforms:
  - name: debian-bookworm-arm64

    image_arch: aarch64 # optional, default is x86_64
    image_url: https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-arm64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
    image_format: qcow2 # optional, default is qcow2

    network_mode: vmnet-shared # optional, default is user
    network_extra_args: "" # optional, only used when network_mode: user
    network_ssh_port: 2222 # optional, default is 2222
    network_ssh_user: ansible # optional, default is ansible

    vm_cpus: 1 # optional, default is 1
    vm_memory: 512 # optional, default is 512
    vm_disk: 8G # optional, default is 8G
    vm_extra_args: "" # optional, additional arguments to be passed to QEMU, default is empty

    disk_type: virtio-scsi # optional, default is virtio

    bios_type: bios # optional, default is uefi
```

### Dependencies

Driver depends on:

- QEMU (tested with 6.2.0, 8.0.2, 8.0.4, 8.1.0)
- mkisofs (tested with 3.02a09)

Install QEMU and CDRTools on macOS:

```bash
brew install qemu cdrtools
```

Install QEMU on Ubuntu:

```bash
apt-get install mkisofs qemu-system-x86 qemu-utils
```

## Network modes

### `user` network mode

This is the default network mode. It uses QEMU's user networking mode.

Mode is selected by setting `network_mode: user` in `molecule.yml`. This is the default mode. SSH port is forwarded to the host and must be unique for each platform (use `network_ssh_port` option to set it).
Additional port forwarding can be achieved by setting `network_extra_args`. Example:

```yaml
- name: debian-bullseye-arm64
  image_arch: aarch64
    image_url: https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-arm64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
  network_mode: user
  network_ssh_port: 2222
  network_extra_args: hostfwd=tcp::8080-:80
```

### `vmnet-shared` network mode

This mode uses QEMU's `vmnet-shared` networking mode. It requires `vmnet.framework` to be installed on the host. This mode is only supported on MacOS. It requires _passwordless_ `sudo` access for current user.

Mode is selected by setting `network_mode: vmnet-shared` in `molecule.yml`. Example:

```yaml
- name: debian-bullseye-arm64
  image_arch: aarch64
  image_url: https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-arm64.qcow2
  image_checksum: sha512:https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
  network_mode: vmnet-shared
```

# Examples

See [tests](https://github.com/andreygubarev/molecule-qemu/tree/main/tests/molecule) for more examples.

## Sample platforms configuration

```yaml
platforms:
  - name: debian-bullseye-amd64
    image_url: https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-amd64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS
    network_ssh_port: 2222

  - name: debian-bullseye-arm64
    image_arch: aarch64
    image_url: https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-arm64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS
    network_ssh_port: 2223

  - name: debian-bookworm-amd64
    image_url: https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
    network_ssh_port: 2224

  - name: debian-bookworm-arm64
    image_arch: aarch64
    image_url: https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-arm64.qcow2
    image_checksum: sha512:https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
    network_ssh_port: 2225

  - name: ubuntu-focal-amd64
    image_url: https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
    network_ssh_port: 2226

  - name: ubuntu-focal-arm64
    image_arch: aarch64
    image_url: https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-arm64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
    network_ssh_port: 2227

  - name: ubuntu-jammy-amd64
    image_url: https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/jammy/current/SHA256SUMS
    network_ssh_port: 2228

  - name: ubuntu-jammy-arm64
    image_arch: aarch64
    image_url: https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-arm64.img
    image_checksum: sha256:https://cloud-images.ubuntu.com/jammy/current/SHA256SUMS
    network_ssh_port: 2229

   - name: ubuntu-noble-amd64
     image_url: https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
     image_checksum: sha256:https://cloud-images.ubuntu.com/noble/current/SHA256SUMS
     network_ssh_port: 2230

   - name: ubuntu-noble-arm64
     image_url: https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-arm64.img
     image_checksum: sha256:https://cloud-images.ubuntu.com/noble/current/SHA256SUMS
     network_ssh_port: 2231
```

## Cloud Images URLs

For convenience, here are the URLs for the cloud images used in the examples above.

### [Debian](https://cloud.debian.org/images/cloud/)

- https://cloud.debian.org/images/cloud/bullseye/latest/SHA512SUMS
  - https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-amd64.qcow2
  - https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-arm64.qcow2
- https://cloud.debian.org/images/cloud/bookworm/latest/SHA512SUMS
  - https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2
  - https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-arm64.raw

### [Ubuntu](https://cloud-images.ubuntu.com/)

- https://cloud-images.ubuntu.com/focal/current/SHA256SUMS
  - https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-arm64.img
  - https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
- https://cloud-images.ubuntu.com/jammy/current/SHA256SUMS
  - https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-arm64.img
  - https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
- https://cloud-images.ubuntu.com/noble/current/SHA256SUMS
  - https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-arm64.img
  - https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img

# Troubleshooting

Molecule working directory is: `~/.cache/molecule/<role-name>/<scenario-name>`.

QEMU images caches is: `~/.cache/molecule/.qemu`.

# Motivation

The development of the Molecule `QEMU` driver was motivated by the author's choice of the Apple M1 as their primary development machine. He wanted to test Ansible roles on the Apple M1 but preferred not to rely on `Docker` for testing due to challenges with Docker's `systemd` support. Author never liked to install supplementary software such as `Vagrant` and `VirtualBox` on development machine. Author is aware of `libvirt` and `virt-manager` but their complexity and the lack of support was frustrating.

About molecule `0.6.x` and higher. Author has no idea why `molecule` decided to re-implement its own architecture and discard third-party drivers support. Explanations are not clear and the author does not understand the benefits of the new architecture. `molecule` of version `0.5.x` provides a mature and stable functionality that is sufficient for complex testing scenarios. `molecule` of version `0.6.x` focuses on simplicity and ease of use, focuses on Docker as the primary driver for testing, which is not suitable for most of the cases met by the author.

# Reference

- [Ansible](https://www.ansible.com/)
- [Molecule](https://molecule.readthedocs.io/en/latest/)
- [QEMU](https://www.qemu.org/)
- [QEMU BIOS](https://packages.debian.org/bullseye/qemu-efi-aarch64)

## QEMU vmnet-shared networking

- [vmnet.framework modes](https://lore.kernel.org/all/20220315230741.21578-7-Vladislav.Yaroshchuk@jetbrains.com/T/)
