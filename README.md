# ATOLL
Visualization tool for transmembrane protein structures

## Description
ATOLL (Aligned Transmembrane dOmain Layout fLattening) est un petit programme permettant la visualisation de structures 3D de protéines transmembranaires (PTM). Le principe est de projeter des portion d'hélices sur le plan de la membrane comme un utilisateur regardant la protéine vue du dessus. Ainsi, il est possible de caractériser les états structuraux des structures sur un graphique simple et intuitif.

## Réquis
ATOLL est écrit en Python 3 et nécessite les librairies NumPy, SciPy, Matplotlib, PyYAML, Biopython et MDAnalysis. Il est fortement conseillé de créer un environnement Anaconda en utilisant le fichier conda3.yaml fourni. Le programme est compatible avec les systèmes d'exploitation Windows, Mac OS et Linux.

## Fonctionnement d'ATOLL
### Fichiers d'entrées
Pour lancer ATOLL, vous aurez besoin de plusieurs fichiers :
- Les structures à analyser
- Une structure de référence
- Un fichier d'alignement des séquences
- Un fichier d'annotation

#### Fichiers des structures à analyser
Les fichiers comportent toutes les structures qui seront analysées par le programme ATOLL. Ils peuvent décrire une ou plusieurs protéines, dont chacune peut être représentée par une ou plusieurs structures comme pour les simulations par dynamique moléculaire. Ces fichiers n'impliquent pas de dispositions particulières en terme de préparation. Il est possible d'utiliser des structures issues de la PDB telles quelles, de même pour les trajectoires de dynamique moléculaire. Cependant, il est intéressant d'enlever tous les objets non-essentiels des fichiers comme les molécules d'eau qui vont augmenter le temps de lecture des trajectoires. ATOLL est capable de traiter à la fois des trajectoires et des structures statiques dans la même analyse.
Pour les trajectoires de dynamique moléculaire, le fichier de topologie et le ou les fichiers de coordonnées de chaque entrée doivent être placés dans un répertoire dédié. Le programme effectue un scan du répertoire afin de retrouver les fichiers de topologie et de coordonnées selon l'extension de ces derniers.
Ces fichiers peuvent contenir une seule structure (*statique* : PDB ou MOL2) ou plusieurs (*multiple* : CRD, RST, NC, DCD, ...). La liste des formats et extensions de fichier est la suivante :
- Statique
    - Protein Data Bank (PDB): .pdb
    - SYBYLL (MOL2): .mol2
- Multiple
    - Topologie
        - AMBER TOP: .prmtop, .top, parm7
        - CHARMM PSF: .psf
        - Protein Data Bank (PDB): .topdb
    - Coordonnée
        - AMBER CRD: .inpcrd
        - AMBER RST: .inprst
        - AMBER TRJ: .trj
        - AMBER NetCDF: .ncdf, .nc
        - CHARMM DCD: .dcd
        - GROMACS XTC: .xtc
        - GROMACS TRR: .trr

En fonction de la nature *statique* ou *multiple* du fichier, ATOLL représentera les protéines différemment (Voir la rubrique correspondante).

#### Fichier de référence
La structure de référence joue un rôle crucial dans la procédure ATOLL. En effet, c'est sur cette dernière que sont superposées les structures à analyser. De plus, la définition des domaines est basée sur les résidus de la structure de référence. Par conséquent, la protéine doit être identique à celle des structures à analyser ou proche tout du moins. Il est également nécessaire que la structure soit placée dans un référentiel de coordonnées adapté aux projections. Actuellement, les positions des extrémités sont projetées sur le plan $xy$. Prochainement une routine sera ajoutée afin de placer la structure dans le référentiel adaptée en indiquant le plan de la membrane par des atomes. Il existe deux solutions afin d'avoir le référentiel adéquat. La première est que l'utilisateur place lui-même la protéine avec un logiciel tel que MOE ou Maestro. La deuxième possibilité est de télécharger la structure sur la base de données structurales des orientations des protéines dans la membrane (Orientation of proteins in membrane database, [OPM](https://opm.phar.umich.edu/)) et de spécifier à ATOLL les résidus utilisés pour l'alignement.
A noter que le programme ATOLL ne prend en compte que le premier conformère pour la structure de référence, les suivants étant ignorés. Les formats de fichier supportés sont ceux des structures *statiques*.

#### Fichier d'alignement de séquences
Ce fichier est indispensable si les séquences des protéines décrites dans les structures sont différentes. Le programme n'incorpore pas de routine capable d'effectuer des alignements de séquences multiples. Par conséquent, il doit être fait par des logiciels tiers comme MOE capable d'intégrer l'information structurale lors de l'alignement ou bien Clustal Omega via le [webservice](https://www.ebi.ac.uk/Tools/msa/clustalo/).

Le seul format supporté par ATOLL est le format Stockholm (.sto ou .stk) utilisé par exemple dans la base de donnée [Pfam](http://pfam.xfam.org/). Ce format a l'avantage d'offrir la possibilité à l'utilisateur d'y insérer des annotations par le biais de fonctionnalités préexistantes ou personnalisées. Chaque séquence possède une étiquette composée le plus souvent du nom de la protéine ainsi que de l'intervalle de séquence représenté. Dans le fichier, la séquence de référence est identifiée par la balise "#=GS label RE reference" et sa numérotation sera utilisée afin de définir les domaines.

#### Fichier d'annotation
Le fichier d'annotation est indispensable afin de fournir au programme toutes les informations sur les structures qu'il traitera. Les différentes informations sont formatées sous forme de tableau au format CSV (séparateur virgule) ou TSV (séparateur tabulation). Dans ATOLL, chaque structure *statique* et chaque répertoire comportant des structures *multiples* est considéré comme UNE entrée. Le tableau est composé de 6 champs :
- "Entry": label unique pour chaque entrée
- "Sequence name": le label associé dans le fichier d'alignement de séquences.
- "Group": permet de définir un groupe pour plusieurs entrées
- "Type": spécifie si il s'agit d'une entrée *statique* ou *multiple*
- "Path": le chemin d'accès de l'entrée. Doit être un fichier si l'entrée est *statique* et un répertoire si l'entrée est *multiple*
- "Color": la couleur associée à l'entrée lors de la génération du graphique

### Lancement du programme
Le programme ce lance via un terminal. Voici un exemple :

```bash
python ../../bin/atoll.py -ref reference.pdb -seq sequences.sto -inf info.tsv -out results -ra 31-57+64-88+99-129+143-164+190-219+235-256+277-300 -rh 26-57+64-89+98-131+142-165+187-223+228-259+269-300 -rn resid --overwrite
```

Dans les détails, les différentes options sont :
- ```-ref```: le chemin de la structure de référence.
- ```-seq```: le chemin du fichier d'alignement de séquence.
- ```-inf```: le chemin du fichier d'annotation.
- ```-out```: le chemin du répertoire ou toutes les sorties d'ATOLL seront stockées.
- ```-ra```: les résidus utilisés lors de l'alignement structural.
- ```-rh```: la définition des hélices transmembranaires à projeter.
- ```-rn```: la manière dont sont interprétées les résidus fournis dans ```-ra``` et ```-rh```. Les valeurs autorisées sont "position" qui correspond à la position des résidus dans le fichier d'alignement de séquence, et "resid" qui correspond au numéro des résidus dans le même fichier. A noter que le numéro de résidu est défini dans l'étiquette de la séquence.
- ```--overwrite```: Si le répertoire de sorti est existant, il sera alors écrasé.

NB: La synthaxe de résidus dans  ```-ra``` et ```-rh``` permet de définir une étendue avec le caractère '-' et de séparer les étendues avec le caractère '+'.