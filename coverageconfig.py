import hardboundary
import particlesim
import langevin
import runtumble
import metropolis
import brownianmotion
import voronoi
import forcedistribution

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
			'boundary': hardboundary.Rectangle(particlesim.R_MAX * 4, particlesim.R_MAX / 2)
		},
		{
			'name': 'Run and Tumble Quadrilateral',
			'filePath': 'data/run tumble Quadrilateral n={} iter={}'.format(n, iter),
			'moveFn': runtumble.moveParticles,
			'boundary': hardboundary.WierdQuadrilateral()
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
			'boundary': hardboundary.Rectangle(particlesim.R_MAX * 4, particlesim.R_MAX / 2)
		},
		{
			'name': 'Langevin Quadrilateral',
			'filePath': 'data/langevin Quadrilateral n={} iter={}'.format(n, iter),
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.WierdQuadrilateral()
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
			'boundary': hardboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Electrostatic circle',
			'filePath': 'data/electrostatic circle n={} iter={}'.format(n, iter),
			'moveFn': forcedistribution.moveParticles,
			'boundary': hardboundary.Circle(particlesim.R_MAX)
		}
	]