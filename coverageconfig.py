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

ITERATIONS = 3000
N = 150
TRIALS = 20

SHAPE_COMPARISON = [
	{
		'name': 'Run and Tumble Circle',
		'filePath': 'data/run tumble circle',
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.Circle(R_MAX)
	},
	{
		'name': 'Run and Tumble Rectangle',
		'filePath': 'data/run tumble Rectangle',
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
	},
	{
		'name': 'Langevin Circle',
		'filePath': 'data/langevin circle',
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.2}
	},
	{
		'name': 'Langevin Rectangle',
		'filePath': 'data/langevin Rectangle',
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.2}
	},
	{
		'name': 'Voronoi circle',
		'filePath': 'data/voronoi circle',
		'moveFn': voronoi.moveParticles,
		'boundary': voronoiboundary.Circle(R_MAX),
		'params': {
			'rMax': R_MAX
		}
	},
	{
		'name': 'Electrostatic circle',
		'filePath': 'data/electrostatic circle',
		'moveFn': electrostaticforce.moveParticles,
		'boundary': electrostaticboundary.Circle(R_MAX)
	},
	{
		'name': 'Electrostatic rectangle',
		'filePath': 'data/electrostatic rectangle',
		'moveFn': electrostaticforce.moveParticles,
		'boundary': electrostaticboundary.CompactPolygon(RECTANGLE_VERTICES)
	},
	{
		'name': 'Linear Repulsion Circle',
		'filePath': 'data/linear repulsion circle',
		'moveFn': linearrepulsion.moveParticles,
		'boundary': hardboundary.Circle(R_MAX)
	},
	{
		'name': 'Linear Repulsion Rectangle',
		'filePath': 'data/linear repulsion Rectangle',
		'moveFn': linearrepulsion.moveParticles,
		'boundary': hardboundary.CompactPolygon(RECTANGLE_VERTICES)
	}
]

INERTIA_COMPARISON = [
	{
		'name': 'Inertia comparison m=0_1',
		'filePath': 'data/inertia comparison m=0_1',
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 0.1, 'gamma': 0.2, 's': 0.5}
	},
	{
		'name': 'Inertia comparison m=1',
		'filePath': 'data/inertia comparison m=1',
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.2, 's': 0.5}
	},
	{
		'name': 'Inertia comparison m=10',
		'filePath': 'data/inertia comparison m=10',
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 10.0, 'gamma': 0.2, 's': 0.5}
	},
	{
		'name': 'Inertia comparison m=100',
		'filePath': 'data/inertia comparison m=100',
		'moveFn': langevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 100.0, 'gamma': 0.2, 's': 0.5}
	},
]

RUN_TUMBLE_RATE_COMPARISON = [
	{
		'name': 'RT rate=1',
		'filePath': 'data/run tumble rate=1',
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'rate': 1.0, 's': 0.5}
	},
	{
		'name': 'RT rate=0_25',
		'filePath': 'data/run tumble rate=0_25',
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'rate': 0.25, 's': 0.5}
	},
	{
		'name': 'RT rate=0_1',
		'filePath': 'data/run tumble rate=0_1',
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'rate': 0.1, 's': 0.5}
	},
	{
		'name': 'RT rate=0_01',
		'filePath': 'data/run tumble rate=0_01',
		'moveFn': runtumble.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'rate': 0.01, 's': 0.5}
	}
]

ELECTROSTATIC_LANGEVIN_COMPARISON = [
	{
		'name': 'EL qTotal=1',
		'filePath': 'data/EL qTotal=1',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.5, 'rNeighbour': 3.0, 'qTotal': 1.0, 'alpha': -2}
	},
	{
		'name': 'EL qTotal=2',
		'filePath': 'data/EL qTotal=2',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.5, 'rNeighbour': 3.0, 'qTotal': 2.0, 'alpha': -2}
	},
	{
		'name': 'EL qTotal=3',
		'filePath': 'data/EL qTotal=3',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.5, 'rNeighbour': 3.0, 'qTotal': 3.0, 'alpha': -2}
	}
]

LINEAR_REPULSION = [
	{
		'name': 'LR rNeighbour=0.25',
		'filePath': 'data/LR rNeighbour=0_25',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 0.25, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=0.5',
		'filePath': 'data/LR rNeighbour=0_5',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 0.5, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=1',
		'filePath': 'data/LR rNeighbour=1',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 1.0, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=2',
		'filePath': 'data/LR rNeighbour=2',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 2.0, 'qTotal': 10.0, 'alpha': 0}
	},
	{
		'name': 'LR rNeighbour=3',
		'filePath': 'data/LR rNeighbour=3',
		'moveFn': electrostaticlangevin.moveParticles,
		'boundary': hardboundary.Circle(R_MAX),
		'params': {'m': 1.0, 'gamma': 0.1, 's': 0.01, 'rNeighbour': 3.0, 'qTotal': 10.0, 'alpha': 0}
	}
]