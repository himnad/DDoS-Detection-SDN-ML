
# Installation Guide

## Environment Setup

To ensure a stable and isolated development environment, this project is executed using a virtualized Linux system.

* Virtualization Tool: Oracle VM VirtualBox
* Guest Operating System: Ubuntu 20.04.6 LTS

The Ubuntu ISO image was downloaded from the official website. Due to its large size, a download manager integration was used to accelerate the process.

---

## Step 1: Install VirtualBox

1. Download VirtualBox from the official website:
   [https://www.virtualbox.org/](https://www.virtualbox.org/)

2. Install it on your host system (Windows/Linux).

3. Launch VirtualBox and create a new virtual machine with:

   * Type: Linux
   * Version: Ubuntu (64-bit)
   * RAM: Minimum 4 GB (Recommended)
   * Storage: 20 GB (Dynamically allocated)

---

## Step 2: Install Ubuntu on Virtual Machine

1. Download Ubuntu 20.04.6 LTS ISO from:
   [https://releases.ubuntu.com/20.04/](https://releases.ubuntu.com/20.04/)

2. Attach the ISO file to the virtual machine.

3. Start the VM and follow the installation wizard:

   * Select language and keyboard layout
   * Choose “Normal Installation”
   * Allocate disk space
   * Set username and password

4. Complete installation and restart the VM.

---

## Step 3: Optional – Faster Download Using IDM

To speed up the download of the Ubuntu ISO file:

* Use Internet Download Manager integration with your browser
* This improves download speed and stability for large files

---

## Step 4: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 5: Install Python and Pip

```bash
sudo apt install python3 python3-pip -y
```

Verify installation:

```bash
python3 --version
pip3 --version
```

---

## Step 6: Install Mininet

```bash
sudo apt install mininet -y
```

Verify:

```bash
mn --version
```

---

## Step 7: Install Ryu Controller

```bash
pip3 install ryu
```

Verify:

```bash
ryu-manager --version
```

---

## Step 8: Install Open vSwitch

```bash
sudo apt install openvswitch-switch -y
```

---

## Step 9: Install Required Python Libraries

```bash
pip3 install pandas numpy scikit-learn
```

---

## Installation Complete

Your system is now fully configured to run the DDoS Detection and Mitigation using Machine Learning (SDN) project.

---

## Author

Akhil Himnad
MTech Scholar,NIT Bhopal

---

