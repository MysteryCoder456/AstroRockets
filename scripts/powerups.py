"""
Produced by Rehatbir Singh(MysteryCoder456)
Contact at rehatbir.singh@gmail.com for any questions
Full Rights Reserved under MIT License
"""

import pygame


# Base Class for PowerUps
class PowerUp:
	def __init__(self, x, y):
		self.id = 0

		self.x = x
		self.y = y
		self.radius = 12
		self.color = (255, 255, 255)
		self.draw_x = self.x - self.radius
		self.draw_y = self.y - self.radius

	def render(self, window):
		pygame.draw.ellipse(window, self.color, (self.draw_x, self.draw_y, self.radius * 2, self.radius * 2))


# Subclasses of PowerUp base class (Arranged by ID number)

class ScatterShot(PowerUp):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.id = 1
		self.color = (30, 230, 209)


class Missile(PowerUp):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.id = 2
		self.color = (149, 0, 2)
		self.inner_color = (251, 251, 251)
		self.inner_radius = self.radius / 2

	def render(self, window):
		pygame.draw.ellipse(window, self.color, (self.draw_x, self.draw_y, self.radius * 2, self.radius * 2))
		pygame.draw.ellipse(window, self.inner_color, (self.x - self.inner_radius, self.y - self.inner_radius, self.inner_radius * 2, self.inner_radius * 2))
