from mycroft import MycroftSkill, intent_handler


class CpuTemperature(MycroftSkill):
    """ Speak the CPU temperature.

    The temperature value is obtained from thermal_zone0 temp file at
    /sys/class/thermal/thermal_zone0/temp

    The user can set the temperature unit to Celsius or Fahrenheit on the
    user's Mycroft account skill configuration page.
    """
    
    def __init__(self):
        MycroftSkill.__init__(self)
        

    @intent_handler('temperature.cpu.intent')
    def handle_temperature_cpu(self, message):
        """Open and read temp file.

        File contains a string that is the CPU temperature in Celsius
        read to the thousandths place with no decimal.
        """
        try:
            with open ('/sys/class/thermal/thermal_zone0/temp') as f:
                cputempraw = f.read()
        except:
            self.log.error("File not found error.")
            self.speak("Error. I could not find the temperature file.")
        else:
            # Retrieve the temperature unit that was set by user from settings.json file. Default is Celsius.
            unit_setting = self.settings.get('degree_unit', 'c')

            if unit_setting == 'c':
                # Format and speak temperature in celsius.
                cputempC = int(cputempraw) // 1000
                cputempC = str(cputempC)
                self.speak_dialog('temperature.cpu', {'cputemp': cputempC, 'unit': 'celsius'})
            if unit_setting == 'f':
                # Format, convert to fahrenheit, and speak temperature.
                cputempF = int(cputempraw) // 1000
                cputempF = int((cputempF * 1.8) + 32)
                cputempF = str(cputempF)
                self.speak_dialog('temperature.cpu', {'cputemp': cputempF, 'unit': 'fahrenheit'}) 

def create_skill():
    return CpuTemperature()

