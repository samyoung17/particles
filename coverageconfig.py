import hardboundary
import langevin
import runtumble
import linearrepulsion
import voronoi
import voronoiboundary
import electrostaticforce
import electrostaticboundary
import electrostaticlangevin

WIERD_QUADRILATERAL_VERTICES = [(-10.0, -10.0), (-3.0, 2.0), (7.0, 4.0), (9.0, 0.0)]
RECTANGLE_VERTICES = [(-15.71, -3.93), (-15.71, 3.93), (15.71, 3.93), (15.71, -3.93)]
SQUARE_VERTICES = [(-7.86, -7.86), (-7.86, 7.86), (7.86, 7.86), (7.86, -7.86)]
R_MAX = 10.0

ITERATIONS = 4000
N = 200

SHAPE_COMPARISON = [
	{
		'name': 'Run and Tumble Circle',
		'filePath': 'data/run tumble circle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.Circle(R_MAX)
	},
	{
		'name': 'Run and Tumble Rectangle',
		'filePath': 'data/run tumble Rectangle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
	},
	# {
	# 	'name': 'Run and Tumble Quadrilateral',
	# 	'filePath': 'data/run tumble Quadrilateral n={} iter={}'.format(N, ITERATIONS),
	# 	'moveFn': runtumble.moveParticles,
	# 	'boundary': hardboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
	# },
	{
		'name': 'Langevin Circle',
		'filePath': 'data/langevin circle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX)
	},
	{
		'name': 'Langevin Rectangle',
		'filePath': 'data/langevin Rectangle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
	},
	# {
	# 	'name': 'Langevin Quadrilateral',
	# 	'filePath': 'data/langevin Quadrilateral n={} iter={}'.format(N, ITERATIONS),
	# 	'moveFn': langevin.moveParticles,
	# 	'boundary': hardboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
	# },
	{
		'name': 'Voronoi circle',
		'filePath': 'data/voronoi circle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': voronoi.moveParticles,
		'boundary': voronoiboundary.Circle(R_MAX),
		'params': {
			'rMax': R_MAX
		}
	},
	{
		'name': 'Electrostatic circle',
		'filePath': 'data/electrostatic circle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticforce.moveParticles,
		'boundary': electrostaticboundary.Circle(R_MAX)
	},
	{
		'name': 'Electrostatic rectangle',
		'filePath': 'data/electrostatic rectangle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticforce.moveParticles,
		'boundary': electrostaticboundary.CompactPolygon(RECTANGLE_VERTICES)
	},
	# {
	# 	'name': 'Electrostatic quadrilateral',
	# 	'filePath': 'data/electrostatic quadrilateral n={} iter={}'.format(N, ITERATIONS),
	# 	'moveFn': electrostaticforce.moveParticles,
	# 	'boundary': electrostaticboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
	# },

	{
		'name': 'Linear Repulsion Circle',
		'filePath': 'data/linear repulsion circle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': linearrepulsion.moveParticles,
		'boundary': hardboundary.Circle(R_MAX)
	},
	{
		'name': 'Linear Repulsion Rectangle',
		'filePath': 'data/linear repulsion Rectangle n={} iter={}'.format(N, ITERATIONS),
		'moveFn': linearrepulsion.moveParticles,
		'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
	}
	# {
	# 	'name': 'Linear Repulsion Quadrilateral',
	# 	'filePath': 'data/linear repulsion Quadrilateral n={} iter={}'.format(N, ITERATIONS),
	# 	'moveFn': linearrepulsion.moveParticles,
	# 	'boundary': hardboundary.CompactPolygon(WIERD_QUADRILATERAL_VERTICES)
	# }
]

ELECTROSTATIC_LANGEVIN_COMPARISON = [
	{
		'name': 'EL qTotal=1',
		'filePath': 'data/EL qTotal=1 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 3.0, 'qTotal': 1.0, 'alpha': -2}
	},
	{
		'name': 'EL qTotal=2',
		'filePath': 'data/EL qTotal=2 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 3.0, 'qTotal': 2.0, 'alpha': -2}
	},
	{
		'name': 'EL qTotal=3',
		'filePath': 'data/EL qTotal=3 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 3.0, 'qTotal': 3.0, 'alpha': -2}
	}
]

LINEAR_REPULSION = [
	{
		'name': 'LR rNeighbour=0.25',
		'filePath': 'data/LR rNeighbour=0_25 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 0.25, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=0.5',
		'filePath': 'data/LR rNeighbour=0_5 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 0.5, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=1',
		'filePath': 'data/LR rNeighbour=1 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 1.0, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=2',
		'filePath': 'data/LR rNeighbour=2 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 2.0, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=3',
		'filePath': 'data/LR rNeighbour=3 n={} iter={}'.format(N, ITERATIONS),
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 3.0, 'qTotal': 10.0, 'alpha': 0}
	}
]