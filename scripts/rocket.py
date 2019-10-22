"""
Produced by Rehatbir Singh(MysteryCoder456)
Contact at rehatbir.singh@gmail.com for any questions
Full Rights Reserved under MIT License
"""

import pygame
from math import sin, cos, radians


class Rocket:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.old_x = x
		self.old_y = y
		self.x_vel = 0
		self.y_vel = 0
		self.drift_heading = 0
		self.heading = 0
		self.speed = 0

		self.vertex_distance = 28
		self.rear_vertex_angle = 137
		self.vertices = [(self.vertex_distance, 0), (self.vertex_distance, self.rear_vertex_angle), (self.vertex_distance, -self.rear_vertex_angle)] # Polar coordinates

		self.color = color
		self.collider_size = 20
		self.wall_collider = pygame.Rect(self.x - self.collider_size, self.y - self.collider_size, self.collider_size * 2, self.collider_size * 2)
		
		self.bullets = []
		self.bullet_is_shot = False
		self.shoot_timer = 0
		
		self.current_powerup = 0

	def assign_powerup(self, powerup=0):
		self.current_powerup = powerup

	def update_collider(self):
		self.wall_collider = pygame.Rect(self.x - self.collider_size, self.y - self.collider_size, self.collider_size * 2, self.collider_size * 2)

	def update_old_coords(self):
		self.old_x = self.x
		self.old_y = self.y

	def accelerate(self, speed):
		self.speed += speed
		self.heading = self.drift_heading
		# self.drift_x_vel = cos(radians(self.drift_heading)) * speed
		# self.drift_y_vel = sin(radians(self.drift_heading)) * speed
		# self.x_vel += self.drift_x_vel
		# self.y_vel += self.drift_y_vel

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
		self.shoot_timer += 1

		if self.shoot_timer > 100:
			self.bullet_is_shot = False
