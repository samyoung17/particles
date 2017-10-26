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
			'name': 'Langevin Circle',
			'filePath': 'data/langevin circle n={} iter={}'.format(n, iter),
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(particlesim.R_MAX)
		},
		{
			'name': 'Run and Tumble Square',
			'filePath': 'data/run tumble square n={} iter={}'.format(n, iter),
			'moveFn': runtumble.moveParticles,
			'boundary': hardboundary.Square(particlesim.R_MAX * 2)
		},
		{
			'name': 'Langevin Square',
			'filePath': 'data/langevin square n={} iter={}'.format(n, iter),
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Square(particlesim.R_MAX * 2)
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