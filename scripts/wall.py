import pygame


class Wall:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
		self.color = (25, 213, 194)
		self.line_width = 5

	def render(self, window):
		pygame.draw.line(window, self.color, (self.x, self.y), (self.x + self.width, self.y), self.line_width)
		pygame.draw.line(window, self.color, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), self.line_width)
		pygame.draw.line(window, self.color, (self.x + self.width, self.y + self.height), (self.x, self.y + self.height), self.line_width)
		pygame.draw.line(window, self.color, (self.x, self.y + self.height), (self.x, self.y), self.line_width)
