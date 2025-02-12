import random
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

import streamlit as st
st.title("Science Bowl Question Generator")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

science_bowl_topics = {
    "Physics": 0.2,
    "Chemistry": 0.2,
    "Biology": 0.2,
    "Math": 0.2,
    "Energy": 0.2
}

subtopics = {
    "Math": ["Triangles", "Quadrilaterals", "Coordinate Plane", "Area and Perimeter", "Volume and surface area", "Pythagorean Theorem", "Congruence", "Similarity", "Circles", "Composite and Inverse Functions", "Complex numbers", "Rational functions", "Conic secctions", "Vectors", "Matrices", "Series", "Polynomial multiplication/division/arithmetic", "Logarithms", "Exponential models", "Trigonometric identities", "Trigonometric equations", "Law of cosines/sines", "Unit circle", "Limits and Continuity", "Derivatives", "Derivative Tests", "Integrals", "Differential equations", "Polar coordinates"],
    "Physics": ["Describing Motion: Kinematics in One Dimension", "Kinematics in Two Dimensions; Vectors", "Dynamics: Newton's Laws of Motion", "Circular Motion; Gravitation", "Work and Energy", "Linear Momentum", "Rotational Motion", "Static Equilibrium; Elasticity and Fracture", "Fluids"],
    "Chemistry": ["Chemical Foundations", "Atoms;Molecules;Ions", "Stoichiometry", "Types of Chemical Reactions and Solution Stoichiometry", "Gases", "Thermochemistry", "Atomic Structure and Periodicity", "Atomic Bonding"],
    "Biology": ["Evolution and the Foundations of Biology", "Chemistry in Biology", "Carbon's Versatility and the Macromolecules", "Cells and Organelles", "Membrane Transport and Cell Signaling", "Metabolism", "Cellular Respiration and Fermentation", "Photosynthesis", "The Cell Cycle", "Meiosis and Sexual Life Cycles", "Mendel and the Gene Idea", "The Chromosomal Basis of Inheritance", "The Molecular Basis of Inheritance", "Gene Expression: From Gene to Protein", "Regulation of Gene Expression"],
}

def select_topic():
    category = random.choices(list(science_bowl_topics.keys()), weights=list(science_bowl_topics.values()))[0]
    if(category=="Energy"):
        topic = ""
    else:
        topic = random.choice(subtopics[category])
    return category, topic

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

chem_text = [

    '''

Key terms
Section 1.2
scientific method
measurement
hypothesis
theory
model
natural law
law of conservation of mass
Section 1.3
SI system
mass
weight
Section 1.4
uncertainty
significant figures
accuracy
precision
random error
systematic error
Section 1.5
exponential notation
Section 1.7
unit factor method
dimensional analysis
Section 1.9
density
Section 1.10
matter
states (of matter)
homogeneous mixture
heterogeneous mixture
solution
pure substance
physical change
distillation
filtration
chromatography
paper chromatography
compound
chemical change
element
Scientific method
❯ Make observations
❯ Formulate hypotheses
❯ Perform experiments
Models (theories) are explanations of why nature behaves in a
particular way.
❯ They are subject to modification over time and sometimes fail.
Quantitative observations are called measurements.
❯ Measurements consist of a number and a unit.
❯ Measurements involve some uncertainty.
❯ Uncertainty is indicated by the use of significant figures.
❯ Rules to determine significant figures
❯ Calculations using significant figures
❯ Preferred system is the SI system.
Temperature conversions
❯ TK 5 TC 1 273.15
❯ TC 5 1TF 2 32°F2 a
5°C
9°F b
❯ TF 5 TC a
9°F
5°Cb 1 32°F
Density
❯ Density 5 mass
volume
Matter can exist in three states:
❯ Solid
❯ Liquid
❯ Gas
Mixtures can be separated by methods involving only physical
changes:
❯ Distillation
❯ Filtration
❯ Chromatography
Compounds can be decomposed to elements only through
chemical changes.

''',

'''

Key terms
Section 2.2
law of conservation of mass
law of definite proportion
law of multiple proportions
Section 2.3
atomic masses
atomic weights
Avogadro’s hypothesis
Section 2.4
cathode-ray tubes
electrons
radioactivity
nuclear atom
nucleus
Section 2.5
proton
neutron
isotopes
atomic number
mass number
Section 2.6
chemical bond
covalent bond
molecule
chemical formula
structural formula
space-filling model
ball-and-stick model
ion
cation
anion
ionic bond
ionic solid
polyatomic ion
Fundamental laws
❯ Conservation of mass
❯ Definite proportion
❯ Multiple proportions
Dalton’s atomic theory
❯ All elements are composed of atoms.
❯ All atoms of a given element are identical.
❯ Chemical compounds are formed when atoms combine.
❯ Atoms are not changed in chemical reactions, but the way they are bound together changes.
Early atomic experiments and models
❯ Thomson model
❯ Millikan experiment
❯ Rutherford experiment
❯ Nuclear model
Atomic structure
❯ Small, dense nucleus contains protons and neutrons.
❯ Protons—positive charge
❯ Neutrons—no charge
❯ Electrons reside outside the nucleus in the relatively large remaining atomic volume.
❯ Electrons—negative charge, small mass (1y1840 of proton)
❯ Isotopes have the same atomic number but different mass numbers.
Atoms combine to form molecules by sharing electrons to form
covalent bonds.
❯ Molecules are described by chemical formulas.
❯ Chemical formulas show number and type of atoms.
❯ Structural formula
❯ Ball-and-stick model
❯ Space-filling model
Formation of ions
❯ Cation—formed by loss of an electron, positive charge
❯ Anion—formed by gain of an electron, negative charge
❯ Ionic bonds—formed by interaction of cations and anions
64 CHAPTER 2 Atoms, Molecules, and Ions
Copyright 2018 Cengage Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. WCN 02-200-203
The periodic table organizes elements in order of increasing
atomic number.
❯ Elements with similar properties are in columns, or groups.
❯ Metals are in the majority and tend to form cations.
❯ Nonmetals tend to form anions.
Compounds are named using a system of rules depending on the
type of compound.
❯ Binary compounds
❯ Type I—contain a metal that always forms the same cation
❯ Type II—contain a metal that can form more than one cation
❯ Type III—contain two nonmetals
❯ Compounds containing a polyatomic ion
Key terms
Section 2.7
periodic table
metal
nonmetal
group (family)
alkali metals
alkaline earth metals
halogens
noble gases
period
Section 2.8
binary compounds
binary ionic compounds
oxyanions
binary covalent compounds
acid

''',

'''

Key terms
chemical stoichiometry
Section 3.2
mass spectrometer
average atomic mass
Section 3.3
mole
Avogadro’s number
Section 3.4
molar mass
Section 3.5
conceptual problem solving
Section 3.6
mass percent
Section 3.7
empirical formula
molecular formula
Stoichiometry
❯ Deals with the amounts of substances consumed and/or produced in a chemical reaction.
❯ We count atoms by measuring the mass of the sample.
❯ To relate mass and the number of atoms, the average atomic mass is required.
Mole
❯ The amount of carbon atoms in exactly 12 g of pure 12C
❯ 6.022 3 1023 units of a substance
❯ The mass of 1 mole of an element 5 the atomic mass in grams
Molar mass
❯ Mass (g) of 1 mole of a compound or element
❯ Obtained for a compound by finding the sum of the average masses of its constituent atoms
Percent composition
❯ The mass percent of each element in a compound
❯ Mass percent 5 mass of element in 1 mole of substance
mass of 1 mole of substance
3 100%

Key terms
Section 3.8
chemical equation
reactants
products
balancing a chemical
equation
Section 3.10
mole ratio
Section 3.11
stoichiometric mixture
limiting reactant
theoretical yield
percent yield

Empirical formula
❯ The simplest whole-number ratio of the various types of atoms in a compound
❯ Can be obtained from the mass percent of elements in a compound
Molecular formula
❯ For molecular substances:
❯ The formula of the constituent molecules
❯ Always an integer multiple of the empirical formula
❯ For ionic substances:
❯ The same as the empirical formula
Chemical reactions
❯ Reactants are turned into products.
❯ Atoms are neither created nor destroyed.
❯ All of the atoms present in the reactants must also be present in the products.
Characteristics of a chemical equation
❯ Represents a chemical reaction
❯ Reactants on the left side of the arrow, products on the right side
❯ When balanced, gives the relative numbers of reactant and product molecules or ions
Stoichiometry calculations
❯ Amounts of reactants consumed and products formed can be determined from the balanced
chemical equation.
❯ The limiting reactant is the one consumed first, thus limiting the amount of product that can
form.
Yield
❯ The theoretical yield is the maximum amount that can be produced from a given amount of
the limiting reactant.
❯ The actual yield, the amount of product actually obtained, is always less than the theoretical
yield.
❯ Percent yield 5 actual yield 1g2
theoretical yield 1g2 3 100%

''',

'''
Key terms
aqueous solution
Section 4.1
polar molecule
hydration
solubility
Section 4.2
solute
solvent
electrical conductivity
strong electrolyte
weak electrolyte
nonelectrolyte
acid
strong acid
strong base
weak acid
weak base
Section 4.3
molarity
standard solution
dilution
Section 4.5
precipitation reaction
precipitate
Section 4.6
formula equation
complete ionic equation
spectator ions
net ionic equation
Section 4.8
acid
base
neutralization reaction
volumetric analysis
titration
stoichiometric (equivalence)
point
indicator
endpoint
Chemical reactions in solution are very important in everyday life.
Water is a polar solvent that dissolves many ionic and polar
substances.
Electrolytes
❯ Strong electrolyte: 100% dissociated to produce separate ions; strongly conducts an electric
current
❯ Weak electrolyte: Only a small percentage of dissolved molecules produce ions; weakly
conducts an electric current
❯ Nonelectrolyte: Dissolved substance produces no ions; does not conduct an electric current
Acids and bases
❯ Arrhenius model
❯ Acid: produces H1
❯ Base: produces OH2
❯ Brønsted–Lowry model
❯ Acid: proton donor
❯ Base: proton acceptor
❯ Strong acid: completely dissociates into separated H1 and anions
❯ Weak acid: dissociates to a slight extent
Molarity
❯ One way to describe solution composition
Molarity 1M2 5 moles of solute
volume of solution 1L2
❯ Moles solute 5 volume of solution (L) 3 molarity
❯ Standard solution: molarity is accurately known
Dilution
❯ Solvent is added to reduce the molarity
❯ Moles of solute after dilution 5 moles of solute before dilution
M1V1 5 M2V2
Types of equations that describe solution reactions
❯ Formula equation: All reactants and products are written as complete formulas
❯ Complete ionic equation: All reactants and products that are strong electrolytes are written
as separated ions
❯ Net ionic equation: Only those compounds that undergo a change are written; spectator ions
are not included
Solubility rules
❯ Based on experiment observation
❯ Help predict the outcomes of precipitation reactions

Key terms
Section 4.9
oxidation–reduction (redox)
reaction
oxidation state
oxidation
reduction
oxidizing agent (electron
acceptor)
reducing agent (electron
donor)
Section 4.10
half-reaction
Important types of solution reactions
❯ Acid–base reactions: involve a transfer of H1 ions
❯ Precipitation reactions: formation of a solid occurs
❯ Oxidation–reduction reactions: involve electron transfer
Titrations
❯ Measures the volume of a standard solution (titrant) needed to react with a substance in
solution
❯ Stoichiometric (equivalence) point: the point at which the required amount of titrant has
been added to exactly react with the substance being analyzed
❯ Endpoint: the point at which a chemical indicator changes color
Oxidation–reduction reactions
❯ Oxidation states are assigned using a set of rules to keep track of electron flow
❯ Oxidation: increase in oxidation state (a loss of electrons)
❯ Reduction: decrease in oxidation state (a gain of electrons)
❯ Oxidizing agent: gains electrons (is reduced)
❯ Reducing agent: loses electrons (is oxidized)
❯ Equations for oxidation–reduction reactions can be balanced by the oxidation states method

''',

'''
Key terms
Section 5.1
barometer
manometer
mm Hg
torr
standard atmosphere
pascal
Section 5.2
Boyle’s law
ideal gas
Charles’s law
absolute zero
Avogadro’s law
Section 5.3
universal gas constant
ideal gas law
Section 5.4
molar volume
standard temperature and
pressure (STP)
Section 5.5
Dalton’s law of partial
pressures
partial pressure
mole fraction
Section 5.6
kinetic molecular theory
(KMT)
root mean square velocity
joule
Section 5.7
diffusion
effusion
Graham’s law of effusion
Section 5.8
real gas
van der Waals equation
Section 5.10
atmosphere
air pollution
photochemical smog
acid rain
State of a gas
❯ The state of a gas can be described completely by specifying its pressure (P), volume (V),
temperature (T), and the amount (moles) of gas present (n)
❯ Pressure
❯ Common units
1 torr 5 1 mm Hg
 1 atm 5 760 torr
❯ SI unit: pascal
1 atm 5 101,325 Pa
Gas laws
❯ Discovered by observing the properties of gases
❯ Boyle’s law: PV 5 k
❯ Charles’s law: V 5 bT
❯ Avogadro’s law: V 5 an
❯ Ideal gas law: PV 5 nRT
❯ Dalton’s law of partial pressures: Ptotal 5 P1 1 P2 1 P3 1 c, where Pn represents the
partial pressure of component n in a mixture of gases
Kinetic molecular theory (KMT)
❯ Model that accounts for ideal gas behavior
❯ Postulates of the KMT:
❯ Volume of gas particles is zero
❯ No particle interactions
❯ Particles are in constant motion, colliding with the container walls to produce pressure
❯ The average kinetic energy of the gas particles is directly proportional to the temperature
of the gas in kelvins
Gas properties
❯ The particles in any gas sample have a range of velocities
❯ The root mean square (rms) velocity for a gas represents the average of the squares of the
particle velocities
urms 5 Å
3RT
M
❯ Diffusion: the mixing of two or more gases
❯ Effusion: the process in which a gas passes through a small hole into an empty chamber
Real gas behavior
❯ Real gases behave ideally only at high temperatures and low pressures
❯ Understanding how the ideal gas equation must be modified to account for real gas behavior
helps us understand how gases behave on a molecular level
❯ Van der Waals found that to describe real gas behavior we must consider particle interactions
and particle volumes
''',

'''

Key terms
Section 6.1
energy
law of conservation of energy
potential energy
kinetic energy
heat
work
pathway
state function (property)
system
surroundings
exothermic
endothermic
thermodynamics
first law of thermodynamics
internal energy
Section 6.2
enthalpy
calorimeter
calorimetry
heat capacity
specific heat capacity
molar heat capacity
constant-pressure calorimetry
constant-volume calorimetry
Section 6.3
Hess’s law
Energy
❯ The capacity to do work or produce heat
❯ Is conserved (first law of thermodynamics)
❯ Can be converted from one form to another
❯ Is a state function
❯ Potential energy: stored energy
❯ Kinetic energy: energy due to motion
❯ The internal energy for a system is the sum of its potential and kinetic energies
❯ The internal energy of a system can be changed by work and heat:
DE 5 q 1 w
Work
❯ Force applied over a distance
❯ For an expanding/contracting gas
❯ Not a state function
w 5 2PDV
Heat
❯ Energy flow due to a temperature difference
❯ Exothermic: energy as heat flows out of a system
❯ Endothermic: energy as heat flows into a system
❯ Not a state function
❯ Measured for chemical reactions by calorimetry

Key terms
Section 6.4
standard enthalpy of
formation
standard state
Section 6.5
fossil fuels
petroleum
natural gas
coal
greenhouse effect
Section 6.6
syngas
Enthalpy
❯ H 5 E 1 PV
❯ Is a state function
❯ Hess’s law: the change in enthalpy in going from a given set of reactants to a given set of products is the same whether the process takes place in one step or a series of steps
❯ Standard enthalpies of formation (DHf8) can be used to calculate DH for a chemical reaction
DH°reaction 5 S npDH°f 1products2 2 S nrDH°1reactants2
Energy use
❯ Energy sources from fossil fuels are associated with difficult supply and environmental
impact issues
❯ The greenhouse effect results from release into the atmosphere of gases, including carbon
dioxide, that strongly absorb infrared radiation, thus warming the earth
❯ Alternative fuels are being sought to replace fossil fuels:
❯ Hydrogen
❯ Syngas from coal
❯ Biofuels from plants such as corn and certain seed-producing plants

''',

'''

Key terms
Section 7.1
electromagnetic radiation
wavelength
frequency
Section 7.2
Planck’s constant
quantization
photon
photoelectric effect
dual nature of light
diffraction
diffraction pattern
Section 7.3
continuous spectrum
line spectrum
Section 7.4
quantum model
ground state
Section 7.5
standing wave
wave function
orbital
quantum (wave) mechanical
model
Heisenberg uncertainty
principle
probability distribution
radial probability distribution
Electromagnetic radiation
❯ Characterized by its wavelength (l), frequency (n), and speed (c 5 2.9979 3 108
 m/s)
ln 5 c
❯ Can be viewed as a stream of “particles” called photons, each with energy hn, where h is
Planck’s constant (6.626 3 10234 J*s)
Photoelectric effect
❯ When light strikes a metal surface, electrons are emitted
❯ Analysis of the kinetic energy and numbers of the emitted electrons led Einstein to suggest
that electromagnetic radiation can be viewed as a stream of photons
Hydrogen spectrum
❯ The emission spectrum of hydrogen shows discrete wavelengths
❯ Indicates that hydrogen has discrete energy levels
Bohr model of the hydrogen atom
❯ Using the data from the hydrogen spectrum and assuming angular momentum to be quantized, Bohr devised a model in which the electron traveled in circular orbits
❯ Although an important pioneering effort, this model proved to be entirely incorrect
Wave (quantum) mechanical model
❯ An electron is described as a standing wave
❯ The square of the wave function (often called an orbital) gives a probability distribution for
the electron position
❯ The exact position of the electron is never known, which is consistent with the Heisenberg
uncertainty principle: It is impossible to know accurately both the position and the momentum of a particle simultaneously
❯ Probability maps are used to define orbital shapes
❯ Orbitals are characterized by the quantum numbers n, ,, and m,

Key terms
Section 7.6
quantum numbers
principal quantum number (n)
angular momentum quantum
number (,)
magnetic quantum
number (m,)
subshell
Section 7.7
nodal surface
node
degenerate orbital
Section 7.8
electron spin
electron spin quantum
number (ms)
Pauli exclusion principle
Section 7.9
polyelectronic atoms
Section 7.11
aufbau principle
Hund’s rule
valence electrons
core electrons
transition metals
lanthanide series
actinide series
main-group elements
(representative elements)
Section 7.12
first ionization energy
second ionization energy
electron affinity
atomic radii
Section 7.13
metalloids (semimetals)
Electron spin
❯ Described by the spin quantum number ms, which can have values of 61
2
❯ Pauli exclusion principle: No two electrons in a given atom can have the same set of quantum
numbers n, ,, m,, and ms
❯ Only two electrons with opposite spins can occupy a given orbital
Periodic table
❯ By populating the orbitals from the wave mechanical model (the aufbau principle), the form
of the periodic table can be explained
❯ According to the wave mechanical model, atoms in a given group have the same valence
(outer) electron configuration
❯ The trends in properties such as ionization energies and atomic radii can be explained in
terms of the concepts of nuclear attraction, electron repulsions, shielding, and penetration

''',

'''

Key terms
Section 8.1
bond energy
ionic bonding
ionic compound
Coulomb’s law
bond length
covalent bonding
polar covalent bond
Section 8.2
electronegativity
Section 8.3
dipolar
dipole moment
Section 8.4
isoelectronic ions
Section 8.5
lattice energy
Section 8.8
single bond
double bond
triple bond
Chemical bonds
❯ Hold groups of atoms together
❯ Occur when a group of atoms can lower its total energy by aggregating
❯ Types of chemical bonds
❯ Ionic: electrons are transferred to form ions
❯ Covalent: equal sharing of electrons
❯ Polar covalent: unequal electron sharing
❯ Percent ionic character of a bond XOY
Measured dipole moment of XiY
Calculated dipole moment for X1 Y2 3 100%
❯ Electronegativity: the relative ability of an atom to attract shared electrons
❯ The polarity of a bond depends on the electronegativity difference of the bonded atoms
❯ The spatial arrangement of polar bonds in a molecule determines whether the molecule has
a dipole moment
Ionic bonding
❯ An ion has a different size than its parent atom
❯ An anion is larger than its parent atom
❯ A cation is smaller than its parent atom
❯ Lattice energy: the change in energy when ions are packed together to form an ionic solid

''',

'''

Key terms
Section 8.9
localized electron (LE) model
lone pair
bonding pair
Section 8.10
Lewis structure
duet rule
octet rule
Section 8.12
resonance
resonance structure
formal charge
Section 8.13
molecular structure
valence shell electron-pair
repulsion (VSEPR) model
linear structure
trigonal planar structure
tetrahedral structure
trigonal pyramid
trigonal bipyramid
octahedral structure
square planar structure
Bond energy
❯ The energy necessary to break a covalent bond
❯ Increases as the number of shared pairs increases
❯ Can be used to estimate the enthalpy change for a chemical reaction
Lewis structures
❯ Show how the valence electron pairs are arranged among the atoms in a molecule or polyatomic ion
❯ Stable molecules usually contain atoms that have their valence orbitals filled
❯ Leads to a duet rule for hydrogen
❯ Leads to an octet rule for second-row elements
❯ The atoms of elements in the third row and beyond can exceed the octet rule
❯ Several equivalent Lewis structures can be drawn for some molecules, a concept called
resonance
❯ When several nonequivalent Lewis structures can be drawn for a molecule, formal charge is
often used to choose the most appropriate structure(s)
VSEPR model
❯ Based on the idea that electron pairs will be arranged around a central atom in a way that
minimizes the electron repulsions
❯ Can be used to predict the geometric structure of most molecules

''']

phys_text = [
    
'''

Kinematics deals with the description of how objects
move. The description of the motion of any object must
always be given relative to some particular reference frame.
The displacement of an object is the change in position of
the object.

Average speed is the distance traveled divided by the elapsed
time or time interval, (the time period over which we choose
to make our observations). An object’s average velocity over
a particular time interval is

v = x/t

where x is the displacement during the time interval t
The instantaneous velocity, whose magnitude is the same
as the instantaneous speed, is defined as the average velocity
taken over an infinitesimally short time interval.

Acceleration is the change of velocity per unit time. An
object’s average acceleration over a time interval t is

a = v/t

where v is the change of velocity during the time interval t
Instantaneous acceleration is the average acceleration taken
over an infinitesimally short time interval.

If an object has position and velocity at time and
moves in a straight line with constant acceleration, the velocity v
and position x at a later time are related to the acceleration a,
the initial position x0 and the initial velocity v0 by:

v = v0 + at,
x = x0 + v0 t + 1/2 at^2
v^2 = v0^2 + 2a(x-x0)
v_average = (v+v0)/2

Objects that move vertically near the surface of the Earth,
either falling or having been projected vertically up or down,
move with the constant downward acceleration due to gravity,
whose magnitude is g = 9.80 m/s^2 if air resistance can be
ignored. We can apply Eqs. 2–11 for constant acceleration to
objects that move up or down freely near the Earth’s surface.
The slope of a curve at any point on a graph is the slope
of the tangent to the curve at that point. On a graph of position vs. time, the slope is equal to the instantaneous velocity.
On a graph of velocity vs. time, the slope is the acceleration.

''',

'''

A quantity such as velocity, that has both a magnitude and a
direction, is called a vector. A quantity such as mass, that has
only a magnitude, is called a scalar. On diagrams, vectors are
represented by arrows.
Addition of vectors can be done graphically by placing the
tail of each successive arrow at the tip of the previous one. The
sum, or resultant vector, is the arrow drawn from the tail of the
first vector to the tip of the last vector. Two vectors can also be
added using the parallelogram method.
Vectors can be added more accurately by adding their
components along chosen axes with the aid of trigonometric
functions. A vector of magnitude V making an angle with the
axis has components

Vx = V cos u, Vy = V sin u.

Given the components, we can find a vector’s magnitude and
direction from

V = sqrt(Vx^2+Vy^2), tan(theta) = Vy/Vx

''',

'''

Projectile motion is the motion of an object in the air near the
Earth’s surface under the effect of gravity alone. It can be analyzed
as two separate motions if air resistance can be ignored. The horizontal component of motion is at constant velocity, whereas the
vertical component is at constant acceleration, just as for an
object falling vertically under the action of gravity.
The velocity of an object relative to one frame of reference can be found by vector addition if its velocity relative to a
second frame of reference, and the relative velocity of the two
reference frames, are known.

Newton’s three laws of motion are the basic classical laws
describing motion.
Newton’s first law (the law of inertia) states that if the net
force on an object is zero, an object originally at rest remains
at rest, and an object in motion remains in motion in a straight
line with constant velocity.
Newton’s second law states that the acceleration of an
object is directly proportional to the net force acting on it, and
inversely proportional to its mass:
(4;1)
Newton’s second law is one of the most important and fundamental laws in classical physics.
Newton’s third law states that whenever one object exerts
a force on a second object, the second object always exerts a
force on the first object which is equal in magnitude but opposite in direction:
(4;2)
where is the force on object B exerted by object A.
The tendency of an object to resist a change in its motion
is called inertia. Mass is a measure of the inertia of an object.
F
B
BA
F
B
AB = –F
B
BA
©F
B
= ma
B
.
Weight refers to the gravitational force on an object, and is
equal to the product of the object’s mass m and the acceleration
of gravity
(4;3)
Force, which is a vector, can be considered as a push or pull;
or, from Newton’s second law, force can be defined as an action
capable of giving rise to acceleration. The net force on an object
is the vector sum of all forces acting on that object.
When two objects slide over one another, the force of
friction that each object exerts on the other can be written
approximately as where is the normal force
(the force each object exerts on the other perpendicular to their
contact surfaces), and is the coefficient of kinetic friction. If
the objects are at rest relative to each other, then is just
large enough to hold them at rest and satisfies the inequality
where is the coefficient of static friction.
For solving problems involving the forces on one or more
objects, it is essential to draw a free-body diagram for each
object, showing all the forces acting on only that object.
Newton’s second law can be applied to the vector components
for each object.

''',

'''

An object moving in a circle of radius r with constant speed v is
said to be in uniform circular motion. It has a radial acceleration
that is directed radially toward the center of the circle (also
called centripetal acceleration), and has magnitude
(5;1)
The velocity vector and the acceleration vector are continually changing in direction, but are perpendicular to each other
at each moment.
A force is needed to keep an object revolving in a circle,
and the direction of this force is toward the center of the circle.
This force could be due to gravity (as for the Moon), to tension
in a cord, to a component of the normal force, or to another
type of force or combination of forces.
[*When the speed of circular motion is not constant, the
acceleration has two components, tangential as well as
centripetal.]
Newton’s law of universal gravitation states that every
particle in the universe attracts every other particle with a force
a
B
R
aR = v2
r .
aR
proportional to the product of their masses and inversely proportional to the square of the distance between them:
(5;4)
The direction of this force is along the line joining the two
particles, and the force is always attractive. It is this gravitational
force that keeps the Moon revolving around the Earth, and the
planets revolving around the Sun.
Satellites revolving around the Earth are acted on by
gravity, but “stay up” because of their high tangential speed.
Newton’s three laws of motion, plus his law of universal
gravitation, constituted a wide-ranging theory of the universe.
With them, motion of objects on Earth and in space could be
accurately described. And they provided a theoretical base for
Kepler’s laws of planetary motion.
The four fundamental forces in nature are (1) the gravitational force, (2) the electromagnetic force, (3) the strong nuclear
force, and (4) the weak nuclear force. The first two fundamental
forces are responsible for nearly all “everyday” forces.

''',

'''

Work is done on an object by a force when the object moves
through a distance d. If the direction of a constant force
makes an angle with the direction of motion, the work done
by this force is
(6;1)
Energy can be defined as the ability to do work. In SI units,
work and energy are measured in joules
Kinetic energy (KE) is energy of motion. An object of
mass m and speed v has translational kinetic energy
(6;3)
The work-energy principle states that the net work done on
an object (by the net force) equals the change in kinetic energy
of that object:
(6;4)
Potential energy (PE) is energy associated with forces that
depend on the position or configuration of objects. Gravitational
potential energy is
(6;6)
where y is the height of the object of mass m above an arbitrary
reference point. Elastic potential energy is given by
(6;9)
for a stretched or compressed spring, where x is the displacement
peel = 1
2 kx2
peG = mgy,
Wnet = ¢ke = 1
2 mv2
2 - 1
2 mv1
2
.
ke = 1
2 mv2
.
(1 J = 1 Nm).
W = Fd cos u.
u
F
B
from the unstretched position and k is the spring stiffness constant. Other potential energies include chemical, electrical, and
nuclear energy. The change in potential energy when an object
changes position is equal to the external work needed to take
the object from one position to the other.
Potential energy is associated only with conservative forces,
for which the work done by the force in moving an object from
one position to another depends only on the two positions and
not on the path taken. Nonconservative forces like friction are
different—work done by them does depend on the path taken
and potential energy cannot be defined for them.
The law of conservation of energy states that energy can
be transformed from one type to another, but the total energy
remains constant. It is valid even when friction is present,
because the heat generated can be considered a form of energy
transfer. When only conservative forces act, the total mechanical
energy is conserved:
(6;12)
When nonconservative forces such as friction act, then
(6;10, 6;15)
where is the work done by nonconservative forces.
Power is defined as the rate at which work is done, or the
rate at which energy is transformed. The SI unit of power is
the watt (1 W = 1 Js).

''',

'''

The linear momentum, of an object is defined as the product
of its mass times its velocity,
(7;1)
In terms of momentum, Newton’s second law can be written
as
(7;2)
That is, the rate of change of momentum of an object equals
the net force exerted on it.
When the net external force on a system of objects is
zero, the total momentum remains constant. This is the law of
conservation of momentum. Stated another way, the total
momentum of an isolated system of objects remains constant.
The law of conservation of momentum is very useful in
dealing with collisions. In a collision, two (or more) objects
interact with each other over a very short time interval, and the
force each exerts on the other during this time interval is very
large compared to any other forces acting.
The impulse delivered by a force on an object is defined as
(7;5)
where is the average force acting during the (usually very
short) time interval The impulse is equal to the change in
momentum of the object:
(7;4)
Total momentum is conserved in any collision as long as
any net external force is zero or negligible. If and
are the momenta of two objects before the collision and mA v
B
A
œ
mB v
B
mA v B B
A
Impulse = F
B
¢t = ¢p
B
.
¢t.
F
B
Impulse = F
B
¢t,
©F
B
= ¢p
B
¢t
.
p
B
= mv
B
.
p
B
,
Summary
An interesting application is the discovery of nearby stars (see Section 5–8)
that seem to “wobble.” It could be that a planet
orbits the star, and each exerts a gravitational force on the other. The planets are
too small and too far away to be observed directly by telescopes. But the slight
wobble in the motion of the star suggests that both the planet and the star (its sun)
orbit about their mutual center of mass, and hence the star appears to have a wobble.
Irregularities in the star’s motion can be measured to high accuracy, yielding
information on the size of the planets’ orbits and their masses. See Fig. 5–30 in
Chapter 5.
and are their momenta after, then momentum conservation tells us that
(7;3)
for this two-object system.
Total energy is also conserved. But this may not be helpful
unless kinetic energy is conserved, in which case the collision is
called an elastic collision and we can write
(7;6)
If kinetic energy is not conserved, the collision is called
inelastic. Macroscopic collisions are generally inelastic.
A completely inelastic collision is one in which the colliding
objects stick together after the collision.
The center of mass (CM) of an extended object (or group of
objects) is that point at which the net force can be considered
to act, for purposes of determining the translational motion of
the object as a whole. The x component of the CM for objects
with mass is given by
(7;9a)
[*The center of mass of a system of total mass M moves in
the same path that a particle of mass M would move if subjected
to the same net external force. In equation form, this is Newton’s
second law for a system of particles (or extended objects):
(7;11)
where M is the total mass of the system, is the acceleration
of the CM of the system, and is the total (net) external
force acting on all parts of the system.

''',

'''

When a rigid object rotates about a fixed axis, each point of the
object moves in a circular path. Lines drawn perpendicularly
from the rotation axis to various points in the object all sweep
out the same angle in any given time interval.
Angles are conventionally measured in radians, where one
radian is the angle subtended by an arc whose length is equal
to the radius, or
Angular velocity, is defined as the rate of change of
angular position:
(8;2)
All parts of a rigid object rotating about a fixed axis have the
same angular velocity at any instant.
Angular acceleration, is defined as the rate of change of
angular velocity:
(8;3)
The linear velocity v and acceleration a of a point located
a distance r from the axis of rotation are related to and
by
(8;4)
(8;5)
(8;6)
where and are the tangential and radial (centripetal)
components of the linear acceleration, respectively.
The frequency f is related to by
(8;7)
and to the period T by
(8;8)
If a rigid object undergoes uniformly accelerated rotational
motion equations analogous to those for linear
motion are valid:
(8;9)
The torque due to a force exerted on a rigid object is
equal to
(8;10)
where called the lever arm, is the perpendicular distance
from the axis of rotation to the line along which the force acts,
and is the angle between and F r. B
u
r⊥ ,
t = r⊥ F = rF⊥ = rF sin u,
F
B
v2 = v0
2 + 2au, j = v + v0
2 .
v = v0 + at, u = v0 t + 1
2 at
2 ,
(a = constant),
T = 1f.
v = 2pf,
v
atan aR
aR = v2
r,
atan = ra,
v = rv,
av
a = ¢v
¢t
.
a,
v = ¢u
¢t
.
v,
 1 rad L 57.3°.
 2p rad = 360°
u
The rotational equivalent of Newton’s second law is
(8;14)
where is the moment of inertia of the object about
the axis of rotation. I depends not only on the mass of the
object but also on how the mass is distributed relative to the
axis of rotation. For a uniform solid cylinder or sphere of
radius R and mass M, I has the form or
respectively (see Fig. 8–20).
The rotational kinetic energy of an object rotating about a
fixed axis with angular velocity is
(8;15)
For an object both translating and rotating, the total
kinetic energy is the sum of the translational kinetic energy of
the object’s center of mass plus the rotational kinetic energy
of the object about its center of mass:
(8;16)
as long as the rotation axis is fixed in direction.
The angular momentum L of an object rotating about a
fixed rotation axis is given by
(8;18)
Newton’s second law, in terms of angular momentum, is
(8;19)
If the net torque on an object is zero, so
This is the law of conservation of angular
momentum for a rotating object.
The following Table summarizes angular (or rotational)
quantities, comparing them to their translational analogs.
Translation Rotation Connection
x
v
a
m I
F
[*Angular velocity, angular acceleration, and angular
momentum are vectors. For a rigid object rotating about a
fixed axis, the vectors , and point along the rotation
axis. The direction of or is given by the L right-hand rule.] B
V
B
L
B
A
B
V
B
,
©t = ¢L
¢t
©F = ¢p
¢t
©F = ma ©t = Ia
W = Fd W = tu
p = mv L = Iv
1
2 Iv2 ke = 1
2 mv2
t t = rF sin u
I = ©mr2
a atan = ra
v v = rv
u x = ru
L = constant.
¢L¢t = 0,
©t = ¢L
¢t
.

''',

'''

An object at rest is said to be in equilibrium. The subject concerned with the determination of the forces within a structure
at rest is called statics.
The two necessary conditions for an object to be in equilibrium are (1) the vector sum of all the forces on it must
be zero, and (2) the sum of all the torques (calculated about
any arbitrary axis) must also be zero. For a two-dimensional
problem we can write
(9;1, 9;2)
It is important when doing statics problems to apply the
equilibrium conditions to only one object at a time.
An object in static equilibrium is said to be in (a) stable,
(b) unstable, or (c) neutral equilibrium, depending on whether a
slight displacement leads to (a) a return to the original position,
(b) further movement away from the original position, or
(c) rest in the new position. An object in stable equilibrium is
also said to be in balance.
Hooke’s law applies to many elastic solids, and states
that the change in length of an object is proportional to the
©Fx = 0, ©Fy = 0, ©t = 0.
applied force:
(9;3)
If the force is too great, the object will exceed its elastic limit,
which means it will no longer return to its original shape when
the distorting force is removed. If the force is even greater, the
ultimate strength of the material can be exceeded, and the
object will fracture. The force per unit area acting on an object
is the stress, and the resulting fractional change in length is the
strain.
The stress on an object is present within the object and
can be of three types: compression, tension, or shear. The ratio
of stress to strain is called the elastic modulus of the material.
Young’s modulus applies for compression and tension, and the
shear modulus for shear. Bulk modulus applies to an object
whose volume changes as a result of pressure on all sides. All
three moduli are constants for a given material when distorted
within the elastic region.
[*Arches and domes are special ways to span a space that
allow the stresses to be managed well.]

''',

'''
The three common phases of matter are solid, liquid, and gas.
Liquids and gases are collectively called fluids, meaning they
have the ability to flow. The density of a material is defined as
its mass per unit volume:
(10;1)
Specific gravity (SG) is the ratio of the density of the material to
the density of water (at 4°C).
Pressure is defined as force per unit area:
(10;2)
The pressure P at a depth h in a liquid of constant density , due
to the weight of the liquid, is given by
(10;3a)
where g is the acceleration due to gravity.
Pascal’s principle says that an external pressure applied to
a confined fluid is transmitted throughout the fluid.
Pressure is measured using a manometer or other type of
gauge. A barometer is used to measure atmospheric pressure.
Standard atmospheric pressure (average at sea level) is
Gauge pressure is the total (absolute) pressure minus atmospheric pressure.
Archimedes’ principle states that an object submerged
wholly or partially in a fluid is buoyed up by a force equal to
the weight of fluid it displaces (FB = mF g = rFVdispl g).
1.013 * 105 Nm2
.
P = rgh,
r
P = F
A .
r = m
V .
Fluid flow can be characterized either as streamline
(also called laminar), in which the layers of fluid move
smoothly and regularly along paths called streamlines, or as
turbulent, in which case the flow is not smooth and regular but
is characterized by irregularly shaped whirlpools.
Fluid flow rate is the mass or volume of fluid that passes a
given point per unit time. The equation of continuity states
that for an incompressible fluid flowing in an enclosed tube,
the product of the velocity of flow and the cross-sectional area
of the tube remains constant:
(10;4)
Bernoulli’s principle tells us that where the velocity of a
fluid is high, the pressure in it is low, and where the velocity is
low, the pressure is high. For steady laminar flow of an incompressible and nonviscous fluid, Bernoulli’s equation, which is
based on the law of conservation of energy, is
(10;5)
for two points along the flow.
[*Viscosity refers to friction within a fluid and is essentially
a frictional force between adjacent layers of fluid as they move
past one another.]
[*Liquid surfaces hold together as if under tension
(surface tension), allowing drops to form and objects like needles
and insects to stay on the surface.
'''

]

bio_text = [

'''
CONCEPT 1.1
Studying the diverse forms of life reveals common
themes (pp. 2–7)
Theme: Organization
t The hierarchy of life unfolds as follows: biosphere > ecosystem >
community > population > organism > organ system > organ
> tissue > cell > organelle > molecule > atom. With each step
up, new properties emerge (emergent properties) as a result of
interactions among components at the lower levels.
t Structure and function are correlated at all levels of biological
organization. The cell is the lowest level of organization that can
perform all activities required for life. Cells are either prokaryotic
or eukaryotic. Eukaryotic cells have a DNA-containing nucleus
and other membrane-enclosed organelles. Prokaryotic cells lack
such organelles.
Theme: Information
t Genetic information is encoded in the nucleotide sequences
of DNA. It is DNA that transmits heritable information from
parents to offspring. DNA sequences (called genes) program a
cell’s protein production by being transcribed into RNA and then
translated into specific proteins, a process called gene expression. Gene expression also produces RNAs that are not translated into protein but serve other important functions.
Theme: Energy and Matter
t Energy flows through an ecosystem. All organisms must perform work, which requires energy. Producers convert energy
from sunlight to chemical energy, some of which is then passed
on to consumers (the rest is lost from the ecosystem as heat).
Chemicals cycle between organisms and the environment.
Theme: Interactions
Plants take up nutrients from the soil and chemicals from the air and
use energy from the sun. Interactions among plants, animals,
and other organisms affect the participants in varying ways.
CONCEPT 1.2
The Core Theme: Evolution accounts for the unity
and diversity of life (pp. 7–11)
t Biologists classify species according to a system of broader and
broader groups. Domain Bacteria and domain Archaea consist of prokaryotes. Domain Eukarya, the eukaryotes, includes
various groups of protists as well as plants, fungi, and animals.
As diverse as life is, there is also evidence of remarkable unity,
which is revealed in the similarities between different kinds of
organisms.
t Darwin proposed natural selection as the mechanism for evolutionary adaptation of populations to their environments. Each
species is one twig of a branching tree of life extending back in
time through ancestral species more and more remote. All of life
is connected through its long evolutionary history.

Biological inquiry entails forming and testing
hypotheses based on observations of nature
(pp. 11–16)
t In scientific inquiry, scientists make observations (collect data)
and use inductive reasoning to draw a general conclusion,
which can be developed into a testable hypothesis. Deductive
reasoning makes predictions that can be used to test hypotheses.
Scientific hypotheses must be falsifiable.
t Controlled experiments, such as the study investigating coat
color in mouse populations, are designed to demonstrate the effect of one variable by testing control groups and experimental
groups that differ in only that one variable.
t A scientific theory is broad in scope, generates new hypotheses,
and is supported by a large body of evidence.
t Scientists must be able to repeat each other’s results, so integrity
is key. Biologists approach questions at different levels; their approaches complement each other. Technology is a method or
device that applies scientific knowledge for some specific purpose that affects society as well as for scientific research. Diversity among scientists promotes progress in science.

''',

'''

CONCEPT 2.1
Matter consists of chemical elements in pure form and
in combinations called compounds (pp. 19–20)
• Elements cannot be broken down chemically to other substances. A compound contains two or more different elements
in a fixed ratio. Oxygen, carbon, hydrogen, and nitrogen make up
approximately 96% of living matter.
CONCEPT 2.2
An element’s properties depend on the structure
of its atoms (pp. 20–24)
• An atom, the smallest unit of an element, has the following
components:
• An electrically neutral atom has equal numbers of electrons and
protons; the number of protons determines the atomic number.
Isotopes of an element differ from each other in neutron number
and therefore mass. Unstable isotopes give off particles and energy as radioactivity.
• In an atom, electrons occupy specific electron shells; the electrons
in a shell have a characteristic energy level. Electron distribution in
shells determines the chemical behavior of an atom. An atom that
has an incomplete outer shell, the valence shell, is reactive.
DRAW IT Draw the electron distribution diagrams for neon
(10Ne) and argon (18Ar).
CONCEPT 2.3
The formation and function of molecules depend on
chemical bonding between atoms (pp. 24–28)
• Chemical bonds form when atoms interact and complete their
valence shells. Covalent bonds form when pairs of electrons
are shared. H2 has a single bond: H i H. A double bond is the
sharing of two pairs of electrons, as in O w O.
• Molecules consist of two or more covalently bonded atoms. The
attraction of an atom for the electrons of a covalent bond is its
electronegativity. Electrons of a polar covalent bond are pulled
closer to the more electronegative atom.
• An ion forms when an atom or molecule gains or loses an electron and becomes charged. An ionic bond is the attraction between two oppositely charged ions, such as Na+ and Cl−.
• Weak bonds reinforce the shapes of large molecules and help molecules adhere to each other. A hydrogen bond is an attraction between a hydrogen atom carrying a partial positive charge (δ+) and
an electronegative atom (δ−). Van der Waals interactions occur
between transiently positive and negative regions of molecules.

• Molecular shape is usually the basis for the recognition of one
biological molecule by another.
CONCEPT 2.4
Chemical reactions make and break chemical bonds
(pp. 28–29)
• Chemical reactions change reactants into products while conserving matter. All chemical reactions are theoretically reversible.
Chemical equilibrium is reached when the forward and reverse
reaction rates are equal.
What would happen to the concentration of products if more
reactants were added to a reaction that was in chemical equilibrium How would this addition affect the equilibrium
CONCEPT 2.5
Hydrogen bonding gives water properties that help
make life possible on Earth (pp. 29–37)
• A hydrogen bond forms when the
slightly negatively charged oxygen of one
water molecule is attracted to the slightly
positively charged hydrogen of a nearby
water molecule. Hydrogen bonding
between water molecules is the
basis for water’s properties.
• Hydrogen bonding keeps
water molecules close to each
other, giving water cohesion.
Hydrogen bonding is also
responsible for water’s surface
tension.
• Water has a high specific heat: Heat is absorbed when hydrogen
bonds break and is released when hydrogen bonds form. This
helps keep temperatures relatively steady, within limits that permit life. Evaporative cooling is based on water’s high heat of
vaporization. The evaporative loss of the most energetic water
molecules cools a surface.
• Ice floats because it is less
dense than liquid water.
This property allows life to
exist under the frozen surfaces
of lakes and seas.
• Water is an unusually versatile solvent because its polar
molecules are attracted to ions
and polar substances that can form hydrogen bonds. Hydrophilic
substances have an affinity for water; hydrophobic substances do
not. Molarity, the number of moles of solute per liter of solution,
is used as a measure of solute concentration in solutions. A mole
is a certain number of molecules of a substance. The mass of a
mole of a substance in grams is the same as the molecular mass
in daltons.
• A water molecule can transfer an H+ to another water molecule
to form H3O+ (represented simply by H+) and OH−.

The concentration of H+ is
expressed as pH; pH = –log
[H+]. A buffer consists of an
acid-base pair that combines
reversibly with hydrogen
ions, allowing it to resist pH
changes.
• The burning of fossil fuels
increases the amount of CO2
in the atmosphere. Some CO2
dissolves in the oceans, causing ocean acidification, which
has potentially grave consequences for coral reefs.

''',

'''

Carbon atoms can form diverse molecules by bonding
to four other atoms (pp. 41–44)
t Carbon, with a valence of 4, can bond to various other atoms,
including O, H, and N. Carbon can also bond to other carbon
atoms, forming the carbon skeletons of organic compounds.
These skeletons vary in length and shape.
t Chemical groups attached to the carbon skeletons of organic
molecules participate in chemical reactions (functional
groups) or contribute to function by affecting molecular shape.
t ATP (adenosine triphosphate) can react with water, releasing
energy that can be used by the cell.

Macromolecules are polymers, built from monomers
(pp. 44–45)
t Proteins, nucleic acids, and large carbohydrates (polysaccharides)
are polymers, which are chains of monomers. Monomers form
larger molecules by dehydration reactions, in which water molecules are released. Polymers can disassemble by the reverse process, hydrolysis. In cells, dehydration reactions and hydrolysis
are catalyzed by enzymes. An immense variety of polymers can
be built from a small set of monomers.

Large Biological Molecules Components Examples Functions
CONCEPT 3.3
Carbohydrates serve as fuel
and building material (pp.
45–49)
Compare the composition,
structure, and function of
starch and cellulose. 
Monosaccharides: glucose,
fructose
Fuel; carbon sources that can be
converted to other molecules or
combined into polymers Disaccharides: lactose, sucrose
Polysaccharides:
t Cellulose (plants)
t Starch (plants)
t Glycogen (animals)
t Chitin (animals and fungi)
t Strengthens plant cell walls
t Stores glucose for energy in plants
t Stores glucose for energy in animals
t Strengthens exoskeletons and fungal
cell walls
CONCEPT 3.4
Lipids are a diverse group
of hydrophobic molecules
(pp. 49–51)
Triacylglycerols (fats or oils):
glycerol + 3 fatty acids
Important energy source
Phospholipids: phosphate group
+ glycerol + 2 fatty acids
Lipid bilayers of membranes
Steroids: four fused rings with
attached chemical groups
t Component of cell membranes
(cholesterol)
t Signaling molecules that travel through
the body (hormones)
CONCEPT 3.5
Proteins include a diversity
of structures, resulting in
a wide range of functions
(pp. 51–59)
t Enzymes
t Structural proteins
t Storage proteins
t Transport proteins
t Hormones
t Receptor proteins
t Motor proteins
t Defensive proteins
t Catalyze chemical reactions
t Provide structural support
t Store amino acids
t Transport substances
t Coordinate organismal responses
t Receive signals from outside cell
t Function in cell movement
t Protect against disease

Large Biological Molecules Components Examples Functions
CONCEPT 3.6
Nucleic acids store, transmit,
and help express hereditary
information (pp. 60–63)
DNA:
t Sugar = deoxyribose
t Nitrogenous bases = C, G, A, T
t Usually double-stranded
RNA:
t Sugar = ribose
t Nitrogenous bases = C, G, A, U
t Usually single-stranded
Stores hereditary information
Various functions in gene expression,
including carrying instructions from DNA
to ribosomes

''',

'''

Biologists use microscopes and the tools of
biochemistry to study cells (pp. 67–69)
• Improvements in microscopy that affect the parameters of magnification, resolution, and contrast have catalyzed progress in the
study of cell structure. The light microscope (LM) and electron
microscope (EM), as well as other types, remain important tools.
• Cell biologists can obtain pellets enriched in particular cellular components by centrifuging disrupted cells at sequential speeds, a process known as cell fractionation. Larger cellular components are in
the pellet after lower-speed centrifugation, and smaller components
are in the pellet after higher-speed centrifugation

Eukaryotic cells have internal membranes that
compartmentalize their functions (pp. 69–74)
• All cells are bounded by a plasma membrane.
• Prokaryotic cells lack nuclei and other membrane-enclosed
organelles, while eukaryotic cells have internal membranes that
compartmentalize cellular functions.
• The surface-to-volume ratio is an important parameter affecting
cell size and shape.
• Plant and animal cells have most of the same organelles: a nucleus,
endoplasmic reticulum, Golgi apparatus, and mitochondria. Some
organelles are found only in plant or in animal cells. Chloroplasts
are present only in cells of photosynthetic eukaryotes.

CONCEPT 4.3
The eukaryotic cell’s genetic
instructions are housed in the
nucleus and carried out by the
ribosomes (pp. 74–76)
  Surrounded by nuclear envelope
(double membrane) perforated
by nuclear pores; nuclear
envelope continuous with
endoplasmic reticulum (ER)
Houses chromosomes, which are
made of chromatin (DNA and
proteins); contains nucleoli, where
ribosomal subunits are made;
pores regulate entry and exit of
materials
Ribosome Two subunits made of ribosomal
RNA and proteins; can be free in
cytosol or bound to ER
Protein synthesis
CONCEPT 4.4
The endomembrane system
regulates protein traffic and
performs metabolic functions
in the cell (pp. 76–81)
Endoplasmic reticulum Extensive network of membranebounded tubules and sacs;
membrane separates lumen from
cytosol; continuous with nuclear
envelope
Smooth ER: synthesis of lipids,
metabolism of carbohydrates,
Ca2+
 storage, detoxification of
drugs and poisons
Rough ER: aids in synthesis of
secretory and other proteins
from bound ribosomes; adds
carbohydrates to proteins to make
glycoproteins; produces new
membrane
Golgi apparatus Stacks of flattened membranous
sacs; has polarity (cis and trans
faces)
Modification of proteins,
carbohydrates on proteins, and
phospholipids; synthesis of many
polysaccharides; sorting of Golgi
products, which are then released
in vesicles
Lysosome Membranous sac of hydrolytic
enzymes (in animal cells)
Breakdown of ingested substances,
cell macromolecules, and damaged
organelles for recycling
Large membrane-bounded
vesicle
Digestion, storage, waste disposal,
water balance, plant cell growth
and protection
CONCEPT 4.5
Mitochondria and chloroplasts
change energy from one form
to another (pp. 81–84)
Mitochondrion Bounded by double membrane;
inner membrane has infoldings
(cristae)
Cellular respiration
  Chloroplast Typically two membranes around
fluid stroma, which contains
thylakoids stacked into grana
(in cells of photosynthetic
eukaryotes, including plants)
Photosynthesis
Specialized metabolic
compartment bounded by a
single membrane
Contains enzymes that transfer
hydrogen atoms from certain
molecules to oxygen, producing
hydrogen peroxide (H2O2) as a
by-product; H2O2 is converted to
water by another enzyme

CONCEPT 4.6
The cytoskeleton is a network of fibers that organizes
structures and activities in the cell (pp. 84–88)
• The cytoskeleton functions in structural support for the cell and
in motility and signal transmission.
• Microtubules shape the cell, guide organelle movement, and
separate chromosomes in dividing cells. Cilia and flagella are
motile appendages containing microtubules. Primary cilia play
sensory and signaling roles. Microfilaments are thin rods functioning in muscle contraction, amoeboid movement, cytoplasmic
streaming, and support of microvilli. Intermediate filaments
support cell shape and fix organelles in place.
CONCEPT 4.7
Extracellular components and connections between
cells help coordinate cellular activities (pp. 88–91)
• Plant cell walls are made of cellulose fibers embedded in other
polysaccharides and proteins.
• Animal cells secrete glycoproteins and proteoglycans that form
the extracellular matrix (ECM), which functions in support,
adhesion, movement, and regulation.
• Cell junctions connect neighboring cells in plants and animals.
Plants have plasmodesmata that pass through adjoining cell
walls. Animal cells have tight junctions, desmosomes, and
gap junctions.

'''

,

'''

concentration gradient. Ion channels facilitate the diffusion of
ions across a membrane. Carrier proteins can undergo changes
in shape that transport bound solutes.
Describe the free water concentration inside and out.
CONCEPT 5.4
Active transport uses energy to move solutes against
their gradients (pp. 103–106)
t Specific membrane proteins use energy,
usually in the form of ATP, to do the work
of active transport.
t Ions can have both a concentration (chemical) gradient and an electrical gradient
(voltage). These combine in the electrochemical gradient, which determines the
net direction of ionic diffusion.
t Cotransport of two solutes occurs when
a membrane protein enables the “downhill” diffusion of one solute to drive the
“uphill” transport of the other.
CONCEPT 5.5
Bulk transport across the plasma membrane occurs
by exocytosis and endocytosis (pp. 106–107)
t Three main types of endocytosis are phagocytosis,
pinocytosis, and receptor-mediated endocytosis.
CONCEPT 5.6
The plasma membrane plays a key role in most cell
signaling (pp. 108–113)
t In local signaling, animal cells may communicate by direct contact
or by secreting local regulators. For long-distance signaling, both
animals and plants use hormones; animals also signal electrically.
t Signaling molecules that bind to membrane receptors trigger a
three-stage cell-signaling pathway:
5 Chapter Review
SUMMARY OF KEY CONCEPTS
CONCEPT 5.1
Cellular membranes are fluid mosaics of lipids
and proteins (pp. 94–98)
t In the fluid mosaic model, amphipathic proteins are embedded
in the phospholipid bilayer.
t Phospholipids and some proteins move laterally within the
membrane. The unsaturated hydrocarbon tails of some phospholipids keep membranes fluid at lower temperatures, while
cholesterol helps membranes resist changes in fluidity caused by
temperature changes.
t Membraine proteins function in transport, enzymatic activity, attachment to the cytoskeleton and extracellular matrix, cell-cell
recognition, intercellular joining, and signal transduction. Short
chains of sugars linked to proteins (in glycoproteins) and lipids (in
glycolipids) on the exterior side of the plasma membrane interact
with surface molecules of other cells.
t Membrane proteins and lipids are synthesized in the ER and
modified in the ER and Golgi apparatus. The inside and outside
faces of membranes differ in molecular composition.
CONCEPT 5.2
Membrane structure results in selective permeability
(p. 99)
t A cell must exchange substances with its surroundings, a process
controlled by the selective permeability of the plasma membrane. Hydrophobic molecules pass through membranes rapidly,
whereas polar molecules and ions usually need specific transport
proteins.
CONCEPT 5.3
Passive transport is diffusion of a substance across
a membrane with no energy investment
(pp. 99–103)
t Diffusion is the spontaneous movement of a substance down its
concentration gradient. Water diffuses out through the permeable membrane of a cell (osmosis) if the solution outside has a
higher solute concentration than the cytosol (is hypertonic); water
enters the cell if the solution has a lower solute concentration (is
hypotonic). If the
concentrations are
equal (isotonic), no
net osmosis occurs.
Cell survival depends
on balancing water
uptake and loss.
t In facilitated
diffusion, a transport protein speeds
the movement of
water or a solute
across a membrane down its
114 UNIT ONE CHEMISTRY AND CELLS
Carrier
protein
Channel
protein
Passive transport:
Facilitated diffusion
Relay molecules
Activation
of cellular
response
Reception
Signaling
molecule
Receptor
1 2 Transduction 3 Response
t In reception, a signaling molecule binds to a receptor protein,
causing the protein to change shape. Two major types of membrane
receptors are G protein-coupled receptors (GPCRs), which work with the help of cytoplasmic G proteins, and ligand-gated ion
channels, which open or close in response to binding by signaling molecules. Signaling molecules that are hydrophobic cross the
plasma membrane and bind to receptors inside the cell.
t At each step in a signal transduction pathway, the signal is transduced into a different form, which commonly involves a change in a
protein’s shape. Many pathways include phosphorylation cascades,
in which a series of protein kinases each add a phosphate group to
the next one in line, activating it. The balance between phosphorylation and dephosphorylation, by protein phosphatases, regulates
the activity of proteins in the pathway.
t Second messengers, such as the small molecule cyclic AMP
(cAMP), diffuse readily through the cytosol and thus help broadcast signals quickly. Many G proteins activate the enzyme that
makes cAMP from ATP.
t The cell’s response to a signal may be the regulation of transcription in the nucleus or of an activity in the cytoplasm.


''',


'''
SUMMARY OF KEY CONCEPTS
CONCEPT 6.1
An organism’s metabolism transforms matter and
energy (pp. 116–119)
t Metabolism is the collection of chemical reactions that occur in an organism. Enzymes catalyze reactions in intersecting
metabolic pathways, which may be catabolic (breaking down
molecules, releasing energy) or anabolic (building molecules,
consuming energy).
t Energy is the capacity to cause change; some forms of energy do
work by moving matter. Kinetic energy is associated with motion and includes thermal energy, associated with the random
motion of atoms or molecules. Heat is thermal energy in transfer
from one object to another. Potential energy is related to the
location or structure of matter and includes chemical energy
possessed by a molecule due to its structure.
t The first law of thermodynamics, conservation of energy, states
that energy cannot be created or destroyed, only transferred or
transformed. The second law of thermodynamics states that
spontaneous processes, those requiring no outside input of energy, increase the entropy (disorder) of the universe.
CONCEPT 6.2
The free-energy change of a reaction tells us whether
or not the reaction occurs spontaneously (pp. 119–122)
t A living system’s free energy is energy that can do work under
cellular conditions. Organisms live at the expense of free energy.
The change in free energy (ΔG) during a biological process tells us
if the process is spontaneous. During a spontaneous process, free
energy decreases and the stability of a system increases. At maximum stability, the system is at equilibrium and can do no work.
t In an exergonic (spontaneous) chemical reaction, the products
have less free energy than the reactants (–ΔG). Endergonic (nonspontaneous) reactions require an input of energy (+ΔG). The
addition of starting materials and the removal of end products
prevent metabolism from reaching equilibrium.
CONCEPT 6.3
ATP powers cellular work by coupling exergonic
reactions to endergonic reactions (pp. 122–124)
t ATP is the cell’s energy shuttle. Hydrolysis of its terminal phosphate yields ADP and P i
 and releases free energy.
t Through energy coupling, the exergonic process of ATP hydrolysis drives endergonic reactions by transfer of a phosphate group
to specific reactants, forming a phosphorylated intermediate
that is more reactive. ATP hydrolysis (sometimes with protein
phosphorylation) also causes changes in the shape and binding
affinities of transport and motor proteins.
t Catabolic pathways drive regeneration of ATP from ADP + P i
.
CONCEPT 6.4
Enzymes speed up metabolic reactions by lowering
energy barriers (pp. 125–130)
t In a chemical reaction, the energy necessary to break the bonds
of the reactants is the activation energy, EA.
t Enzymes lower the EA barrier: Free energy
Progress of the reaction
Reactants
Products
ΔG is unaffected
by enzyme
EA
without
enzyme
Course of
reaction
without
enzyme EA with
enzyme
is lower
Course of
reaction
with enzyme
t Each type of enzyme has a unique active site that combines specifically with its substrate(s), the reactant molecule(s) on which
it acts. The enzyme changes shape slightly when it binds the
substrate(s) (induced fit).
t The active site can lower an EA barrier by orienting substrates
correctly, straining their bonds, providing a favorable microenvironment, or even covalently bonding with the substrate.
t Each enzyme has an optimal temperature and pH. Inhibitors
reduce enzyme function. A competitive inhibitor binds to the
active site, whereas a noncompetitive inhibitor binds to a different site on the enzyme.
t Natural selection, acting on organisms with mutant genes encoding altered enzymes, is a major evolutionary force responsible for
the diverse array of enzymes found in organisms.
CONCEPT 6.5
Regulation of enzyme activity helps control
metabolism (pp. 130–132)
t Many enzymes are subject to allosteric regulation: Regulatory
molecules, either activators or inhibitors, bind to specific regulatory sites, affecting the shape and function of the enzyme. In
cooperativity, binding of one substrate molecule can stimulate
binding or activity at other active sites. In feedback inhibition,
the end product of a metabolic pathway allosterically inhibits the
enzyme for a previous step in the pathway.
t Some enzymes are grouped into complexes, some are incorporated into membranes, and some are contained inside organelles,
increasing the efficiency of metabolic processes.

''',

'''

Catabolic pathways yield energy by oxidizing organic
fuels (pp. 136–140)
t Cells break down glucose and other organic fuels to yield chemical energy in the form of ATP. Fermentation is a partial degradation of glucose without the use of oxygen. Cellular respiration is
a more complete breakdown of glucose; in aerobic respiration,
oxygen is used as a reactant. The cell taps the energy stored in
food molecules through redox reactions, in which one substance
partially or totally shifts electrons to another. Oxidation is the
loss of electrons from one substance, while reduction is the addition of electrons to the other.
t During aerobic respiration, glucose (C6H12O6) is oxidized to CO2,
and O2 is reduced to H2O. Electrons lose potential energy during their transfer from glucose or other organic compounds to
oxygen. Electrons are usually passed first to NAD+
, reducing it to
NADH, and then from NADH to an electron transport chain,
which conducts them to O2 in energy-releasing steps. The energy
is used to make ATP.
t Aerobic respiration occurs in three stages: (1) glycolysis,
(2) pyruvate oxidation and the citric acid cycle, and (3) oxidative
phosphorylation (electron transport and chemiosmosis).
CONCEPT 7.2
Glycolysis harvests chemical energy by oxidizing
glucose to pyruvate (pp. 140–141)
Glycolysis
Glucose
Inputs Outputs
2 Pyruvate + 2 ATP + 2 NADH
CONCEPT 7.3
After pyruvate is oxidized, the citric acid cycle
completes the energy-yielding oxidation of organic
molecules (pp. 142–143)
t In eukaryotic cells, pyruvate enters the mitochondrion and is oxidized
to acetyl CoA, which is further oxidized in the citric acid cycle.
2 Pyruvate
2 Oxaloacetate
2 Acetyl CoA
2
8
6
2 ATP NADH
FADH2
Citric
acid
cycle CO2
Inputs Outputs
CONCEPT 7.4
During oxidative phosphorylation, chemiosmosis couples
electron transport to ATP synthesis (pp. 143–148)
t NADH and FADH2 transfer electrons to the electron transport
chain. Electrons move down the chain, losing energy in several
energy-releasing steps. Finally, electrons are passed to O2, reducing it to H2O.
7 Chapter Review
CHAPTER 7 CELLULAR RESPIRATION AND FERMENTATION 153
H 2 H+ + O2 2O
NAD+
FAD
(carrying electrons from food)
MITOCHONDRIAL MATRIX
INTERMEMBRANE
SPACE
Cyt c
Q
Protein complex
of electron
carriers
I III
IV
1 2
II
H+
H+ H+
NADH
FADH2
t At certain steps along the
electron transport chain, electron transfer causes protein
complexes to move H+
 from
the mitochondrial matrix (in
eukaryotes) to the intermembrane space, storing energy as
a proton-motive force (H+
gradient). As H+
 diffuses back
into the matrix through ATP
synthase, its passage drives
the phosphorylation of ADP, a
process called chemiosmosis.
t About 34% of the energy
stored in a glucose molecule is
transferred to ATP during cellular respiration, producing a maximum of about 32 ATP.
CONCEPT 7.5
Fermentation and anaerobic respiration enable
cells to produce ATP without the use of oxygen
(pp. 148–151)
t Glycolysis nets 2 ATP by substrate-level phosphorylation,
whether oxygen is present or not. Under anaerobic conditions,
either anaerobic respiration or fermentation can take place. In
anaerobic respiration, an electron transport chain is present
with a final electron acceptor other than oxygen. In fermentation, the electrons from NADH are passed to pyruvate or a derivative of pyruvate, regenerating the NAD+
 required to oxidize
more glucose. Two common types of fermentation are alcohol
fermentation and lactic acid fermentation.
t Fermentation, anaerobic respiration, and aerobic respiration
all use glycolysis to oxidize glucose, but they differ in their final

electron acceptor and whether an electron transport chain is used
(respiration) or not (fermentation). Respiration yields more ATP;
aerobic respiration, with O2 as the final electron acceptor, yields
about 16 times as much ATP as does fermentation.
t Glycolysis occurs in nearly all organisms and is thought to
have evolved in ancient prokaryotes before there was O2 in the
atmosphere.

t Catabolic pathways funnel electrons from many kinds of organic
molecules into cellular respiration. Many carbohydrates can
enter glycolysis, most often after conversion to glucose. Amino
acids of proteins must be deaminated before being oxidized.
The fatty acids of fats undergo beta oxidation to two-carbon
fragments and then enter the citric acid cycle as acetyl CoA.
Anabolic pathways can use small molecules from food directly
or build other substances using intermediates of glycolysis or the
citric acid cycle.
''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 8.1
Photosynthesis converts light energy to the chemical
energy of food (pp. 156–159)
t In autotrophic eukaryotes, photosynthesis occurs in
chloroplasts, organelles containing thylakoids. Stacks
of thylakoids form grana. Photosynthesis is summarized as
6 CO2 + 12 H2O + Light energy → C6H12O6 + 6 O2 + 6 H2O.
Chloroplasts split water into hydrogen and oxygen, incorporating the electrons of hydrogen into sugar molecules. Photosynthesis is a redox process: H2O is oxidized, and CO2 is reduced. The
light reactions in the thylakoid membranes split water, releasing
O2, producing ATP, and forming NADPH. The Calvin cycle in
the stroma forms sugars from CO2, using ATP for energy and
NADPH for reducing power.
CONCEPT 8.2
The light reactions convert solar energy to the
chemical energy of ATP and NADPH (pp. 159–167)
t Light is a form of electromagnetic energy. The colors we see as
visible light include those wavelengths that drive photosynthesis.
A pigment absorbs light of specific wavelengths; chlorophyll a is
the main photosynthetic pigment in plants. Other accessory pigments absorb different wavelengths of light and pass the energy on
to chlorophyll a.
t A pigment goes from a ground state to an excited state when a
photon of light boosts one of the pigment’s electrons to a higherenergy electron shell. Electrons from isolated pigments tend to
fall back to the ground state, giving off heat and/or light.
t A photosystem is composed of a reaction-center complex surrounded by light-harvesting complexes that funnel the energy
of photons to the reaction-center complex. When a special pair
of reaction-center chlorophyll a molecules absorbs energy, one of
its electrons is boosted to a higher energy level and transferred to
the primary electron acceptor. Photosystem II contains P680
chlorophyll a molecules in the reaction-center complex;
photosystem I contains P700 molecules.
t Linear electron flow during the light reactions uses both photosystems and produces NADPH, ATP, and oxygen:
t During chemiosmosis in both mitochondria and chloroplasts,
electron transport chains generate an H+
 (proton) gradient across
a membrane. ATP synthase uses this proton-motive force to synthesize ATP.
CONCEPT 8.3
The Calvin cycle uses the chemical energy of ATP
and NADPH to reduce CO2 to sugar (pp. 167–171)
t The Calvin cycle occurs in the stroma, using electrons from
NADPH and energy from ATP. One molecule of G3P exits the
cycle per three CO2 molecules fixed and is converted to glucose
and other organic molecules.
8 Chapter Review
172 UNIT ONE CHEMISTRY AND CELLS
Photosystem II
Photosystem I ATP
Pq
Fd
Primary
acceptor
Pc
Cytochrome
complex
NADP+
reductase
NADP+
+ H+
NADPH
Primary
acceptor
O2
H2
O
Electron transport
chain
Electron transport
chain
Calvin
Cycle
Carbon fixation
Regeneration of
CO2 acceptor
Reduction
3 x 5C 6 x 3C
5 x 3C
1 G3P (3C)
3 CO2
t On hot, dry days, C3 plants close their stomata, conserving
water but keeping CO2 out and O2 in. Under these conditions,
photorespiration can occur: Rubisco binds O2 instead of CO2,
leading to consumption of ATP and release of CO2 without the
production of sugar. Photorespiration may be an evolutionary relic
and it may also play a protective role.
t C4 plants are adapted to hot, dry climates. Even with their stomata partially or completely closed, they minimize the cost of
photorespiration by incorporating CO2 into four-carbon compounds in mesophyll cells. These compounds are exported to
bundle-sheath cells, where they release carbon dioxide for use in
the Calvin cycle.
t CAM plants are also adapted to hot, dry climates. They open
their stomata at night, incorporating CO2 into organic acids,
which are stored in mesophyll cells. During the day, the stomata
close, and the CO2 is released from the organic acids for use in
the Calvin cycle.
t Organic compounds produced by photosynthesis provide the energy and building material for ecosystems.

''',

'''

SUMMARY OF KEY CONCEPTS
t Unicellular organisms reproduce by cell division; multicellular
organisms depend on cell division for their development from a
fertilized egg and for growth and repair. Cell division is part of the
cell cycle, an ordered sequence of events in the life of a cell from
its origin until it divides into daughter cells.
CONCEPT 9.1
Most cell division results in genetically identical
daughter cells (pp. 175–176)
t The genetic material (DNA) of a cell—its genome—is partitioned
among chromosomes. Each eukaryotic chromosome consists of
one DNA molecule associated with many proteins that maintain
chromosome structure and help control the activity of genes.
Together, the complex of DNA and associated proteins is called
chromatin. The chromatin of a chromosome exists in different
states of condensation at different times. In animals, gametes
have one set of chromosomes and somatic cells have two sets.
t Cells replicate their genetic material before they divide, ensuring that each daughter cell can receive a copy of the DNA. In
preparation for cell division, chromosomes are duplicated, each
one then consisting of two identical sister chromatids joined
along their lengths by sister chromatid cohesion and held most
tightly together at a constricted region at the centromeres of the
chromatids. When this cohesion is broken, the chromatids separate during cell division, becoming the chromosomes of the new
daughter cells. Eukaryotic cell division consists of mitosis (division of the nucleus) and cytokinesis (division of the cytoplasm).
CONCEPT 9.2
The mitotic phase alternates with interphase
in the cell cycle (pp. 177–183)
t Between divisions, a cell is in interphase: the G1, S, and G2
phases. The cell grows throughout interphase, but DNA is replicated only during the synthesis (S) phase. Mitosis and cytokinesis
make up the mitotic (M) phase of the cell cycle.
t The mitotic spindle is an apparatus of microtubules that controls chromosome movement during mitosis. In animal cells,
the spindle arises from the centrosomes and includes spindle
microtubules and asters. Some spindle microtubules attach
to the kinetochores of chromosomes and move the chromosomes to the metaphase plate. In anaphase, sister chromatids
separate, and motor proteins move them along the kinetochore
microtubules toward opposite ends of the cell. Meanwhile, motor
proteins push nonkinetochore microtubules from opposite poles
away from each other, elongating the cell. In telophase, genetically
identical daughter nuclei form at opposite ends of the cell.
t Mitosis is usually followed by cytokinesis. Animal cells carry out
cytokinesis by cleavage, and plant cells form a cell plate.
t During binary fission in bacteria, the chromosome replicates
and the two daughter chromosomes actively move apart. Some
of the proteins involved in bacterial binary fission are related to
eukaryotic actin and tubulin. Since prokaryotes preceded eukaryotes by more than a billion years, it is likely that mitosis evolved
from prokaryotic cell division.

The eukaryotic cell cycle is regulated by a molecular
control system (pp. 183–189)
t Signaling molecules present in the cytoplasm regulate progress
through the cell cycle.
t The cell cycle control system is molecularly based; key regulatory proteins are kinases and cyclins. The cell cycle clock has
specific checkpoints where the cell cycle stops until a go-ahead
signal is received. Cell culture has enabled researchers to study
the molecular details of cell division. Both internal signals and
external signals control the cell cycle checkpoints via signal transduction pathways. Most cells exhibit density-dependent inhibition of cell division as well as anchorage dependence.
t Cancer cells elude normal cell cycle regulation and divide out of
control, forming tumors. Malignant tumors invade surrounding tissues and can undergo metastasis, exporting cancer cells to
other parts of the body, where they may form secondary tumors.
Recent advances in understanding the cell cycle and cell signaling, as well as techniques for sequencing DNA, have allowed improvements in cancer treatment.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 10.1
Offspring acquire genes from parents by inheriting
chromosomes (pp. 193–194)
t Each gene in an organism’s DNA exists at a specific locus on a
certain chromosome.
t In asexual reproduction, a single parent produces genetically
identical offspring by mitosis. Sexual reproduction combines
genes from two parents, leading to genetically diverse offspring.
CONCEPT 10.2
Fertilization and meiosis alternate in sexual life cycles
(pp. 194–197)
t Normal human somatic cells are diploid. They have 46 chromosomes made up of two sets of 23 chromosomes, one set from
each parent. Human diploid cells have 22 homologous pairs of
autosomes and one pair of sex chromosomes; the latter determines whether the person is female (XX) or male (XY).
t In humans, ovaries and testes produce haploid gametes by
meiosis, each gamete containing a single set of 23 chromosomes
(n = 23). During fertilization, an egg and sperm unite, forming a
diploid (2n = 46) single-celled zygote, which develops into a
multicellular organism by mitosis.

Sexual life cycles differ in the timing of meiosis relative to fertilization and in the point(s) of the cycle at which a multicellular
organism is produced by mitosis.

CONCEPT 10.3
Meiosis reduces the number of chromosome sets
from diploid to haploid (pp. 197–201)
t Meiosis I and meiosis II produce four haploid daughter cells.
The number of chromosome sets is reduced from two (diploid) to
one (haploid) during meiosis I, the reductional division.
t Meiosis is distinguished from mitosis by three events of meiosis I:
Prophase I: Each homologous pair undergoes synapsis
and crossing over between nonsister chromatids with
the subsequent appearance of chiasmata.
Metaphase I: Chromosomes line up as homologous
pairs on the metaphase plate.
Anaphase I: Homologs separate from each other; sister
chromatids remain joined at the centromere.
Meiosis II then separates the sister chromatids.
t Sister chromatid cohesion and crossing over allow chiasmata to
hold homologs together until anaphase I. Cohesins are cleaved
along the arms at anaphase I, allowing homologs to separate, and
at the centromeres in anaphase II, releasing sister chromatids.

CONCEPT 10.4
Genetic variation produced in sexual life cycles
contributes to evolution (pp. 201–204)
t Three events in sexual reproduction contribute to genetic variation in a population: independent assortment of chromosomes
during meiosis, crossing over during meiosis I, and random fertilization of egg cells by sperm. During crossing over, DNA of nonsister chromatids in a homologous pair is broken and rejoined.
t Genetic variation is the raw material for evolution by natural
selection. Mutations are the original source of this variation; recombination of variant genes generates additional diversity

''',

'''
SUMMARY OF KEY CONCEPTS
CONCEPT 11.1
Mendel used the scientific approach to identify two
laws of inheritance (pp. 207–212)
t Gregor Mendel formulated a theory of inheritance based on experiments with garden peas, proposing that parents pass on to
their offspring discrete genes that retain their identity through
generations. This theory includes two “laws.”
t The law of segregation states that
genes have alternative forms, or alleles. In a diploid organism, the two
alleles of a gene segregate (separate)
during meiosis and gamete formation; each sperm or egg carries only
one allele of each pair. This law explains the 3:1 ratio of F2 phenotypes
observed when monohybrids selfpollinate. Each organism inherits one
allele for each gene from each parent.
In heterozygotes, the two alleles are
different, and expression of one (the
dominant allele) masks the phenotypic effect of the other (the recessive allele). Homozygotes have identical alleles of a given gene
and are true-breeding.
t The law of independent assortment states that the pair of
alleles for a given gene segregates into gametes independently
of the pair of alleles for any other gene. In a cross between
dihybrids (individuals heterozygous for two genes), the offspring
have four phenotypes in a 9:3:3:1 ratio.

CONCEPT 11.2
The laws of probability govern Mendelian inheritance
(pp. 213–214)
t The multiplication rule states that the probability of two or
more events occurring together is equal to the product of the
individual probabilities of the independent single events. The
addition rule states that the probability of an event that can
occur in two or more independent, mutually exclusive ways is
the sum of the individual probabilities.
t The rules of probability can be used to solve complex genetics
problems. A dihybrid or other multicharacter cross is equivalent
to two or more independent monohybrid crosses occurring simultaneously. In calculating the chances of the various offspring
genotypes from such crosses, each character is first considered
separately and then the individual probabilities are multiplied.

CONCEPT 11.3
Inheritance patterns are often more complex than
predicted by simple Mendelian genetics (pp. 214–219)
t Extensions of Mendelian genetics for a single gene:
Relationship among
alleles of a single gene
Complete dominance
of one allele
Description Example
Incomplete dominance
of either allele
Codominance
Multiple alleles
Pleiotropy
Heterozygous phenotype
same as that of homozygous dominant
PP Pp
CRCR
I
AI
B
I
A, I
B, i
CRCW CWCW
Heterozygous phenotype
intermediate between
the two homozygous
phenotypes
Both phenotypes
expressed in
heterozygotes
ABO blood group alleles
Sickle-cell disease
In the whole population,
some genes have more
than two alleles
One gene is able to affect
multiple phenotypic
characters
t Extensions of Mendelian genetics for two or more genes:
BE
BE
bE
Be
be
BbEe BbEe
bE Be be
×
AaBbCc AaBb × Cc
9
Epistasis
Polygenic inheritance
The phenotypic
expression of one gene
affects the expression
of another gene
A single phenotypic
character is affected by
two or more genes
Relationship among
two or more genes Description Example
:3 :4
t The expression of a genotype can be affected by environmental
influences. Polygenic characters that are also influenced by the
environment are called multifactorial characters.
t An organism’s overall phenotype reflects its complete genotype
and unique environmental history. Even in more complex inheritance patterns, Mendel’s fundamental laws still apply.

CONCEPT 11.4
Many human traits follow Mendelian patterns
of inheritance (pp. 219–223)
t Analysis of family pedigrees can be used to deduce the possible genotypes of individuals and make predictions about future
offspring. Predictions are statistical probabilities rather than
certainties.

Many genetic disorders are inherited as simple recessive traits,
ranging from relatively mild disorders (albinism, for example) to
life-threatening ones such as sickle-cell disease and cystic fibrosis.
Most affected (homozygous recessive) individuals are children of
phenotypically normal, heterozygous carriers.
t The sickle-cell allele has probably persisted for evolutionary reasons: Heterozygotes have an advantage because one copy of the
sickle-cell allele reduces both the frequency and severity of malaria attacks.
t Lethal dominant alleles are eliminated from the population if affected people die before reproducing. Nonlethal dominant alleles
and lethal alleles that are expressed relatively late in life are inherited in a Mendelian way.
t Many human diseases are multifactorial—that is, they have both
genetic and environmental components and do not follow simple
Mendelian inheritance patterns.
t Using family histories, genetic counselors help couples determine
the probability of their children having genetic disorders
''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 12.1
Mendelian inheritance has its physical basis
in the behavior of chromosomes (pp. 228–231)
t The chromosome theory of inheritance states that genes are
located on chromosomes and that the behavior of chromosomes
during meiosis accounts for Mendel’s laws of segregation and independent assortment.
t Morgan’s discovery that transmission of the X chromosome in
Drosophila correlates with inheritance of an eye-color trait was
the first solid evidence indicating that a specific gene is associated
with a specific chromosome.

CONCEPT 12.2
Sex-linked genes exhibit unique patterns
of inheritance (pp. 231–234)
t Sex is often chromosomally based. Humans and other mammals
have an X-Y system in which sex is determined by whether a
Y chromosome is present.
t The sex chromosomes carry sex-linked genes, virtually all of
which are on the X chromosome (X-linked). Any male who inherits a recessive X-linked allele (from his mother) will express
the trait, such as color blindness.
t In mammalian females, one of the two X chromosomes in each cell
is randomly inactivated during early embryonic development, becoming highly condensed into a Barr body.

CONCEPT 12.3
Linked genes tend to be inherited together because
they are located near each other on the same
chromosome (pp. 234–240)
d
d
Egg
e
e
c
b
a
f
c ba f
D
D
Sperm
P generation
gametes + E
E
C
B
A
F
C
B
A
F
This F1 cell has 2n = 6 chromosomes and is heterozygous for all
six genes shown (AaBbCcDdEeFf ).
Red = maternal; blue = paternal.
Each chromosome has
hundreds or thousands
of genes. Four (A, B, C,
F) are shown on this one.
The alleles of unlinked
genes are either on
separate chromosomes
(such as d and e)
or so far apart on the
same chromosome
(c and f ) that they
assort independently.
Genes on the same chromosome whose alleles are so
close together that they do
not assort independently
(such as a, b, and c) are said
to be genetically linked.
t An F1 testcross yields parental types with the same combination of
traits as those in the P generation parents and recombinant types
with new combinations of traits. Unlinked genes exhibit a 50%
frequency of recombination in the gametes. For genetically linked
genes, crossing over accounts for the observed recombinants, always less than 50%.
t Recombination frequencies observed in genetic crosses allow
construction of a linkage map (a type of genetic map).

CONCEPT 12.4
Alterations of chromosome number or structure cause
some genetic disorders (pp. 240–243)
t Aneuploidy, an abnormal chromosome number, results from
nondisjunction during meiosis. When a normal gamete unites
with one containing two copies or no copies of a particular chromosome, the resulting zygote and its descendant cells either have
one extra copy of that chromosome (trisomy, 2n + 1) or are
missing a copy (monosomy, 2n − 1). Polyploidy (extra sets of
chromosomes) can result from complete nondisjunction.
t Chromosome breakage can result in alterations of chromosome
structure: deletions, duplications, inversions, and translocations.

''',

'''

CONCEPT 13.1
DNA is the genetic material (pp. 245–251)
t Experiments with bacteria and phages provided the first strong
evidence that the genetic material is DNA.
t Watson and Crick deduced that DNA is a double helix and built
a structural model. Two antiparallel sugar-phosphate chains
wind around the outside of the molecule; the nitrogenous bases
project into the interior, where they hydrogen-bond in specific
pairs: A with T, G with C.

Many proteins work together in DNA replication
and repair (pp. 251–259)
t The Meselson-Stahl experiment showed that DNA replication
is semiconservative: The parental molecule unwinds, and each
strand then serves as a template for the synthesis of a new strand
according to base-pairing rules.
t DNA replication at one replication fork is summarized here:

DNA polymerases proofread new DNA, replacing incorrect
nucleotides. In mismatch repair, enzymes correct errors that
persist. Nucleotide excision repair is a general process by which
nucleases cut out and replace damaged stretches of DNA.

A chromosome consists of a DNA molecule packed
together with proteins (pp. 259–261)
t The chromosome of most bacterial species is a circular DNA
molecule with some associated proteins, making up the nucleoid of the cell. The chromatin making up a eukaryotic chromosome
is composed of DNA, histones, and other proteins. The histones
bind to each other and to the DNA to form nucleosomes, the
most basic units of DNA packing. Additional coiling and folding
lead ultimately to the highly condensed chromatin of the metaphase chromosome. In interphase cells, most chromatin is less
compacted (euchromatin), but some remains highly condensed
(heterochromatin). Euchromatin, but not heterochromatin, is
generally accessible for transcription of genes.

Understanding DNA structure and replication makes
genetic engineering possible (pp. 261–265)
t Gene cloning (or DNA cloning) produces multiple copies of a
gene (or DNA fragment) that can be used to manipulate and analyze DNA and to produce useful new products or organisms with
beneficial traits.
t In genetic engineering, bacterial restriction enzymes are
used to cut DNA molecules within short, specific nucleotide
sequences (restriction sites), yielding a set of double-stranded
restriction fragments with single-stranded sticky ends.

DNA fragments of different lengths can be separated and their
lengths assessed by gel electrophoresis.
t The sticky ends on restriction fragments from one DNA source—
such as a bacterial plasmid or other cloning vector—can basepair with complementary sticky ends on fragments from other
DNA molecules; sealing the base-paired fragments with DNA
ligase produces recombinant DNA molecules.
t The polymerase chain reaction (PCR) can produce many copies
of (amplify) a specific target segment of DNA in vitro for use as a
DNA fragment for cloning. PCR uses primers that bracket the desired segment and requires a heat-resistant DNA polymerase.
t The rapid development of fast, inexpensive techniques for
DNA sequencing is based on sequencing by synthesis: DNA
polymerase is used to replicate a stretch of DNA from a singlestranded template, and the order in which nucleotides are added
reveals the sequence.
''',

'''
SUMMARY OF KEY CONCEPTS
CONCEPT 14.1
Genes specify proteins via transcription
and translation (pp. 269–274)
t DNA controls metabolism by directing cells to make specific
enzymes and other proteins, via the process of gene expression.
Beadle and Tatum’s studies of mutant strains of Neurospora led to
the one gene–one polypeptide hypothesis. Genes code for polypeptide chains or specify RNA molecules.
t Transcription is the synthesis of RNA complementary to a
template strand of DNA, providing a nucleotide-to-nucleotide
transfer of information. Translation is the synthesis of a polypeptide whose amino acid sequence is specified by the nucleotide
sequence in mRNA; this informational transfer involves a change
of language, from that of nucleotides to that of amino acids.
t Genetic information is encoded as a sequence of nonoverlapping nucleotide triplets, or codons. A codon in messenger RNA
(mRNA) either is translated into an amino acid (61 of the 64 codons) or serves as a stop signal (3 codons). Codons must be read
in the correct reading frame.

CONCEPT 14.2
Transcription is the DNA-directed synthesis of RNA:
a closer look (pp. 274–276)
t RNA synthesis is catalyzed by RNA polymerase, which links
together RNA nucleotides complementary to a DNA template
strand. This process follows the same base-pairing rules as DNA
replication, except that in RNA, uracil substitutes for thymine.
The three stages of transcription are initiation, elongation, and termination. A promoter, often including a TATA box in eukaryotes,
establishes where RNA synthesis is initiated. Transcription factors
help eukaryotic RNA polymerase recognize promoter sequences,
forming a transcription initiation complex. The mechanisms of
termination are different in bacteria and eukaryotes.

CONCEPT 14.3
Eukaryotic cells modify RNA
after transcription
(pp. 276–278)
t Eukaryotic pre-mRNAs undergo
RNA processing, which includes
RNA splicing, the addition of a modified nucleotide 5′ cap to the 5′ end, and the addition of a
poly-A tail to the 3′ end.
t Most eukaryotic genes are split into segments: They have introns
interspersed among the exons (regions included in the mRNA). In
RNA splicing, introns are removed and exons joined. RNA splicing
is typically carried out by spliceosomes, but in some cases, RNA
alone catalyzes its own splicing. The catalytic ability of some RNA
molecules, called ribozymes, derives from the properties of RNA.
The presence of introns allows for alternative RNA splicing.

CONCEPT 14.4
Translation is the RNA-directed synthesis
of a polypeptide: a closer look (pp. 278–288)
t A cell translates an mRNA message into protein using transfer
RNAs (tRNAs). After being bound to a specific amino acid by an
aminoacyl-tRNA synthetase, a tRNA lines up via its anticodon
at the complementary codon on mRNA. A ribosome, made up
of ribosomal RNAs (rRNAs) and proteins, facilitates this coupling with binding sites for mRNA and tRNA.
t Ribosomes coordinate the three stages of translation: initiation,
elongation, and termination. The formation of peptide bonds between amino acids is catalyzed by rRNA as tRNAs move through
the A and P sites and exit through the E site.
t After translation, modifications
to proteins can affect their shape.
Free ribosomes in the cytosol initiate synthesis of all proteins, but
proteins with a signal peptide
are synthesized on the ER.
t A gene can be transcribed by
multiple RNA polymerases
simultaneously. A single mRNA
molecule can be translated simultaneously by a number of ribosomes, forming a polyribosome.
In bacteria, these processes are
coupled, but in eukaryotes they
are separated in time and space by the nuclear membrane.

CONCEPT 14.5
Mutations of one or a few nucleotides can affect
protein structure and function (pp. 288–290)
t Small-scale mutations include point mutations, changes in one
DNA nucleotide pair, which may lead to production of nonfunctional proteins. Nucleotide-pair substitutions can cause
missense or nonsense mutations. Nucleotide-pair insertions
or deletions may produce frameshift mutations.
t Spontaneous mutations can occur during DNA replication, recombination, or repair. Chemical and physical mutagens cause
DNA damage that can alter genes.
''',

'''
Summary of Key Conept
CONCEPT 15.1
Bacteria often respond to environmental change
by regulating transcription (pp. 293–298)
•	 In bacteria, certain groups of genes are clustered into an operon
with a single promoter. An operator site on the DNA switches the
operon on or off, resulting in coordinate regulation of the genes.
•	 Both repressible and inducible operons are examples of negative
gene regulation. Binding of a specific repressor protein to the
operator shuts off transcription. (The repressor is encoded by a
separate regulatory gene.) In a repressible operon, the repressor is
active when bound to a corepressor.
In an inducible operon, binding of an inducer to an innately
active repressor inactivates the repressor and turns on transcription. Inducible enzymes usually function in catabolic pathways.
•	 Some operons have positive gene regulation. A stimulatory activator protein (such as CAP, when activated by cyclic AMP),
binds to a site within the promoter and stimulates transcription.

ukaryotic gene expression is regulated at many
stages (pp. 298–305)
Chromatin modification
• Genes in highly compacted
chromatin are generally not
transcribed.
Transcription
• Regulation of transcription initiation:
DNA control elements in enhancers
bind specific transcription factors.
• The genes in a coordinately controlled
group all share a combination of control
elements.
• Alternative RNA splicing:
• Initiation of translation can be controlled via
regulation of initiation factors.
Bending of
the DNA
enables
activators to
contact proteins at
the promoter, initiating transcription.
• Histone acetylation seems
to loosen chromatin
structure,
enhancing
transcription.
• DNA methylation generally
reduces transcription.
Chromatin modification
Transcription
RNA processing
mRNA
degradation
Translation
Protein processing
and degradation
Primary RNA
transcript
mRNA or
RNA processing
• Each mRNA has a
characteristic life span.
mRNA degradation
Translation
• Protein processing and degradation are
subject to regulation.

CONCEPT 15.3
Noncoding RNAs play multiple roles in controlling
gene expression (pp. 305–306)
t Noncoding RNAs (e.g., miRNAs and siRNAs) can block translation or cause degradation of mRNAs.

Researchers can monitor expression of specific genes
(pp. 307–309)
t In nucleic acid hybridization, a nucleic acid probe is used to
detect the presence of a specific mRNA.
t In situ hybridization and RT-PCR can detect the presence of a
given mRNA in a tissue or an RNA sample, respectively.
t DNA microarrays are used to identify sets of genes co-expressed
by a group of cells. Their cDNAs can also be sequenced.
'''

]

n = 0

math_prompt = "This is a math question. Unlike other kinds of questions, you will not be asking for terms like 'what method allows you to do this' or 'what is the name of this formula.' Everything is centered around calculations and computations."

energy_topics = ["Physics", "Chemistry", "Biology"]
x = random.randint(0, 2)
y = random.randint(0,len(subtopics[energy_topics[x]])-1)
energy_prompt = f"This is an energy question. In energy questions, you will briefly mention research being done at a random lab - e.g. Sandia National Labs, Ames Laboratory, Argonne National Laboratory, Brookhaven National Laboratory, Fermi National Accelerator Laboratory, Frederick National Laboratory for Cancer Research, Idaho National Laboratory, Lawrence Berkeley National Laboratory, Lawrence Livermore National Laboratory. After that, you will ask a random {energy_topics[x]} question based on that research. Do this for both the toss-up question and the bonus question."

import time

if st.button("Generate Question"):
    while True:
        category, topic = select_topic()
        index = 0
        if(category=="Energy"):
            index = y
        else:
            for i in range(len(subtopics[category])):
                if(subtopics[category][i]==(topic)):
                    index = i
                    break
        ans = []
        if(category=="Chemistry"):
            ans = chem_text
        elif(category=="Physics"):
            ans = phys_text
        elif(category=="Biology"):
            ans = bio_text
        elif(category=="Math"):
            ans.append(subtopics[category][index])
            index = 0
        elif(category=="Energy"):
            if(x==0):
                ans = phys_text
            elif(x==1):
                ans = chem_text
            else:
                ans = bio_text
        difficulty = 3
        def generate_science_bowl_question():
            retrieved_text = ans[index]
            prompt = ""
            if(category=="Energy"):
                prompt += energy_prompt
            elif(category=="Math"):
                prompt += math_prompt

            if(difficulty==0):
                prompt += "These questions are meant to be relatively easy and maybe a sentence or two. They should be straightforward and for middle school students."
            elif(difficulty==1):
                prompt += "These questions are meant to be relatively medium and at least a couple of sentences. They should be logical and not too complex yet not simple and for advanced high school students."
            elif(difficulty==2):
                prompt += "These questions are meant to be difficult and relatively lengthy. They should require high-level thinking and reference difficult terms; these are meant for college-level students."
            elif(difficulty==3):
                prompt += "These questions are extremely difficult and pretty lengthy. They cannot just be rote memorization and should require a significant degree of high-level thinking and intelligence. These are meant for highly advanced graduate-level students and PhDs in a field."
            
            prompt +=  f"""

            This is the category: {category} and this is the specific subtopic {topic}.

            In short answer questions, the answer should not be more than one word!!!! You understand that???!!! If it's more than one word, I will kill myself. I actually will.

            Science Bowl is an advanced high-school, challenging buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z).

            These questions are read out loud. Make sure that the questions are 50-50 multiple-choice and short answer, and ensure that no short answer questions ask to explain anything - short answers answers should be either a term or a number resulting from a calculation (one word max). Also ensure that in multiple-choice questions, there are 4 choices and each choice is designated with the letters W, X, Y, and Z.

            Also ensure that the answer to all questions is logical but still decently difficult and not just elementary school stuff. Even it's some randomly specific word, it should be clear from the context of the question. But make sure that these questions are challenging and made for advanced high-school level students.

            Using ONLY this context {retrieved_text}, generate a Science Bowl question.

            Once again, this is the category: {category}.

            NEVER EVER REFER TO THE PASSAGE. The competitors answering these questions do not have access to the context you are given.

            I want to EMPHASIZE SOME REALLY IMPORTANT INFORMATION now, PROBABLY THE MOST FREAKING IMPORTANTLY IMPORTANT INFORMATION HERE that you have to ENSURE that the question CAN BE ANSWERED solely using the provided context. If the context talks about something, you must incorporate the words of the context into your question. No adding of other information!! Otherwise I will make sure you don't generate a single response ever again.

            ANOTHER MASSIVELY HUGE THING THAT IS SUPER IMPORTANT. I WILL GIVE YOU ONE HUNDRED EXTRA CREDIT POINTS IF YOU DO THIS: DON'T PROVIDE THE ANSWER TO THE QUESTION at the end. Just leave the question. Someone else will answer the question, you WILL NOT PROVIDE THE ANSWER.

            This means that someone should be able to answer your queston simply by looking at the context provided. No added information other than the context. I don't care what it is, no adding information outside of your narrow context. If that happens, I will kill myself.

            The question should be properly formatted and should not contain any errors.

            """

            completion = client.chat.completions.create(
                model="ft:gpt-4o-mini-2024-07-18:personal::AzCT79vQ",
                messages=[
                    {"role": "developer", "content": "You ask Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        
        question = generate_science_bowl_question()
        st.write(question)

        def answer_science_bowl_question():
            prompt = f"""

            Explain how to solve this question: {question}.

            While verifying, make sure that you don't need to make any unnecessary assumptions to solve it.

            If the answer to the question is already given, don't hesitate to question the given answer. It may be wrong.

            You will be returning an explanation of your solution to the questions.

            If any of the questions are wrong (a decent fraction of them may be wrong), then rewrite the entire question (both the toss-up and bonus) by keeping the original ideas intact but making the necessary changes.

            For example, in a multiple choice question, if none of the answers are right, change the question by replacing one of the answer choices with the correct choice.

            ONE SUPER IMPORTANT THING IS THAT COMPETITORS DON'T HAVE ACCESS TO A CALCULATOR. Therefore, keep your answer in terms of constants if possible (like pi).

            Add your fixed question at the end of your response. Even if the given question is correct, then write the same thing at the end of your response.

            Before writing the questions at the end, prelude it with the phrase THESE ARE THE QUESTIONS.

            Also, make sure you provide the answers to the questions given, without a solution. Just the answers.

            """

            # Explain how to solve this question: {question}. You will be returning an explanation of your solution to the questions.

            # Follow these criteria while verifying the validity and appropriateness of the question:
            #     - Does the answer you get not match any of the listed answers (multiple choice) or does your answer not match the given answer listed by the question?
            #     - Does it require a calculator? If it does, make the numbers nicer or change the question entirely. The contestants solving these questions won't have access to a calculator.
            #     - Can the toss-up be solved in less than 5 seconds?
            #     - Can the bonus be solved in less than 20 seconds?
            #     - Does the question make the answer too obvious? (e.g. mentioning the answer in the question or hinting at it with a very obvious key word)
            #     - Does the question require any unnecessary assumptions? (e.g. having to guess the mass of an object if it's not given)

            completion = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "developer", "content": "You solve Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content

        ans = answer_science_bowl_question()
        st.write(ans)

        # def fix_science_bowl_question():
        #     prompt = f"""

        #     Given this {question} and this feedback on the question {ans}, 
            
        #     You will be rewriting the given question accordingly.
        #     """

        

