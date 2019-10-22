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
		self.radius = 10
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
