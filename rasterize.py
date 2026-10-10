import random
from numba import njit

@njit
def edge(x0, y0, x1, y1, x2, y2):
	return (x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0)

@njit
def triangle(fb, zb, tx, p0, p1, p2, affine=True):

	x0, y0, z0, u0, v0 = p0
	x1, y1, z1, u1, v1 = p1
	x2, y2, z2, u2, v2 = p2

	w, h = fb.shape
	th, tw = tx.shape

	cx, cy = fb.shape[0] * 0.5, fb.shape[1] * 0.5

	x0 += cx; y0 += cy
	x1 += cx; y1 += cy
	x2 += cx; y2 += cy

	area = edge(x0, y0, x1, y1, x2, y2)

	if area == 0:
		return

	minx = max(0,   int(min(x0, x1, x2)))
	maxx = min(w-1, int(max(x0, x1, x2)))
	miny = max(0,   int(min(y0, y1, y2)))
	maxy = min(h-1, int(max(y0, y1, y2)))

	inv_area = 1.0 / area

	A0 = (y2 - y1) * inv_area; B0 = (x1 - x2) * inv_area
	A1 = (y0 - y2) * inv_area; B1 = (x2 - x0) * inv_area
	A2 = (y1 - y0) * inv_area; B2 = (x0 - x1) * inv_area

	w0_row = edge(x1, y1, x2, y2, minx, miny) * inv_area
	w1_row = edge(x2, y2, x0, y0, minx, miny) * inv_area
	w2_row = edge(x0, y0, x1, y1, minx, miny) * inv_area

	iz0 = 1.0 / z0
	iz1 = 1.0 / z1
	iz2 = 1.0 / z2

	uz0 = u0 * iz0; vz0 = v0 * iz0
	uz1 = u1 * iz1; vz1 = v1 * iz1
	uz2 = u2 * iz2; vz2 = v2 * iz2

	for x in range(minx, maxx + 1):

		w0 = w0_row
		w1 = w1_row
		w2 = w2_row
		
		for y in range(miny, maxy + 1):
			
			if w0 >= 0 and w1 >= 0 and w2 >= 0:

				iz_interp = w0 * iz0 + w1 * iz1 + w2 * iz2

				if iz_interp > zb[x, y]:

					if affine:

						u = w0 * u0 + w1 * u1 + w2 * u2
						v = w0 * v0 + w1 * v1 + w2 * v2

					else:

						uz_interp = w0 * uz0 + w1 * uz1 + w2 * uz2
						vz_interp = w0 * vz0 + w1 * vz1 + w2 * vz2

						u = uz_interp / iz_interp
						v = vz_interp / iz_interp

					tex_x = int(u * tw) % tw
					tex_y = int(v * th) % th

					fb[x, y] = tx[tex_y, tex_x]
					zb[x, y] = iz_interp

			w0 += B0
			w1 += B1
			w2 += B2
			
		w0_row += A0
		w1_row += A1
		w2_row += A2