# ATOLL
Visualization tool for transmembrane protein structures

## Description
ATOLL (Aligned Transmembrane dOmain Layout fLattening) is a program for visualizing 3D structures of transmembrane proteins (TMPs). The principle is to project portions of helices onto the plane of the membrane as a user looking at the protein from above. Thus, it is possible to characterise the structural states of the structures on a simple and intuitive chart. The program is associated with a publication (in progress).

## Réquis
ATOLL is written in Python 3 and requires the NumPy, SciPy, Matplotlib, PyYAML, Biopython and MDAnalysis modules. It is strongly recommended to create an Anaconda environment using the *conda3.yaml* file provided. The program is compatible with Windows, Mac OS and Linux operating systems.

## How ATOLL works
### Input files
To launch ATOLL, several files must be providen:
- structure(s) to be analysed
- reference structure
- sequence alignment file
- annotation file

#### Structure file(s)
These files contain the structures that will be analysed by the ATOLL program. They can describe one or more proteins, each of which can be represented by one or more structures as in molecular dynamics simulations. Note that if a file describes several proteins, they must be in a single chain.

These files do not require any special preparation. It is possible to use structures from the PDB as they are, as well as the molecular dynamics (MD) trajectories. However, it is recommanded to remove all non-essential objects from the files, such as water molecules, which will increase the time required to read MD trajectories. Furthermore, the different structures should be consistent, i.e. have identical amino acid sequences. Otherwise, a sequence alignment file shall be provided (see below).

ATOLL is able to process both trajectories and static structures in the same analysis.
For molecular dynamics trajectories, the topology file and coordinate file(s) for each entry must be placed in a dedicated directory. The program scans the directory to find the topology and coordinate files by their extension.

These files can contain a single structure (*static*: PDB or MOL2) or several (*multiple*: CRD, RST, NC, DCD, ...). The list of file formats and extensions is:
- Static
    - Protein Data Bank (PDB): .pdb
    - SYBYLL (MOL2): .mol2
- Multiple
    - Topology
        - AMBER TOP: .prmtop, .top, parm7
        - CHARMM PSF: .psf
        - Protein Data Bank (PDB): .topdb
    - Coordinate
        - AMBER CRD: .inpcrd
        - AMBER RST: .inprst
        - AMBER TRJ: .trj
        - AMBER NetCDF: .ncdf, .nc
        - CHARMM DCD: .dcd
        - GROMACS XTC: .xtc
        - GROMACS TRR: .trr

Depending on the *static* or *multiple* nature of the file, ATOLL will represent the proteins differently.

#### Reference file
The reference structure plays a crucial role in the ATOLL procedure. Indeed, the structures to be analyzed are superimposed on it. Moreover, the definition of the domains is based on the residues of the reference structure. Therefore, the protein must be identical or close to that of the structures to be analyzed. If the user assigns the structural alignment with ATOLL, it is necessary that the structure is placed in a coordinate frame suitable for the projections. Currently, the positions of the ends are projected on the *XY* plane.

There are two solutions for having the appropriate coordinate system. The first way is that the user places the protein himself with a software such as MOE or Maestro. The second way is to download the structure from the structural database of orientations of proteins in membrane [OPM](https://opm.phar.umich.edu/) and to specify to ATOLL the residues used for the alignment.
Note that the ATOLL program takes into account only the first conformer for the reference structure, the following ones being ignored. The supported file formats are those of *static* structures.

#### Sequence alignment file
This file is crucial if the sequences of the proteins described in the structures are different. The program does not incorporate a routine capable of performing multiple sequence alignments. Therefore, it must be done by third party software such as MOE or Clustal Omega via the [webservice](https://www.ebi.ac.uk/Tools/msa/clustalo/).

The only supported format by ATOLL is the Stockholm format (extension .sto or .stk) used for example in the [Pfam](http://pfam.xfam.org/) database. In the file, the reference sequence is identified by the tag "#=GS label RE reference" and its numbering will be used to define domains.

#### Annotation file
The annotation file is essential in order to provide all the information on the structures during ATOLL procesing. Data is formatted as a table in CSV (comma separator) or TSV (tab separator) format. In ATOLL, each *static* structure and each directory with *multiple* structures is considered as an entry. The table is composed of 6 fields:
- "Entry": unique label for each entry.
- "Sequence name": associated label in the sequence alignment file.
- "Group": define a group for several entries.
- "Type": specifies whether it is a *static* or *multiple* entry.
- "Path": path of the entry. Must be a file if the entry is *static* and a directory if the entry is *multiple*.
- "Color": entry color when generating the chart.

### Running ATOLL
The program is launched via a terminal. Here is an example:

```bash
python ../../bin/atoll.py -ref reference.pdb -seq sequences.sto -inf info.tsv -out results -ra 31-57+64-88+99-129+143-164+190-219+235-256+277-300 -rh 26-57+64-89+98-131+142-165+187-223+228-259+269-300 -rn resid --overwrite
```

In detail, the different options are :
- ```-ref```: path of the reference structure.
- ```-seq```: path of the sequence alignment file.
- ```-inf```: path of the annotation file.
- ```-out```: path of the directory where outputs will be stored.
- ```-ra```: residues used during structural alignment.
- ```-rh```: definition of the transmembrane helices to be projected.
- ```-rn```: how the residues provided in ```-ra``` and ```-rh``` are interpreted. The allowed values are "position" which corresponds to the position of the residues in the sequence alignment file or in the reference structure, and "resid" which corresponds to the residue number.
- ```--overwrite```: If the output directory exists, it will be overwritten.

NB: The residue synthax in ```-ra``` and ```-rh``` allows to define a range with the character '-' and to separate the ranges with the character '+'.