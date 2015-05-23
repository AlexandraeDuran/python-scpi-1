"""ROHDE&SCHWARZ CMD57 specific device implementation and helpers"""

from scpi import scpi_device

class cmd57(scpi_device):
    """Adds the ROHDE&SCHWARZ CMD57 specific SCPI commands as methods"""

    def __init__(self, transport, *args, **kwargs):
        """Initializes a device for the given transport"""
        super(cmd57, self).__init__(transport, *args, **kwargs)
        self.scpi.command_timeout = 1.5 # Seconds
        self.scpi.ask_default_wait = 0 # Seconds

    ######################################
    ###   Low level functions
    ######################################

    def ask_installed_options(self):
        """ List installed option """
        return self.scpi.ask_str_list("*OPT?")

    def ask_io_used(self):
        """ 2.1 Inputs and outputs used """
        return self.scpi.ask_str("ROUT:IOC?")

    def ask_bts_mcc(self):
        """ 2.2.1 Detected BTS MCC """
        return self.scpi.ask_int("SENSE:SIGN:IDEN:MCC?")

    def ask_bts_mnc(self):
        """ 2.2.1 Detected BTS MNC """
        return self.scpi.ask_int("SENSE:SIGN:IDEN:MNC?")

    def ask_bts_bsic(self):
        """ 2.2.1 Detected BTS BSIC """
        return self.scpi.ask_int("SENSE:SIGN:BSIC?")

    def ask_bts_ccch_arfcn(self):
        """ 2.2.2 Configured CCCH ARFCN """
        return self.scpi.ask_int("CONF:CHAN:BTS:CCCH:ARFCN?")

    def set_bts_ccch_arfcn(self, arfcn):
        """ 2.2.2 Configure CCCH ARFCN """
        return self.scpi.send_command("CONF:CHAN:BTS:CCCH:ARFCN %d"%int(arfcn), False)

    def ask_bts_tch_arfcn(self):
        """ 2.2.2 Configured TCH ARFCN """
        return self.scpi.ask_int("CONF:CHAN:BTS:TCH:ARFCN?")

    def set_bts_tch_arfcn(self, arfcn):
        """ 2.2.2 Configure TCH ARFCN """
        return self.scpi.send_command("CONF:CHAN:BTS:TCH:ARFCN %d"%int(arfcn), False)

    def ask_bts_tch_ts(self):
        """ 2.2.2 Configured TCH timeslot """
        return self.scpi.ask_int("CONF:CHAN:BTS:TCH:SLOT?")

    def set_bts_tch_ts(self, slot):
        """ 2.2.2 Configure TCH timeslot """
        return self.scpi.send_command("CONF:CHAN:BTS:TCH:SLOT %d"%int(slot), False)

    def ask_bts_tsc(self):
        """ 2.2.2 Configured BTS TSC """
        return self.scpi.ask_int("CONF:CHAN:BTS:TSC?")

    def set_bts_tsc(self, tsc):
        """ 2.2.2 Configure BTS TSC """
        return self.scpi.send_command("CONF:CHAN:BTS:TSC %d"%int(tsc), False)

    def ask_ban_tsc(self):
        """ 2.3 Burst Analysis (Module testing) TSC """
        return self.scpi.ask_int("CONF:CHAN:BANalysis:TSC?")

    def set_ban_tsc(self, tsc):
        """ 2.3 Burst Analysis (Module testing) TSC """
        return self.scpi.send_command("CONF:CHAN:BANalysis:TSC %d"%int(tsc), False)

    def ask_test_mode(self):
        """ 2.4 Test mode
            See set_test_mode() for the list of supported modes
        """
        return self.scpi.ask_str("PROCedure:SEL?")

    def set_test_mode(self, mode):
        """ 2.4 Test mode
            Supported modes:
              NONE        - No tes mode (switch on state)
              MANual      - BTS test aka signaling test
              MODultest   - Module test (same as BAN?)
              BANalysis   - Burst analysis (same as MOD?)
              RFM         - RF generator (same as RFG?)
              RFGenerator - RF generator (same as RFM?)
              IQSPec      - IQ spectrum (requires hardware option)
        """
        return self.scpi.send_command("PROCedure:SEL %s"%str(mode), False)

    def bcch_sync(self):
        """ 3 Perform Synchronization with BCCH or Wired Sync """
        # TODO: Introduce longer timeout
        return self.scpi.send_command("PROCedure:SYNChronize", False)

    def ask_sync_state(self):
        """ 3 Selected Measurement State
            See set_sync_state() for the list of supported modes
        """
        return self.scpi.ask_str("PROCedure:BTSState?")

    def set_sync_state(self, state):
        """ 3 Selecting Measurement State
            Supported states:
              BIDL      - Idle
              BBCH      - BCCH measurements
              BTCH      - TCH measurements
              BEXTernal - BER measurements with RS232 / IEEE488
        """
        return self.scpi.send_command("PROCedure:BTSState %s"%str(state), False)

    def ask_peak_power(self):
        """ 7.8 Other measurements / Peak Power Measurement (read) """
        return self.scpi.ask_int("READ:POWer?")

    def fetch_peak_power(self):
        """ 7.8 Other measurements / Peak Power Measurement (fetch) """
        return self.scpi.ask_int("FETCh:POWer?")

    def ask_dev_state(self):
        """ 9.1 Current Device State """
        return self.scpi.ask_str("STATus:DEVice?")

    ######################################
    ###   High level functions
    ######################################



def rs232(port, **kwargs):
    """Quick helper to connect via RS232 port"""
    import serial as pyserial
    from scpi.transports import rs232 as serial_transport

    # Try opening at 2400 baud (default setting) and switch to 9600 baud
    serial_port = pyserial.Serial(port, 2400, timeout=0, **kwargs)
    transport = serial_transport(serial_port)
    dev = cmd57(transport)
    dev.scpi.command_timeout = 0.1 # Seconds
    try:
        dev.scpi.send_command_unchecked(":SYSTem:COMMunicate:SERial:BAUD 9600", expect_response=False)
    except:
        # It's ok to fail, because we can already be at 9600
        pass
    dev.quit()

    # Now we should be safe to open at 9600 baud
    serial_port = pyserial.Serial(port, 9600, timeout=0, **kwargs)
    transport = serial_transport(serial_port)
    dev = cmd57(transport)
    # Clear error status
    dev.scpi.send_command("*CLS", expect_response=False)
    # This must be excessive, but check that we're actually at 9600 baud
    ret = dev.scpi.ask_int(":SYSTem:COMMunicate:SERial:BAUD?")
    if ret != 9600:
       raise Exception("Can't switch to 9600 baud!")

    return dev

