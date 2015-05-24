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
    print "Module test - Burst Analysis configuration"
    print "  Expected power:     %f dBm" % dev.ask_ban_expected_power()
    print "  RF Channel:         %d" % dev.ask_ban_arfcn()
    print "  Training sequence:  %d" % dev.ask_ban_tsc()
    print "  Decode:             NA"
    print "  Peak power bandw:   %s" % dev.ask_ban_input_bandwidth()
    print "  Trigger mode:       %s" % dev.ask_ban_trigger_mode()
    print "  Used RF Input:      %d" % dev.parse_io_str(dev.ask_io_used())[0]
    print "  Ext atten RF In1:   %f" % dev.ask_ext_att_rf_in1()
    print "  Ext atten RF In2:   %f" % dev.ask_ext_att_rf_in2()

def show_mod_info(dev):
    (pk_phase_err_match, avg_phase_err_match, freq_err_match) = dev.ask_phase_freq_match_avg()
    print "Module test - Burst Analysis measurements"
    print "  Peak power:         %f dBm" % dev.ask_peak_power()
    print "  Avg. burst power:   NA dBm"
    print "  Power ramp:         NA"
    print "  Frequency error:    NA Hz  (%s)" % freq_err_match
    print "  Phase Error (PK):   NA deg (%s)" % pk_phase_err_match
    print "  Phase Error (AVG):  NA deg (%s)" % avg_phase_err_match
    print "Module test - Extra measurements"
    print "  Spectrum modulation: %s" % dev.ask_spectrum_modulation_match()
    print "  Spectrum switching:  %s" % dev.ask_spectrum_switching_match()

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

