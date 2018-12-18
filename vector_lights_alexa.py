#!/usr/bin/python3

#
# This script is based off the example Anki SDK programs. 
# If I did anything incorrect with the licensing below, please let me know.
# --Shaun Miller
#

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import anki_vector      # For Anki Vector API calls
import time             # For sleeping...not to my liking
import re               # For regular expressions

#
# Upon running this script, Vector will do 3 things:
# 1.  Turn the lights off
# 2.  Tell you his battery status
# 3.  Turn the lights back on
#
# Vector is talking to a full fledge Amazon Echo, and not using his built in Alexa functionality.
# 
# I have several Belkin WeMo light switches in my room which I have called "Video Game Lights".
# Thus a human can say "Alexa, video game lights off" and the lights will go off. 
# But since we can tell what Vector to say, Vector can do this as well.
#
# Since the volume is a little low on Vector, sometimes Alexa will respond with wispering.
#

def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:

        robot.say_text("Alexa")
        robot.say_text("Video game lights off")

        # I would prefer a .wait_for_completed() like they have in Cozmo, but couldn't find it yet.
        # Instead just adding a little delay.
        time.sleep(1)

        robot.say_text("And now I will tell you my battery status, just because I can.")

        # We get the battery info from here.  I suspect it's some sort of JSON or other text 
        # structure.  But I'm old school, and prefer using regular expressions to parse out
        # the specific data that I want.
        battery_info_output = str(robot.get_battery_state())

        match_object_level = re.search('(battery_level)(:)(.*)', battery_info_output)
        match_object_volts = re.search('(battery_volts)(:)(.*)', battery_info_output)

        if match_object_level:
            battery_level = match_object_level.group(3)
            print ("Battery level is: " + battery_level)


        if match_object_volts:
            # The volts is returned with something like: 4.34342904890324
            # I don't really want to hear Vector rattle off that many digits right of the decimal.
            # So we round it to 2, but first we have to convert the string 4.324whatever to a float.
            volts_float = float(match_object_volts.group(3))
            volts_rounded = round(volts_float, 2)

            battery_volts = volts_rounded

            print ("Battery volts is: " + str(volts_rounded))

        # The words for the battery returned are separated by '_'.  We translate those here to spaces
        # so that Vector can read the words normally.
        battery_level_parsed = battery_level.translate(str.maketrans('_',' '))

        # Now we say what our battery status is:
        print ("My battery level is: " + battery_level_parsed + " at " + str(battery_volts) + " volts.")
        robot.say_text("My battery is " + battery_level_parsed + " at " + str(battery_volts) + " volts.")

        # I had to put a 2 second sleep statement here.  Either Vector was speaking too fast or Alexa, hering 
        # Vector chatter, is delaying responding to her name.  Basically at 1 second, Alexa wasn't responding.
        # Will hopefully not have to rely on sleep statements in the future.
        time.sleep(2)

        robot.say_text("Alexa")
        # Had to give a little padding after saying Alexa so she responds.  Not sure why I had to do this 
        # here when I didn't have to when Vector first starts speaking at the beginning of the script.
        time.sleep(0.5)
        robot.say_text("Video game lights on")
    
if __name__ == "__main__":
    main()
