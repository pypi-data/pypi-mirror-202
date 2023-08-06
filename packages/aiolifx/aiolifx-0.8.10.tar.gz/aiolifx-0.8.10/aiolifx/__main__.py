#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# This application is an example on how to use aiolifx
#
# Copyright (c) 2016 François Wautier
# Copyright (c) 2022 Michael Farrell <micolous+git@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
import sys
import asyncio as aio
import aiolifx as alix
from functools import partial
from time import sleep
import argparse

UDP_BROADCAST_PORT = 56700


# Simple bulb control frpm console
class bulbs:
    """A simple class with a register and unregister methods"""

    def __init__(self):
        self.bulbs = []
        self.boi = None  # bulb of interest

    def register(self, bulb):
        global opts
        bulb.get_label()
        bulb.get_location()
        bulb.get_version()
        bulb.get_group()
        bulb.get_wififirmware()
        bulb.get_hostfirmware()
        self.bulbs.append(bulb)
        self.bulbs.sort(key=lambda x: x.label or x.mac_addr)
        if opts.extra:
            bulb.register_callback(lambda y: print("Unexpected message: %s" % str(y)))

    def unregister(self, bulb):
        idx = 0
        for x in list([y.mac_addr for y in self.bulbs]):
            if x == bulb.mac_addr:
                del self.bulbs[idx]
                break
            idx += 1


def readin():
    """Reading from stdin and displaying menu"""
    global MyBulbs

    selection = sys.stdin.readline().strip("\n")
    MyBulbs.bulbs.sort(key=lambda x: x.label or x.mac_addr)
    lov = [x for x in selection.split(" ") if x != ""]
    if lov:
        if MyBulbs.boi:
            try:
                if True:
                    if int(lov[0]) == 0:
                        MyBulbs.boi = None
                    elif int(lov[0]) == 1:
                        if len(lov) > 1:
                            MyBulbs.boi.set_power(lov[1].lower() in ["1", "on", "true"])
                            MyBulbs.boi = None
                        else:
                            print("Error: For power you must indicate on or off\n")
                    elif int(lov[0]) == 2:
                        if len(lov) > 2:
                            try:
                                MyBulbs.boi.set_color(
                                    [
                                        58275,
                                        0,
                                        int(round((float(lov[1]) * 65365.0) / 100.0)),
                                        int(round(float(lov[2]))),
                                    ]
                                )

                                MyBulbs.boi = None
                            except:
                                print(
                                    "Error: For white brightness (0-100) and temperature (2500-9000) must be numbers.\n"
                                )
                        else:
                            print(
                                "Error: For white you must indicate brightness (0-100) and temperature (2500-9000)\n"
                            )
                    elif int(lov[0]) == 3:
                        if len(lov) > 3:
                            try:
                                MyBulbs.boi.set_color(
                                    [
                                        int(round((float(lov[1]) * 65535.0) / 360.0)),
                                        int(round((float(lov[2]) * 65535.0) / 100.0)),
                                        int(round((float(lov[3]) * 65535.0) / 100.0)),
                                        3500,
                                    ]
                                )
                                MyBulbs.boi = None
                            except:
                                print(
                                    "Error: For colour hue (0-360), saturation (0-100) and brightness (0-100)) must be numbers.\n"
                                )
                        else:
                            print(
                                "Error: For colour you must indicate hue (0-360), saturation (0-100) and brightness (0-100))\n"
                            )

                    elif int(lov[0]) == 4:
                        print(MyBulbs.boi.device_characteristics_str("    "))
                        print(MyBulbs.boi.device_product_str("    "))
                        MyBulbs.boi = None
                    elif int(lov[0]) == 5:
                        print(MyBulbs.boi.device_firmware_str("   "))
                        MyBulbs.boi = None
                    elif int(lov[0]) == 6:
                        mypartial = partial(MyBulbs.boi.device_radio_str)
                        MyBulbs.boi.get_wifiinfo(
                            callb=lambda x, y: print("\n" + mypartial(y))
                        )
                        MyBulbs.boi = None
                    elif int(lov[0]) == 7:
                        mypartial = partial(MyBulbs.boi.device_time_str)
                        MyBulbs.boi.get_hostinfo(
                            callb=lambda x, y: print("\n" + mypartial(y))
                        )
                        MyBulbs.boi = None
                    elif int(lov[0]) == 8:
                        if len(lov) > 3:
                            try:
                                MyBulbs.boi.set_waveform(
                                    {
                                        "color": [
                                            int(
                                                round((float(lov[1]) * 65535.0) / 360.0)
                                            ),
                                            int(
                                                round((float(lov[2]) * 65535.0) / 100.0)
                                            ),
                                            int(
                                                round((float(lov[3]) * 65535.0) / 100.0)
                                            ),
                                            3500,
                                        ],
                                        "transient": 1,
                                        "period": 100,
                                        "cycles": 30,
                                        "skew_ratio": 0,
                                        "waveform": 3,
                                    }
                                )
                                MyBulbs.boi = None
                            except:
                                print(
                                    "Error: For pulse hue (0-360), saturation (0-100) and brightness (0-100)) must be numbers.\n"
                                )
                        else:
                            print(
                                "Error: For pulse you must indicate hue (0-360), saturation (0-100) and brightness (0-100))\n"
                            )
                    elif int(lov[0]) == 9:
                        if (
                            alix.aiolifx.features_map[MyBulbs.boi.product]["hev"]
                            is True
                        ):
                            # HEV cycle
                            if len(lov) == 1:
                                # Get current state
                                print("Getting current HEV state")
                                MyBulbs.boi.get_hev_cycle(
                                    callb=lambda _, r: print(
                                        f"\nHEV: duration={r.duration}, "
                                        f"remaining={r.remaining}, "
                                        f"last_power={r.last_power}"
                                    )
                                )
                                MyBulbs.boi.get_last_hev_cycle_result(
                                    callb=lambda _, r: print(
                                        f"\nHEV result: {r.result_str}"
                                    )
                                )

                            elif len(lov) == 2:
                                try:
                                    duration = int(lov[1])
                                    enable = duration >= 0
                                    if enable:
                                        print(
                                            f"Running HEV cycle for {duration} second(s)"
                                        )
                                    else:
                                        print(f"Aborting HEV cycle")
                                        duration = 0
                                    MyBulbs.boi.set_hev_cycle(
                                        enable=enable,
                                        duration=duration,
                                        callb=lambda _, r: print(
                                            f"\nHEV: duration={r.duration}, "
                                            f"remaining={r.remaining}, "
                                            f"last_power={r.last_power}"
                                        ),
                                    )
                                except:
                                    print("Error: duration must be an integer")
                            else:
                                print("Error: maximum 1 argument for HEV cycle")
                            MyBulbs.boi = None
                        elif (
                            alix.aiolifx.features_map[MyBulbs.boi.product]["multizone"]
                            is True
                        ):
                            # Multizone firmware effect
                            print(
                                "Getting current firmware effect state from multizone device"
                            )
                            MyBulbs.boi.get_multizone_effect(
                                callb=lambda _, r: print(
                                    f"\nCurrent effect={r.effect_str}"
                                    f"\nSpeed={r.speed/1000 if getattr(r, 'speed', None) is not None else 0}"
                                    f"\nDuration={r.duration/1000000000 if getattr(r, 'duration', None) is not None else 0:4f}"
                                    f"\nDirection={r.direction_str}"
                                )
                            )
                            MyBulbs.boi = None

                    elif int(lov[0]) == 10:
                        if (
                            alix.aiolifx.features_map[MyBulbs.boi.product]["hev"]
                            is True
                        ):
                            # HEV cycle configuration
                            if len(lov) == 1:
                                # Get current state
                                print("Getting current HEV configuration")
                                MyBulbs.boi.get_hev_configuration(
                                    callb=lambda _, r: print(
                                        f"\nHEV: indication={r.indication}, "
                                        f"duration={r.duration}"
                                    )
                                )

                            elif len(lov) == 3:
                                try:
                                    indication = bool(int(lov[1]))
                                    duration = int(lov[2])
                                    print(
                                        f"Configuring default HEV cycle with "
                                        f"{'' if indication else 'no '}indication for "
                                        f"{duration} second(s)"
                                    )
                                    MyBulbs.boi.set_hev_configuration(
                                        indication=indication,
                                        duration=duration,
                                        callb=lambda _, r: print(
                                            f"\nHEV: indication={r.indication}, "
                                            f"duration={r.duration}"
                                        ),
                                    )
                                except:
                                    print(
                                        "Error: both indication and duration must be integer."
                                    )
                            else:
                                print("Error: 0 or 2 arguments for HEV config")
                            MyBulbs.boi = None
                        elif (
                            alix.aiolifx.features_map[MyBulbs.boi.product]["multizone"]
                            is True
                        ):
                            can_set = True
                            if len(lov) == 3:
                                effect = str(lov[1])
                                direction = str(lov[2])

                                if effect.lower() not in ["off", "move"]:
                                    print(
                                        "Error: effect parameter must be 'off' or 'move'"
                                    )
                                    can_set = False
                                if direction.lower() not in ["left", "right"]:
                                    print(
                                        "Error: direction parameter must be 'right' or 'left"
                                    )
                                    can_set = False

                                if can_set:
                                    e = alix.aiolifx.MultiZoneEffectType[
                                        effect.upper()
                                    ].value
                                    d = alix.aiolifx.MultiZoneDirection[
                                        direction.upper()
                                    ].value
                                    MyBulbs.boi.set_multizone_effect(
                                        effect=e, speed=3, direction=d
                                    )

                            elif len(lov) == 2:
                                MyBulbs.boi.set_multizone_effect(effect=0)

                            else:
                                print(
                                    "Error: need to provide effect and direction parameters."
                                )

                            MyBulbs.boi = None
                    elif int(lov[0]) == 99:
                        # Reboot bulb
                        print(
                            "Rebooting bulb in 3 seconds. If the bulb is on, it will flicker off and back on as it reboots."
                        )
                        print(
                            "Hit CTRL-C within 3 seconds to to quit without rebooting the bulb."
                        )
                        sleep(3)
                        MyBulbs.boi.set_reboot()
                        print("Bulb rebooted.")
            except:
                print("\nError: Selection must be a number.\n")
        else:
            try:
                if int(lov[0]) > 0:
                    if int(lov[0]) <= len(MyBulbs.bulbs):
                        MyBulbs.boi = MyBulbs.bulbs[int(lov[0]) - 1]
                    else:
                        print("\nError: Not a valid selection.\n")

            except:
                print("\nError: Selection must be a number.\n")

    if MyBulbs.boi:
        print("Select Function for {}:".format(MyBulbs.boi.label))
        print("\t[1]\tPower (0 or 1)")
        print("\t[2]\tWhite (Brigthness Temperature)")
        print("\t[3]\tColour (Hue Saturation Brightness)")
        print("\t[4]\tInfo")
        print("\t[5]\tFirmware")
        print("\t[6]\tWifi")
        print("\t[7]\tUptime")
        print("\t[8]\tPulse")
        if alix.aiolifx.features_map[MyBulbs.boi.product]["hev"] is True:
            print("\t[9]\tHEV cycle (Nothing for query, duration or -1 to stop)")
            print("\t[10]\tHEV configuration (Nothing for query, indication duration)")
        if alix.aiolifx.features_map[MyBulbs.boi.product]["multizone"] is True:
            print("\t[9]\tGet firmware effect status")
            print("\t[10]\tStart or stop firmware effect ([off/move] [right|left])")
        print("\t[99]\tReboot the bulb (indicated by a reboot blink)")
        print("")
        print("\t[0]\tBack to bulb selection")
    else:
        idx = 1
        print("Select Bulb:")
        for x in MyBulbs.bulbs:
            print("\t[{}]\t{}".format(idx, x.label or x.mac_addr))
            idx += 1
    print("")
    print("Your choice: ", end="", flush=True)


async def amain():
    global MyBulbs

    # Avoid any asyncio error message
    await aio.sleep(0)

    MyBulbs = bulbs()
    loop = aio.get_event_loop()
    discovery = alix.LifxDiscovery(loop, MyBulbs)
    try:
        loop.add_reader(sys.stdin, readin)
        discovery.start()
        print('Hit "Enter" to start')
        print("Use Ctrl-C to quit")
        await aio.Event().wait()
    finally:
        discovery.cleanup()
        loop.remove_reader(sys.stdin)


def main():
    global opts

    parser = argparse.ArgumentParser(
        description="Track and interact with Lifx light bulbs."
    )
    parser.add_argument(
        "-6",
        "--ipv6prefix",
        default=None,
        help="Connect to Lifx using IPv6 with given /64 prefix (Do not end with colon unless you have less than 64bits).",
    )
    parser.add_argument(
        "-x",
        "--extra",
        action="store_true",
        default=False,
        help="Print unexpected messages.",
    )
    try:
        opts = parser.parse_args()
    except Exception as e:
        parser.error("Error: " + str(e))
    try:
        aio.run(amain())
    except KeyboardInterrupt:
        print("\nExiting at user's request.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
