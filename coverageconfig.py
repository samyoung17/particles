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
import numpy as np

WIERD_QUADRILATERAL_VERTICES = [(-10.0, -10.0), (-3.0, 2.0), (7.0, 4.0), (9.0, 0.0)]
RECTANGLE_VERTICES = [(-15.71, -3.93), (-15.71, 3.93), (15.71, 3.93), (15.71, -3.93)]
SQUARE_VERTICES = [(-7.86, -7.86), (-7.86, 7.86), (7.86, 7.86), (7.86, -7.86)]
R_MAX = 10.0
H = np.sqrt(2 * np.pi / (3 * np.sqrt(3)))

ITERATIONS = 400
N = 200

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
			'name': 'm=0.1',
			'filePath': 'data/inertia comparison m=0_1',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.35}
		},
		{
			'name': 'm=1',
			'filePath': 'data/inertia comparison m=1',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 1.0, 'gamma': 0.05, 's': 0.35}
		},
		{
			'name': 'm=10',
			'filePath': 'data/inertia comparison m=10',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 10.0, 'gamma': 0.05, 's': 0.35}
		},
		{
			'name': 'm=100',
			'filePath': 'data/inertia comparison m=100',
			'moveFn': langevin.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'m': 100.0, 'gamma': 0.05, 's': 0.35}
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


	'LR_INFLUENCE': [
		{
			'name': f'eta={eta:.1f}',
			'filePath': f'data/linear repulsion eta={eta:.1f}',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {
				'm': 1,
				'gamma': 0.5,
				's': 0.05,
				'rNeighbour': eta * R_MAX / np.sqrt(N),
				'q': 2.0 / eta,
				'qRing': 3.0,
				'alpha': 0
			}
		} for eta in np.arange(1.0, 4.1, 0.5)
	],

    'LR_INTERACTION': [
		{
			'name': f'phi={phi:.2f}',
			'filePath': f'data/linear repulsion phi={phi:.2f}',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {
				'm': 1,
				'gamma': 0.5,
				'd': pow(.5-phi, 2) * 0.5 * 2 / np.pi,
				'rNeighbour': H * np.sqrt(3) * R_MAX / np.sqrt(N),
				'q': np.sqrt(phi * np.sqrt(0.5) / (pow(H,2) * 3)),
				'qRing': 3.0,
				'alpha': 0
			}
		} for phi in np.arange(0, 0.55, 0.05)
	],

	'LANGEVIN_GAMMA': [
		{
			'name': f'gamma={gamma:.2f}',
			'filePath': f'data/langevin gamma={gamma:.2f}',
			'moveFn': electrostaticlangevin.moveParticles,
			'boundary': repulsiveboundary.Circle(R_MAX),
			'params': {
				'm': 1.0,
				'gamma': gamma,
				'd': pow(0.5, 2) * gamma * 2 / np.pi,
				'rNeighbour': 0.0,
				'q': 0.0,
				'qRing': 3.0,
				'alpha': 0
			}
		} for gamma in np.arange(0.05, 0.55, 0.05)
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
			'params': {'m': 0.1, 'gamma': 0.05, 's': 0.35}
		},
		{
			'name': 'Run and Tumble',
			'filePath': 'data/low noise run and tumble',
			'moveFn': runtumble.moveParticles,
			'boundary': hardboundary.Circle(R_MAX),
			'params': {'s': 0.35, 'rate': 0.1}
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
