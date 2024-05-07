#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import numpy as np
import math
from npid import nPID

ex = 0
ew = 0
eAx = 0
d_ex = 0
i_ex = 0
etax = 0
ey = 0
eAy = 0
d_ey = 0
i_ey = 0
etay = 0
t = 1
d = 0.08
neurona_x = nPID(3,0.5)
neurona_y = nPID(3,0.3)

def Callback(msg_in):
		global ex			# Error en x
		global eAx 			# Error en x anterior
		global d_ex			# derivada error en x
		global i_ex			# integral error x
		global ey 			# Error en y			
		global eAy			# Error en y anterior
		global t			# tiempo
		global d_ey			# derivada error y
		global i_ey			# integral error y
		global d			# Distancia
		
		# Consigue la posicion en coordenadas x.y.
		x = msg_in.pose.pose.position.x		
		y = msg_in.pose.pose.position.y

		# Orientacion?, quaterniones
		quater = np.zeros(4)
		quater[0] = msg_in.pose.pose.orientation.w		# tetha
		quater[1] = msg_in.pose.pose.orientation.x		# x
		quater[2] = msg_in.pose.pose.orientation.y		# y
		quater[3] = msg_in.pose.pose.orientation.z		# z?, dron?

		theta = math.atan2(2*(quater[0]*quater[3]+quater[1]*quater[2]),1-2*(quater[2]*quater[2]+quater[3]*quater[3]))
		
		xd = 3.0
		yd = 3.0
		
		# Velocdad lineal
		xp = x + d*math.cos(theta)
		yp = y + d*math.sin(theta)
		
		# Error lineal
		ex = xd - xp
		ey = yd - yp
		

		# Control
		i_ex = (i_ex + ex)*(1/t)
		d_ex = ex - eAx
		eAx = ex
		error_x = np.array([ex,i_ex,d_ex])
		
		i_ey = (i_ey + ey)*(1/t)
		d_ey = ey - eAy
		eAy = ey
		error_y = np.array([ey,i_ey,d_ey])
		
		
		kx = neurona_x.control_u(error_x)
		neurona_x.fit(ex,error_x)
		
		ky = neurona_y.control_u(error_y)
		neurona_y.fit(ey,error_y,0.03)
		
		errores = np.array([kx,ky])
		
		matriz_modelo = np.array([[np.cos(theta),-d*np.sin(theta)],[np.sin(theta),d*np.cos(theta)]])
		u = np.dot(np.linalg.inv(matriz_modelo),np.array([kx,ky]))
		
		print(u)
		
		
		msg = Twist()
		msg.linear.x = u[0]
		msg.linear.y = 0.0
		msg.linear.z = 0.0
		msg.angular.x = 0.0
		msg.angular.y = 0.0
		msg.angular.z = u[1]
		
		if ex < 0.01 and ey < 0.01:
			msg.linear.x = 0
			msg.angular.z = 0
			pub.publish(msg)
			rospy.spin()
		
		t = t+1
		
		pub.publish(msg)
		print('x=',x,' y=',y)

	
rospy.init_node('control_py', anonymous=True)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10) # 10hz

rospy.Subscriber("/odom", Odometry, Callback)
rospy.spin()
