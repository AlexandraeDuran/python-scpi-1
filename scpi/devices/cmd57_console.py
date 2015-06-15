"""ROHDE&SCHWARZ CMD57 specific device implementation and helpers"""

from scpi.devices import cmd57

def format_int(val):
    if val is None: return "nan"
    else: return "%6d" % val

def format_float(val):
    return "%6.2f" % val

class cmd57_console(cmd57.cmd57):
    """ROHDE&SCHWARZ CMD57 specific class with console output"""

    def __init__(self, transport, *args, **kwargs):
        """Initializes a device for the given transport"""
        super(cmd57_console, self).__init__(transport, *args, **kwargs)

    def print_sys_info(self):
        print "System version:       %s" % " ".join(self.identify())
        print "Installed options:    %s" % " ".join(self.ask_installed_options())

    def print_sys_config(self):
        print "RF input/output port: %s" % self.ask_io_used()

    def print_man_config(self):
        print "Manual BTS test - Synchronized mode (no signaling)"
        print "  CCCH ARFCN:       %s" % format_int(self.ask_bts_ccch_arfcn())
        print "  TCH ARFCN:        %s" % format_int(self.ask_bts_tch_arfcn())
        print "  TCH timeslot:     %s" % format_int(self.ask_bts_tch_ts())
        print "  Expected power:   %s dBm" % format_float(self.ask_bts_expected_power())
        print "  Used TS power:    %s dBm" % format_float(self.ask_bts_tch_tx_power())
        print "  Mode:             %s" % self.ask_bts_tch_mode()
        print "  Timing advance:   %s qbits" % format_int(self.ask_bts_tch_timing())
        print "  Input bandwidth:  %s" % self.ask_bts_tch_input_bandwidth()

    def print_man_bidl_info(self):
        print "Manual BTS test - Synchronized mode (no signaling)"
        print "  Peak power:         %s dBm" % format_float(self.ask_peak_power())

    def print_man_bbch_info(self):
        print "Manual BTS test - Synchronized mode (no signaling)"
        print "  MCC:              %d" % self.ask_bts_mcc()
        print "  MNC:              %d" % self.ask_bts_mcc()
        print "  BSIC:             %d" % self.ask_bts_bsic()
        print "  burst avg power:  %d dBm" % self.ask_burst_power_avg()

    def print_man_bbch_info(self, update=False):
        if (update):
            freq_err = self.ask_freq_err()
        else:
            freq_err = self.fetch_freq_err()
        (pk_phase_err_match, avg_phase_err_match, freq_err_match) = self.ask_phase_freq_match()
        print "Manual test - Control Channel"
        print "  RF channel:           %d" % self.ask_bts_ccch_arfcn()
        print "    Frequency error:    %s Hz  (%s)" % (format_int(freq_err), freq_err_match)
        print "    Phase Error (PK):   %s deg (%s)" % (format_float(self.fetch_phase_err_pk()), pk_phase_err_match)
        print "    Phase Error (AVG):  %s deg (%s)" % (format_float(self.fetch_phase_err_rms()), avg_phase_err_match)
        print "  BTS power:            %s dBm" % format_float(self.ask_peak_power())
        #TODO: print network information

    def print_man_btch_info(self, update=False):
        self.print_mod_info(update)

    def print_man_phase_freq_info(self, update=False):
        print "TCH Burst Phase/Frequency:"
        if update:
            err_arr = self.ask_phase_err_arr()
            freq_err = self.ask_freq_err()
        else:
            err_arr = self.fetch_phase_err_arr()
            freq_err = self.fetch_freq_err()
        (pk_phase_err_match, avg_phase_err_match, freq_err_match) = self.ask_phase_freq_match()
        print "  TCH channel:          %d" % self.ask_bts_tch_arfcn()
        print "    Frequency error:    %s Hz  (%s)" % (format_int(freq_err), freq_err_match)
        print "    Phase Error (PK):   %s deg (%s)" % (format_float(self.fetch_phase_err_pk()), pk_phase_err_match)
        print "    Phase Error (AVG):  %s deg (%s)" % (format_float(self.fetch_phase_err_rms()), avg_phase_err_match)
        print "  Burst phase error:    ", err_arr

    def print_man_power(self, update=False):
        if update:
            avg_power = self.ask_burst_power_avg()
            power_arr = self.ask_burst_power_arr()
        else:
            avg_power = self.fetch_burst_power_avg()
            power_arr = self.fetch_burst_power_arr()
        print "Burst Power mask measurements"
        print "  Peak power:         %s dBm" % format_float(self.ask_peak_power())
        print "  Avg. burst power:   %s dBm" % format_float(avg_power)
        print "  Power ramp:         %s" % self.ask_power_mask_match()
        print "  Power (q-bits):     ", power_arr

    def print_man_spectrum_modulation(self, update=False):
        print "Spectrum due to Modulation:"
        print "  Absolute tolerance mask (dBm):          ", self.ask_spectrum_modulation_tolerance_abs()
        print "  Relative tolerance mask (dBc):          ", self.ask_spectrum_modulation_tolerance_rel()
        print "  Measurement offsets (kHz):              ", self.fetch_spectrum_modulation_offsets()
        if update:
            spectrum = self.ask_spectrum_modulation()
        else:
            spectrum = self.fetch_spectrum_modulation()
        print "  Measured values (dBc):                  ", spectrum
        print "  Mask match?                             ", self.ask_spectrum_modulation_match()

    def print_man_spectrum_switching(self, update=False):
        print "Spectrum due to Switching:"
        print "  Absolute tolerance mask (dBm):          ", self.ask_spectrum_switching_tolerance_abs()
        print "  Relative tolerance mask (dBc):          ", self.ask_spectrum_switching_tolerance_rel()
        print "  Measurement offsets (kHz):              ", self.fetch_spectrum_switching_offsets()
        if update:
            spectrum = self.ask_spectrum_switching()
        else:
            spectrum = self.fetch_spectrum_switching()
        print "  Measured values (dBc):                  ", spectrum
        print "  Mask match?                             ", self.ask_spectrum_switching_match()

    def print_mod_config(self):
        rf_in_num = self.parse_io_str(self.ask_io_used())[0]
        print "Module test - Burst Analysis configuration"
        print "  Expected power:     %f dBm" % self.ask_ban_expected_power()
        print "  RF Channel:         %d" % self.ask_ban_arfcn()
        print "  Training sequence:  %d" % self.ask_ban_tsc()
        print "  Decode:             %s" % self.ask_phase_decoding_mode()
        if rf_in_num == 1:
            print "  Peak power bandw:   %s" % self.ask_ban_input_bandwidth()
        print "  Trigger mode:       %s" % self.ask_ban_trigger_mode()
        print "  Used RF Input:      %d" % rf_in_num
        if rf_in_num == 1:
            print "  Ext atten RF In1:   %f" % self.ask_ext_att_rf_in1()
        else:
            print "  Ext atten RF In2:   %f" % self.ask_ext_att_rf_in2()

    def print_mod_info(self, update=False):
        if update:
            self.ask_burst_power_avg()
        (pk_phase_err_match, avg_phase_err_match, freq_err_match) = self.ask_phase_freq_match()
        print "Module test - Burst Analysis measurements"
        print "  Peak power:         %s dBm" % format_float(self.ask_peak_power())
        print "  Avg. burst power:   %s dBm" % format_float(self.fetch_burst_power_avg())
        print "  Power ramp:         %s" % self.ask_power_mask_match()
        print "  Frequency error:    %s Hz  (%s)" % (format_int(self.fetch_freq_err()), freq_err_match)
        print "  Phase Error (PK):   %s deg (%s)" % (format_float(self.fetch_phase_err_pk()), pk_phase_err_match)
        print "  Phase Error (AVG):  %s deg (%s)" % (format_float(self.fetch_phase_err_rms()), avg_phase_err_match)

    def print_ber_test_settings(self):
        power_ts_unused = self.ask_ber_unused_ts_power()
        print "BER Test %d settings:" % self.ask_ber_test_num()
        print "  Used TS power:      %.1f dBm" % self.ask_ber_used_ts_power()
        print "  Unused TS power:    %s dB" % ("OFF" if power_ts_unused is None else ("%.1f"%power_ts_unused),)
        print "  Frames to send:     %d" % self.ask_ber_frames_num()
        print "  Test time:          %.1f s" % self.ask_ber_max_test_time()
        print "  Abort condition:    %s" % self.ask_ber_abort_cond()
        print "  Hold-off time:      %.1f s" % self.ask_ber_holdoff_time()
        print "                Tolerance      Total"
        print "  Class Ib         %6d     %6d"    % (self.ask_ber_limit_class_1b(), self.ask_ber_max_class_1b_samples())
        print "  Class II         %6d     %6d"    % (self.ask_ber_limit_class_2(), self.ask_ber_max_class_2_samples())
        print "  Erased Frames    %6d     %6d"    % (self.ask_ber_limit_erased_frames(), self.ask_ber_max_erased_frames_samples())

    def print_ber_test_result(self, update=False):
        if update:
            res = self.read_ber_test_result()
        else:
            res = self.fetch_ber_test_result()
        print "BER Test result:"
        print "  Test result:           %s"    % res
        if res in ["PASS", "FAIL"]:
            (ber1b_events, ber1b_ber, ber1b_rber) = (self.fetch_ber_class_1b_events(), self.fetch_ber_class_1b_ber(), self.fetch_ber_class_1b_rber())
            (ber2_events, ber2_ber, ber2_rber) = (self.fetch_ber_class_2_events(), self.fetch_ber_class_2_ber(), self.fetch_ber_class_2_rber())
            (fer_events, fer_percent) = (self.fetch_ber_erased_events(), self.fetch_ber_erased_fer())
            crc_errors = self.fetch_ber_crc_errors()
            print "                events    BER       RBER"
            print "  Class Ib      %6d  %7.3f%%  %7.3f%%"    % (ber1b_events, ber1b_ber, ber1b_rber)
            print "  Class II      %6d  %7.3f%%  %7.3f%%"    % (ber2_events, ber2_ber, ber2_rber)
            print "                events    FER"
            print "  Erased Frames %6d  %7.3f%%"             % (fer_events, fer_percent)
            print "  CRC errors:   %6d"                   % crc_errors


    def print_cur_mode(self):
        print "Current test mode:    %s" % self.ask_test_mode()
        print "Current device state: %s" % self.ask_dev_state()

def rs232(port, **kwargs):
    return cmd57_console(cmd57.rs232(port, **kwargs))
