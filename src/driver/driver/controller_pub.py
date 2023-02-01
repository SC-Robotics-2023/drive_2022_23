import rclpy
from rclpy.node import Node
# from calibrate import *
from . import gamepad_input as gmi
import subprocess
from std_msgs.msg import Float64MultiArray


AXIS_DEADZONE = 0.3 # Deadzone is 0 to 1 | Note: axis value will be 0 until you move past the deadzone





class Buttons:
    def north():
        print("North")

    def west():
        print("West")

    def south():
        print("South")
        # gmi.rumbleAll(0, 0.3, 100)

    def east():
        print("East")

    def share():
        print("Share")

    def options():
        print("Options")

    def home():
        print("Home")

    def l1():
        print("L1")

    def r1():
        print("R1")

    def l3():
        print("L3")

    def r3():
        print("R3")


    # Button UP callbacks
    def northUp():
        ...

    def westUp():
        ...

    def southUp():
        ...

    def eastUp():
        ...

    def shareUp():
        ...

    def optionsUp():
        ...

    def homeUp():
        ...

    def l1Up():
        ...

    def r1Up():
        ...

    def l3Up():
        ...

    def r3Up():
        ...


    # Hat callbacks
    def hatNorth():
        ...

    def hatSouth():
        ...

    def hatWest():
        print("🦽 Going backwards!! 🦽")

    def hatEast():
        print("💨 Ramp up Speed!! 💨")

    def hatCentered():
        ...


    # Connection callbacks
    def onGamepadConnect():
        ...

    def onGamepadDisconnect():
        ...


class ControllerPub(Node):
    def __init__(self):
        super().__init__('controller_pub')

        self.publisher_ = self.create_publisher(Float64MultiArray, 'controls', 10)

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        b = Buttons()

        self.buttonDownEvents = [
            b.north, b.west, b.south, b.east,
            b.share, b.options, b.home,                       
            b.l1, b.r1, b.l3, b.r3]
        self.buttonUpEvents = [
            b.northUp, b.westUp, b.southUp, b.eastUp, 
            b.shareUp, b.optionsUp, b.homeUp, 
            b.l1Up, b.r1Up, b.l3Up, b.r3Up]

        self.hatEvents = [b.hatNorth, b.hatWest, b.hatSouth, b.hatEast]

        self.connectionEvents = [b.onGamepadConnect, b.onGamepadDisconnect]

        gmi.run_event_loop(self.buttonDownEvents, self.buttonUpEvents, self.hatEvents, self.connectionEvents)   # Async loop to handle gamepad button events
 

    def timer_callback(self):
        gp = gmi.getGamepad(0)
        msg = Float64MultiArray()

        (ls_x, ls_y) = gmi.getLeftStick(gp, AXIS_DEADZONE)  # Get left stick
        (rs_x, rs_y) = gmi.getRightStick(gp, AXIS_DEADZONE) # Get right stick
        (l2, r2) = gmi.getTriggers(gp, AXIS_DEADZONE)       # Get triggers
        (hat_x, hat_y) = gmi.getHat(gp)                     # Get hat

        msg.data = [ls_x, ls_y, rs_x, rs_y, l2, r2, hat_x, hat_y]

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    controller_pub = ControllerPub()

    rclpy.spin(controller_pub)

    controller_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()