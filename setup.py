#!/usr/bin/env python
# coding: utf8

import os
import sys


def main():
	print("Installing bma280 accelerometer...")

	if os.system("mkdir -p /lib/modules/5.4.65-v7-axo-r01+/kernel/drivers/iio/accel") != 0:
		print("Could not create directory")
		sys.exit(1)
	if os.system("install -m 644 bmc150-accel-core.ko /lib/modules/5.4.65-v7-axo-r01+/kernel/drivers/iio/accel/") != 0:
		print("Could not copy kernel module")
		sys.exit(1)
	if os.system("install -m 644 bmc150-accel-i2c.ko /lib/modules/5.4.65-v7-axo-r01+/kernel/drivers/iio/accel/") != 0:
		print("Could not copy kernel module")
		sys.exit(1)
	if os.system("depmod -a") != 0:
		print("Could not run depmod")
		sys.exit(1)

	if os.system("cp actez.dtbo /boot/overlays/") != 0:
		print("Could not copy overlay")
		sys.exit(1)


	dtoverlayFound = False
	newConfigData = ""
	f = open("/boot/config.txt", "r")
	for line in f:
		newConfigData += line

		if ("dtoverlay" in line) and ("actez" in line):
			dtoverlayFound = True
	f.close()

	if not dtoverlayFound:
		newConfigData += "\ndtoverlay=actez\n"
		f = open("/boot/config.txt", "w")
		f.write(newConfigData)
		f.close()

	os.system("sync")
	print("done")

if __name__ == '__main__':
	main()
