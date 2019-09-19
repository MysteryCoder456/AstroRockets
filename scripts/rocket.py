import pygame
from math import sin, cos, radians


class Rocket:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.x_vel = 0
		self.y_vel = 0
		self.drift_heading = 0
		self.heading = 0
		self.speed = 0

		self.vertex_distance = 28
		self.rear_vertex_angle = 137
		self.vertices = [(self.vertex_distance, 0), (self.vertex_distance, self.rear_vertex_angle), (self.vertex_distance, -self.rear_vertex_angle)] # Polar coordinates

		self.color = color
		self.collider_size = 28

	def render(self, window):
		v = self.vertices

		# Convert polar coordinates to cartesian coordinates
		x1 = cos(radians(v[0][1])) * v[0][0] + self.x
		y1 = sin(radians(v[0][1])) * v[0][0] + self.y

		x2 = cos(radians(v[1][1])) * v[1][0] + self.x
		y2 = sin(radians(v[1][1])) * v[1][0] + self.y

		x3 = cos(radians(v[2][1])) * v[2][0] + self.x
		y3 = sin(radians(v[2][1])) * v[2][0] + self.y

		# Store cartesian coordinates in list so pygame can read them in polygon()
		v_list = [(x1, y1), (x2, y2), (x3, y3)]

		pygame.draw.polygon(window, self.color, v_list)

	def update(self):
		# Acceleration
		self.x_vel = cos(radians(self.heading)) * self.speed
		self.y_vel = sin(radians(self.heading)) * self.speed

		# Movement
		self.x += self.x_vel
		self.y += self.y_vel

		self.vertices = [(self.vertex_distance, self.drift_heading), (self.vertex_distance, self.rear_vertex_angle+self.drift_heading), (self.vertex_distance, -self.rear_vertex_angle+self.drift_heading)]
