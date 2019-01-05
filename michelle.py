#!/usr/bin/env python3

import functools
import threading

import anki_vector
from anki_vector.events import Events
from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes
from anki_vector.util import degrees


def main():
    evt = threading.Event()

    def on_object_appeared(robot, event_type, event):
        print(f"--------- Vector started seeing an object --------- \n{event.obj}")

        robot.say_text("hello")

    def on_object_disappeared(robot, event_type, event):
        print(f"--------- Vector stopped seeing an object --------- \n{event.obj}")
            
        robot.say_text("goodbye")

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial,
                           default_logging=False,
                           show_viewer=True,
                           show_3d_viewer=True,
                           enable_camera_feed=True,
                           enable_custom_object_detection=True,
                           enable_nav_map_feed=True) as robot:
        # If necessary, move Vector's Head and Lift to make it easy to see his face
        robot.behavior.set_head_angle(degrees(45.0))
        robot.behavior.set_lift_height(0.0)

        on_object_appeared = functools.partial(on_object_appeared, robot)
        robot.events.subscribe(on_object_appeared, Events.object_appeared)

        on_object_disappeared = functools.partial(on_object_disappeared, robot)
        robot.events.subscribe(on_object_disappeared, Events.object_disappeared)


        #cube_obj = robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType00,
        #                                          marker=CustomObjectMarkers.Circles2,
        #                                          size_mm=44.0,
        #                                          marker_width_mm=50.0,
        #                                          marker_height_mm=50.0,
        #                                          is_unique=True)

        cube_obj = robot.world.define_custom_wall(custom_object_type=CustomObjectTypes.CustomType00,
                                                  marker=CustomObjectMarkers.Circles2,
                                                  width_mm=70,
                                                  height_mm=100,
                                                  marker_width_mm=52.0,
                                                  marker_height_mm=52.0,
                                                  is_unique=True)



        if (cube_obj is not None):
            print("All objects defined successfully!")
        else:
            print("One or more object definitions failed!")
            return


        try:
            if not evt.wait(timeout=30):
                print("\n\nShow a marker specified in the Python script to Vector and you will see the related 3d objects\n"
                      "display in Vector's 3d_viewer window. You will also see messages print every time a custom object\n"
                      "enters or exits Vector's view. Markers can be found from the docs under CustomObjectMarkers.\n\n")
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
