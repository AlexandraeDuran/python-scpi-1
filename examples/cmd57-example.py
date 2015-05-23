#!/usr/bin/env python -i
import os,sys
# Add the parent dir to search paths
#libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..')
#if os.path.isdir(libs_dir):                                       
#    sys.path.append(libs_dir)

from scpi.devices import cmd57
import atexit

def show_sys_info(dev):
    print "System version:       %s" % " ".join(dev.identify())
    print "Installed options:    %s" % " ".join(dev.ask_installed_options())

def show_sys_config(dev):
    print "RF input/output port: %s" % dev.ask_io_used()

def show_bts_config(dev):
    print "BTS CCCH ARFCN:       %d" % dev.ask_bts_ccch_arfcn()
    print "BTS TCH ARFCN:        %d" % dev.ask_bts_tch_arfcn()
    print "BTS TCH timeslot:     %d" % dev.ask_bts_tch_ts()
    print "BTS TSC:              %d" % dev.ask_bts_tsc()

def show_bts_info(dev):
    print "BTS MCC:              %d" % dev.ask_bts_mcc()
    print "BTS MNC:              %d" % dev.ask_bts_mcc()
    print "BTS BSIC:             %d" % dev.ask_bts_bsic()
    print "BTS burst avg power:  %d dBm" % dev.ask_burst_power_avg()

def show_mod_config(dev):
    print "Module test ARFCN:    %d" % dev.ask_ban_arfcn()
    print "Module test TSC:      %d" % dev.ask_ban_tsc()
    print "Module test exp.power %f dBm" % dev.ask_ban_expected_power()

def show_mod_info(dev):
    print "Module peak power:    %f dBm" % dev.ask_peak_power()
    print "Module pk.phase, avg.phase, freq: %s" % ", ".join(dev.ask_phase_freq_match_avg())
    print "Module spectrum modulation: %s" % dev.ask_spectrum_modulation_match()
    print "Module spectrum switching: %s" % dev.ask_spectrum_switching_match()

def show_cur_mode(dev):
    print "Current test mode:    %s" % dev.ask_test_mode()
    print "Current device state: %s" % dev.ask_dev_state()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:"
        print "  python -i cmd57-example.py /dev/ttyUSB0"
        sys.exit(1)
    # Then put to interactive mode
    os.environ['PYTHONINSPECT'] = '1'
    dev = cmd57.rs232(sys.argv[1], rtscts=True)
    atexit.register(dev.quit)

    show_sys_info(dev)
    show_sys_config(dev)
    show_bts_config(dev)
    show_mod_config(dev)
    show_cur_mode(dev)

    print
    print "Expecting your input now"

