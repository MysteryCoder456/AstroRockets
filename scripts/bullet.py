import pygame
from math import radians, cos, sin


class Bullet:
	def __init__(self, x, y, hdg, color):
		self.x = x
		self.y = y
		self.radius = 8
		self.draw_x = self.x - self.radius
		self.draw_y = self.y - self.radius
		self.heading = hdg
		self.speed = 10
		self.x_vel = 0
		self.y_vel = 0
		self.color = color
		self.despawn_timer = 0

	def render(self, window):
		pygame.draw.ellipse(window, self.color, (self.draw_x, self.draw_y, self.radius * 2, self.radius * 2))

	def update(self):
		self.x_vel = cos(radians(self.heading)) * self.speed
		self.y_vel = sin(radians(self.heading)) * self.speed

		self.x += self.x_vel
		self.y += self.y_vel

		self.draw_x = self.x - self.radius
		self.draw_y = self.y - self.radius

		self.despawn_timer += 1
