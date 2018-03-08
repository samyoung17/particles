import hardboundary
import langevin
import runtumble
import runtumblenoise
import linearrepulsion
import repulsiveboundary
import voronoi
import voronoiboundary
import electrostaticforce
import electrostaticboundary
import electrostaticlangevin

WIERD_QUADRILATERAL_VERTICES = [(-10.0, -10.0), (-3.0, 2.0), (7.0, 4.0), (9.0, 0.0)]
RECTANGLE_VERTICES = [(-15.71, -3.93), (-15.71, 3.93), (15.71, 3.93), (15.71, -3.93)]
SQUARE_VERTICES = [(-7.86, -7.86), (-7.86, 7.86), (7.86, 7.86), (7.86, -7.86)]
R_MAX = 10.0

ITERATIONS = 2000
N = 300

CONFIG = {
	'SHAPE_COMPARISON': [
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
	],

	'INERTIA_COMPARISON': [
		{
			'name': 'Inertia comparison m=0_1',
			'filePath': 'data/inertia comparison m=0_1',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.5}
		},
		{
			'name': 'Inertia comparison m=1',
			'filePath': 'data/inertia comparison m=1',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 1.0, 'gamma': 0.05, 's': 0.5}
		},
		{
			'name': 'Inertia comparison m=10',
			'filePath': 'data/inertia comparison m=10',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 10.0, 'gamma': 0.05, 's': 0.5}
		},
		{
			'name': 'Inertia comparison m=100',
			'filePath': 'data/inertia comparison m=100',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 100.0, 'gamma': 0.05, 's': 0.5}
		},
	],

	'RUN_TUMBLE_RATE_COMPARISON': [
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
	],

	'ELECTROSTATIC_LANGEVIN_COMPARISON': [
		{
			'name': 's=0',
			'filePath': 'data/Electrostatic Langeivn s=0',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': electrostaticboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.02, 's': 0.0, 'rNeighbour': 20.0, 'qTotal': 3.0, 'qRing': 1.5, 'alpha':-2}
		},
		{
			'name': 's=0.02',
			'filePath': 'data/Electrostatic Langeivn s=0_02',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': electrostaticboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.02, 's': 0.02, 'rNeighbour': 20.0, 'qTotal': 3.0, 'qRing': 1.5, 'alpha':-2}
		},
		{
			'name': 's=0.1',
			'filePath': 'data/EL s=0.1',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': electrostaticboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.02, 's': 0.1, 'rNeighbour': 20.0, 'qTotal': 3.0, 'qRing': 1.5, 'alpha':-2}
		},
		{
			'name': 's=0.5',
			'filePath': 'data/EL s=0.5',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': electrostaticboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.02, 's': 0.5, 'rNeighbour': 20.0, 'qTotal': 3.0, 'qRing': 1.5, 'alpha':-2}
		}
	],

	'LINEAR_REPULSION_COMPARISON': [
		{
			'name': 's=0',
			'filePath': 'data/linear repulsion s=0',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.0, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 1.5, 'alpha':0}
		},
		{
			'name': 's=0.02',
			'filePath': 'data/linear repulsion s=0_02',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.02, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 1.5, 'alpha':0}
		},
		{
			'name': 's=0.1',
			'filePath': 'data/linear repulsion s=0_1',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.1, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 1.5, 'alpha':0}
		},
		{
			'name': 's=0.5',
			'filePath': 'data/linear repulsion s=0_5',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.5, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 1.5, 'alpha':0}
		}
	],

	'LR_INFLUENCE_COMPARISON': [
		{
			'name': 'r=0.7',
			'filePath': 'data/linear repulsion r=0_7',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.02, 'rNeighbour': 0.7, 'qTotal': 30.0, 'qRing': 3.0, 'alpha': 0}
		},
		{
			'name': 'r=0.9',
			'filePath': 'data/linear repulsion r=0_9',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.02, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 3.0, 'alpha': 0}
		},
		{
			'name': 'r=1.1',
			'filePath': 'data/linear repulsion r=1_1',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.02, 'rNeighbour': 1.1, 'qTotal': 30.0, 'qRing': 3.0, 'alpha': 0}
		},
		{
			'name': 'r=1.3',
			'filePath': 'data/linear repulsion r=1_3',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.02, 'rNeighbour': 1.3, 'qTotal': 30.0, 'qRing': 3.0, 'alpha': 0}
		}
	],

	'LOW_NOISE_COMPARISON': [
		{
			'name': 'Linear Repulsion',
			'filePath': 'data/low noise linear repulsion',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.025, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 3.0, 'alpha': 0}
		},
		{
			'name': 'Electrostatic Repulsion',
			'filePath': 'data/low noise electrostatic repulsion',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': electrostaticboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.01, 's': 0.025, 'rNeighbour': 20.0, 'qTotal': 1.0, 'qRing': 0.5, 'alpha':-2}
		},
		{
			'name': 'Langevin Dynamics',
			'filePath': 'data/low noise langevin dynamics',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.2, 's': 0.275}
		},
		{
			'name': 'Run and Tumble',
			'filePath': 'data/low noise run and tumble',
			'moveFn': runtumblenoise.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.2, 'sNoise': 0.025, 's': 0.25, 'rate': 0.25}
		}
	],

	'HIGH_NOISE_COMPARISON': [
		{
			'name': 'Linear Repulsion',
			'filePath': 'data/high noise linear repulsion',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.25, 'rNeighbour': 0.9, 'qTotal': 30.0, 'qRing': 3.0, 'alpha': 0}
		},
		{
			'name': 'Electrostatic Repulsion',
			'filePath': 'data/high noise electrostatic repulsion',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': electrostaticboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.01, 's': 0.25, 'rNeighbour': 20.0, 'qTotal': 1.0, 'qRing': 0.5, 'alpha': -2}
		},
		{
			'name': 'Langevin Dynamics',
			'filePath': 'data/high noise langevin dynamics',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.2, 's': 0.5}
		},
		{
			'name': 'Run and Tumble',
			'filePath': 'data/high noise langevin dynamics',
			'moveFn': runtumblenoise.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.2, 'sNoise': 0.25, 's': 0.25, 'rate': 0.25}
		}
	]
}
