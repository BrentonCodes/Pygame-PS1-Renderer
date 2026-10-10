import numpy
import pygame

class Camera:

	def __init__(self):

		self.position = numpy.array((0.0,0.5,-5.0))
		self.rotation = numpy.array((0.0,0.0,0.0))

		self.f = 571

		self.speed = 15
		self.sense = 0.001

	def update(self, timestep):

		keys = pygame.key.get_pressed()
	
		if keys[pygame.K_w]:
			self.position[0] += numpy.sin(self.rotation[1]) * self.speed * timestep
			self.position[2] += numpy.cos(self.rotation[1]) * self.speed * timestep

		if keys[pygame.K_s]:
			self.position[0] -= numpy.sin(self.rotation[1]) * self.speed * timestep
			self.position[2] -= numpy.cos(self.rotation[1]) * self.speed * timestep

		if keys[pygame.K_a]:
			self.position[0] -= numpy.cos(self.rotation[1]) * self.speed * timestep
			self.position[2] += numpy.sin(self.rotation[1]) * self.speed * timestep

		if keys[pygame.K_d]:
			self.position[0] += numpy.cos(self.rotation[1]) * self.speed * timestep
			self.position[2] -= numpy.sin(self.rotation[1]) * self.speed * timestep

		if keys[pygame.K_SPACE]:
			self.position[1] += self.speed * timestep

		if keys[pygame.K_LSHIFT]:
			self.position[1] -= self.speed * timestep

		mx, my = pygame.mouse.get_rel()

		self.rotation[1] += mx * self.sense
		self.rotation[0] += my * self.sense
		self.rotation[0] = max(-numpy.pi/2, min(numpy.pi/2, self.rotation[0]))