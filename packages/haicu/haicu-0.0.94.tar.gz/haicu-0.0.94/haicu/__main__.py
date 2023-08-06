#!/bin/python

import signal
import argparse
import sys
import random
import time
import configparser
import os
import pprint
from simplejson import dumps
import ftdi as haicu_ftdi
import format as haicu_format

VERSION = "1.0"

# Table to convert 'get' request name to status register address
GET_REG_TABLE = {
    'invert_frontpanel': 22,
    'invert_right_address': 21,
    'invert_left_address': 20,
    'invert_tunebox8': 19,
    'invert_tunebox7': 18,
    'invert_tunebox6': 17,
    'invert_tunebox5': 16,
    'invert_tunebox4': 15,
    'invert_tunebox3': 14,
    'invert_tunebox2': 13,
    'invert_tunebox1': 12,
    'enable_frontpanel': 11,
    'enable_right_address': 10,
    'enable_left_address': 9,
    'enable_tunebox8': 8,
    'enable_tunebox7': 7,
    'enable_tunebox6': 6,
    'enable_tunebox5': 5,
    'enable_tunebox4': 4,
    'enable_tunebox3': 3,
    'enable_tunebox2': 2,
    'enable_tunebox1': 1,
    'trigger_invert': 0,
}

GET_PROGRAM_TABLE = {
    'left': 0,
    'right': 1,
    'extension': 2
}

# Thank you stack overflow user nonDucor
# https://stackoverflow.com/questions/72651513/argparse-how-to-map-choices-to-different-values
class RenameSetChoice(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         setattr(namespace, self.dest, GET_REG_TABLE[values])

class RenameProgramChoice(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         setattr(namespace, self.dest, GET_PROGRAM_TABLE[values])

"""
CTRL+C Interrupt Handler
"""
class GracefulExiter():

    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self, signum, frame):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def exit(self):
        return self.state

flag = GracefulExiter()

def main():
    prog='haicu_ctl'
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    parser.add_argument('--latency', type=int, default=-1, help='Set USB driver latency, expert use only')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase logging verbosity, can be repeated')
    parser.add_argument('-l', '--log', metavar='file', help='Log to output file')
    parser.add_argument('-d', '--dev', type=str, default='', help='FTDI device to connect')
    parser.add_argument('-j', '--json', default=False, action='store_true', help='Send response as JSON object')

    cmd_parser = parser.add_subparsers(dest="command", description="Valid subcommands", help=" ")

    ftdi_list_parser = cmd_parser.add_parser("list", help="List available MLD1200 devices")
    ftdi_list_parser.set_defaults(func=arg_list)

    memtest_parser = cmd_parser.add_parser("memtest", help="Memory test")
    memtest_parser.set_defaults(func=arg_memtest)

    get_parser = cmd_parser.add_parser("info", help="Get status information")
    get_parser.set_defaults(func=arg_info)

    set_parser = cmd_parser.add_parser("set", help="Read/Write register value")
    set_parser.set_defaults(func=arg_set)
    set_parser.add_argument("request", type=str, action=RenameSetChoice, choices=GET_REG_TABLE)
    set_parser.add_argument("data", nargs='?', type=str, help="Value to write to register")

    status_parser = cmd_parser.add_parser("status", aliases=['stat'], help="Read status register")
    status_parser.set_defaults(func=arg_status)
    status_parser.add_argument("addr", type=str, help="address to read")

    reg_parser = cmd_parser.add_parser("register", aliases=['reg'], help="Read/Write control register")
    reg_parser.set_defaults(func=arg_reg)
    reg_parser.add_argument("addr", type=str, help="address to read/write")
    reg_parser.add_argument("data", nargs='?', type=str, help="32-bit value to write to register")

    mem_parser = cmd_parser.add_parser("memory", aliases=['mem'], help="Read/Write memory")
    mem_parser.set_defaults(func=arg_mem)
    mem_parser.add_argument("addr", type=str, help="25-bit address to read/write")
    mem_parser.add_argument("data", nargs='?', type=str, help="32-bit value to write to memory")

    block_parser = cmd_parser.add_parser("block", aliases=['bmem'], help="Block Read memory")
    block_parser.set_defaults(func=arg_block)
    block_parser.add_argument("addr", type=str, help="25-bit address to read")
    block_parser.add_argument("count", type=str, help="Number of words to read")

    upload_parser = cmd_parser.add_parser("upload", help="Upload file to memory")
    upload_parser.set_defaults(func=arg_upload)
    upload_parser.add_argument("file", type=str, help="Program file to upload")
    upload_parser.add_argument("section", action=RenameProgramChoice, choices=GET_PROGRAM_TABLE)

    program_parser = cmd_parser.add_parser("program", help="Program MLD1200s")
    program_parser.add_argument("config_file", nargs="?", type=str, default="haicu.ini", help="INI file to use for programming")
    program_parser.add_argument("-a", "--auto", default=False, action='store_true', help="Auto-reload after sequence is finished")
    program_parser.set_defaults(func=arg_program)

    convert_parser = cmd_parser.add_parser("convert", help="Convert")
    convert_parser.add_argument("infile", type=str, help="Derived file to convert")
    convert_parser.add_argument("outfile", type=str, help="RLE file to create")
    convert_parser.set_defaults(func=arg_convert)

    compare_parser = cmd_parser.add_parser("compare", help="Compare derived file to rle")
    compare_parser.add_argument("dfile", type=str, help="Derived file to compare")
    compare_parser.add_argument("rfile", type=str, help="RLE file to compare")
    compare_parser.set_defaults(func=arg_compare)

    csv_parser = cmd_parser.add_parser("csv", help="Parse CSV file")
    csv_parser.add_argument("csvfile", type=str, help="CSV sum file")
    csv_parser.set_defaults(func=arg_csv)

    monitor_parser = cmd_parser.add_parser("monitor", help="Monitor MLD1200")
    monitor_parser.set_defaults(func=arg_monitor)

    args = parser.parse_args()

    try:
        ftdi_dev = haicu_ftdi.init(args.dev, args.latency)
    except:
        print("Device '" + str(args.dev) + "' not found!")
        print()
        arg_list(args, None)
        sys.exit(-1)

    if(args.command == None):
        parser.print_usage()
        sys.exit(0)

    args.func(args, ftdi_dev)

def arg_list(args, ftdi_dev):
    print("Available devices:")
    result = haicu_ftdi.list_devices()
    for n, r in enumerate(result):
        print(str(n+1) + "\t" + str(r[0]) + "\t" + str(r[1]))

    if(len(result) == 0):
        print("No devices found")

def arg_memtest(args, ftdi_dev):
    # Generate random data of 'tlen' length
    tlen = 1048576 # number of 32-bit words to transfer
    tlen_in_bytes = tlen * 4
    print("Test transfer size: " + str(tlen_in_bytes) + " bytes")
    test_data = []
    for n in range(0, tlen):
        test_data.append(random.randrange(100))

    # Write test
    start_time = time.time()
    haicu_ftdi.write_memory(ftdi_dev, 0, test_data)
    end_time = time.time()
    delta_time = end_time - start_time
    print("Write done. Elapsed time: " + f"{delta_time:.3f}" + " Rate: " + f"{(tlen_in_bytes / 1000000) / delta_time :.3f}" + " MBps (" + f"{(tlen_in_bytes / delta_time) * 8 / 1000000:.3f}" + " Mbps)")

    # Read test
    start_time = time.time()
    result = haicu_ftdi.read_memory(ftdi_dev, 0, tlen)
    end_time = time.time()
    delta_time = end_time - start_time
    print("Read done. Elapsed time: " + f"{delta_time:.3f}" + " Rate: " + f"{(tlen_in_bytes / 1000000) / delta_time:.3f}" + " MBps (" + f"{(tlen_in_bytes / delta_time) * 8 / 1000000:.3f}" + " Mbps)")

    # Validate
    result_len = len(result)
    if(result_len == 0):
        print("Null result (check if program_load is set!")
        sys.exit(-1)

    for n in range(0, tlen):
        if(result[n] != test_data[n]):
            print("Mismatch at " + str(n) + "\tExpected: " + str(test_data[n]) + " Result: " + str(result[n]))
            sys.exit(-1)

    print("Verification Successful")

## Converts status values into human read-able format
def arg_info(args, ftdi_dev):
    status_resp = haicu_ftdi.gather_status_registers(ftdi_dev)
    control_resp = haicu_ftdi.gather_control_registers(ftdi_dev)

    if(not args.json):
        print("Status:")
        print("\tFrontpanel Bits: 0x" + f"{(status_resp['fp_status']):02X}")
        print("\tProgram Load: " + str(status_resp['program_load']))
        print("\tProgram Armed: " + str(status_resp['program_armed']))
        print("\tProgram Active: " + str(status_resp['program_active']))
        print("\tProgram Done: " + str(status_resp['program_done']))
        print("\tProgram Error: " + str(status_resp['program_error']))
        print("\tProgram DDR Load: " + str(status_resp['program_ddr_load']))
        print("\tProgram DDR Lock: " + str(status_resp['program_ddr_lock']))
        print("\tProgram Run Count: " + str(status_resp['program_run_count']))
        print("\tProgram Error Count: " + str(status_resp['program_error_count']))
        print()
        print("\tTrigger Active: " + str(status_resp['trigger_active']))
        print("\tTrigger Counter: " + str(status_resp['trigger_counter']))
        print("\tExternal Clock Frequency: " + f"{status_resp['external_clock_freq']:.3f}" + " MHz")
        print("\tExternal Clock Active: " + str(status_resp['external_clock_active']))
        print("\tExternal Clock Counter: " + str(status_resp['external_clock_counter']))
        print("\tBuildtime: "+ str(status_resp['buildtime']))
        print()
        print("Control:")
        print("\tProgram Load: " + str(control_resp['program_load']))
        print("\tProgram Numwords: " + str(control_resp['program_numwords']))
        print()
        print("\tTrigger Inverted: " + str(control_resp['trigger_invert']))
        print("\tTrigger Delay: " + str(control_resp['trigger_delay']))
        print()
        print("\tEnable Tunebox1: 0x" + f"{(control_resp['enable_tunebox1']):02X}")
        print("\tEnable Tunebox2: 0x" + f"{(control_resp['enable_tunebox2']):02X}")
        print("\tEnable Tunebox3: 0x" + f"{(control_resp['enable_tunebox3']):02X}")
        print("\tEnable Tunebox4: 0x" + f"{(control_resp['enable_tunebox4']):02X}")
        print("\tEnable Tunebox5: 0x" + f"{(control_resp['enable_tunebox5']):02X}")
        print("\tEnable Tunebox6: 0x" + f"{(control_resp['enable_tunebox6']):02X}")
        print("\tEnable Tunebox7: 0x" + f"{(control_resp['enable_tunebox7']):02X}")
        print("\tEnable Tunebox8: 0x" + f"{(control_resp['enable_tunebox8']):02X}")
        print()
        print("\tInvert Tunebox1: 0x" + f"{(control_resp['invert_tunebox1']):02X}")
        print("\tInvert Tunebox2: 0x" + f"{(control_resp['invert_tunebox2']):02X}")
        print("\tInvert Tunebox3: 0x" + f"{(control_resp['invert_tunebox3']):02X}")
        print("\tInvert Tunebox4: 0x" + f"{(control_resp['invert_tunebox4']):02X}")
        print("\tInvert Tunebox5: 0x" + f"{(control_resp['invert_tunebox5']):02X}")
        print("\tInvert Tunebox6: 0x" + f"{(control_resp['invert_tunebox6']):02X}")
        print("\tInvert Tunebox7: 0x" + f"{(control_resp['invert_tunebox7']):02X}")
        print("\tInvert Tunebox8: 0x" + f"{(control_resp['invert_tunebox8']):02X}")
        print()
        print("\tEnable Frontpanel: 0x" + f"{(control_resp['enable_frontpanel']):02X}")
        print("\tEnable Left Address: 0x" + f"{(control_resp['enable_left_address']):03X}")
        print("\tEnable Right Address: 0x" + f"{(control_resp['enable_right_address']):03X}")
        print()
        print("\tInvert Frontpanel: 0x" + f"{(control_resp['invert_frontpanel']):02X}")
        print("\tInvert Left Address: 0x" + f"{(control_resp['invert_left_address']):03X}")
        print("\tInvert Right Address: 0x" + f"{(control_resp['invert_right_address']):03X}")
    else:
        print("{\"status\":" + dumps(status_resp) + ",\"control\":" + dumps(control_resp) + "}")

## Converts register values into human read-able format
def arg_set(args, ftdi_dev):
    addr = args.request
    if(addr == GET_REG_TABLE["trigger_invert"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 2) & 0xBFFFFFFF
        value = (int(args.data, 0) & 0x1) << 30
        haicu_ftdi.write_register(ftdi_dev, 2, value | init_value)

    if(addr == GET_REG_TABLE["trigger_delay"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 2) & 0xFFFFFF00
        value = (int(args.data, 0) & 0xFF)
        haicu_ftdi.write_register(ftdi_dev, 2, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox1"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 3) & 0xFFFFFF00
        value = (int(args.data, 0) & 0xFF)
        haicu_ftdi.write_register(ftdi_dev, 3, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox2"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 3) & 0xFFFF00FF
        value = (int(args.data, 0) & 0xFF) << 8
        haicu_ftdi.write_register(ftdi_dev, 3, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox3"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 3) & 0xFF00FFFF
        value = (int(args.data, 0) & 0xFF) << 16
        haicu_ftdi.write_register(ftdi_dev, 3, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox4"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 3) & 0x00FFFFFF
        value = (int(args.data, 0) & 0xFF) << 24
        haicu_ftdi.write_register(ftdi_dev, 3, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox5"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 4) & 0xFFFFFF00
        value = (int(args.data, 0) & 0xFF)
        haicu_ftdi.write_register(ftdi_dev, 4, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox6"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 4) & 0xFFFF00FF
        value = (int(args.data, 0) & 0xFF) << 8
        haicu_ftdi.write_register(ftdi_dev, 4, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox7"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 4) & 0xFF00FFFF
        value = (int(args.data, 0) & 0xFF) << 16
        haicu_ftdi.write_register(ftdi_dev, 4, value | init_value)

    if(addr == GET_REG_TABLE["enable_tunebox8"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 4) & 0x00FFFFFF
        value = (int(args.data, 0) & 0xFF) << 24
        haicu_ftdi.write_register(ftdi_dev, 4, value | init_value)

    if(addr == GET_REG_TABLE["enable_left_address"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 5) & 0xFFFFF000
        value = (int(args.data, 0) & 0xFFF)
        haicu_ftdi.write_register(ftdi_dev, 5, value | init_value)

    if(addr == GET_REG_TABLE["enable_right_address"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 5) & 0xF000FFFF
        value = (int(args.data, 0) & 0xFFF) << 16
        haicu_ftdi.write_register(ftdi_dev, 5, value | init_value)

    if(addr == GET_REG_TABLE["enable_frontpanel"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 5) & 0x0FFF0FFF
        value1 = (int(args.data, 0) & 0x0F) << 12
        value2 = (int(args.data, 0) & 0xF0) << 24
        haicu_ftdi.write_register(ftdi_dev, 5, value1 | value2 | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox1"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 6) & 0xFFFFFF00
        value = (int(args.data, 0) & 0xFF)
        haicu_ftdi.write_register(ftdi_dev, 6, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox2"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 6) & 0xFFFF00FF
        value = (int(args.data, 0) & 0xFF) << 8
        haicu_ftdi.write_register(ftdi_dev, 6, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox3"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 6) & 0xFF00FFFF
        value = (int(args.data, 0) & 0xFF) << 16
        haicu_ftdi.write_register(ftdi_dev, 6, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox4"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 6) & 0x00FFFFFF
        value = (int(args.data, 0) & 0xFF) << 24
        haicu_ftdi.write_register(ftdi_dev, 6, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox5"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 7) & 0xFFFFFF00
        value = (int(args.data, 0) & 0xFF)
        haicu_ftdi.write_register(ftdi_dev, 7, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox6"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 7) & 0xFFFF00FF
        value = (int(args.data, 0) & 0xFF) << 8
        haicu_ftdi.write_register(ftdi_dev, 7, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox7"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 7) & 0xFF00FFFF
        value = (int(args.data, 0) & 0xFF) << 16
        haicu_ftdi.write_register(ftdi_dev, 7, value | init_value)

    if(addr == GET_REG_TABLE["invert_tunebox8"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 7) & 0x00FFFFFF
        value = (int(args.data, 0) & 0xFF) << 24
        haicu_ftdi.write_register(ftdi_dev, 7, value | init_value)

    if(addr == GET_REG_TABLE["invert_left_address"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 8) & 0xFFFFF000
        value = (int(args.data, 0) & 0xFFF)
        haicu_ftdi.write_register(ftdi_dev, 8, value | init_value)

    if(addr == GET_REG_TABLE["invert_right_address"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 8) & 0xF000FFFF
        value = (int(args.data, 0) & 0xFFF) << 16
        haicu_ftdi.write_register(ftdi_dev, 8, value | init_value)

    if(addr == GET_REG_TABLE["invert_frontpanel"]):
        init_value = haicu_ftdi.read_register(ftdi_dev, 8) & 0x0FFF0FFF
        value1 = (int(args.data, 0) & 0x0F) << 12
        value2 = (int(args.data, 0) & 0xF0) << 24
        haicu_ftdi.write_register(ftdi_dev, 8, value1 | value2 | init_value)

## Low level status register read
def arg_status(args, ftdi_dev):
    addr = int(args.addr, 0)
    val = haicu_ftdi.read_status(ftdi_dev, addr)
    if(not args.json):
        if(val != None):
            if(args.verbose > 0):
                print("[" + "0x{:02x}".format(addr) + "] " + '0x{:08x}'.format(val) + " (" + str(val) + ")")
            else:
                print('0x{:08x}'.format(val))
        else:
            print("No/Invalid response")
            sys.exit(-1)
    else:
        if(val != None):
            print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": " + '{:d}'.format(val) + "}")
        else:
            print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": null}")


## Read/Write a register
# if no data is passed 'read' is assumed
def arg_reg(args, ftdi_dev):
    addr = int(args.addr, 0)
    if(not args.data == None):
        haicu_ftdi.write_register(ftdi_dev, addr, int(args.data, 0))
    else:
        val = haicu_ftdi.read_register(ftdi_dev, addr)
        if(not args.json):
            if(val != None):
                if(args.verbose > 0):
                    print("[" + "0x{:02x}".format(addr) + "] " + '0x{:08x}'.format(val) + " (" + str(val) + ")")
                else:
                    print('0x{:08x}'.format(val))
            else:
                print("No/Invalid response")
                sys.exit(-1)
        else:
            if(val != None):
                print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": " + '{:d}'.format(val) + "}")
            else:
                print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": null}")

def arg_mem(args, ftdi_dev):
    addr = int(args.addr, 0)
    if(not args.data == None):
        haicu_ftdi.write_memory(ftdi_dev, addr, int(args.data, 0))
    else:
        val = haicu_ftdi.read_memory(ftdi_dev, addr, 1)
        if(not args.json):
            if(len(val) > 0):
                if(args.verbose > 0):
                    print('[0x{:07x}'.format(addr)+"] " + '0x{:08x}'.format(val[0]) + " (" + str(val[0]) + ")")
                else:
                    print('0x{:08x}'.format(val[0]))
            else:
                print("No/Invalid response")
                sys.exit(-1)
        else:
            if(len(val) > 0):
                print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": " + '{:d}'.format(val[0]) + "}")
            else:
                print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": null}")

def arg_block(args, ftdi_dev):
    addr = int(args.addr, 0)
    count = int(args.count, 0)
    response = haicu_ftdi.read_memory(ftdi_dev, addr, count)
    if(not args.json):
        if(len(response) > 0):
            for idx, val in enumerate(response):
                if(args.verbose > 0):
                    print('[0x{:07x}'.format(addr + idx)+"] " + '0x{:08x}'.format(val) + " (" + str(val) + ")")
                else:
                    print('0x{:08x}'.format(val))
        else:
            print("No/Invalid response")
            sys.exit(-1)
    else:
        if(len(response) > 0):
            result_str = "{\"address\": " + "{:d}".format(addr)  + ", \"value\": ["
            for idx, val in enumerate(response):
                if(idx == len(response)-1):
                    result_str = result_str + '{:d}'.format(val) + "]}"
                else:
                    result_str = result_str + '{:d}'.format(val) + ","
            print(result_str)
        else:
            print("{\"address\": " + "{:d}".format(addr)  + ", \"value\": null}")


def arg_upload(args, ftdi_dev):
    if(not os.path.exists(args.file)):
        print("File " + args.file + " does not exist")
        sys.exit(-1)

    in_name, in_ext = os.path.splitext(args.file)

    try:
        if(in_ext.lower() == ".txt"):
            print("Generating RLE from " + args.file)
            rle = haicu_format.convert_derived2rle(args.file)
        elif(in_ext.lower() == ".rle"):
            rle = haicu_format.load_rle_from_file(args.file)
        else:
            print("Invalid filetype " + in_ext + ". Must be .rle or .txt")
            sys.exit(-1)

    except:
        if(os.path.exists(args.file)):
            print("Error parsing " + args.file)
        else:
            print("File not found: " + args.file)
            sys.exit(-1)

    upload(ftdi_dev, rle, args.section, args.verbose)
    # haicu_ftdi.write_register(ftdi_dev, 0, 1) # Turn on program load

def arg_program(args, ftdi_dev):
    if(not os.path.exists(args.config_file)):
        if(args.verbose > 0):
            print("Config file " + args.config_file + " not found")
        sys.exit(-1)

    config = configparser.ConfigParser()
    config.read(args.config_file)

    in_file = config['DEFAULT']['file']
    in_name, in_ext = os.path.splitext(in_file)

    # Load the RLE file
    try:
        if(in_ext.lower() == ".txt"):
            if(args.verbose > 0):
                print("Generating RLE from " + in_file)
            rle = haicu_format.convert_derived2rle(in_file)
        elif(in_ext.lower() == ".rle"):
            if(args.verbose > 0):
                print("Loading RLE payload from " + in_file)
            rle = haicu_format.load_rle_from_file(in_file)
        else:
            if(args.verbose > 0):
                print("Invalid filetype " + in_ext + ". Must be .rle or .txt")
            sys.exit(-1)

    except:
        if(os.path.exists(in_file)):
            print("Error parsing " + in_file)
        else:
            print("File not found: " + in_file)
            sys.exit(-1)

    # Program each section
    dev_list = []
    for n in range(len(rle)):
        section_name = next(key for key, value in GET_PROGRAM_TABLE.items() if value == n)

        if(config['DEFAULT'][section_name]):
            try:
                dev = haicu_ftdi.init(config['DEFAULT'][section_name], args.latency)
            except:
                print("Error initializing MLD1200 device '" + config['DEFAULT'][section_name] + "'")

            dev_list.append(dev)
            # Turn off program load prior to upload, as it will be blocked otherwise
            haicu_ftdi.write_register(dev, 0, 0)

            # Write config
            config_str = 'config.' + section_name
            if(config_str in config.keys()):
                if(args.verbose > 0):
                    print("Writing config for " + section_name + " section")
                haicu_ftdi.write_control_registers(dev, config[config_str])

            if(args.verbose > 0):
                print("Programming " + config['DEFAULT'][section_name] + " with " + section_name + " section")
            upload(dev, rle, GET_PROGRAM_TABLE[section_name], args.verbose)

            # Turn on program load
            val = haicu_ftdi.read_register(dev, 0)
            if(args.auto):
                val = val | 0x40000000
            haicu_ftdi.write_register(dev, 0, 0x80000000 | val)
        else:
            if(args.verbose > 0):
                print("No device specified for " + section_name + " section")

        if(args.verbose > 0):
            print()

    monitor(dev_list)

def arg_convert(args, ftdi_dev):
    if(args.verbose > 0):
        print("Converting " + args.infile + " to RLE")

    in_name, in_ext = os.path.splitext(args.infile)
    if(in_ext != ".txt"):
        print("Invalid extension, input file must be .txt")
        sys.exit(-1)

    out_name, out_ext = os.path.splitext(args.outfile)
    if(out_ext != ".rle"):
        print("Invalid extension, output file must be .rle")
        sys.exit(-1)

    rle = haicu_format.convert_derived2rle(args.infile)
    if(args.verbose > 1):
        pprint.pprint(rle) # Debug print, only useful for tiny derived.txt files

    if(args.verbose > 0):
        print("Creating RLE file " + args.outfile)

    with open(args.outfile, "wb+") as f:
        for n in range(len(rle)):
            f.write(rle[n])

def arg_compare(args, ftdi_dev):
    # Verification
    if(haicu_format.match(args.dfile, args.rfile, args.verbose)):
        if(args.verbose > 0):
            print("RLE and Derived files match")
    else:
        if(args.verbose > 0):
            print("RLE and Derived files do not match!")
            print()
            sys.exit(-1)

def arg_monitor(args, ftdi_dev):
    monitor([ftdi_dev])

def arg_csv(args, ftdi_dev):
    haicu_format.convert_sum_to_obj(args.csvfile)

def monitor(ftdi_dev_list):
    log = ""
    while(not flag.state):
        for ftdi_dev in ftdi_dev_list:
            log = log + hex(haicu_ftdi.read_status(ftdi_dev, 0)) + "\n"

    print(log)

def upload(ftdi_dev, rle, mld_section, verbose):
    section_name = next(key for key, value in GET_PROGRAM_TABLE.items() if value == mld_section)

    if(mld_section >= len(rle)):
        print("MLD section '" + section_name + "' does not exist")
        sys.exit(-1)

    reg = haicu_ftdi.read_register(ftdi_dev, 0)
    if(reg != 0):
        print("Device is in program load mode, clear register 0 bit 1 to proceed")
        return

    payload = rle[mld_section]

    tlen = len(payload)

    if(verbose > 0):
        start_time = time.time()

    haicu_ftdi.write_memory(ftdi_dev, 0, payload)
    if(verbose > 0):
        end_time = time.time()
        delta_time = end_time - start_time
        print("Write done. Elapsed time: " + f"{delta_time:.3f}" + " Rate: " + f"{(tlen / delta_time) * 4 / 1000000:.3f}" + " MBps (" + f"{(tlen / delta_time) * 32 / 1000000:.3f}" + " Mbps)")

    if(verbose > 0):
        start_time = time.time()
    result = haicu_ftdi.read_memory(ftdi_dev, 0, tlen)

    if(verbose > 0):
        end_time = time.time()
        delta_time = end_time - start_time
        print("Read done. Elapsed time: " + f"{delta_time:.3f}" + " Rate: " + f"{(tlen / delta_time) * 4 / 1000000:.3f}" + " MBps (" + f"{(tlen / delta_time) * 32 / 1000000:.3f}" + " Mbps)")

    # Validate
    if(len(result) > 0):
        for n in range(0, len(payload)):
            if result[n] != payload[n]:
                print("Verification Failed. Mismatch at " + str(n) + "\tExpected: " + str(payload[n]) + " Result: " + str(result[n]))
                sys.exit(-1)

        if(verbose > 0):
            print("Verification Successful")
            print("Payload length in words: " + str(tlen))
            print("Payload length in bytes: " + str(tlen * 4))
            print("Updating program count register")

        haicu_ftdi.write_register(ftdi_dev, 1, tlen) # Load program count
    else:
        print("Verification failed. Null result payload")

if __name__ == "__main__":
    main()
