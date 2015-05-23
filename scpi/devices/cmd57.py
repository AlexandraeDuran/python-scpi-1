"""ROHDE&SCHWARZ CMD57 specific device implementation and helpers"""

from scpi import scpi_device

class cmd57(scpi_device):
    """Adds the ROHDE&SCHWARZ CMD57 specific SCPI commands as methods"""

    def __init__(self, transport, *args, **kwargs):
        """Initializes a device for the given transport"""
        super(cmd57, self).__init__(transport, *args, **kwargs)
        self.scpi.command_timeout = 1.5 # Seconds
        self.scpi.ask_default_wait = 0 # Seconds

    def ask_installed_options(self):
        """ List installed option """
        return self.scpi.ask_str("*OPT?")

    def ask_io_used(self):
        """ Inputs and outputs used """
        return self.scpi.ask_str("ROUT:IOC?")

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

