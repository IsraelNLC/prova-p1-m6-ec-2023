#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class controller(Node):

    def __init__(self):
        super().__init__("controller")
        # comentar para ver a estrutura de fila
        self.subscription = self.create_subscription(Pose, "turtle1/pose", self.callback, 10)
        self.publisher = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.twist = Twist()
    
    def callback(self, msg):
        self.get_logger().info(f"Posição atual: {msg.x}, {msg.y}")
        return [msg.x, msg.y]
    
    def move(self, path):
        self.twist.linear.x = path[0]
        self.twist.angular.z = path[1]
        self.publisher.publish(self.twist)
        return self.twist


class Fila(list):
    def __init__(self, path):
        super().__init__(item for item in path)

    def append(self, arrPath):
        if arrPath.__len__() != 2 or type(arrPath[0]) != float or type(arrPath[1]) != float:
            raise ValueError("O caminho deve ser uma lista de tamanho 2 com valores float.")
        return super().append(arrPath)
    
    def pop(self):
        return super().pop(0)
    
    def __str__(self):
        return f"Caminho a ser feito: {super().__str__()}"
    
def main():
    rclpy.init()
    f = Fila([[0.5, 0.0]])
    c = controller()

    f.append([0.0, 1.0])
    f.append([0.5, 0.0])
    f.append([0.0, 1.0])
    f.append([1.0, 0.0])
    f.append([0.0, 5.0])
    f.pop()
    print(f)

    rclpy.spin(c)

    # era pra ser uma logica que sempre que chegasse em um node, desse pop no atual e fosse para o próximo
    while f.__len__() > 0:
        c.move(f.pop())

    c.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()