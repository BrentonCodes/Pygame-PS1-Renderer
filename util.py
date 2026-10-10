import trimesh
import numpy
import pygame

def load_obj(path):

	mesh = trimesh.load_mesh(path, process=False)

	verts = numpy.asarray(mesh.vertices, dtype=numpy.float32)
	faces = numpy.asarray(mesh.faces, dtype=numpy.int32)

	uv = getattr(mesh.visual, "uv", None)

	if uv is None:

		uv = numpy.zeros((len(vertices), 2), dtype=numpy.float32)

	return verts, faces, uv

def load_tex(path):

	img = pygame.image.load(path).convert()

	arr = pygame.surfarray.array3d(img)

	packed = (
		(arr[:, :, 0].astype(numpy.uint32) << 16) |
		(arr[:, :, 1].astype(numpy.uint32) << 8)  |
		(arr[:, :, 2].astype(numpy.uint32))
	)

	return packed

def rgb_to_packed(color):

	r, g, b = color

	return (int(r) << 16) | (int(g) << 8) | int(b)