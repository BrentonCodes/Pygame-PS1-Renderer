import pygame
import numpy

import rasterize
import transform
import camera
import util

pygame.init()

RESOLUTION = (640, 360)

framebuffer = numpy.zeros(RESOLUTION, dtype=numpy.uint32)
depthbuffer = numpy.zeros(RESOLUTION, dtype=numpy.float32)

window = pygame.display.set_mode(RESOLUTION)

pygame.mouse.set_visible(False)
pygame.mouse.set_relative_mode(True)

clock = pygame.time.Clock()

c = camera.Camera()

sky_color = util.rgb_to_packed((100, 190, 235))

# Model Loading
verts, faces, uvs = util.load_obj("demo.obj")
texture = util.load_tex("demo.png")

pos = numpy.array((0,0,0))
rot = numpy.array((0,0,0))
scale = numpy.array((1,1,1))

running = True

while running:

	dt = clock.tick(0) / 1000

	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			running = False

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:

				running = False

	c.update(dt)

	framebuffer.fill(sky_color)
	depthbuffer.fill(0)

	window.fill(0)

	points = transform.transform(verts, uvs, pos, rot, scale, c)

	for i in range(faces.shape[0]):

		f = faces[i]

		v0 = points[f[0]]
		v1 = points[f[1]]
		v2 = points[f[2]]

		if v0[2] > 0 and v1[2] > 0 and v2[2] > 0:

			rasterize.triangle(framebuffer, depthbuffer, texture, v0, v1, v2, affine=False)

	pygame.surfarray.blit_array(window, framebuffer)

	pygame.display.update()