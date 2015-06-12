#!/usr/bin/env python -i
import os,sys
# Add the parent dir to search paths
#libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..')
#if os.path.isdir(libs_dir):                                       
#    sys.path.append(libs_dir)

from scpi.devices import cmd57
import atexit

def format_int(val):
    if val is None: return "nan"
    else: return "%6d" % val

def format_float(val):
    return "%6.2f" % val

def print_sys_info(dev):
    print "System version:       %s" % " ".join(dev.identify())
    print "Installed options:    %s" % " ".join(dev.ask_installed_options())

def print_sys_config(dev):
    print "RF input/output port: %s" % dev.ask_io_used()

def print_man_config(dev):
    print "Manual BTS test - Synchronized mode (no signaling)"
    print "  CCCH ARFCN:       %s" % format_int(dev.ask_bts_ccch_arfcn())
    print "  TCH ARFCN:        %s" % format_int(dev.ask_bts_tch_arfcn())
    print "  TCH timeslot:     %s" % format_int(dev.ask_bts_tch_ts())
    print "  Expected power:   %s dBm" % format_float(dev.ask_bts_expected_power())
    print "  Used TS power:    %s dBm" % format_float(dev.ask_bts_tch_tx_power())
    print "  Mode:             %s" % dev.ask_bts_tch_mode()
    print "  Timing advance:   %s qbits" % format_int(dev.ask_bts_tch_timing())
    print "  Input bandwidth:  %s" % dev.ask_bts_tch_input_bandwidth()

def print_man_bidl_info(dev):
    print "Manual BTS test - Synchronized mode (no signaling)"
    print "  Peak power:         %s dBm" % format_float(dev.ask_peak_power())

def print_man_bbch_info(dev):
    print "Manual BTS test - Synchronized mode (no signaling)"
    print "  MCC:              %d" % dev.ask_bts_mcc()
    print "  MNC:              %d" % dev.ask_bts_mcc()
    print "  BSIC:             %d" % dev.ask_bts_bsic()
    print "  burst avg power:  %d dBm" % dev.ask_burst_power_avg()

def print_man_btch_info(dev):
    print_mod_info(dev)

def update_man_btch_info(dev):
    update_mod_info(dev)

def print_mod_config(dev):
    rf_in_num = dev.parse_io_str(dev.ask_io_used())[0]
    print "Module test - Burst Analysis configuration"
    print "  Expected power:     %f dBm" % dev.ask_ban_expected_power()
    print "  RF Channel:         %d" % dev.ask_ban_arfcn()
    print "  Training sequence:  %d" % dev.ask_ban_tsc()
    print "  Decode:             %s" % dev.ask_phase_decoding_mode()
    if rf_in_num == 1:
        print "  Peak power bandw:   %s" % dev.ask_ban_input_bandwidth()
    print "  Trigger mode:       %s" % dev.ask_ban_trigger_mode()
    print "  Used RF Input:      %d" % rf_in_num
    if rf_in_num == 1:
        print "  Ext atten RF In1:   %f" % dev.ask_ext_att_rf_in1()
    else:
        print "  Ext atten RF In2:   %f" % dev.ask_ext_att_rf_in2()

def print_mod_info(dev, update=False):
    if update:
        dev.ask_burst_power_avg()
    (pk_phase_err_match, avg_phase_err_match, freq_err_match) = dev.ask_phase_freq_match()
    print "Module test - Burst Analysis measurements"
    print "  Peak power:         %s dBm" % format_float(dev.ask_peak_power())
    print "  Avg. burst power:   %s dBm" % format_float(dev.fetch_burst_power_avg())
    print "  Power ramp:         %s" % dev.ask_power_mask_match()
    print "  Frequency error:    %s Hz  (%s)" % (format_int(dev.fetch_freq_err()), freq_err_match)
    print "  Phase Error (PK):   %s deg (%s)" % (format_float(dev.fetch_phase_err_pk()), pk_phase_err_match)
    print "  Phase Error (AVG):  %s deg (%s)" % (format_float(dev.fetch_phase_err_rms()), avg_phase_err_match)
    print "Module test - Extra measurements"
    print "  Spectrum modulation: %s" % dev.ask_spectrum_modulation_match()
    print "  Spectrum switching:  %s" % dev.ask_spectrum_switching_match()

def print_ber_test_settings(dev):
    power_ts_unused = dev.ask_ber_unused_ts_power()
    print "BER Test %d settings:" % dev.ask_ber_test_num()
    print "  Used TS power:      %.1f dBm" % dev.ask_ber_used_ts_power()
    print "  Unused TS power:    %s dB" % ("OFF" if power_ts_unused is None else ("%.1f"%power_ts_unused),)
    print "  Frames to send:     %d" % dev.ask_ber_frames_num()
    print "  Test time:          %.1f s" % dev.ask_ber_max_test_time()
    print "  Abort condition:    %s" % dev.ask_ber_abort_cond()
    print "  Hold-off time:      %.1f s" % dev.ask_ber_holdoff_time()
    print "                Tolerance      Total"
    print "  Class Ib         %6d     %6d"    % (dev.ask_ber_limit_class_1b(), dev.ask_ber_max_class_1b_samples())
    print "  Class II         %6d     %6d"    % (dev.ask_ber_limit_class_2(), dev.ask_ber_max_class_2_samples())
    print "  Erased Frames    %6d     %6d"    % (dev.ask_ber_limit_erased_frames(), dev.ask_ber_max_erased_frames_samples())

def print_ber_test_result(dev, update=False):
    if update:
        res = dev.read_ber_test_result()
    else:
        res = dev.fetch_ber_test_result()
    print "BER Test result:"
    print "  Test result:           %s"    % res
    if res in ["PASS", "FAIL"]:
        (ber1b_events, ber1b_ber, ber1b_rber) = (dev.fetch_ber_class_1b_events(), dev.fetch_ber_class_1b_ber(), dev.fetch_ber_class_1b_rber())
        (ber2_events, ber2_ber, ber2_rber) = (dev.fetch_ber_class_2_events(), dev.fetch_ber_class_2_ber(), dev.fetch_ber_class_2_rber())
        (fer_events, fer_percent) = (dev.fetch_ber_erased_events(), dev.fetch_ber_erased_fer())
        crc_errors = dev.fetch_ber_crc_errors()
        print "                events    BER       RBER"
        print "  Class Ib      %6d  %7.3f%%  %7.3f%%"    % (ber1b_events, ber1b_ber, ber1b_rber)
        print "  Class II      %6d  %7.3f%%  %7.3f%%"    % (ber2_events, ber2_ber, ber2_rber)
        print "                events    FER"
        print "  Erased Frames %6d  %7.3f%%"             % (fer_events, fer_percent)
        print "  CRC errors:   %6d"                   % crc_errors


def print_cur_mode(dev):
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

    dev.configure_man(ccch_arfcn=100, tch_arfcn=100, tch_ts=2, tsc=7, expected_power=37, tch_tx_power=-50, tch_mode='LOOP', tch_timing=0)
    dev.configure_mod(expected_power=37, arfcn=100, tsc=7, decode='STANdard', input_bandwidth='NARRow', trigger_mode='POWer')
    dev.configure_spectrum_modulation_mask_rel(43) # most strict spectrum mask

    print_sys_info(dev)
    print_sys_config(dev)
    print_man_config(dev)
    print_mod_config(dev)
    print_cur_mode(dev)

    print
    print "Expecting your input now"

