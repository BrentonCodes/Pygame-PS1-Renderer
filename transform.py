import numpy

def transform(vertices, uvs, m_pos, m_rot, m_scale, camera):

	c_pos = camera.position
	c_rot = camera.rotation
	focal_length = camera.f
	
	num_verts = vertices.shape[0]

	out = numpy.empty((num_verts, 5), dtype=numpy.float32)

	rx, ry, rz = m_rot[0], m_rot[1], m_rot[2]
	cos_my, sin_my = numpy.cos(ry), numpy.sin(ry)
	cos_mx, sin_mx = numpy.cos(rx), numpy.sin(rx)
	cos_mz, sin_mz = numpy.cos(rz), numpy.sin(rz)

	crx, cry, crz = c_rot[0], c_rot[1], c_rot[2]
	cos_cy, sin_cy = numpy.cos(-cry), numpy.sin(-cry)
	cos_cx, sin_cx = numpy.cos(-crx), numpy.sin(-crx)
	cos_cz, sin_cz = numpy.cos(-crz), numpy.sin(-crz)
	
	eps = 1e-6

	for i in range(num_verts):

		x = vertices[i, 0]
		y = vertices[i, 1]
		z = vertices[i, 2]

		# SCALING

		sx = x * m_scale[0]
		sy = y * m_scale[1]
		sz = z * m_scale[2]

		# MESH ROTATION
		if ry != 0:
			sx, sz = sx * cos_my + sz * sin_my, -sx * sin_my + sz * cos_my
		if rx != 0:
			sy, sz = sy * cos_mx - sz * sin_mx, sy * sin_mx + sz * cos_mx
		if rz != 0:
			sx, sy = sx * cos_mz - sy * sin_mz, sx * sin_mz + sy * cos_mz

		# TRANSLATION
		tx = sx + m_pos[0] - c_pos[0]
		ty = sy + m_pos[1] - c_pos[1]
		tz = sz + m_pos[2] - c_pos[2]

		# CAMERA ROTATION
		if cry != 0:
			tx, tz = tx * cos_cy + tz * sin_cy, -tx * sin_cy + tz * cos_cy
		if crx != 0:
			ty, tz = ty * cos_cx - tz * sin_cx, ty * sin_cx + tz * cos_cx
		if crz != 0:
			tx, ty = tx * cos_cz - ty * sin_cz, tx * sin_cz + ty * cos_cz

		# PROJECTION
		tz_safe = eps if numpy.abs(tz) < eps else tz

		px = (tx / tz_safe) * focal_length
		py = -(ty / tz_safe) * focal_length

		out[i, 0] = px
		out[i, 1] = py
		out[i, 2] = tz
		out[i, 3] = uvs[i, 0]
		out[i, 4] = uvs[i, 1]

	return out
