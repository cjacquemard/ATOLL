import sys
import os
from copy import deepcopy

import sequence
import frame
import procedure
import plot
import initialize as init

__authors__ = ('Célien Jacquemard', 'Guillaume Bret')
__version__ = (0, 1)
__creation_date__ = '2020.07.16'
__last_update__ = '2020.07.16'
__email__ = 'gbret@unistra.fr'
__status__ = 'InDev'

prog_dir = os.path.realpath(os.path.dirname(__file__))
logger = init.get_logger()

'''
    ..TODO: Add method to check if selected residues for analysis exists in structures
    ..TODO: When more than 1 topology files are encountered the script should raise an error but it doesn't !!!
    ..TODO: Add PDB file as topology
    ..TODO: Correct helix radius. It doesn't correspond on plot!
    ..TODO: Add multiple reference handling
    ..TODO: Create log file with alignments and residue numbering
    ..TODO: Problem with MOL2 file residue parsing
    ..TODO: Write sequence alignments
    ..TODO: Handle gap in reference sequence after alignment
    ..TODO: Create class to handle sequence formatting
    ..TODO: Print warning when sequence identity is to low
    ..TODO: Add density merging by class name
'''

class Atoll:
	def __init__(self):
		self.reference = None
		self.structures = {}

	def load_from_cli(self, args):
		# Load sequence file
		if args.sequence_filepath:
			self.sequence_loader = sequence.SequenceLoader(args.sequence_filepath)
		else:
			self.sequence_loader = sequence.BasicSequenceLoader()

		# Load structure informations
		if args.info_filepath:
			self.info = frame.Info(args.info_filepath)
		else:
			self.info = frame.BasicInfo()

		# Domain definition
		self.domains = {}
		self.resnum = args.resnum

		# Residues use for structure alignment
		if args.resalign:
			self.domains['alignment'] = frame.Selector.split(args.resalign)

		# Residues use for analysis
		if args.reshelix:
			self.domains['phelix'] = frame.Selector.split(args.reshelix)
		else:
			raise NotImplementedError

		# Load reference and query structures
		self.reference = self.load_reference(args.reference_filepath)
		self.reference.set_referential()
		self.structures = self.load_structures(self.info)

		if not self.structures:
			raise ValueError('No input files were loaded!')

		# Load protein informations
		self.set_info(self.reference)
		for structure in self.structures:
			self.set_info(structure)

		# Define amino acid sequences for reference and structures
		self.set_sequence(self.reference)
		for structure in self.structures:
			self.set_sequence(structure)

		# Set domains to reference and queries
		self.set_domain(self.reference)
		for structure in self.structures:
			self.set_domain(structure)

		# Align reference sequence onto structure sequence
		sequence_aligner = sequence.SequenceAligner()
		sequence_aligner.align_reference(self.reference)
		for structure in self.structures:
			logger.info(f'Sequence alignment of "{structure.label}"')
			sequence_aligner.align_reference(structure)

		self.output = frame.Output(args.output_dirpath, args.overwrite)

		self.analyzer = procedure.Analyzer(self.structures, self.reference, self.output.dirpath)
		if args.resalign is not None:
			self.analyzer.add_analysis('align')
		# self.analyzer.add_analysis('trajwrite')
		self.analyzer.add_analysis('phelix')
		self.analyzer.run()

		pm = plot.ProjectionMap(
			self.analyzer.analysis_procedures[-1],
			output_filepath=os.path.join(self.output.plot_dirpath, 'projection_map.svg'),
			merging_type=args.merging_type,
			colors=self.info.get_dict_values('color')
		)
		logger.info('DONE')

	@classmethod
	def load_reference(cls, path):
		logger.info(f'Loading reference {path}...')
		reference = frame.Reference(args.reference_filepath)
		return reference

	@classmethod
	def load_structures(cls, info):
		structures = []
		for entry in info.entries.values():
			path = entry.path
			label = entry.id
			fileprefix, fileext = os.path.splitext(os.path.basename(path))

			if os.path.isfile(path):
				structure = frame.Static(label, path)
			else:
				structure = frame.Multiple(label, path)

			structures.append(structure)

		return structures

	def set_info(self, frame):
		if frame.label in self.info:
			frame.load_info(self.info[frame.label])

	def set_sequence(self, frame):
		if frame.label in self.sequence_loader:
			logger.info('by label')
			frame_sequence = self.sequence_loader[frame.label]
		elif frame.protein_name in self.sequence_loader:
			logger.info(f'by protein name {frame.protein_name}')
			frame_sequence = self.sequence_loader[frame.protein_name]
		elif self.sequence_loader.reference is not None:
			logger.info('by reference')
			frame_sequence = self.sequence_loader.reference
		else:
			logger.info('by structure')
			frame_sequence = sequence.Sequence(frame.protein)

		frame.sequence = deepcopy(frame_sequence)

	def set_domain(self, frame):
		for domain_name, intervals in self.domains.items():
			frame.domains.set_group_intervals(domain_name, intervals, self.resnum, prefix='TM')


def main(args):
	atoll = Atoll()
	atoll.load_from_cli(args)


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(
		prog='phelix',
		description='The Phelix program analyzes membrane protein helix conformations. Specify several structures to analyze with the "--input" arguments.',
		epilog='For more details, see doc/note.md.'
	)

	input_group = parser.add_argument_group('input')
	# input_group.add_argument('--input', '-in', nargs='+', required=True, dest='input_pathes',
	# 	help='Input structure files to analyze.', metavar='PATHES')
	input_group.add_argument('--reference', '-ref', required=True, dest='reference_filepath',
		help='Reference structure file.', metavar='FILEPATH')
	input_group.add_argument('--sequence', '-seq', dest='sequence_filepath',
		help='Sequence file of studied proteins.', metavar='FILEPATH')
	input_group.add_argument('--info', '-inf', dest='info_filepath', required=True,
		help='Information file for each entry.', metavar='FILEPATH')

	selection_group = parser.add_argument_group('selection')
	selection_group.add_argument('--resnum', '-rn', choices=['position', 'resid'], default='position',
		help='Residue numbering to apply.')
	selection_group.add_argument('--resalign', '-ra',
		help='Selection of residues involved in structure alignment.')
	selection_group.add_argument('--reshelix', '-rh', required=True,
		help='Selection of residues to analyze that correspond to transmembrane helice ends.')

	output_group = parser.add_argument_group('output')
	output_group.add_argument('--output', '-out', required=True, dest='output_dirpath',
		help='Output directory where results will be stored.', metavar='DIRPATH')
	output_group.add_argument('--overwrite', action='store_true',
		help='Overwrite data if output directory is already exist.')

	phelix_group = parser.add_argument_group('atoll')
	phelix_group.add_argument('--merge', default=None, choices=[None, 'class'], dest='merging_type',
		help='Merge contour with same class name.', metavar='MERGING_TYPE')

	misc_group = parser.add_argument_group('miscellaneous')
	# Optional argument that count the number of flag occurence (-v or -vv).
	misc_group.add_argument('-v', '--verbosity', action='count', default=0,
		help='Increase output verbosity.')


	parser.set_defaults(func=main)
	args = parser.parse_args()

	# Run
	status = args.func(args)
	sys.exit(status)
