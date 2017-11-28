import hardboundary
import particlesim
import langevin
import runtumble
import linearrepulsion
import metropolis
import brownianmotion
import voronoi
import voronoiboundary
import electrostaticforce
import electrostaticboundary

WIERD_QUADRILATERAL_VERTICES = [(-10.0, -10.0), (-3.0, 2.0), (7.0, 4.0), (9.0, 0.0)]
RECTANGLE_VERTICES = [(-20.0, -5.0), (-20.0, 5.0), (20.0, 5.0), (20.0, -5.0)]
SQUARE_VERTICES = [(-10.0, -10.0), (-10.0, 10.0), (10.0, 10.0), (10.0, -10.0)]

def getConfig(n, iter):
	return [
		{
			'name': 'Run and Tumble Circle',
			'filePath': 'data/run tumble circle n={} iter={}'.format(n, iter),
			'moveFn': runtumble.moveParticles,
			'boundary': hardboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Run and Tumble Rectangle',
			'filePath': 'data/run tumble Rectangle n={} iter={}'.format(n, iter),
			'moveFn': runtumble.moveParticles,
			'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
		},
		{
			'name': 'Run and Tumble Quadrilateral',
			'filePath': 'data/run tumble Quadrilateral n={} iter={}'.format(n, iter),
			'moveFn': runtumble.moveParticles,
			'boundary': hardboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
		},
		{
			'name': 'Langevin Circle',
			'filePath': 'data/langevin circle n={} iter={}'.format(n, iter),
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Langevin Rectangle',
			'filePath': 'data/langevin Rectangle n={} iter={}'.format(n, iter),
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
		},
		{
			'name': 'Langevin Quadrilateral',
			'filePath': 'data/langevin Quadrilateral n={} iter={}'.format(n, iter),
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
		},
		# {
		# 	'name': 'Metropolis',
		# 	'filePath': 'data/metropolis n={} iter={}'.format(n, iter),
		# 	'moveFn': metropolis.moveParticles
		# },
		# {
		# 	'name': 'Brownian',
		# 	'filePath': 'data/brownian n={} iter={}'.format(n, iter),
		# 	'moveFn': brownianmotion.moveParticles
		# },
		{
			'name': 'Voronoi circle',
			'filePath': 'data/voronoi circle n={} iter={}'.format(n, iter),
			'moveFn': voronoi.moveParticles,
			'boundary': voronoiboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Electrostatic circle',
			'filePath': 'data/electrostatic circle n={} iter={}'.format(n, iter),
			'moveFn': electrostaticforce.moveParticles,
			'boundary': electrostaticboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Electrostatic rectangle',
			'filePath': 'data/electrostatic rectangle n={} iter={}'.format(n, iter),
			'moveFn': electrostaticforce.moveParticles,
			'boundary': electrostaticboundary.CompactPolygon(RECTANGLE_VERTICES)
		},
		{
			'name': 'Electrostatic quadrilateral',
			'filePath': 'data/electrostatic quadrilateral n={} iter={}'.format(n, iter),
			'moveFn': electrostaticforce.moveParticles,
			'boundary': electrostaticboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
		},

		{
			'name': 'Linear Repulsion Circle',
			'filePath': 'data/linear repulsion circle n={} iter={}'.format(n, iter),
			'moveFn': linearrepulsion.moveParticles,
			'boundary': hardboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Linear Repulsion Rectangle',
			'filePath': 'data/linear repulsion Rectangle n={} iter={}'.format(n, iter),
			'moveFn': linearrepulsion.moveParticles,
			'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
		},
		{
			'name': 'Linear Repulsion Quadrilateral',
			'filePath': 'data/linear repulsion Quadrilateral n={} iter={}'.format(n, iter),
			'moveFn': linearrepulsion.moveParticles,
			'boundary': hardboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
		}
	]