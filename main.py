import random
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# import streamlit as st
# st.title("Science Bowl Question Generator")

question_database = {
    "Earth Science": [],
    "Biology": [],
    "Physics": [],
    "Chemistry": []
}

science_bowl_topics = {
    "Earth Science": 0.2,
    "Physics": 0.2,
    "Chemistry": 0.2,
    "Biology": 0.2,
}

subtopics = {
    "Easy Math": ["Triangles", "Quadrilaterals", "Coordinate Plane", "Area and Perimeter", "Volume and surface area", "Pythagorean Theorem", "Congruence", "Similarity", "Circles", "Composite and Inverse Functions", "Complex numbers", "Rational functions", "Conic secctions", "Vectors", "Matrices", "Series", "Polynomial multiplication/division/arithmetic", "Logarithms", "Exponential models", "Trigonometric identities", "Trigonometric equations", "Law of cosines/sines", "Unit circle", "Limits and Continuity", "Derivatives", "Derivative Tests", "Integrals", "Differential equations", "Polar coordinates"],
    "Math": ["Complex numbers", "Rational functions", "Conic secctions", "Vectors", "Matrices", "Series", "Polynomial multiplication/division/arithmetic", "Exponential models", "Trigonometric identities", "Trigonometric equations", "Law of cosines/sines", "Unit circle", "Limits and Continuity", "Derivatives", "Derivative Tests", "Integrals", "Differential equations", "Polar coordinates"],
    "Chemistry": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5", "Topic 6", "Topic 7", "Topic 8", "Topic 9", "Topic 10",
  "Topic 11", "Topic 12", "Topic 13", "Topic 14", "Topic 15", "Topic 16", "Topic 17", "Topic 18", "Topic 19", "Topic 20",
  "Topic 21", "Topic 22", "Topic 23", "Topic 24", "Topic 25", "Topic 26", "Topic 27", "Topic 28", "Topic 29", "Topic 30",
  "Topic 31", "Topic 32", "Topic 33", "Topic 34", "Topic 35", "Topic 36", "Topic 37", "Topic 38", "Topic 39", "Topic 40",
  "Topic 41", "Topic 42", "Topic 43", "Topic 44", "Topic 45", "Topic 46", "Topic 47", "Topic 48", "Topic 49", "Topic 50",
  "Topic 51", "Topic 52", "Topic 53", "Topic 54", "Topic 55", "Topic 56", "Topic 57", "Topic 58", "Topic 59", "Topic 60",
  "Topic 61", "Topic 62", "Topic 63", "Topic 64", "Topic 65", "Topic 66", "Topic 67", "Topic 68", "Topic 69", "Topic 70",
  "Topic 71", "Topic 72", "Topic 73"],
    "Earth Science": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5", "Topic 6", "Topic 7", "Topic 8", "Topic 9", "Topic 10",
  "Topic 11", "Topic 12", "Topic 13", "Topic 14", "Topic 15", "Topic 16", "Topic 17", "Topic 18", "Topic 19", "Topic 20",
  "Topic 21", "Topic 22", "Topic 23", "Topic 24", "Topic 25", "Topic 26", "Topic 27", "Topic 28", "Topic 29", "Topic 30",
  "Topic 31", "Topic 32", "Topic 33", "Topic 34", "Topic 35", "Topic 36", "Topic 37", "Topic 38", "Topic 39", "Topic 40",
  "Topic 41", "Topic 42", "Topic 43", "Topic 44", "Topic 45", "Topic 46", "Topic 47", "Topic 48", "Topic 49", "Topic 50",
  "Topic 51", "Topic 52", "Topic 53", "Topic 54", "Topic 55", "Topic 56", "Topic 57", "Topic 58", "Topic 59", "Topic 60",
  "Topic 61", "Topic 62", "Topic 63", "Topic 64", "Topic 65", "Topic 66", "Topic 67", "Topic 68", "Topic 69", "Topic 70",
  "Topic 71", "Topic 72", "Topic 73", "Topic 74", "Topic 75", "Topic 76", "Topic 77", "Topic 78", "Topic 79", "Topic 80",
  "Topic 81", "Topic 82", "Topic 83", "Topic 84", "Topic 85", "Topic 86", "Topic 87", "Topic 88", "Topic 89", "Topic 90",
  "Topic 91", "Topic 92", "Topic 93", "Topic 94", "Topic 95", "Topic 96", "Topic 97", "Topic 98", "Topic 99", "Topic 100",
  "Topic 101", "Topic 102", "Topic 103", "Topic 104", "Topic 105", "Topic 106", "Topic 107", "Topic 108", "Topic 109", "Topic 110",
  "Topic 111", "Topic 112", "Topic 113", "Topic 114", "Topic 115", "Topic 116", "Topic 117", "Topic 118", "Topic 119", "Topic 120",
  "Topic 121", "Topic 122", "Topic 123", "Topic 124", "Topic 125", "Topic 126", "Topic 127", "Topic 128", "Topic 129", "Topic 130",
  "Topic 131", "Topic 132", "Topic 133", "Topic 134", "Topic 135", "Topic 136", "Topic 137", "Topic 138", "Topic 139", "Topic 140",
  "Topic 141", "Topic 142", "Topic 143", "Topic 144", "Topic 145", "Topic 146", "Topic 147", "Topic 148", "Topic 149", "Topic 150",
  "Topic 151", "Topic 152", "Topic 153", "Topic 154", "Topic 155", "Topic 156", "Topic 157", "Topic 158", "Topic 159", "Topic 160",
  "Topic 161", "Topic 162", "Topic 163", "Topic 164", "Topic 165", "Topic 166", "Topic 167", "Topic 168", "Topic 169", "Topic 170",
  "Topic 171", "Topic 172", "Topic 173", "Topic 174", "Topic 175"],
    "Physics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5", "Topic 6", "Topic 7", "Topic 8", "Topic 9", "Topic 10",
  "Topic 11", "Topic 12", "Topic 13", "Topic 14", "Topic 15", "Topic 16", "Topic 17", "Topic 18", "Topic 19", "Topic 20",
  "Topic 21", "Topic 22", "Topic 23", "Topic 24", "Topic 25", "Topic 26", "Topic 27", "Topic 28", "Topic 29", "Topic 30",
  "Topic 31", "Topic 32", "Topic 33", "Topic 34", "Topic 35", "Topic 36", "Topic 37", "Topic 38", "Topic 39", "Topic 40",
  "Topic 41"],
    "Biology": [
  "Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5", "Topic 6", "Topic 7", "Topic 8", "Topic 9", "Topic 10",
  "Topic 11", "Topic 12", "Topic 13", "Topic 14", "Topic 15", "Topic 16", "Topic 17", "Topic 18", "Topic 19", "Topic 20",
  "Topic 21", "Topic 22", "Topic 23", "Topic 24", "Topic 25", "Topic 26", "Topic 27", "Topic 28", "Topic 29", "Topic 30",
  "Topic 31", "Topic 32", "Topic 33", "Topic 34", "Topic 35", "Topic 36", "Topic 37", "Topic 38", "Topic 39", "Topic 40",
  "Topic 41", "Topic 42", "Topic 43", "Topic 44", "Topic 45", "Topic 46", "Topic 47", "Topic 48", "Topic 49", "Topic 50",
  "Topic 51", "Topic 52", "Topic 53", "Topic 54", "Topic 55", "Topic 56", "Topic 57", "Topic 58", "Topic 59", "Topic 60",
  "Topic 61", "Topic 62", "Topic 63", "Topic 64", "Topic 65", "Topic 66", "Topic 67", "Topic 68", "Topic 69", "Topic 70",
  "Topic 71", "Topic 72", "Topic 73", "Topic 74", "Topic 75", "Topic 76", "Topic 77", "Topic 78", "Topic 79", "Topic 80",
  "Topic 81", "Topic 82", "Topic 83", "Topic 84", "Topic 85", "Topic 86", "Topic 87", "Topic 88", "Topic 89", "Topic 90",
  "Topic 91", "Topic 92", "Topic 93", "Topic 94", "Topic 95", "Topic 96", "Topic 97", "Topic 98", "Topic 99", "Topic 100",
  "Topic 101", "Topic 102", "Topic 103", "Topic 104", "Topic 105", "Topic 106", "Topic 107", "Topic 108", "Topic 109", "Topic 110",
  "Topic 111", "Topic 112", "Topic 113", "Topic 114", "Topic 115", "Topic 116", "Topic 117", "Topic 118", "Topic 119", "Topic 120",
  "Topic 121", "Topic 122", "Topic 123", "Topic 124", "Topic 125", "Topic 126", "Topic 127", "Topic 128", "Topic 129", "Topic 130",
  "Topic 131", "Topic 132", "Topic 133", "Topic 134", "Topic 135", "Topic 136", "Topic 137", "Topic 138", "Topic 139", "Topic 140",
  "Topic 141", "Topic 142", "Topic 143", "Topic 144", "Topic 145", "Topic 146", "Topic 147", "Topic 148", "Topic 149", "Topic 150",
  "Topic 151", "Topic 152", "Topic 153", "Topic 154", "Topic 155", "Topic 156", "Topic 157", "Topic 158", "Topic 159", "Topic 160",
  "Topic 161", "Topic 162", "Topic 163", "Topic 164", "Topic 165", "Topic 166", "Topic 167", "Topic 168", "Topic 169", "Topic 170",
  "Topic 171", "Topic 172", "Topic 173", "Topic 174", "Topic 175", "Topic 176", "Topic 177", "Topic 178", "Topic 179", "Topic 180",
  "Topic 181", "Topic 182", "Topic 183", "Topic 184", "Topic 185", "Topic 186", "Topic 187", "Topic 188", "Topic 189", "Topic 190",
  "Topic 191", "Topic 192", "Topic 193", "Topic 194", "Topic 195", "Topic 196", "Topic 197", "Topic 198", "Topic 199", "Topic 200",
  "Topic 201", "Topic 202", "Topic 203", "Topic 204", "Topic 205", "Topic 206", "Topic 207", "Topic 208", "Topic 209", "Topic 210",
  "Topic 211", "Topic 212", "Topic 213", "Topic 214", "Topic 215", "Topic 216", "Topic 217", "Topic 218", "Topic 219", "Topic 220",
  "Topic 221", "Topic 222", "Topic 223", "Topic 224", "Topic 225", "Topic 226", "Topic 227", "Topic 228", "Topic 229", "Topic 230",
  "Topic 231", "Topic 232", "Topic 233"
]

}

question_styles_tossups = {
    "Physics": ["Short Answer Direct Term", "Short Answer Numerical", "Multiple Choice Direct Term", "Multiple Choice Numerical", "Short Answer Numbered Identification"],
    "Biology": ["Short Answer Direct Term", "Multiple Choice Direct Term", "Short Answer Numbered Identification"],
    "Earth Science": ["Short Answer Direct Term", "Multiple Choice Direct Term", "Short Answer Numbered Identification"],
    "Chemistry": ["Short Answer Direct Term", "Short Answer Numerical", "Multiple Choice Direct Term", "Multiple Choice Numerical", "Short Answer Numbered Identification"],
}

question_styles_examples_tossups = {
    "Physics": [" Physics – Short Answer What semiconductor device was instrumental in replacing vacuum tubes as the basic logical component in digital electronics? ANSWER: TRANSISTOR", " Physics – Short Answer A remote control car drops from a cliff and travels 19.6 meters before hitting the ground. How long, in seconds, did it spend in the air? ANSWER: 2", "Energy – Multiple Choice Fermi National Accelerator scientists are looking for physics beyond the Standard Model in the form of decay pathways that do not conserve lepton flavor. Which of the following particles has already been observed violating this conservation principle? W) Electrons X) Neutrinos Y) Protons Z) Bosons ANSWER: X) NEUTRINOS", " Physics – Multiple Choice Kate is tuning her cello's A string by producing an A note on a string that is already tuned and comparing the sounds. Which of the following beat frequencies, in hertz, would indicate that the strings are closest to having the same pitch? W) 2 X) 100 Y) 440 Z) 880 ANSWER: W) 2", " Physics – Multiple Choice An asteroid with linear momentum is gravitationally captured by a planet. Which of the following best explains where the linear momentum of the asteroid went? W) Converted into angular momentum X) Conserved in the asteroid's orbital velocity Y) Dissipated by frictional forces Z) Translating the planet-asteroid system ANSWER: Z) TRANSLATING THE PLANET-ASTEROID SYSTEM", " Physics – Short Answer Identify all of the following three statements that are true of free- fall: 1) Apparent weightlessness is the sensation that occurs when the gravitational force is negated by air friction; 2) Satellites orbiting the earth are in near free-fall; 3) Objects free-falling on Earth all reach terminal velocity. ANSWER: 2"],
    "Biology": ["Biology – Short Answer Atherosclerotic [athero-sklair-AW-tic] plaques are composed of what lipid that is stored in LDL and HDL particles? ANSWER: CHOLESTEROL", " Biology – Multiple Choice In which of the following organ systems do the tonsils primarily function? W) Lymphatic X) Digestive Y) Respiratory Z) Integumentary [in-TEG-you-MEN-tary] ANSWER: W) LYMPHATIC ", "Biology – Short Answer Identify all of the following four cell types that are considered white blood cells: 1) T cells; 2) Erythrocytes; 3) Thrombocytes; 4) Neutrophils. ANSWER: 1, 4 "],
    "Chemistry": ["Chemistry – Short Answer What is the name of the aldehyde [AL-deh-hide] with only a single carbon atom? ANSWER: FORMALDEHYDE (ACCEPT: METHANAL) ", "Chemistry – Short Answer Suppose that at a certain temperature, one mole of chlorine gas and one mole of PCl3 gas are placed in a 1-liter container, and then equilibrate to form 0.2 moles of PCl5 gas. What is the K-sub-C value for the gas-phase reaction PCl3 + Cl2 yields PCl5 at this temperature? ANSWER: 5/16 (ACCEPT: 0.3125)", "Chemistry – Multiple Choice Which of the following alkali metals has the most negative standard reduction potential? W) Sodium X) Cesium Y) Rubidium [roo-BID-ee-um] Z) Potassium ANSWER: X) CESIUM", "Chemistry – Multiple Choice A balloon is inflated with 10 grams of helium. Under the same conditions, a second balloon is inflated to the same volume with nitrogen. To the nearest gram, what is the mass of nitrogen in the second balloon? W) 40 X) 50 Y) 60 Z) 70 ANSWER: Z) 70 ", "Chemistry – Short Answer Identify all of the following four molecules that are linear: 1) Carbon dioxide; 2) Selenium [sih-LEE-nee-um] dioxide; 3) Beryllium dichloride; 4) Xenon [ZEE-non] difluoride. ANSWER: 1, 3, AND 4 "],
    "Chemistry2": ["Chemistry – Short Answer Suppose that at a certain temperature, one mole of chlorine gas and one mole of PCl3 gas are placed in a 1-liter container, and then equilibrate to form 0.2 moles of PCl5 gas. What is the K-sub-C value for the gas-phase reaction PCl3 + Cl2 yields PCl5 at this temperature? ANSWER: 5/16 (ACCEPT: 0.3125)", "21) Chemistry – Multiple Choice A balloon is inflated with 10 grams of helium. Under the same conditions, a second balloon is inflated to the same volume with nitrogen. To the nearest gram, what is the mass of nitrogen in the second balloon? W) 40 X) 50 Y) 60 Z) 70 ANSWER: Z) 70"],
    "Earth Science": ["7) Earth and Space – Short Answer What planet of the solar system has the highest albedo? ANSWER: VENUS", "2) Earth and Space – Multiple Choice Horsts and grabens [GRAH-bens] are bounded by what type of fault? W) Strike-slip X) Reverse Y) Thrust Z) Normal ANSWER: Z) NORMAL", "2) Earth and Space – Short Answer Identify all of the following three regions that are passive margins: 1) East coast of North America; 2) West coast of North America; 3) West coast of Africa. ANSWER: 1, 3"]
}

question_styles_bonuses = {
    "Physics": ["Short Answer Numerical", "Multiple Choice Numerical", "Short Answer Numbered Identification", "Multiple Choice Analytical"],
    "Biology": ["Short Answer Numbered Identification", "Multiple Choice Analytical"],
    "Earth Science": ["Short Answer Numbered Identification", "Multiple Choice Analytical"],
    "Chemistry": ["Short Answer Numerical", "Multiple Choice Numerical", "Short Answer Numbered Identification", "Multiple Choice Analytical"],
}

question_styles_examples_bonuses = {
    "Physics": [" Physics – Short Answer A remote control car drops from a cliff and travels 19.6 meters before hitting the ground. How long, in seconds, did it spend in the air? ANSWER: 2", "Physics – Multiple Choice Kate is tuning her cello's A string by producing an A note on a string that is already tuned and comparing the sounds. Which of the following beat frequencies, in hertz, would indicate that the strings are closest to having the same pitch? W) 2 X) 100 Y) 440 Z) 880 ANSWER: W) 2", "Physics – Short Answer Identify all of the following three statements that are true of free- fall: 1) Apparent weightlessness is the sensation that occurs when the gravitational force is negated by air friction; 2) Satellites orbiting the earth are in near free-fall; 3) Objects free-falling on Earth all reach terminal velocity. ANSWER: 2", "Physics – Multiple Choice An asteroid with linear momentum is gravitationally captured by a planet. Which of the following best explains where the linear momentum of the asteroid went? W) Converted into angular momentum X) Conserved in the asteroid's orbital velocity Y) Dissipated by frictional forces Z) Translating the planet-asteroid system ANSWER: Z) TRANSLATING THE PLANET-ASTEROID SYSTEM"],
    "Biology": ["Biology – Short Answer Identify all of the following four cell types that are considered white blood cells: 1) T cells; 2) Erythrocytes; 3) Thrombocytes; 4) Neutrophils. ANSWER: 1, 4", "Biology – Multiple Choice A population of actively dividing cells contains, on average, 30 femtograms of DNA per cell. After some period of time, you make another measurement and observe that the cells now have 60 femtograms of DNA per cell. Which of the following is the most reasonable conclusion to make about these cells? W) They are going to perform meiosis [my-OH-sis] X) They are going to perform mitosis Y) S phase has occurred Z) They are in G1 phase ANSWER: Y) S PHASE HAS OCCURRED"],
    "Chemistry": ["Chemistry – Short Answer Suppose that at a certain temperature, one mole of chlorine gas and one mole of PCl3 gas are placed in a 1-liter container, and then equilibrate to form 0.2 moles of PCl5 gas. What is the K-sub-C value for the gas-phase reaction PCl3 + Cl2 yields PCl5 at this temperature? ANSWER: 5/16 (ACCEPT: 0.3125)",  "Chemistry – Multiple Choice A balloon is inflated with 10 grams of helium. Under the same conditions, a second balloon is inflated to the same volume with nitrogen. To the nearest gram, what is the mass of nitrogen in the second balloon? W) 40 X) 50 Y) 60 Z) 70 ANSWER: Z) 70 ", "Chemistry – Short Answer Identify all of the following four molecules that are linear: 1) Carbon dioxide; 2) Selenium [sih-LEE-nee-um] dioxide; 3) Beryllium dichloride; 4) Xenon [ZEE-non] difluoride. ANSWER: 1, 3, AND 4", "Chemistry – Multiple Choice Kevin performs a titration [tie-TRAY-shun] using sodium hydroxide as the titrant. He finds that the pH at the equivalence point is above 7. What does this imply about the analyte? W) It is a strong acid X) It is a weak acid Y) It is a strong base Z) It is a weak base ANSWER: X) IT IS A WEAK ACID"],
    "Earth Science": ["Earth and Space – Short Answer Identify all of the following three regions that are passive margins: 1) East coast of North America; 2) West coast of North America; 3) West coast of Africa. ANSWER: 1, 3", "Earth and Space – Multiple Choice Which of the following statements regarding Earth's core is NOT true? W) It contains a liquid outer core and a solid inner core X) The inner core has a higher temperature than the outer core Y) The inner core is responsible for Earth's magnetic field Z) The inner core has a greater density than the outer core ANSWER: Y) THE INNER CORE IS RESPONSIBLE FOR EARTH'S MAGNETIC FIELD "]
}

question_style_explanations = {
    "Short Answer Direct Term": "This question must be a short answer and have a specific term as an answer.",
    "Short Answer Numerical": "This question must be a short answer and have a number as an answer.",
    "Multiple Choice Direct Term": "This question must be a multiple-choice and have specific terms as answer choices.",
    "Multiple Choice Numerical": "This question must be a multiple-choice and have numbers as answer choices.",
    "Multiple Choice Analytical": "This question must be a multiple-choice and require critical thinking, involving a long question with lengthy, sentence long answer choices.",
    "Short Answer Numbered Identification": "This question must be a short answer and have three answer choices numbered with 1,2, and 3, and the question must ask to identify all of the following choices that are true or to order them or do something else with them."
}

def select_topic(category):
    if(category=="Random"):
        category = random.choices(list(science_bowl_topics.keys()), weights=list(science_bowl_topics.values()))[0]
    topic = random.choice(subtopics[category])
    return category, topic
    
import numpy as np

harder_phys_text = [

    '''


Scalars and Vectors Scalars, such as temperature, have magni- tude only. They are specified by a number with a unit (10°C) and obey the rules of arithmetic and ordinary algebra. Vectors, such as displacement, have both magnitude and direction (5 m, north) and obey the rules of vector algebra.
Adding Vectors Geometrically Two vectors a and b may be added geometrically by drawing them to a common scale and placing them head to tail. The vector connecting the tail of the first to the head of the second is the vector sum 3. To subtract from a, reverse the direction of b to get -b; then add -b to a. Vector addition is commutative
a+b=b+a
and obeys the associative law
(a + b) + ¿ = a + (b + c).
(3-2)
(3-3)
Components of a Vector The (scalar) components a, and a, of any two-dimensional vector a along the coordinate axes are found by dropping perpendicular lines from the ends of a onto the coor- dinate axes. The components are given by
a = a cos and a1 = a sin 0,
(3-5)
where is the angle between the positive direction of the x axis and the direction of a. The algebraic sign of a component indi- cates its direction along the associated axis. Given its compo- nents, we can find the magnitude and orientation (direction) of the vector a by using
a = Va+a2 and tan 0 =
ay ax
(3-6)
Unit-Vector Notation Unit vectors i, j, and â have magnitudes of unity and are directed in the positive directions of the x, y, and z axes, respectively, in a right-handed coordinate system (as defined by the vector products of the unit vectors). We can write a vector a in terms of unit vectors as
a = ai +a,j+ak,
(3-7) in which ai, a,j, and ask are the vector components of a and a, ay, and a, are its scalar components.
Adding Vectors in Component Form To add vectors in com- ponent form, we use the rules
rx = ax + bx ry = a, + by r2 = a+b2 (3-10 to 3-12) Here a and b are the vectors to be added, and 7 is the vector sum. Note that we add components axis by axis. We can then express the sum in unit-vector notation or magnitude-angle notation.
Product of a Scalar and a Vector The product of a scalar s and a vector v is a new vector whose magnitude is sv and whose direc- tion is the same as that of v if s is positive, and opposite that of v if s is negative. (The negative sign reverses the vector.) To divide v by s, multiply by 1/s.
The Scalar Product The scalar (or dot) product of two vectors a and b is written a·b and is the scalar quantity given by
a. b = ab cos 4,
(3-20)
in which is the angle between the directions of a and B. A scalar product is the product of the magnitude of one vector and the scalar component of the second vector along the direction of the first vector. Note that a·bba, which means that the scalar product obeys the commutative law.
In unit-vector notation,
a·b − (ai+a+ak)·(b ̧î +b‚ĵ +b,k),
(3-22)
which may be expanded according to the distributive law. The Vector Product The vector (or cross) product of two vectors a and b is written a× б and is a vector whose magnitude c is given by (3-24)
c = ab sin o,
in which is the smaller of the angles between the directions of a and . The direction of is perpendicular to the plane defined by a and b and is given by a right-hand rule, as shown in Fig. 3-19. Note that a × b = -(ba), which means that the vec- tor product does not obey the commutative law. In unit-vector notation,
axb-(a,i+a+a,k) × (b,i +b,j +b ̧k),
which we may expand with the distributive law.
(3-26)

    ''',


    '''


Position Vector The location of a particle relative to the ori- gin of a coordinate system is given by a position vector 7, which in unit-vector notation is
7 = xî + yĵ + zk.
(4-1)
Here xi, yj, and zk are the vector components of position vector 7, and x, y, and z are its scalar components (as well as the coordinates of the particle). A position vector is described either by a magni- tude and one or two angles for orientation, or by its vector or scalar components.
Displacement If a particle moves so that its position vector changes from 71 to 72, the particle's displacement A is
As At in Eq. 4-8 is shrunk to 0, avg reaches a limit called either the velocity or the instantaneous velocity v:
dr dt'
which can be rewritten in unit-vector notation as
v=v,i+vj+vk.
(4-10)
(4-11)
where v1 = dx/dt, v1 = dy/dt, and v2 = dz/dt. The instantaneous velocity of a particle is always directed along the tangent to the particle's path at the particle's position.
Average Acceleration and Instantaneous Acceleration If a particle's velocity changes from v1 to 2 in time interval At, its average acceleration during At is
A7 = 72-71.
(4-2)
The displacement can also be written as
V2V
a ave
Δε
AV Δε
(4-15)
A7 = (x2 − x1)î + (y1⁄2 − y1)Î + (Z2 − Z1)Ê = Axî + Ayj + Azk.
(4-3) (4-4)
As At in Eq. 4-15 is shrunk to 0, avg reaches a limiting value called either the acceleration or the instantaneous acceleration a:
Average Velocity and Instantaneous Velocity If a parti- cle undergoes a displacement A7 in time interval At, its average ve- locity Vavg for that time interval is
dv dt
(4-16)
In unit-vector notation,
Vavg
ΔΕ Δε
(4-8)
=
ã = a ̧î + a‚ĵ + a ̧Ê, where a, dv,/dt, a, = dv,/dt, and a2 = dv2/dt.
(4-17)
82
CHAPTER 4 MOTION IN TWO AND THREE DIMENSIONS
Projectile Motion Projectile motion is the motion of a particle that is launched with an initial velocity Vo. During its flight, the par- ticle's horizontal acceleration is zero and its vertical acceleration is the free-fall acceleration -g. (Upward is taken to be a positive di- rection.) If v is expressed as a magnitude (the speed vo) and an an- gle 0 (measured from the horizontal), the particle's equations of motion along the horizontal x axis and vertical y axis are
x-xo (Vo cos 00)t,
yyo (vo sin 00)t - gt2,
Vyvo sin gt,
v (vo sin 66)22g(y-yo).
(4-21)
(4-22)
(4-23)
(4-24)
The trajectory (path) of a particle in projectile motion is parabolic and is given by
y = (tan 00)x
gx2 2(vo cos 00)2
(4-25)
if x and yo of Eqs. 4-21 to 4-24 are zero. The particle's horizontal range R, which is the horizontal distance from the launch point to the point at which the particle returns to the launch height, is
R =
v sin 200- g
(4-26)
Uniform Circular Motion If a particle travels along a circle or circular arc of radius r at constant speed v, it is said to be in uniform circular motion and has an acceleration a of constant magnitude
(4-34)
The direction of a is toward the center of the circle or circular arc, and a is said to be centripetal. The time for the particle to complete a circle is
2πr
T =
ν
(4-35)
T is called the period of revolution, or simply the period, of the motion.
Relative Motion When two frames of reference A and B are moving relative to each other at constant velocity, the velocity of a par- ticle P as measured by an observer in frame A usually differs from that measured from frame B. The two measured velocities are related by
Yes = Tee + Pau
(4-44)
where VBA is the velocity of B with respect to A. Both observers measure the same acceleration for the particle:
apa = a PB.
(4-45)

    ''',

    '''


Review & Summary
Newtonian Mechanics The velocity of an object can change (the object can accelerate) when the object is acted on by one or more forces (pushes or pulls) from other objects. Newtonian me- chanics relates accelerations and forces.
Force Forces are vector quantities. Their magnitudes are de- fined in terms of the acceleration they would give the standard kilogram. A force that accelerates that standard body by exactly 1 m/s2 is defined to have a magnitude of 1 N. The direction of a force is the direction of the acceleration it causes. Forces are com- bined according to the rules of vector algebra. The net force on a body is the vector sum of all the forces acting on the body.
Newton's First Law If there is no net force on a body, the body remains at rest if it is initially at rest or moves in a straight line at constant speed if it is in motion.
Inertial Reference Frames Reference frames in which Newtonian mechanics holds are called inertial reference frames or inertial frames. Reference frames in which Newtonian mechanics does not hold are called noninertial reference frames or noniner- tial frames.
Mass The mass of a body is the characteristic of that body that relates the body's acceleration to the net force causing the acceler- ation. Masses are scalar quantities.
Newton's Second Law The net force Fnet on a body with mass m is related to the body's acceleration a by
Fe-ma,
which may be written in the component versions
(5-1)
Fnet, x = max Fnet, y = may
and
Fnet, z
= ma2.
(5-2)
The second law indicates that in SI units
A free-body diagram is a stripped-down diagram in which only one body is considered. That body is represented by either a sketch or a dot. The external forces on the body are drawn, and a coordinate system is superimposed, oriented so as to simplify the solution.
Some Particular Forces A gravitational force Fg on a body is a pull by another body. In most situations in this book, the other body is Earth or some other astronomical body. For Earth, the force is directed down toward the ground, which is assumed to be an inertial frame. With that assumption, the magnitude of Fis
F = mg,
(5-8)
where m is the body's mass and g is the magnitude of the free-fall acceleration.
The weight W of a body is the magnitude of the upward force needed to balance the gravitational force on the body. A body's weight is related to the body's mass by
W = mg.
(5-12)
A normal force F is the force on a body from a surface against which the body presses. The normal force is always perpen- dicular to the surface.
A frictional force ƒ is the force on a body when the body slides or attempts to slide along a surface. The force is always par- allel to the surface and directed so as to oppose the sliding. On a frictionless surface, the frictional force is negligible.
When a cord is under tension, each end of the cord pulls on a body. The pull is directed along the cord, away from the point of at- tachment to the body. For a massless cord (a cord with negligible mass), the pulls at both ends of the cord have the same magnitude T, even if the cord runs around a massless, frictionless pulley (a pul- ley with negligible mass and negligible friction on its axle to op- pose its rotation).
Newton's Third Law If a force FBC acts on body B due to body C, then there is a force FCB on body C due to body B:
1 N = 1 kg. m/s2.
(5-3)
Fac=-FCB

    ''',

    '''


Review & Summary
Friction When a force F tends to slide a body along a surface, a frictional force from the surface acts on the body. The frictional force is parallel to the surface and directed so as to oppose the sliding. It is due to bonding between the atoms on the body and the atoms on the surface, an effect called cold-welding.
If the body does not slide, the frictional force is a static frictional force f. If there is sliding, the frictional force is a kinetic frictional force fk.
1. If a body does not move, the static frictional force F, and the component of F parallel to the surface are equal in magnitude, and F, is directed opposite that component. If the component increases, f, also increases.
2. The magnitude of F, has a maximum value fs,max given by
f=MFN
(6-1)
where μ, is the coefficient of static friction and F is the magni- tude of the normal force. If the component of F parallel to the surface exceeds fs,max, the static friction is overwhelmed and the body slides on the surface.
3. If the body begins to slide on the surface, the magnitude of the frictional force rapidly decreases to a constant value f given by
fx=μ1FN
where μ is the coefficient of kinetic friction.
(6-2)
Drag Force When there is relative motion between air (or some other fluid) and a body, the body experiences a drag force Ď that opposes the relative motion and points in the direction in which the fluid flows relative to the body. The magnitude of Ď is
related to the relative speed v by an experimentally determined drag coefficient C according to
D - CpAv2,
(6-14)
where p is the fluid density (mass per unit volume) and A is the effective cross-sectional area of the body (the area of a cross sec- tion taken perpendicular to the relative velocity v).
Terminal Speed When a blunt object has fallen far enough through air, the magnitudes of the drag force Ď and the gravita- tional force Fg on the body become equal. The body then falls at a constant terminal speed v, given by
2F
g
V1
CpA
(6-16)
Uniform Circular Motion If a particle moves in a circle or a circular arc of radius R at constant speed v, the particle is said to be in uniform circular motion. It then has a centripetal acceleration a with magnitude given by
v2 R
(6-17)
This acceleration is due to a net centripetal force on the particle, with magnitude given by
F =
mv2 R
(6-18)
where m is the particle's mass. The vector quantities a and Fare directed toward the center of curvature of the particle's path. A particle can move in circular motion only if a net centripetal force acts on it.

    ''',

    '''


Review & Summary
Kinetic Energy The kinetic energy K associated with the mo- tion of a particle of mass m and speed v, where v is well below the speed of light, is
K = mv2 (kinetic energy).
(7-1)
Work Work W is energy transferred to or from an object via a force acting on the object. Energy transferred to the object is posi- tive work, and from the object, negative work.
Work Done by a Constant Force The work done on a par- ticle by a constant force F during displacement & is
(work, constant force),
(7-7,7-8)
W = Fd cos = F⋅d in which is the constant angle between the directions of F and d. Only the component of F that is along the displacement & can do work on the object. When two or more forces act on an object, their net work is the sum of the individual works done by the forces, which is also equal to the work that would be done on the object by the net force Fnet of those forces.
Work and Kinetic Energy For a particle, a change AK in the kinetic energy equals the net work W done on the particle:
AK = K1- K1 = W (work-kinetic energy theorem), (7-10)
in which K, is the initial kinetic energy of the particle and K, is the ki- netic energy after the work is done. Equation 7-10 rearranged gives us (7-11)
K1 = K1 + W.
Work Done by the Gravitational Force The work W done by the gravitational force Fon a particle-like object of mass m as the object moves through a displacement & is given by mgd cos 6, (7-12)
W
in which is the angle between Fg and d.
g
Work Done in Lifting and Lowering an Object The work W done by an applied force as a particle-like object is either lifted or lowered is related to the work Wg done by the gravitational force and the change AK in the object's kinetic energy by
AK = K1-K;= Wa + Wg.
If K1 = K1, then Eq. 7-15 reduces to
Wa=-Wg
(7-15)
(7-16)
which tells us that the applied force transfers as much energy to the object as the gravitational force transfers from it.
QUESTIONS
169
Spring Force The force F, from a spring is
F = -kd
(Hooke's law), (7-20) where a is the displacement of the spring's free end from its posi- tion when the spring is in its relaxed state (neither compressed nor extended), and k is the spring constant (a measure of the spring's stiffness). If an x axis lies along the spring, with the origin at the lo- cation of the spring's free end when the spring is in its relaxed state, Eq. 7-20 can be written as
F-kx
(Hooke's law).
(7-21)
A spring force is thus a variable force: It varies with the displacement of the spring's free end.
Work Done by a Spring Force If an object is attached to the spring's free end, the work W, done on the object by the spring force when the object is moved from an initial position x¡ to a final position x, is
W1 =kx} - kx}.
If x = 0 and x = x, then Eq. 7-25 becomes
W1 = -kx2.
(7-25)
(7-26)
Work Done by a Variable Force When the force F on a particle- like object depends on the position of the object, the work done by F on the object while the object moves from an initial position r, with co- ordinates (x, y, z) to a final position r, with coordinates (xf, yf, Zf)
must be found by integrating the force. If we assume that component F, may depend on x but not on y or z, component F, may depend on y but not on x or z, and component F2 may depend on z but not on x or y, then the work is
= [ "F, dx + [ " F, dy + [ "F.dz. S
W =
If F has only an x component, then Eq. 7-36 reduces to
W =
F(x) dx.
(7-36)
(7-32)
Power The power due to a force is the rate at which that force does work on an object. If the force does work W during a time inter- val At, the average power due to the force over that time interval is
Pavg
W At
Instantaneous power is the instantaneous rate of doing work:
dw P = dt
(7-42)
(7-43)
For a force F at an angle & to the direction of travel of the instan- taneous velocity V, the instantaneous power is
P = Fv cos = F. v.
(7-47,7-48)

    ''',

    '''


Review & Summary
Conservative Forces A force is a conservative force if the net work it does on a particle moving around any closed path, from an initial point and then back to that point, is zero. Equivalently, a force is conservative if the net work it does on a particle moving between two points does not depend on the path taken by the par- ticle. The gravitational force and the spring force are conservative forces; the kinetic frictional force is a nonconservative force.
Potential Energy A potential energy is energy that is associated with the configuration of a system in which a conservative force acts. When the conservative force does work W on a particle within the sys- tem, the change AU in the potential energy of the system is
AU = -W.
(8-1) If the particle moves from point x, to point x,, the change in the potential energy of the system is
AU = − ["F(x) dx.
(8-6)
Gravitational Potential Energy The potential energy asso- ciated with a system consisting of Earth and a nearby particle is gravitational potential energy. If the particle moves from height y; to height y, the change in the gravitational potential energy of the particle-Earth system is
AU= mg(y- y) = mg Ay.
(8-7)
If the reference point of the particle is set as y;= 0 and the cor- responding gravitational potential energy of the system is set as U1 = 0, then the gravitational potential energy U when the parti-
cle is at any height y is
U(y) = mgy.
(8-9)
Elastic Potential Energy Elastic potential energy is the energy associated with the state of compression or extension of an elastic object. For a spring that exerts a spring force F = -kx when its free end has displacement x, the elastic potential energy is
U(x) = kx2.
(8-11)
The reference configuration has the spring at its relaxed length, at which x = 0 and U = 0.
Mechanical Energy The mechanical energy Emec of a system is the sum of its kinetic energy K and potential energy U: Emec = K + U.
(8-12)
An isolated system is one in which no external force causes energy changes. If only conservative forces do work within an isolated sys- tem, then the mechanical energy Emec of the system cannot change. This principle of conservation of mechanical energy is written as (8-17) in which the subscripts refer to different instants during an energy transfer process. This conservation principle can also be written as
K2+ U2 = K1 + U1,
AEmec = AK+ AU = 0.
(8-18)
Potential Energy Curves If we know the potential energy function U(x) for a system in which a one-dimensional force F(x)
200
CHAPTER 8 POTENTIAL ENERGY AND CONSERVATION OF ENERGY
acts on a particle, we can find the force as
F(x)
dU(x) dx
(8-22)
If U(x) is given on a graph, then at any value of x, the force F(x) is the negative of the slope of the curve there and the kinetic energy of the particle is given by
K(x) = Emec - U(x),
(8-24)
where Emec is the mechanical energy of the system. A turning point is a point x at which the particle reverses its motion (there, K = 0). The particle is in equilibrium at points where the slope of the U(x) curve is zero (there, F(x) = 0).
Work Done on a System by an External Force Work W is energy transferred to or from a system by means of an external force acting on the system. When more than one force acts on a system, their net work is the transferred energy. When friction is not involved, the work done on the system and the change AEmec in the mechanical energy of the system are equal:
W = AE mec = AK + AU.
(8-26, 8-25)
When a kinetic frictional force acts within the system, then the ther- mal energy Eh of the system changes. (This energy is associated with the random motion of atoms and molecules in the system.) The work done on the system is then
W=AEmec + AEth
(8-33)
The change AE is related to the magnitude f of the frictional force and the magnitude d of the displacement caused by the external force by (8-31)
AEth=fid.
Conservation of Energy The total energy E of a system (the sum of its mechanical energy and its internal energies, including thermal energy) can change only by amounts of energy that are transferred to or from the system. This experimental fact is known as the law of conservation of energy. If work W is done on the system, then
W = AE = AEmec + AEth + AEint
If the system is isolated (W = 0), this gives
and
AEmec + AEth+AEint = 0 Emec2= Emec,1 AEth - AEint
(8-35)
(8-36) (8-37)
where the subscripts 1 and 2 refer to two different instants. Power The power due to a force is the rate at which that force transfers energy. If an amount of energy AE is transferred by a force in an amount of time At, the average power of the force is ΔΕ Δε
Pavg
The instantaneous power due to a force is
P =
dE dt
(8-40)
(8-41)

    ''',

    '''


Review & Summary
Center of Mass The center of mass of a system of n particles is defined to be the point whose coordinates are given by
or
Χρυσά
M
M
Newton's Second Law for a System of Particles The motion of the center of mass of any system of particles is governed by Newton's second law for a system of particles, which is
=Σ my Zoom-
1
mizi,
M
(9-5)
(9-8)
(9-14) Here is the net force of all the external forces acting on the sys- tem, M is the total mass of the system, and is the acceleration of the system's center of mass.
1
where M is the total mass of the system.
244
CHAPTER 9 CENTER OF MASS AND LINEAR MOMENTUM
Linear Momentum and Newton's Second Law For a sin- gle particle, we define a quantity p called its linear momentum as
(9-22)
must be conserved (it is a constant), which we can write in vector form as (9-50)
and can write Newton's second law in terms of this momentum:
Fret dp
dt
For a system of particles these relations become
(9-23)
P-MV and Fat
dP di
(9-25, 9-27)
Collision and Impulse Applying Newton's second law in momentum form to a particle-like body involved in a collision leads to the impulse-linear momentum theorem:
Pr-Pi-Ap-7,
(9-31,9-32)
where PP-Ap is the change in the body's linear momen- tum, and is the impulse due to the force F(t) exerted on the body by the other body in the collision:
7- Fo) dr.
(9-30)
If Fay is the average magnitude of F(t) during the collision and At is the duration of the collision, then for one-dimensional motion
J-FAL
(9-35)
When a steady stream of bodies, each with mass m and speed v, col- lides with a body whose position is fixed, the average force on the fixed body is
Five-Ap-m Av,
where subscripts i and ƒ refer to values just before and just after the collision, respectively.
If the motion of the bodies is along a single axis, the collision is one-dimensional and we can write Eq. 9-50 in terms of velocity components along that axis:
(9-51)
If the bodies stick together, the collision is a completely inelastic collision and the bodies have the same final velocity V (because they are stuck together).
Motion of the Center of Mass The center of mass of a closed, isolated system of two colliding bodies is not affected by a collision. In particular, the velocity of the center of mass can- not be changed by the collision.
Elastic Collisions in One Dimension
An elastic collision is a special type of collision in which the kinetic energy of a system of colliding bodies is conserved. If the system is closed and isolated, its linear momentum is also conserved. For a one- dimensional collision in which body 2 is a target and body 1 is an incoming projectile, conservation of kinetic energy and linear momentum yield the following expressions for the velocities immediately after the collision:
(9-37)
and
where n/Ar is the rate at which the bodies collide with the fixed body, and Av is the change in velocity of each colliding body. This average force can also be written as
Am Δν, Δε
(9-40)
where Am/Ar is the rate at which mass collides with the fixed body. In Eqs. 9-37 and 9-40, Av-v if the bodies stop upon impact and Av- -2v if they bounce directly backward with no change in their speed.
Conservation of Linear Momentum If a system is isolated so that no net external force acts on it, the linear momentum P of the system remains constant:
P-constant (closed, isolated system).
This can also be written as
PP (closed, isolated system).
(9-42)
(9-43)
where the subscripts refer to the values of P at some initial time and at a later time. Equations 9-42 and 9-43 are equivalent statements of the law of conservation of linear momentum.
Inelastic Collision in One Dimension In an inelastic collision of two bodies, the kinetic energy of the two-body system is not conserved (it is not a constant). If the system is closed and isolated, the total linear momentum of the system
Vu
m1 + m2
2m
Vu
my + m2
(9-67)
(9-68)
Collisions in Two Dimensions If two bodies collide and their motion is not along a single axis (the collision is not head-on), the collision is two-dimensional. If the two-body system is closed and isolated, the law of conservation of momentum applies to the collision and can be written as
P+P-Py+Py
(9-77)
In component form, the law gives two equations that describe the collision (one equation for each of the two dimensions). If the col- lision is also elastic (a special case), the conservation of kinetic en- ergy during the collision gives a third equation:
Ku+K2- K1 + K2-
(9-78)
Variable-Mass Systems In the absence of external forces a rocket accelerates at an instantaneous rate given by
Rved - Ma (first rocket equation).
(9-87)
in which M is the rocket's instantaneous mass (including unexpended fuel), R is the fuel consumption rate, and v is the fuel's exhaust speed relative to the rocket. The term Rv is the thrust of the rocket engine. For a rocket with constant R and V, whose speed changes from v, to vy when its mass changes from M, to My,
M
(second rocket equation).
M
(9-88)

    ''',

    '''


Review & Summary
Angular Position To describe the rotation of a rigid body about a fixed axis, called the rotation axis, we assume a reference line is fixed in the body, perpendicular to that axis and rotating with the body. We measure the angular position of this line relative to a fixed direction. When is measured in radians,
6-
(radian measure),
(10-1) where s is the arc length of a circular path of radius r and angle 6. Radian measure is related to angle measure in revolutions and de- grees by
1 rev - 360° - 2 rad.
(10-2) Angular Displacement A body that rotates about a rotation axis, changing its angular position from 6 to 6, undergoes an angu- lar displacement
40-0-0
(10-4) where A is positive for counterclockwise rotation and negative for
clockwise rotation.
Angular Velocity and Speed If a body rotates through an angular displacement A@ in a time interval Ar, its average angular velocity is
ΔΕ Δε
The (instantaneous) angular velocity of the body is
do dt
(10-5)
(10-6)
Both way and ware vectors, with directions given by the right-hand rule of Fig. 10-6. They are positive for counterclockwise rotation and negative for clockwise rotation. The magnitude of the body's angular velocity is the angular speed.
Angular Acceleration If the angular velocity of a body changes from to an in a time interval A-2-4, the average angular acceleration a... of the body is
4-4
Aa Δε
The (instantaneous) angular acceleration of the body is
Both ag and a are vectors.
dw dt
(10-7)
(10-8)
The Kinematic Equations for Constant Angular Accel- eration Constant angular acceleration (a = constant) is an im- portant special case of rotational motion. The appropriate kine- matic equations, given in Table 10-1, are
(10-12)
(10-13)
a2+2(0-0).
(10-14)
(10-15)
(10-16)
Linear and Angular Variables Related A point in a rigid rotating body, at a perpendicular distance r from the rotation axis,
moves in a circle with radius r. If the body rotates through an angle 6, the point moves along an are with lengths given by sor (radian measure),
where is in radians.
(10-17)
The linear velocity of the point is tangent to the circle; the point's linear speed v is given by
v=aar (radian measure),
(10-18)
where wis the angular speed (in radians per second) of the body. The linear acceleration a of the point has both tangential and radial components. The tangential component is
a, ar (radian measure),
(10-22)
where a is the magnitude of the angular acceleration (in radians per second-squared) of the body. The radial component of a is
a,
(radian measure).
(10-23)
If the point moves in uniform circular motion, the period T of the motion for the point and the body is 2′′ 2π V
T-
(radian measure).
(10-19, 10-20)
Rotational Kinetic Energy and Rotational Inertia The ki- netic energy K of a rigid body rotating about a fixed axis is given by K-a (radian measure), (10-34)
in which / is the rotational inertia of the body, defined as 1- Σ
for a system of discrete particles and defined as
(10-33)
(10-35)
for a body with continuously distributed mass. The r and r, in these expressions represent the perpendicular distance from the axis of rotation to each mass element in the body, and the integration is car- ried out over the entire body so as to include every mass element. The Parallel-Axis Theorem The parallel-axis theorem relates the rotational inertia I of a body about any axis to that of the same body about a parallel axis through the center of mass
I-Icom + Mh2.
(10-36)
Here h is the perpendicular distance between the two axes, and Icom is the rotational inertia of the body about the axis through the com. We can describe h as being the distance the actual rotation axis has been shifted from the rotation axis through the com.
Torque Torque is a turning or twisting action on a body about a ro- tation axis due to a force F. If F is exerted at a point given by the po- sition vector 7 relative to the axis, then the magnitude of the torque is
TrErFrF sin
(10-40, 10-41, 10-39)
where F, is the component of F perpendicular to 7 and is the an- gle between 7 and F. The quantity r, is the perpendicular distance between the rotation axis and an extended line running through the F vector. This line is called the line of action of F, and r, is called the moment arm of F. Similarly, r is the moment arm of F
286
CHAPTER 10 ROTATION
The SI unit of torque is the newton-meter (N·m). A torque is positive if it tends to rotate a body at rest counterclockwise and negative if it tends to rotate the body clockwise.
equations used for translational motion and are
W- 7d0
(10-53)
and
P-
dW dt
(10-55)
(10-45)
When is constant, Eq. 10-53 reduces to
(10-54)
Newton's Second Law in Angular Form The rotational analog of Newton's second law is
T-la,
where he is the net torque acting on a particle or rigid body, I is the ro tational inertia of the particle or body about the rotation axis, and or is the resulting angular acceleration about that axis
Work and Rotational Kinetic Energy The equations used for calculating work and power in rotational motion correspond to
The form of the work-kinetic energy theorem used for rotating bodies is (10-52)
AK-KK-II-W.

    ''',

    '''


Review & Summary
Rolling Bodies For a wheel of radius R rolling smoothly,
VaR,
(11-2) where Vem is the linear speed of the wheel's center of mass and wis the angular speed of the wheel about its center. The wheel may also be viewed as rotating instantaneously about the point P of the "road" that is in contact with the wheel. The angular speed of the wheel about this point is the same as the angular speed of the wheel about its center. The rolling wheel has kinetic energy
K-+M
(11-5) where Icom is the rotational inertia of the wheel about its center of mass and M is the mass of the wheel. If the wheel is being accelerated but is still rolling smoothly, the acceleration of the center of mass com is related to the angular acceleration a about the center with
amaR.
(11-6)
If the wheel rolls smoothly down a ramp of angle 6, its acceleration along an x axis extending up the ramp is
a.com,
g sin @ 1+om/MR
(11-10)
Torque as a Vector In three dimensions, torque 7 is a vector quantity defined relative to a fixed point (usually an origin); it is
(11-14) where F is a force applied to a particle and 7 is a position vector lo- cating the particle relative to the fixed point. The magnitude of Fis - rF sindrF-r_F (11-15, 11-16, 11-17) where ø is the angle between F and 7, F, is the component of F perpendicular to 7, and r, is the moment arm of F. The direction of F is given by the right-hand rule.
QUESTIONS
319
Angular Momentum of a Particle The angular momentum of a particle with linear momentum j, mass m, and linear velocity is a vector quantity defined relative to a fixed point (usually an origin) as
7-7xp-m(7xv).
The magnitude of 7 is given by
e- rmv sin d
- rp1 = rmv
-rip-rmv,
The time rate of change of this angular momentum is equal to the net external torque on the system (the vector sum of the torques due to interactions with particles external to the system):
(11-18)
(system of particles).
dt
(11-29)
(11-19)
(11-20)
(11-21)
Angular Momentum of a Rigid Body For a rigid body rotating about a fixed axis, the component of its angular momentum parallel to the rotation axis is
L-I (rigid body, fixed axis).
(11-31)
where is the angle between 7 and p, p, and v are the compo nents of ō and v perpendicular to 7, and r, is the perpendicular distance between the fixed point and the extension of p. The direc- tion of is given by the right-hand rule for cross products. Newton's Second Law in Angular Form Newton's second law for a particle can be written in angular form as
(11-23)
where is the net torque acting on the particle and is the angu- lar momentum of the particle.
Angular Momentum of a System of Particles The angu- lar momentum Ľ of a system of particles is the vector sum of the angular momenta of the individual particles:
+
Conservation of Angular Momentum The angular mo- mentum Ľ of a system remains constant if the net external torque acting on the system is zero:
or
L-a constant (isolated system) L-L, (isolated system).
This is the law of conservation of angular momentum.
(11-32)
(11-33)
Precession of a Gyroscope A spinning gyroscope can pre- cess about a vertical axis through its support at the rate
Mgr 2 = Iw
(11-46)
(11-26)
where M is the gyroscope's mass, r is the moment arm, I is the rota- tional inertia, and wis the spin rate.
J=1

    ''',

    '''

Review & Summary
Static Equilibrium A rigid body at rest is said to be in static equilibrium. For such a body, the vector sum of the external forces acting on it is zero:
Fet0 (balance of forces).
(12-3)
If all the forces lie in the xy plane, this vector equation is equiva- lent to two component equations:
Feet, and Faty = 0 (balance of forces). Static equilibrium also implies that the vector sum of the external torques acting on the body about any point is zero, or
(12-7, 12-8)
Feet-0 (balance of torques).
(12-5) If the forces lie in the xy plane, all torque vectors are parallel to the z axis, and Eq. 12-5 is equivalent to the single component equation Text: 0 (balance of torques). (12-9)
Center of Gravity The gravitational force acts individually on each element of a body. The net effect of all individual actions may be found by imagining an equivalent total gravitational force F acting at the center of gravity. If the gravitational acceleration g is the same for all the elements of the body, the center of gravity is at the center of mass.
Elastic Moduli Three elastic moduli are used to describe the elastic behavior (deformations) of objects as they respond to forces that act on them. The strain (fractional change in length) is linearly related to the applied stress (force per unit area) by the proper modulus, according to the general relation
stress = modulus X strain.
(12-22)
Tension and Compression When an object is under tension or compression, Eq. 12-22 is written as
AL
(12-23)
where AL/L is the tensile or compressive strain of the object, Fis the magnitude of the applied force F causing the strain, A is the cross-sectional area over which F is applied (perpendicular to A, as in Fig. 12-11a), and E is the Young's modulus for the object. The stress is F/A.
Shearing When an object is under a shearing stress, Eq. 12-22 is
written as
-G
(12-24)
where Ax/L is the shearing strain of the object, Ax is the displacement of one end of the object in the direction of the ap- plied force F (as in Fig. 12-116), and G is the shear modulus of the object. The stress is FIA.
Hydraulic Stress When an object undergoes hydraulic com- pression due to a stress exerted by a surrounding fluid, Eq. 12-22 is written as
(12-25)
where p is the pressure (hydraulic stress) on the object due to the fluid, AVIV (the strain) is the absolute value of the fractional change in the object's volume due to that pressure, and B is the bulk modulus of the object.

    ''',

    '''


Review & Summary
The Law of Gravitation Any particle in the universe attracts any other particle with a gravitational force whose magnitude is F-G- (Newton's law of gravitation),
mm
(13-1)
where my and m2 are the masses of the particles, r is their separation, and G (-6.67 x 10" N-m2/kg) is the gravitational constant Gravitational Behavior of Uniform Spherical Shells The gravitational force between extended bodies is found by adding (integrating) the individual forces on individual particles within the bodies. However, if either of the bodies is a uniform spherical shell or a spherically symmetric solid, the net gravita- tional force it exerts on an external object may be computed as if all the mass of the shell or body were located at its center.
Superposition Gravitational forces obey the principle of su- perposition; that is, if n particles interact, the net force Fat on a particle labeled particle 1 is the sum of the forces on it from all the other particles taken one at a time:
1-2
(13-5)
in which the sum is a vector sum of the forces F1, on particle 1 from particles 2, 3,..., n. The gravitational force F1 on a
particle from an extended body is found by dividing the body into units of differential mass dm, each of which produces a differential force dF on the particle, and then integrating to find the sum of those forces:
F. - Sar
(13-6)
Gravitational Acceleration The gravitational acceleration a, of a particle (of mass m) is due solely to the gravitational force acting on it. When the particle is at distancer from the center of a uniform, spherical body of mass M, the magnitude F of the gravitational force on the particle is given by Eq. 13-1. Thus, by Newton's second law, F-ma
which gives
GM
(13-10)
(13-11)
Free-Fall Acceleration and Weight Because Earth's mass is not distributed uniformly, because the planet is not perfectly spherical, and because it rotates, the actual free-fall acceleration g of a particle near Earth differs slightly from the gravitational accel- eration a, and the particle's weight (equal to mg) differs from the magnitude of the gravitational force on it as calculated by Newton's law of gravitation (Eq. 13-1).
QUESTIONS
377
Gravitation Within a Spherical Shell A uniform shell of matter exerts no net gravitational force on a particle located inside it. This means that if a particle is located inside a uniform solid sphere at distance r from its center, the gravitational force exerted on the particle is due only to the mass that lies inside a sphere of radius r (the inside sphere). The force magnitude is given by
GmM R1
where M is the sphere's mass and R is its radius.
(13-19)
Gravitational Potential Energy The gravitational potential energy U(r) of a system of two particles, with masses M and m and separated by a distance r, is the negative of the work that would be done by the gravitational force of either particle acting on the other if the separation between the particles were changed from infinite (very large) to r. This energy is
GMm
(gravitational potential energy).
(13-21)
Potential Energy of a System If a system contains more than two particles, its total gravitational potential energy U is the sum of the terms representing the potential energies of all the pairs. As an example, for three particles, of masses m1, m2, and m3,
U-
Gmm2 Gm ms 712 713
Gm2my 723
(13-22)
Kepler's Laws The motion of satellites, both natural and artifi- cial, is governed by these laws:
1. The law of orbits. All planets move in elliptical orbits with the Sun at one focus.
2. The law of areas. A line joining any planet to the Sun sweeps out equal areas in equal time intervals. (This statement is equiv alent to conservation of angular momentum.)
3. The law of periods. The square of the period I of any planet is proportional to the cube of the semimajor axis a of its orbit. For circular orbits with radius r,
T-GM
(law of periods),
(13-34)
where M is the mass of the attracting body--the Sun in the case of the solar system. For elliptical planetary orbits, the semi- major axis a is substituted for r.
Energy in Planetary Motion When a planet or satellite with mass m moves in a circular orbit with radius r, its potential energy U and kinetic energy K are given by
The mechanical energy E - K + U is then
E-
GMm 2r
For an elliptical orbit of semimajor axis a,
GMm
U-
and K-
GMm 2r
(13-21, 13-38)
(13-40)
E
GMm 2a
(13-42)
(13-28)
Einstein's View of Gravitation Einstein pointed out that gravi. tation and acceleration are equivalent. This principle of equivalence led him to a theory of gravitation (the general theory of relativity) that explains gravitational effects in terms of a curvature of space.
Escape Speed An object will escape the gravitational pull of an astronomical body of mass M and radius R (that is, it will reach an infinite distance) if the object's speed near the body's surface is at least equal to the escape speed, given by
2GM R

    ''',

    '''


Review & Summary
Density The density p of any material is defined as the material's mass per unit volume:
Am PAV
(14-1)
Usually, where a material sample is much larger than atomic dimensions, we can write Eq. 14-1 as
(14-2)
Fluid Pressure A fluid is a substance that can flow; it conforms to the boundaries of its container because it cannot withstand shear- ing stress. It can, however, exert a force perpendicular to its surface. That force is described in terms of pressure p
AF ΔΑ
(14-3)
in which AF is the force acting on a surface element of area AA. If the force is uniform over a flat area, Eq. 14-3 can be written as
(14-4) a
The force resulting from fluid pressure at a particular point in fluid has the same magnitude in all directions. Gauge pressure is the difference between the actual pressure (or absolute pressure) at a point and the atmospheric pressure.
Pressure Variation with Height and Depth Pressure in a fluid at rest varies with vertical position y. For y measured positive upward, (14-7)
The pressure in a fluid is the same for all points at the same level. If h is the depth of a fluid sample below some reference level at which the pressure is p1, then the pressure in the sample is
P-Po+pgh.
(14-8)
Pascal's Principle A change in the pressure applied to an en- closed fluid is transmitted undiminished to every portion of the fluid and to the walls of the containing vessel.
Archimedes' Principle When a body is fully or partially sub- merged in a fluid, a buoyant force F, from the surrounding fluid acts on the body. The force is directed upward and has a magni- tude given by (14-16)
F-mg.
where m, is the mass of the fluid that has been displaced by the body (that is, the fluid that has been pushed out of the way by the body).
When a body floats in a fluid, the magnitude F, of the (upward) buoyant force on the body is equal to the magnitude F, of the (down- ward) gravitational force on the body. The apparent weight of a body on which a buoyant force acts is related to its actual weight by weight, weight-F
(14-19)
Flow of Ideal Fluids An ideal fluid is incompressible and lacks viscosity, and its flow is steady and irrotational. A streamline is the path followed by an individual fluid particle. A tube of flow is a bundle of streamlines. The flow within any tube of flow obeys the equation of continuity:
Ry- Ava constant,
(14-24)
in which Ry is the volume flow rate, A is the cross-sectional area of the tube of flow at any point, and v is the speed of the fluid at that point. The mass flow rate R., is
RpRy-pAv- a constant.
(14-25)
Bernoulli's Equation Applying the principle of conservation of mechanical energy to the flow of an ideal fluid leads to Bernoulli's equation along any tube of flow:
p+pv2+pgy a constant.
(14-29)

    ''',

    '''


Review & Summary
Frequency The frequency fof periodic, or oscillatory, motion is the number of oscillations per second. In the SI system, it is mea- sured in hertz:
(15-1)
1 hertz = 1 Hz= 1 oscillation per second = 1 s1. Period The period T is the time required for one complete oscil- lation, or cycle. It is related to the frequency by
1
T
(15-2)
Simple Harmonic Motion In simple harmonic motion (SHM), the displacement x(t) of a particle from its equilibrium position is described by the equation
x = xm cos(wt + )
(displacement),
(15-3)
in which x, is the amplitude of the displacement, wt + is the phase of the motion, and is the phase constant. The angular fre- quency w is related to the period and frequency of the motion by
2πf (angular frequency).
2π (15-5) T Differentiating Eq. 15-3 leads to equations for the particle's SHM velocity and acceleration as functions of time:
and
v=wx sin(wt + ) (velocity)
a = w2xm cos(wt+) (acceleration).
(15-6)
(15-7)
In Eq. 15-6, the positive quantity aut, is the velocity amplitude V of the motion. In Eq. 15-7, the positive quantity axis the acceler- ation amplitude am of the motion.
The Linear Oscillator A particle with mass m that moves un- der the influence of a Hooke's law restoring force given by F = -kx exhibits simple harmonic motion with
and
k
@=
(angular frequency)
m
T = 2π
m k
(period).
(15-12)
(15-13)
Such a system is called a linear simple harmonic oscillator. Energy A particle in simple harmonic motion has, at any time, kinetic energy K = m2 and potential energy U = kx2. If no fric- tion is present, the mechanical energy E = K+ U remains con- stant even though K and U change.
Pendulums Examples of devices that undergo simple harmonic motion are the torsion pendulum of Fig. 15-9, the simple pendulum of Fig. 15-11, and the physical pendulum of Fig. 15-12. Their periods of oscillation for small oscillations are, respectively, T = 2π VIIK (torsion pendulum).
T = 2π VL/g
(simple pendulum),
T=2π VI/mgh (physical pendulum).
(15-23)
(15-28)
(15-29)
Simple Harmonic Motion and Uniform Circular Motion Simple harmonic motion is the projection of uniform circular motion onto the diameter of the circle in which the circular motion occurs. Figure 15-15 shows that all parameters of circular motion (position, velocity, and acceleration) project to the corresponding values for simple harmonic motion.
Damped Harmonic Motion The mechanical energy E in a real oscillating system decreases during the oscillations because external forces, such as a drag force, inhibit the oscillations and transfer me- chanical energy to thermal energy. The real oscillator and its motion are then said to be damped. If the damping force is given by F1 = -by, where v is the velocity of the oscillator and b is a damping con- stant, then the displacement of the oscillator is given by
x(t) = xm e-b2m cos(w't + ),
(15-42)
where, the angular frequency of the damped oscillator, is given by
k
b2
m
4m2
(15-43)
If the damping constant is small (b < √km), then w≈ w, where w is the angular frequency of the undamped oscillator. For small b, the mechanical energy E of the oscillator is given by
E(t)=kx2me
-bt/m
(15-44) Forced Oscillations and Resonance If an external driving force with angular frequency, acts on an oscillating sys- tem with natural angular frequency w, the system oscillates with angular frequency . The velocity amplitude v of the system is greatest when
wd = w,
(15-46)
a condition called resonance. The amplitude x of the system is (approximately) greatest under the same condition.

    ''',

    '''


Review & Summary
Transverse and Longitudinal Waves Mechanical waves can exist only in material media and are governed by Newton's laws. Transverse mechanical waves, like those on a stretched string, are waves in which the particles of the medium oscillate perpendi- cular to the wave's direction of travel. Waves in which the particles of the medium oscillate parallel to the wave's direction of travel are longitudinal waves.
Sinusoidal Waves A sinusoidal wave moving in the positive direction of an x axis has the mathematical form
y(x, t) = ym sin(kx – wt),
(16-2) where y, is the amplitude of the wave, k is the angular wave number, w is the angular frequency, and kx - wt is the phase. The wavelength A is related to k by
k
2π λ
The period T and frequency ƒ of the wave are related to w by
ω
2π
1 Τ
Finally, the wave speed v is related to these other parameters by
=
k
λ T
(16-5)
(16-9)
(16-13)
Equation of a Traveling Wave Any function of the form
y(x, t) = h(kx = wt)
(16-17) can represent a traveling wave with a wave speed given by Eq. 16-13 and a wave shape given by the mathematical form of h. The plus sign denotes a wave traveling in the negative direction of the x axis, and the minus sign a wave traveling in the positive direction.
Wave Speed on Stretched String The speed of a wave on a stretched string is set by properties of the string. The speed on a string with tension and linear density μ is
v =
(16-26)
Power The average power of, or average rate at which energy is transmitted by, a sinusoidal wave on a stretched string is given by Pavguvay (16-33)
Superposition of Waves When two or more waves traverse the same medium, the displacement of any particle of the medium is the sum of the displacements that the individual waves would give it. Interference of Waves Two sinusoidal waves on the same string exhibit interference, adding or canceling according to the prin- ciple of superposition. If the two are traveling in the same direction and have the same amplitude ym and frequency (hence the same wavelength) but differ in phase by a phase constant 6, the result is a single wave with this same frequency:
-
y'(x,t) = [2y, cosø] sin(kx − at +48).
(16-51)
If = 0, the waves are exactly in phase and their interference is fully constructive; if = #rad, they are exactly out of phase and their interference is fully destructive.
Phasors A wave y(x, t) can be represented with a phasor. This is a vector that has a magnitude equal to the amplitude ym of the wave and that rotates about an origin with an angular speed equal to the angular frequency @ of the wave. The projection of the rotat- ing phasor on a vertical axis gives the displacement y of a point along the wave's travel.
Standing Waves The interference of two identical sinusoidal waves moving in opposite directions produces standing waves. For a string with fixed ends, the standing wave is given by y'(x, t) = [2y, sin kx] cos wt.
(16-60) Standing waves are characterized by fixed locations of zero dis- placement called nodes and fixed locations of maximum displace- ment called antinodes.
Resonance Standing waves on a string can be set up by reflection of traveling waves from the ends of the string. If an end is fixed, it must be the position of a node. This limits the frequen- cies at which standing waves will occur on a given string. Each pos- sible frequency is a resonant frequency, and the corresponding standing wave pattern is an oscillation mode. For a stretched string of length L with fixed ends, the resonant frequencies are for n = 1, 2, 3,....
ν
ν
λ
-= n 2L'
(16-66)
The oscillation mode corresponding to n = 1 is called the funda- mental mode or the first harmonic; the mode corresponding to n = 2 is the second harmonic; and so on.

    ''',

    '''

    Review & Summary
Sound Waves Sound waves are longitudinal mechanical waves that can travel through solids, liquids, or gases. The speed v of a sound wave in a medium having bulk modulus B and density pis
B
(speed of sound).
In air at 20°C, the speed of sound is 343 m/s.
(17-3)
A sound wave causes a longitudinal displacements of a mass element in a medium as given by
-
S=5, cos(kx-t),
(17-12)
where s,, is the displacement amplitude (maximum displacement) from equilibrium, k-2/A, and w-2πf, A and ƒ being the wave- length and frequency of the sound wave. The wave also causes a pressure change Ap from the equilibrium pressure:
Ap Ap, sin(kx-out),
where the pressure amplitude is
Apm - (vpw)
(17-13)
(17-14)
Interference The interference of two sound waves with identi- cal wavelengths passing through a common point depends on their phase difference & there. If the sound waves were emitted in phase and are traveling in approximately the same direction, is given by AL λ
(17-21)
where AL is their path length difference (the difference in the distances traveled by the waves to reach the common point). Fully constructive interference occurs when is an integer multiple of 2,
-m(2), for m -0,1,2,...,
and, equivalently, when AL is related to wavelength A by AL
0,1,2,...
A
(17-22)
(17-23)
Fully destructive interference occurs when is an odd multiple of #, (17-24)
=(2m+1), for m0,1,2,...,
and, equivalently, when AL is related to A by
AL
-0.5,1.5,2.5,....
(17-25) Sound Intensity The intensity I of a sound wave at a surface is the average rate per unit area at which energy is transferred by the wave through or onto the surface:
(17-26)
where P is the time rate of energy transfer (power) of the sound wave
and A is the area of the surface intercepting the sound. The intensity I
is related to the displacement amplitudes,, of the sound wave by
I-pva's
(17-27) The intensity at a distancer from a point source that emits sound waves of power P, is
1-
(17-28)
Sound Level in Decibels The sound level ẞ in decibels (dB) is defined as
6- (10 dB) log
(17-29)
where 1, (-10-12 W/m2) is a reference intensity level to which all intensities are compared. For every factor-of-10 increase in inten- sity, 10 dB is added to the sound level.
Standing Wave Patterns in Pipes Standing sound wave patterns can be set up in pipes. A pipe open at both ends will resonate at frequencies
nv 2L
n-1,2,3,...,
(17-39)
where v is the speed of sound in the air in the pipe. For a pipe closed at one end and open at the other, the resonant fre- quencies are
ην 4L
n-1,3,5,....
(17-41)
Beats Beats arise when two waves having slightly different fre- quencies, f, and f2, are detected together. The beat frequency is
(17-46)
The Doppler Effect The Doppler effect is a change in the observed frequency of a wave when the source or the detec tor moves relative to the transmitting medium (such as air). For sound the observed frequency f'" is given in terms of the source frequency/by
V vs
(general Doppler effect),
(17-47)
where vo is the speed of the detector relative to the medium, vg is that of the source, and v is the speed of sound in the medium. The signs are chosen such that f' tends to be greater for motion toward and less for motion away.
Shock Wave If the speed of a source relative to the medium exceeds the speed of sound in the medium, the Doppler equation no longer applies. In such a case, shock waves result. The half-angle 6 of the Mach cone is given by
sin -
Vs
(Mach cone angle).
(17-57)

    ''',

    '''

    Review & Summary
Temperature; Thermometers Temperature is an SI base quantity related to our sense of hot and cold. It is measured with a thermometer, which contains a working substance with a measur able property, such as length or pressure, that changes in a regular way as the substance becomes hotter or colder.
Zeroth Law of Thermodynamics When a thermometer and some other object are placed in contact with each other, they even- tually reach thermal equilibrium. The reading of the thermometer is then taken to be the temperature of the other object. The process provides consistent and useful temperature measurements because of the zeroth law of thermodynamics: If bodies A and B are each in thermal equilibrium with a third body C (the thermometer), then A and B are in thermal equilibrium with each other.
The Kelvin Temperature Scale In the SI system, tempera- ture is measured on the Kelvin scale, which is based on the triple point of water (273.16 K). Other temperatures are then defined by
use of a constant-volume gas thermometer, in which a sample of gas is maintained at constant volume so its pressure is proportional to its temperature. We define the temperature T as measured with a gas thermometer to be
T-(273.16 K) (lim
Ps
(18-6)
Here T is in kelvins, and p, and p are the pressures of the gas at 273.16 K and the measured temperature, respectively.
Celsius and Fahrenheit Scales The Celsius temperature scale is defined by
Tc-T-273.15°,
with T'in kelvins. The Fahrenheit temperature scale is defined by T-TC+32°.
(18-7)
(18-8)
REVIEW & SUMMARY
539
Thermal Expansion All objects change size with changes in tem- perature. For a temperature change AT, a change AL in any linear dimension Lis given by
AL - La AT,
(18-9)
in which a is the coefficient of linear expansion. The change AV in the volume V of a solid or liquid is
AV - VBAT.
The integration is necessary because the pressure p may vary dur- ing the volume change.
First Law of Thermodynamics The principle of conser vation of energy for a thermodynamic process is expressed in the first law of thermodynamics, which may assume either of the forms
(18-10)
or
Here ẞ - 3a is the material's coefficient of volume expansion.
Heat Heat Q is energy that is transferred between a system and its environment because of a temperature difference between them. It can be measured in joules (J), calories (cal), kilocalories (Cal or kcal), or British thermal units (Btu), with
1 cal - 3.968 x 10 Btu - 4.1868 J.
(18-12)
Heat Capacity and Specific Heat If heat Q is absorbed by an object, the object's temperature change T/T, is related to Q by
Q-C(T-T).
(18-13)
in which C is the heat capacity of the object. If the object has mass m, then
Q-cm(T-T),
(18-14)
where c is the specific heat of the material making up the object. The molar specific heat of a material is the heat capacity per mole, which means per 6.02 x 1023 elementary units of the material.
Heat of Transformation Matter can exist in three common states: solid, liquid, and vapor. Heat absorbed by a material may change the material's physical state-for example, from solid to liq- uid or from liquid to gas. The amount of energy required per unit mass to change the state (but not the temperature) of a particular material is its heat of transformation L. Thus,
Q-Lm.
(18-16)
The heat of vaporization L, is the amount of energy per unit mass that must be added to vaporize a liquid or that must be removed to condense a gas. The heat of fusion L is the amount of energy per unit mass that must be added to melt a solid or that must be re- moved to freeze a liquid.
Work Associated with Volume Change A gas may exchange energy with its surroundings through work. The amount of work W done by a gas as it expands or contracts from an initial volume V, to a final volume V, is given by
W- dW- pdV.
(18-25)
AE-EE-Q-W dEdQ-dw
(first law)
(18-26)
(first law).
(18-27)
E represents the internal energy of the material, which depends only on the material's state (temperature, pressure, and volume). Q represents the energy exchanged as heat between the system and its surroundings; Q is positive if the system absorbs heat and negative if the system loses heat. W is the work done by the sys- tem; W is positive if the system expands against an external force from the surroundings and negative if the system contracts be- cause of an external force. Q and W are path dependent; AE is path independent.
Applications of the First Law The first law of thermody- namics finds application in several special cases:
adiabatic processes: Q-0, AE-W constant-volume processes: W-0, AE-Q
cyclical processes: AE-0, 0-w free expansions: Q-W-AE-0
Conduction, Convection, and Radiation The rate Podat which energy is conducted through a slab for which one face is maintained at the higher temperature Ty, and the other face is maintained at the lower temperature Teis
Pond -- KA TH-Ic
L
(18-32)
Here each face of the slab has area A, the length of the slab (the distance between the faces) is L, and k is the thermal conductivity of the material.
Convection occurs when temperature differences cause an en- ergy transfer by motion within a fluid.
Radiation is an energy transfer via the emission of electromag- netic energy. The rate P at which an object emits energy via ther- mal radiation is
Pro-EAT,
(18-38)
where (-5.6704 × 10 W/m2K) is the Stefan-Boltzmann constant, is the emissivity of the object's surface, A is its surface area, and T is its surface temperature (in kelvins). The rate Pabu at which an object absorbs energy via thermal radiation from its envi- ronment, which is at the uniform temperature T... (in kelvins), is (18-39)
Pats-σEAT

    ''',

    '''

    Review & Summary
Kinetic Theory of Gases The kinetic theory of gases relates the macroscopic properties of gases (for example, pressure and temperature) to the microscopic properties of gas molecules (for example, speed and kinetic energy).
Avogadro's Number One mole of a substance contains Na (Avogadro's number) elementary units (usually atoms or mole- cules), where N, is found experimentally to be
N-6.02 x 10 mol-1
(Avogadro's number). (19-1)
One molar mass M of any substance is the mass of one mole of the substance. It is related to the mass m of the individual molecules of the substance by (19-4)
M-mNa
The number of moles n contained in a sample of mass Mum consisting of N molecules, is given by
N Mn Mu
(19-2, 19-3)
NA
M
mNA
576
CHAPTER 19 THE KINETIC THEORY OF GASES
Ideal Gas An ideal gas is one for which the pressure p, volume V, and temperature T'are related by
pV = nRT (ideal gas law).
a gas are
Vang-
8RT V M
(average speed),
(19-31)
(19-5)
2RT
Vp
M
(most probable speed).
(19-35)
Here n is the number of moles of the gas present and R is a constant (8.31 J/mol·K) called the gas constant. The ideal gas law can also be
written as
pV - NkT,
where the Boltzmann constant kis
138 x 10-J/K.
NA
(19-9)
(19-7)
and the rms speed defined above in Eq. 19-22.
Molar Specific Heats The molar specific heat Cy of a gas at constant volume is defined as
ΔΕ
η ΔΤ
nAT
(19-39, 19-41)
Work in an Isothermal Volume Change The work done by an ideal gas during an isothermal (constant-temperature) change from volume V, to volume V, is
W-ART In (ideal gas, isothermal process). (19-14)
Pressure, Temperature, and Molecular Speed The pres- sure exerted by n moles of an ideal gas, in terms of the speed of its molecules, is
3V
(19-21) where V-V(v) is the root-mean-square speed of the mole- cules of the gas. With Eq. 19-5 this gives
in which is the energy transferred as heat to or from a sample of n moles of the gas, AT is the resulting temperature change of the gas, and AE is the resulting change in the internal energy of the gas. For an ideal monatomic gas,
CVR 12.5 J/mol K.
"AT'
(19-43)
The molar specific heat C, of a gas at constant pressure is defined to be (19-46) in which Q, n, and AT are defined as above. C, is also given by C-Cy+R.
For n moles of an ideal gas, EnCyT
(ideal gas).
(19-22)
(19-49)
(19-44)
3RT M
Temperature and Kinetic Energy The average transla- tional kinetic energy Kay per molecule of an ideal gas is
Kay-KT.
(19-24)
Mean Free Path The mean free path A of a gas molecule is its average path length between collisions and is given by
(19-25)
1 √2m2 N/V where N/V is the number of molecules per unit volume and d is the molecular diameter.
Maxwell Speed Distribution The Maxwell speed distri- bution P(v) is a function such that P(v) dv gives the fraction of molecules with speeds in the interval dv at speed v:
P(v)-4-
M 2RT
(19-27)
Three measures of the distribution of speeds among the molecules of
If a moles of a confined ideal gas undergo a temperature change AT due to any process, the change in the internal energy of the gas is (19-45)
AEst-nCAT (ideal gas, any process).
Degrees of Freedom and Cy The equipartition of energy theorem states that every degree of freedom of a molecule has an energy kT per molecule (-RT per mole). If f is the number of degrees of freedom, then E-(f/2)nRT and
C-(4)R
R 4.16f J/mol K.
(19-51)
For monatomic gases f-3 (three translational degrees); for di- atomic gases f = 5 (three translational and two rotational degrees). Adiabatic Process When an ideal gas undergoes an adiabatic volume change (a change for which Q = 0),
pV-a constant (adiabatic process),
(19-53)
in which y(-C/C) is the ratio of molar specific heats for the gas. For a free expansion, however, pV a constant.

    ''',

    '''

    Review & Summary
One-Way Processes An irreversible process is one that can- not be reversed by means of small changes in the environment. The direction in which an irreversible process proceeds is set by the change in entropy AS of the system undergoing the process. Entropy S is a state property (or state function) of the system; that is, it depends only on the state of the system and not on the way in which the system reached that state. The entropy postulate states (in part): If an irreversible process occurs in a closed system, the entropy of the system always increases
Calculating Entropy Change The entropy change AS for an irreversible process that takes a system from an initial state i to a final state fis exactly equal to the entropy change AS for any re- versible process that takes the system between those same two states. We can compute the latter (but not the former) with
(20-1)
Here is the energy transferred as heat to or from the system dur- ing the process, and T is the temperature of the system in kelvins during the process.
For a reversible isothermal process, Eq. 20-1 reduces to
(20-2)
When the temperature change AT of a system is small relative to the temperature (in kelvins) before and after the process, the en- tropy change can be approximated as
AS-S-S
TINE
(20-3)
where T., is the system's average temperature during the process. When an ideal gas changes reversibly from an initial state with temperature T, and volume V, to a final state with temperature T and volume V,, the change AS in the entropy of the gas is
V1
AS-S, - S1 = nR In+nC, In-
T T
(20-4)
The Second Law of Thermodynamics This law, which is an extension of the entropy postulate, states: If a process occurs in a closed system, the entropy of the system increases for irreversible processes and remains constant for reversible processes. It never de- creases. In equation form,
AS ≥ 0.
(20-5)
Engines An engine is a device that, operating in a cycle, extracts energy as heat IQH from a high-temperature reservoir and does a cer- tain amount of work W. The efficiency of any engine is defined as W energy we get (20-11) energy we pay for
In an ideal engine, all processes are reversible and no wasteful energy transfers occur due to, say, friction and turbulence. A Carnot engine is an ideal engine that follows the cycle of Fig. 20-9. Its efficiency is
1
TH
(20-12, 20-13)
in which T and T are the temperatures of the high- and low- temperature reservoirs, respectively. Real engines always have an efficiency lower than that given by Eq. 20-13. Ideal engines that are not Carnot engines also have lower efficiencies.
A perfect engine is an imaginary engine in which energy ex- tracted as heat from the high-temperature reservoir is converted com- pletely to work. Such an engine would violate the second law of ther- modynamics, which can be restated as follows: No series of processes is possible whose sole result is the absorption of energy as heat from a thermal reservoir and the complete conversion of this energy to work. Refrigerators A refrigerator is a device that, operating in a cy- cle, has work W done on it as it extracts energy IQ as heat from a low-temperature reservoir. The coefficient of performance K of a refrigerator is defined as
what we want
what we pay for
W
(20-14)
A Carnot refrigerator is a Carnot engine operating in reverse.
QUESTIONS
603
For a Carnot refrigerator, Eq. 20-14 becomes
Ke
ел
T TH-T
(20-15, 20-16)
A perfect refrigerator is an imaginary refrigerator in which energy extracted as heat from the low-temperature reservoir is con- verted completely to heat discharged to the high-temperature reser- voir, without any need for work. Such a refrigerator would violate the second law of thermodynamics, which can be restated as follows: No series of processes is possible whose sole result is the transfer of energy as heat from a reservoir at a given temperature to a reservoir at a higher temperature.
Entropy from a Statistical View The entropy of a system can be defined in terms of the possible distributions of its molecules. For identical molecules, each possible distribution of molecules is called a microstate of the system. All equivalent microstates are grouped into
a configuration of the system. The number of microstates in a config- uration is the multiplicity W of the configuration.
For a system of N molecules that may be distributed between the two halves of a box, the multiplicity is given by
N!
W-
(20-20)
in which n, is the number of molecules in one half of the box and n2 is the number in the other half. A basic assumption of statistical mechanics is that all the microstates are equally probable. Thus, con- figurations with a large multiplicity occur most often.
The multiplicity W of a configuration of a system and the en- tropy S of the system in that configuration are related by Boltzmann's entropy equation:
S-k In W,
where k = 1.38 x 10-2 J/K is the Boltzmann constant.
(20-21)

    ''',

    '''

    Review & Summary
Electric Charge The strength of a particle's electrical interaction with objects around it depends on its electric charge (usually repre- sented as q), which can be either positive or negative. Particles with the same sign of charge repel each other, and particles with opposite signs of charge attract each other. An object with equal amounts of the two kinds of charge is electrically neutral, whereas one with an imbalance is electrically charged and has an excess charge.
Conductors are materials in which a significant number of electrons are free to move. The charged particles in nonconductors (insulators) are not free to move.
Electric current i is the rate dq/dt at which charge passes a point: (electric current).
dg i- dt
(21-3)
Coulomb's Law Coulomb's law describes the electrostatic force (or electric force) between two charged particles. If the parti- cles have charges q, and 92, are separated by distance r, and are at rest (or moving only slowly) relative to each other, then the magni- tude of the force acting on each due to the other is given by
19:
4 TE
(Coulomb's law),
(21-4)
where - 8.85 x 10-12 C/N m2 is the permittivity constant. The ratio 1/4, is often replaced with the electrostatic constant (or Coulomb constant) k=8.99 x 10°N m2/C2.
The electrostatic force vector acting on a charged particle due to a second charged particle is either directly toward the second particle (opposite signs of charge) or directly away from it (same sign of charge). As with other types of forces, if multiple electrostatic forces act on a particle, the net force is the vector sum (not scalar sum) of the individual forces.
The two shell theories for electrostatics are
Shell theorem 1: A charged particle outside a shell with charge uniformly distributed on its surface is attracted or repelled as if the shell's charge were concentrated as a particle at its center. Shell theorem 2: A charged particle inside a shell with charge uniformly distributed on its surface has no net force acting on it due to the shell.
Charge on a conducting spherical shell spreads uniformly over the (external) surface.
The Elementary Charge Electric charge is quantized (re- stricted to certain values). The charge of a particle can be written as ne, where n is a positive or negative integer and e is the elemen- tary charge, which is the magnitude of the charge of the electron and proton (-1.602 × 10-19 C).
Conservation of Charge The net electric charge of any iso- lated system is always conserved.

    ''',

    '''

    Review & Summary
Electric Field To explain the electrostatic force between two charges, we assume that each charge sets up an electric field in the space around it. The force acting on each charge is then due to the electric field set up at its location by the other charge.
Definition of Electric Field The electric field E at any point is defined in terms of the electrostatic force ♬ that would be ex- erted on a positive test charge qoplaced there:
(22-1)
Electric Field Lines Electric field lines provide a means for visu- alizing the direction and magnitude of electric fields. The electric field vector at any point is tangent to a field line through that point. The density of field lines in any region is proportional to the magnitude of the electric field in that region. Field lines originate on positive charges and terminate on negative charges.
Field Due to a Point Charge The magnitude of the electric field E set up by a point charge q at a distance / from the charge is
1
E-
4m r2
(22-3)
The direction of E is away from the point charge if the charge is positive and toward it if the charge is negative.
Field Due to an Electric Dipole An electric dipole consists of two particles with charges of equal magnitude q but opposite sign, separated by a small distance d. Their electric dipole moment p has magnitude qd and points from the negative charge to the positive charge. The magnitude of the electric field set up by the dipole at a distant point on the dipole axis (which runs through both charges) is
E-
2m 21
(22-9)
where z is the distance between the point and the center of the dipole.
Field Due to a Continuous Charge Distribution The electric field due to a continuous charge distribution is found by treating charge elements as point charges and then summing, via integration, the electric field vectors produced by all the charge el- ements to find the net vector.
QUESTIONS
651
Field Due to a Charged Disk The electric field magnitude at a point on the central axis through a uniformly charged disk is given by
2
(22-26)
where z is the distance along the axis from the center of the disk, R is the radius of the disk, and is the surface charge density.
Force on a Point Charge in an Electric Field When a point charge q is placed in an external electric field E, the electro- static force F that acts on the point charge is
Force F has the same direction as E if q is positive and the opposite direction if q is negative.
Dipole in an Electric Field When an electric dipole of dipole moment ♬ is placed in an electric field E, the field exerts a torque 7 on the dipole:
(22-34)
The dipole has a potential energy U associated with its orientation in the field:
U--p.Ē.
(22-28)
(22-38) This potential energy is defined to be zero when is perpendicular to E; it is least (UPE) when p is aligned with E and greatest (U-PE) when is directed opposite E.

    ''',

    '''

    Review & Summary
Gauss' Law Gauss' law and Coulomb's law are different ways of describing the relation between charge and electric field in static situations. Gauss' law is
-
(Gauss' law),
(23-6)
in which gene is the net charge inside an imaginary closed surface (a Gaussian surface) and is the net flux of the electric field through the surface:
0-9 E-dA
(electric flux through a Gaussian surface).
(23-4)
with uniform linear charge density A is perpendicular to the line of charge and has magnitude
E
(line of charge).
2 mar
(23-12)
where r is the perpendicular distance from the line of charge to the point.
4. The electric field due to an infinite nonconducting sheet with
uniform surface charge density or is perpendicular to the plane of the sheet and has magnitude
σ
Coulomb's law can be derived from Gauss' law.
Applications of Gauss' Law Using Gauss' law and, in some cases, symmetry arguments, we can derive several important results in electrostatic situations. Among these are:
1. An excess charge on an isolated conductor is located entirely on the outer surface of the conductor.
2. The external electric field near the surface of a charged conductor is perpendicular to the surface and has a magnitude that depends on the surface charge density o
E- (conducting surface).
Within the conductor, E = 0.
(23-11)
3. The electric field at any point due to an infinite line of charge
E-
(sheet of charge).
200
(23-13)
5. The electric field outside a spherical shell of charge with radius R and total charge q is directed radially and has magnitude
4m
(spherical shell, for r = R).
(23-15)
Here r is the distance from the center of the shell to the point at which E is measured. (The charge behaves, for external points, as if it were all located at the center of the sphere.) The field inside a uniform spherical shell of charge is exactly zero:
E-0 (spherical shell, for r < R).
(23-16)
6. The electric field inside a uniform sphere of charge is directed radially and has magnitude
E-
4 WER
(23-20)

    ''',

    '''

    Review & Summary
Electric Potential The electric potential V at a point P in the electric field of a charged object is
-W
40
(24-2)
where W. is the work that would be done by the electric force on a positive test charge were it brought from an infinite distance to P, and U is the potential energy that would then be stored in the test charge-object system.
Electric Potential Energy If a particle with charge q is placed at a point where the electric potential of a charged object is V, the electric potential energy U of the particle-object system is
U-qV.
(24-3)
If the particle moves through a potential difference AV, the change in the electric potential energy is
AU-qAV = q(V-Vi
(24-4)
Mechanical Energy If a particle moves through a change AV in electric potential without an applied force acting on it, applying the conservation of mechanical energy gives the change in kinetic energy as (24-9)
AK- -qAV.
If, instead, an applied force acts on the particle, doing work Wapp the change in kinetic energy is
AK--qAV + Wapp
(24-11)
In the special case when AK-0, the work of an applied force
708
CHAPTER 24 ELECTRIC POTENTIAL
involves only the motion of the particle through a potential difference:
Wapp-qAV (for K-K).
(24-12)
Equipotential Surfaces The points on an equipotential sur- face all have the same electric potential. The work done on a test charge in moving it from one such surface to another is independent of the locations of the initial and final points on these surfaces and of the path that joins the points. The electric field E is always directed perpendicularly to corresponding equipotential surfaces.
Finding V from E The electric potential difference between two points / and fis
ds,
(24-18)
where the integral is taken over any path connecting the points. If the integration is difficult along any particular path, we can choose a differ- ent path along which the integration might be easier. If we choose V,- 0, we have, for the potential at a particular point,
v-- fx. dr.
(24-19)
In the special case of a uniform field of magnitude E, the po tential change between two adjacent (parallel) equipotential lines separated by distance Ax is
AV--EAX.
(24-21)
Potential Due to a Charged Particle The electric potential due to a single charged particle at a distance r from that particle is (24-26)
14 4T
where V has the same sign as q. The potential due to a collection of charged particles is
v-v-
41
(24-27)
Potential Due to an Electric Dipole At a distance r from an electric dipole with dipole moment magnitude pqd, the elec- tric potential of the dipole is
1
p cos @
V-
(24-30)
4 TE
شو
for r >> d; the angle is defined in Fig. 24-13. Potential Due to a Continuous Charge Distribution For a continuous distribution of charge, Eq. 24-27 becomes
(24-32)
in which the integral is taken over the entire distribution. Calculating E from V The component of E in any direction is the negative of the rate at which the potential changes with dis- tance in that direction:
av
E
as
The x, y, and z components of E may be found from
(24-40)
av
E,
av ду
av
E-
(24-41)
az
E, When E is uniform, Eq. 24-40 reduces to
E-
AV As
(24-42)
where s is perpendicular to the equipotential surfaces. Electric Potential Energy of a System of Charged Particles The electric potential energy of a system of charged particles is equal to the work needed to assemble the system with the particles initially at rest and infinitely distant from each other. For two particles at separation r
U-W- 1992
4 TE
(24-46)
Potential of a Charged Conductor An excess charge placed on a conductor will, in the equilibrium state, be located entirely on the outer surface of the conductor. The charge will distribute itself so that the following occur: (1) The entire conductor, including interior points, is at a uniform potential. (2) At every internal point, the elec tric field due to the charge cancels the external electric field that oth- erwise would have been there. (3) The net electric field at every point on the surface is perpendicular to the surface.

    ''',

    '''

    Review & Summary
Capacitor; Capacitance A capacitor consists of two isolated conductors (the plates) with charges +q and -q. Its capacitance C is defined from
q-CV,
where V is the potential difference between the plates.
(25-1)
Determining Capacitance We generally determine the capacitance of a particular capacitor configuration by (1) assuming a charge q to have been placed on the plates, (2) finding the electric field E due to this charge, (3) evaluating the potential difference V, and (4) calculating C from Eq. 25-1. Some specific results are the following: A parallel-plate capacitor with flat parallel plates of area A and spacing d has capacitance
C-
EA d
(25-9)
A cylindrical capacitor (two long coaxial cylinders) of length Land radii a and b has capacitance
C-2
L In(b/a)
(25-14)
A spherical capacitor with concentric spherical plates of radii a and b has capacitance
C-4
ab b-a
An isolated sphere of radius R has capacitance
C-4 R.
(25-17)
(25-18)
Capacitors in Parallel and in Series The equivalent capacitances C. of combinations of individual capacitors con- nected in parallel and in series can be found from
Ca
Equivalent capacitances can be used to calculate the capacitances of more complicated series-parallel combinations.
Potential Energy and Energy Density The electric poten- tial energy U of a charged capacitor,
2C
(25-21, 25-22)
is equal to the work required to charge the capacitor. This energy can be associated with the capacitor's electric field E. By extension we can associate stored energy with any electric field. In vacuum, the energy density, or potential energy per unit volume, within an electric field of magnitude E is given by
(25-25)
Capacitance with a Dielectric If the space between the plates of a capacitor is completely filled with a dielectric material, the capacitance C is increased by a factor x, called the dielectric constant, which is characteristic of the material. In a region that is completely filled by a dielectric, all electrostatic equations con- taining must be modified by replacing with K-
The effects of adding a dielectric can be understood physically in terms of the action of an electric field on the permanent or induced electric dipoles in the dielectric slab. The result is the for- mation of induced charges on the surfaces of the dielectric, which results in a weakening of the field within the dielectric for a given amount of free charge on the plates.
Gauss' Law with a Dielectric When a dielectric is present, Gauss' law may be generalized to
-C (n capacitors in parallel)
(25-19)
1-1
q.
(25-36)
and
Сод
ΣΕ
(n capacitors in series).
(25-20)
Here q is the free charge; any induced surface charge is accounted for by including the dielectric constant inside the integral.

    ''',

    '''


Current An electric current i in a conductor is defined by
i =
dq dt
(26-1) Here dq is the amount of (positive) charge that passes in time dt through a hypothetical surface that cuts across the conductor. By convention, the direction of electric current is taken as the direc- tion in which positive charge carriers would move. The SI unit of electric current is the ampere (A): 1A = 1 C/s.
Current Density Current (a scalar) is related to current density J (a vector) by
i =
(26-4) where dÃ is a vector perpendicular to a surface element of area dA and the integral is taken over any surface cutting across the conduc- tor. J has the same direction as the velocity of the moving charges if they are positive and the opposite direction if they are negative.
Drift Speed of the Charge Carriers When an electric field E is established in a conductor, the charge carriers (assumed posi- tive) acquire a drift speed va in the direction of E; the velocity va is related to the current density by J = (ne)vd,
where ne is the carrier charge density.
(26-7)
Resistance of a Conductor The resistance R of a conductor is defined as
V
R =
(definition of R),
(26-8) where V is the potential difference across the conductor and i is the current. The SI unit of resistance is the ohm (N): 12 = 1 V/A. Similar equations define the resistivity p and conductivity or of a material: (26-12, 26-10)
1
E
p =
=
(definitions of p and σ),
σ J
764
CHAPTER 26 CURRENT AND RESISTANCE
where E is the magnitude of the applied electric field. The SI unit of resistivity is the ohm-meter (N·m). Equation 26-10 corresponds to the vector equation
Ẻ = p].
(26-11)
The resistance R of a conducting wire of length L and uniform cross section is
L
R = P
噪
where A is the cross-sectional area.
(26-16)
Change of p with Temperature The resistivity p for most materials changes with temperature. For many materials, including metals, the relation between p and temperature T is approximated by the equation
P-Po Poa(T — To).
(26-17)
Here To is a reference temperature, po is the resistivity at To, and a is the temperature coefficient of resistivity for the material.
Ohm's Law A given device (conductor, resistor, or any other electrical device) obeys Ohm's law if its resistance R, defined by Eq. 26-8 as V/i, is independent of the applied potential difference V. A given material obeys Ohm's law if its resistivity, defined by Eq. 26-10, is independent of the magnitude and direction of the ap- plied electric field E.
Resistivity of a Metal By assuming that the conduction elec- trons in a metal are free to move like the molecules of a gas, it is
possible to derive an expression for the resistivity of a metal:
m
p =
e2nT
(26-22)
Here n is the number of free electrons per unit volume and is the mean time between the collisions of an electron with the atoms of the metal. We can explain why metals obey Ohm's law by pointing out that is essentially independent of the magnitude E of any electric field applied to a metal.
Power The power P, or rate of energy transfer, in an electrical device across which a potential difference Vis maintained is
PiV (rate of electrical energy transfer). (26-26) Resistive Dissipation If the device is a resistor, we can write Eq. 26-26 as
P = i2R =
V2 R
(resistive dissipation).
(26-27, 26-28)
In a resistor, electric potential energy is converted to internal ther- mal energy via collisions between charge carriers and atoms. Semiconductors Semiconductors are materials that have few conduction electrons but can become conductors when they are doped with other atoms that contribute charge carriers. Superconductors Superconductors are materials that lose all electrical resistance at low temperatures. Some materials are su- perconducting at surprisingly high temperatures.

''',

'''


Emf An emf device does work on charges to maintain a potential difference between its output terminals. If dW is the work the device does to force positive charge dq from the negative to the positive ter- minal, then the emf (work per unit charge) of the device is
dw 8 = dq
(definition of %).
(27-1)
The volt is the SI unit of emf as well as of potential difference. An ideal emf device is one that lacks any internal resistance. The potential dif- ference between its terminals is equal to the emf. A real emf device has internal resistance. The potential difference between its terminals is equal to the emf only if there is no current through the device. Analyzing Circuits The change in potential in traversing a resistance R in the direction of the current is -iR; in the opposite direction it is +iR (resistance rule). The change in potential in tra- versing an ideal emf device in the direction of the emf arrow is +&; in the opposite direction it is - (emf rule). Conservation of energy leads to the loop rule:
Loop Rule. The algebraic sum of the changes in potential encountered in a complete traversal of any loop of a circuit must be zero. Conservation of charge gives us the junction rule:
Junction Rule. The sum of the currents entering any junction must be equal to the sum of the currents leaving that junction.
Single-Loop Circuits The current in a single-loop circuit con- taining a single resistance R and an emf device with emf & and in- ternal resistance r is
where Vis the potential across the terminals of the battery. The rate P, at which energy is dissipated as thermal energy in the battery is P=Pr (27-16) The rate Pemf at which the chemical energy in the battery changes is Pemf = i8. (27-17)
Series Resistances When resistances are in series, they have the same current. The equivalent resistance that can replace a se- ries combination of resistances is
n
Req=R (n resistances in series).
j=1
(27-7)
Parallel Resistances When resistances are in parallel, they have the same potential difference. The equivalent resistance that can replace a parallel combination of resistances is given by
=
1 R j=1
1
(n resistances in parallel).
(27-24)
RC Circuits When an emf & is applied to a resistance R and ca- pacitance C in series, as in Fig. 27-15 with the switch at a, the charge on the capacitor increases according to
q=CE(1-e-RC) (charging a capacitor),
(27-33)
in which CE = qo is the equilibrium (final) charge and RC = ris the ca- pacitive time constant of the circuit. During the charging, the current is
dq dt
8 R
-)e-
-t/RC
(charging a capacitor).
(27-34)
8 R+r'
which reduces to i = E/R for an ideal emf device with r = 0.
(27-4)
Power When a real battery of emf % and internal resistance r does work on the charge carriers in a current i through the battery, the rate P of energy transfer to the charge carriers is
P = iV,
When a capacitor discharges through a resistance R, the charge on the capacitor decays according to
(27-39)
q = qoe RC (discharging a capacitor). During the discharging, the current is
(27-14)
i =
=
RC
-(10) e-
-1/RC
(discharging a capacitor). (27-40)
da dt

''',

'''


Magnetic Field B A magnetic field B is defined in terms of the force F acting on a test particle with charge q moving through the field with velocity :
FB = qv × B.
The SI unit for B is the tesla (T): 1 T = 1 N/(Am) = 104 gauss.
(28-2)
The Hall Effect When a conducting strip carrying a current i is placed in a uniform magnetic field B, some charge carriers (with charge e) build up on one side of the conductor, creating a poten- tial difference V across the strip. The polarities of the sides indicate the sign of the charge carriers.
A Charged Particle Circulating in a Magnetic Field A charged particle with mass m and charge magnitude |g| moving with velocity v perpendicular to a uniform magnetic field B will travel in a circle. Applying Newton's second law to the circular motion yields
my2 |q|vB =
from which we find the radius r of the circle to be
mv
(28-15)
(28-16) The frequency of revolution f, the angular frequency, and the period of the motion T are given by
f=
ω
=
=
1 q B 2πm
(28-19, 28-18, 28-17)
2π T
Magnetic Force on a Current-Carrying Wire A straight wire carrying a current i in a uniform magnetic field experiences a sideways force (28-26) The force acting on a current element i dĽ in a magnetic field is
F= ILX B.
dF2 = idĽx B.
(28-28)
The direction of the length vector L or d is that of the current i.
Torque on a Current-Carrying Coil A coil (of area A and N turns, carrying current i) in a uniform magnetic field B will experience a torque 7 given by
7=AX B.
(28-37)
Here is the magnetic dipole moment of the coil, with magnitude μ = NiA and direction given by the right-hand rule.
Orientation Energy of a Magnetic Dipole The orienta- tion energy of a magnetic dipole in a magnetic field is
U(0)=-μ.B.
(28-38)
If an external agent rotates a magnetic dipole from an initial orien- tation ; to some other orientation 0 and the dipole is stationary both initially and finally, the work W, done on the dipole by the agent is
Wa=AU = Uf- Uj.
(28-39)

''',

'''

The Biot-Savart Law The magnetic field set up by a current- carrying conductor can be found from the Biot-Savart law. This law asserts that the contribution dB to the field produced by a current-length element i ds at a point P located a distance r from the current element is
dB
мо ids × f 4π 2
(Biot-Savart law).
(29-3)
Here ↑ is a unit vector that points from the element toward P. The quantity μo, called the permeability constant, has the value
4 X 10-7 T.m/A≈ 1.26 × 10-6 T∙m/A.
Magnetic Field of a Long Straight Wire For a long straight wire carrying a current i, the Biot-Savart law gives, for the magnitude of the magnetic field at a perpendicular distance R from the wire,
B
Hol 2πR
(long straight wire).
(29-4)
Magnetic Field of a Circular Arc The magnitude of the magnetic field at the center of a circular arc, of radius R and central angle (in radians), carrying current i, is
B =
Hold 4πR
(at center of circular arc).
Ampere's Law Ampere's law states that
•ds'
B.ds= Holenc (Ampere's law).
(29-14)
The line integral in this equation is evaluated around a closed loop called an Amperian loop. The current i on the right side is the net current encircled by the loop. For some current distributions, Eq. 29-14 is easier to use than Eq. 29-3 to calculate the magnetic field due to the currents.
Fields of a Solenoid and a Toroid Inside a long solenoid carrying current i, at points not near its ends, the magnitude B of the magnetic field is
B = μoin (ideal solenoid),
(29-23)
where n is the number of turns per unit length. Thus the internal magnetic field is uniform. Outside the solenoid, the magnetic field is approximately zero.
At a point inside a toroid, the magnitude B of the magnetic field is
B =
HOIN 1 2π r
(toroid),
(29-24)
(29-9)
Force Between Parallel Currents Parallel wires carrying currents in the same direction attract each other, whereas parallel wires carrying currents in opposite directions repel each other. The magnitude of the force on a length L of either wire is
FbaiLB, sin 90°
Holiis 2πd
(29-13)
where d is the wire separation, and i̟, and i̟ are the currents in the wires.
where r is the distance from the center of the toroid to the point. Field of a Magnetic Dipole The magnetic field produced by a current-carrying coil, which is a magnetic dipole, at a point P lo- cated a distance z along the coil's perpendicular central axis is par- allel to the axis and is given by
where
B(z)
με μ 2π z3'
(29-27)
is the dipole moment of the coil. This equation applies only when z is much greater than the dimensions of the coil.

''',

'''


Magnetic Flux The magnetic flux g through an area A in a magnetic field B is defined as
Φι Рв
(30-1)
where the integral is taken over the area. The SI unit of magnetic flux is the weber, where 1 Wb = 1 T m2. If B is perpendicular to the area and uniform over it, Eq. 30-1 becomes
ØB = BA (B1A, Buniform).
(30-2) Faraday's Law of Induction If the magnetic flux, through an area bounded by a closed conducting loop changes with time, a current and an emf are produced in the loop; this process is called induction. The induced emf is
8
doB dt
(Faraday's law).
(30-4)
If the loop is replaced by a closely packed coil of N turns, the induced emfis
dPB % N- dt
(30-5) Lenz's Law An induced current has a direction such that the magnetic field due to the current opposes the change in the magnetic flux that induces the current. The induced emf has the same direction as the induced current.
Emf and the Induced Electric Field An emf is induced by a changing magnetic flux even if the loop through which the flux is changing is not a physical conductor but an imaginary line. The changing magnetic field induces an electric field E at every point of such a loop; the induced emf is related to E by
8 =
SE-ds.
(30-19)
where the integration is taken around the loop. From Eq. 30-19 we can write Faraday's law in its most general form,
$ E-ds=
d dt
(Faraday's law).
(30-20)
A changing magnetic field induces an electric field E. Inductors An inductor is a device that can be used to produce a known magnetic field in a specified region. If a current i is estab- lished through each of the N windings of an inductor, a magnetic flux links those windings. The inductance L of the inductor is
L
NOB i
(inductance defined).
The SI unit of inductance is the henry (H), where 1 henry = 1 H = 1T m2/A. The inductance per unit length near the middle of a long solenoid of cross-sectional area A and ʼn turns per unit length is -pon A (solenoid).
L
(30-31)
Self-Induction If a current i in a coil changes with time, an emf is induced in the coil. This self-induced emf is
di
EL = L
dt
(30-35)
The direction of is found from Lenz's law: The self-induced emf acts to oppose the change that produces it.
Series RL Circuits If a constant emf & is introduced into a sin- gle-loop circuit containing a resistance R and an inductance L, the current rises to an equilibrium value of %/R:
8 i (1 − e) (rise of current). R
(30-41)
Here 7 (L/R) is the inductive time constant. When the source of constant emf is removed, the current decays from a value i according to
i=ie (decay of current).
(30-45)
Magnetic Energy If an inductor L carries a current i, the inductor's magnetic field stores an energy given by
U-L (magnetic energy).
=
(30-49)
If B is the magnitude of a magnetic field at any point (in an inductor or anywhere else), the density of stored magnetic energy at that point is
Ив
B2 2μ
(magnetic energy density).
(30-55)
Mutual Induction If coils 1 and 2 are near each other, a chang- ing current in either coil can induce an emf in the other. This mu- tual induction is described by
and
(30-28)
di
82=
-M
dt
diz
81
= -M
dt
where M (measured in henries) is the mutual inductance.
(30-64)
(30-65)

''',

'''


LC Energy Transfers In an oscillating LC circuit, energy is shuttled periodically between the electric field of the capacitor and the magnetic field of the inductor; instantaneous values of the two forms of energy are
instantaneous current through the inductor. The total energy U(=UE + UB) remains constant.
LC Charge and Current Oscillations The principle of con- servation of energy leads to
UE
92 2C
and UB
Li2 2
(31-1, 31-2)
where q is the instantaneous charge on the capacitor and i is the
934
d2q L dt2
1
+9=0 (LC oscillations)
CHAPTER 31 ELECTROMAGNETIC OSCILLATIONS AND ALTERNATING CURRENT
(31-11)
as the differential equation of LC oscillations (with no resistance). The solution of Eq. 31-11 is
q=Q cos(wt + ) (charge),
(31-12)
in which Q is the charge amplitude (maximum charge on the capac- itor) and the angular frequency of the oscillations is
@ =
1 VLC
For an inductor, V1 = IX, in which X = L is the inductive reactance; the current here lags the potential difference by 90° (= +90° = +/2 rad).
Series RLC Circuits For a series RLC circuit with an alternat- ing external emf given by Eq. 31-28 and a resulting alternating current given by Eq. 31-29,
(31-4)
I =
The phase constant in Eq. 31-12 is determined by the initial con-
Em VR2+ (XL - Xc)2
ditions (at t = 0) of the system.
The current i in the system at any time t is i=-wQ sin(wt + ) (current),
in which wQ is the current amplitude I.
Em
(current amplitude) (31-60, 31-63)
VR2+ (@L1/wC)2
(31-13)
and
tan
X-Xc R
(phase constant).
(31-65)
Damped Oscillations Oscillations in an LC circuit are damped when a dissipative element R is also present in the circuit. Then
Defining the impedance Z of the circuit as
Z= VR2 + (XL - Xc)2
(impedance)
(31-61)
L
d'a dq +R- dt2 dt
1
9=0 (RLC circuit).
(31-24)
allows us to write Eq. 31-60 as I = 8/Z.
The solution of this differential equation is
where
q= Qe-R2L cos(w't + ),
w' = √w2 - (R/2L)2.
(31-25) (31-26)
We consider only situations with small R and thus small damping; then w' = w.
Alternating Currents; Forced Oscillations A series RLC circuit may be set into forced oscillation at a driving angular fre- quency w by an external alternating emf
8 = 8m sin wat.
The current driven in the circuit is
i = I sin(wat - $),
where is the phase constant of the current.
(31-28)
(31-29)
Resonance The current amplitude I in a series RLC circuit driven by a sinusoidal external emf is a maximum (I = %/R) when the driving angular frequency equals the natural angular frequency of the circuit (that is, at resonance). Then Xc = XL ø = 0, and the current is in phase with the emf.
Single Circuit Elements The alternating potential difference across a resistor has amplitude VR = IR; the current is in phase with the potential difference.
For a capacitor, Vc = IXc, in which Xc = 1/wC is the capacitive reactance; the current here leads the potential difference by 90° (=-90° = m/2 rad).
Power In a series RLC circuit, the average power Pavg of the generator is equal to the production rate of thermal energy in the resistor:
Pavg = Ims R = &rms-rms COS . (31-71, 31-76)
Here rms stands for root-mean-square; the rms_quantities are related to the maximum quantities by Irms = I/V2, Vrms = V/V2, and 8ms = 8m/V2. The term cos is called the power factor of the circuit.
Transformers A transformer (assumed to be ideal) is an iron core on which are wound a primary coil of N, turns and a secondary coil of N, turns. If the primary coil is connected across an alternating-current generator, the primary and secondary voltages are related by
N
(transformation of voltage).
The currents through the coils are related by
N N
(transformation of currents),
(31-79)
(31-80)
and the equivalent resistance of the secondary circuit, as seen by the generator, is
Req
=(x).
(31-82)
where R is the resistive load in the secondary circuit. The ratio N/N, is called the transformer's turns ratio.

''',

'''

Electromagnetic Waves An electromagnetic wave consists of oscillating electric and magnetic fields. The various possible fre- quencies of electromagnetic waves form a spectrum, a small part of which is visible light. An electromagnetic wave traveling along an x axis has an electric field E and a magnetic field B with magnitudes that depend on x and t:
and
E Em sin(kx - wt)
B = Bm sin(kx - wt),
(33-1, 33-2)
where Em and Bm are the amplitudes of E and B. The oscillating electric field induces the magnetic field, and the oscillating mag- netic field induces the electric field. The speed of any electromag- netic wave in vacuum is c, which can be written as
E C = B
1 Vμ0E0
(33-5, 33-3)
where E and B are the simultaneous (but nonzero) magnitudes of the two fields.
Energy Flow The rate per unit area at which energy is trans- ported via an electromagnetic wave is given by the Poynting vector S:
1 S=
EX B.
но
(33-19)
The direction of S (and thus of the wave's travel and the energy transport) is perpendicular to the directions of both E and B. The time-averaged rate per unit area at which energy is transported is Savg, which is called the intensity I of the wave:
I =
1
смо
Erms
(33-26)
in which Erms = Em/V2. A point source of electromagnetic waves emits the waves isotropically—that is, with equal intensity in all di- rections. The intensity of the waves at distance r from a point source of power P, is
I =
P 4πr2
(33-27)
Radiation Pressure When a surface intercepts electro- magnetic radiation, a force and a pressure are exerted on the surface. If the radiation is totally absorbed by the surface, the force is
F=
IA C
(total absorption),
(33-32)
in which I is the intensity of the radiation and A is the area of the surface perpendicular to the path of the radiation. If the radiation is totally reflected back along its original path, the force is
2IA
F=
(total reflection back along path).
C
The radiation pressure p, is the force per unit area:
(33-33)
and
Pr= (total reflection back along path).
с
(33-35) Polarization Electromagnetic waves are polarized if their electric field vectors are all in a single plane, called the plane of os- cillation. From a head-on view, the field vectors oscillate parallel to a single axis perpendicular to the path taken by the waves. Light waves from common sources are not polarized; that is, they are un- polarized, or polarized randomly. From a head-on view, the vectors oscillate parallel to every possible axis that is perpendicular to the path taken by the waves.
Polarizing Sheets When a polarizing sheet is placed in the path of light, only electric field components of the light parallel to the sheet's polarizing direction are transmitted by the sheet; com- ponents perpendicular to the polarizing direction are absorbed. The light that emerges from a polarizing sheet is polarized parallel to the polarizing direction of the sheet.
If the original light is initially unpolarized, the transmitted intensity I is half the original intensity Io:
1 = 14-
(33-36)
If the original light is initially polarized, the transmitted intensity depends on the angle between the polarization direction of the original light (the axis along which the fields oscillate) and the po- larizing direction of the sheet:
I = Io cos2 0.
(33-38)
Geometrical Optics Geometrical optics is an approximate treatment of light in which light waves are represented as straight- line rays.
Reflection and Refraction When a light ray encounters a boundary between two transparent media, a reflected ray and a refracted ray generally appear. Both rays remain in the plane of incidence. The angle of reflection is equal to the angle of incidence, and the angle of refraction is related to the angle of incidence by Snell's law,
(33-40)
n2 sin 2 = n1 sin 1 (refraction), where n1 and n2 are the indexes of refraction of the media in which the incident and refracted rays travel.
Total Internal Reflection A wave encountering a boundary across which the index of refraction decreases will experience total internal reflection if the angle of incidence exceeds a critical angle 0, where
0c = sin-1
n2 n1
(critical angle).
(33-45)
Polarization by Reflection A reflected wave will be fully polarized, with its E vectors perpendicular to the plane of incidence, if the incident, unpolarized wave strikes a boundary at the Brewster angle OB, where
I
Pr=
(total absorption)
с
(33-34)
0B tan
-1
n2
(Brewster angle).
n1
(33-49)

''',

'''


Real and Virtual Images An image is a reproduction of an object via light. If the image can form on a surface, it is a real image and can exist even if no observer is present. If the image requires the visual system of an observer, it is a virtual image.
Image Formation Spherical mirrors, spherical refracting sur- faces, and thin lenses can form images of a source of light-the object by redirecting rays emerging from the source. The image occurs where the redirected rays cross (forming a real image) or where backward extensions of those rays cross (forming a virtual image). If the rays are sufficiently close to the central axis through the spherical mirror, refracting surface, or thin lens, we have the following relations between the object distance p (which is posi- tive) and the image distance i (which is positive for real images and negative for virtual images):
1. Spherical Mirror:
1 + P
f
(34-4, 34-3)
where f is the mirror's focal length and r is its radius of curvature. A plane mirror is a special case for which r→ ∞, so that p = -i. Real images form on the side of a mirror where the object is located, and virtual images form on the opposite side. 2. Spherical Refracting Surface:
+
P
n1 n2 i
n2n1
(single surface).
(34-8)
where n is the index of refraction of the material where the object is located, n, is the index of refraction of the material on the other side of the refracting surface, and r is the radius of curvature of the surface. When the object faces a convex refracting surface, the ra- dius r is positive. When it faces a concave surface, r is negative. Real images form on the side of a refracting surface that is opposite the object, and virtual images form on the same side as the object. 3. Thin Lens:
1 1
1
+
P
i
} = ( − 1 ) ( − 1 )
(34-9, 34-10)
η r2
where f is the lens's focal length, n is the index of refraction of the lens material, and r1 and r2 are the radii of curvature of the two sides of the lens, which are spherical surfaces. A convex lens surface that
faces the object has a positive radius of curvature; a concave lens surface that faces the object has a negative radius of curvature. Real images form on the side of a lens that is opposite the object, and vir- tual images form on the same side as the object.
Lateral Magnification The lateral magnification m produced by a spherical mirror or a thin lens is
i
m
Р
The magnitude of m is given by
|m|=
h' h
(34-6)
(34-5)
where h and h' are the heights (measured perpendicular to the central axis) of the object and image, respectively.
Optical Instruments Three optical instruments that extend human vision are:
1. The simple magnifying lens, which produces an angular magni- fication m, given by
mo
25 cm f
(34-12)
where f is the focal length of the magnifying lens. The distance of 25 cm is a traditionally chosen value that is a bit more than the typical near point for someone 20 years old.
2. The compound microscope, which produces an overall magnifi- cation M given by
M = mm.
s 25 cm fob fey
(34-14)
where m is the lateral magnification produced by the objective, m, is the angular magnification produced by the eyepiece, s is the tube length, and fob and fey are the focal lengths of the objec- tive and eyepiece, respectively.
3. The refracting telescope, which produces an angular magnifica- tion me given by
mo
fob fey
(34-15)
''',

'''


Huygens' Principle The three-dimensional transmission of waves, including light, may often be predicted by Huygens' princi- ple, which states that all points on a wavefront serve as point sources of spherical secondary wavelets. After a time t, the new po- sition of the wavefront will be that of a surface tangent to these secondary wavelets.
The law of refraction can be derived from Huygens' principle by assuming that the index of refraction of any medium is n = c/v, in which v is the speed of light in the medium and c is the speed of light in vacuum.
Wavelength and Index of Refraction The wavelength A of light in a medium depends on the index of refraction n of the medium:
λη
λ n
(35-6)
in which A is the wavelength in vacuum. Because of this dependency, the phase difference between two waves can change if they pass through different materials with different indexes of refraction.
Young's Experiment In Young's interference experiment, light passing through a single slit falls on two slits in a screen. The light leaving these slits flares out (by diffraction), and interference occurs in the region beyond the screen. A fringe pattern, due to the interference, forms on a viewing screen.
The light intensity at any point on the viewing screen depends in part on the difference in the path lengths from the slits to that point. If this difference is an integer number of wavelengths, the waves interfere constructively and an intensity maximum results. If it is an odd number of half-wavelengths, there is destructive in- terference and an intensity minimum occurs. The conditions for maximum and minimum intensity are
d sin = mλ, for m = 0, 1, 2,... (maxima-bright fringes).
d sin 0 = (m + 1)^, for m = 0, 1, 2,... (minima-dark fringes),
(35-14)
(35-16)
where is the angle the light path makes with a central axis and d is the slit separation.
Coherence If two light waves that meet at a point are to interfere perceptibly, the phase difference between them must remain constant with time; that is, the waves must be coherent. When two coherent waves meet, the resulting intensity may be found by using phasors. Intensity in Two-Slit Interference In Young's interference experiment, two waves, each with intensity Io, yield a resultant wave of intensity I at the viewing screen, with
1 = 41% cos2
where &
2πd sin 0. λ
(35-22, 35-23)
Equations 35-14 and 35-16, which identify the positions of the fringe maxima and minima, are contained within this relation. Thin-Film Interference When light is incident on a thin transparent film, the light waves reflected from the front and back surfaces interfere. For near-normal incidence, the wavelength con- ditions for maximum and minimum intensity of the light reflected from a film in air are
2L = (m + 2)
for m = 0, 1, 2,... n2 (maxima-bright film in air),
(35-36)
2L = m
λ n2
for m = 0, 1, 2,...
(minima-dark film in air),
(35-37)
where n is the index of refraction of the film, L is its thickness, and A is the wavelength of the light in air.
If the light incident at an interface between media with dif- ferent indexes of refraction is in the medium with the smaller index of refraction, the reflection causes a phase change of rad, or half a wavelength, in the reflected wave. Otherwise, there is no phase change due to the reflection. Refraction causes no phase shift.
The Michelson Interferometer In Michelson's interferom- eter a light wave is split into two beams that, after traversing paths of different lengths, are recombined so they interfere and form a fringe pattern. Varying the path length of one of the beams allows distances to be accurately expressed in terms of wavelengths of light, by counting the number of fringes through which the pattern. shifts because of the change.

''',

'''


Diffraction When waves encounter an edge, an obstacle, or an aperture the size of which is comparable to the wavelength of the waves, those waves spread out as they travel and, as a result, undergo interference. This is called diffraction.
Single-Slit Diffraction Waves passing through a long narrow slit of width a produce, on a viewing screen, a single-slit diffraction pattern that includes a central maximum and other maxima, sepa- rated by minima located at angles to the central axis that satisfy a sin 0 mλ, for m = 1, 2, 3,... (minima).
The intensity of the diffraction pattern at any given angle is
I(0)
1(6)-1
= Im
(sin o
sin a
πα
where a = sin λ
and I, is the intensity at the center of the pattern.
(36-3)
(36-5,36-6)
Circular-Aperture Diffraction Diffraction by a circular aperture or a lens with diameter d produces a central maximum and concentric maxima and minima, with the first minimum at an angle @ given by
λ
sin 0 = 1.22 2 (first minimum-circular aperture). (36-12)
Rayleigh's Criterion Rayleigh's criterion suggests that two objects are on the verge of resolvability if the central diffraction maximum of one is at the first minimum of the other. Their angular separation can then be no less than
λ
OR = 1.22
(Rayleigh's criterion),
(36-14)
in which d is the diameter of the aperture through which the light passes.
Double-Slit Diffraction Waves passing through two slits, each of width a, whose centers are a distance d apart, display dif- fraction patterns whose intensity I at angle is
1(0) = 1,(cos2 B) (sin
α
a
(double slit),
(36-19)
with ẞ = (πd/λ) sin and a as for single-slit diffraction.
Diffraction Gratings A diffraction grating is a series of "slits" used to separate an incident wave into its component wavelengths by separating and displaying their diffraction maxima. Diffraction by N (multiple) slits results in maxima (lines) at angles @ such that d sin 0 = mλ, for m = 0, 1, 2,... (maxima), with the half-widths of the lines given by
Αθ hw
λ Nd cos 0
(half-widths).
The dispersion D and resolving power R are given by
and
(36-25)
(36-28)
ΔΟ
m
D
(36-29, 36-30)
Αλ
d cos 0
R
avg
Nm.
(36-31, 36-32)
Αλ
X-Ray Diffraction The regular array of atoms in a crystal is a three-dimensional diffraction grating for short-wavelength waves such as x rays. For analysis purposes, the atoms can be visualized as being arranged in planes with characteristic interplanar spacing d Diffraction maxima (due to constructive interference) occur if the incident direction of the wave, measured from the surfaces of these planes, and the wavelength A of the radiation satisfy Bragg's law:
2d sin 0 mλ, for m = 1,2,3,... (Bragg's law).
(36-34)

''',

'''


The Postulates Einstein's special theory of relativity is based on two postulates:
1. The laws of physics are the same for observers in all inertial reference frames. No one frame is preferred over any other.
2. The speed of light in vacuum has the same value c in all directions and in all inertial reference frames.
The speed of light c in vacuum is an ultimate speed that cannot be exceeded by any entity carrying energy or information.
Coordinates of an Event Three space coordinates and one time coordinate specify an event. One task of special relativity is to relate these coordinates as assigned by two observers who are in uniform motion with respect to each other.
Simultaneous Events If two observers are in relative motion, they will not, in general, agree as to whether two events are simultaneous.
Time Dilation If two successive events occur at the same place in an inertial reference frame, the time interval At, between them, measured on a single clock where they occur, is the proper time be- tween the events. Observers in frames moving relative to that frame will measure a larger value for this interval. For an observer moving with relative speed v, the measured time interval is
At =
Ato V1 - (v/c)2
Ato V1-B2
(37-7 to 37-9)
= y Ato (time dilation).
Here ẞ= v/c is the speed parameter and y = 1/V1 - B2 is the
Lorentz factor. An important result of time dilation is that moving clocks run slow as measured by an observer at rest.
Length Contraction The length Lo of an object measured by an observer in an inertial reference frame in which the object is at rest is called its proper length. Observers in frames moving relative to that frame and parallel to that length will measure a shorter length. For an observer moving with relative speed v, the measured length is
Lo
L = L2 √1 - B2 :
(length contraction).
γ
(37-13)
The Lorentz Transformation The Lorentz transformation equations relate the spacetime coordinates of a single event as seen by observers in two inertial frames, S and S', where S' is mov- ing relative to S with velocity v in the positive x and x' direction. The four coordinates are related by
x' = y(x - vt),
y' = y,
z' = z,
t' = y(t - vx/c2).
(37-21)
Relativity of Velocities When a particle is moving with speed u' in the positive x' direction in an inertial reference frame S' that itself is moving with speed v parallel to the x direction of a second inertial frame S, the speed u of the particle as measured in S is
u
u' + v 1+u'v/c2
(relativistic velocity).
(37-29)
Relativistic Doppler Effect When a light source and a light
1144 CHAPTER 37 RELATIVITY
detector move directly relative to each other, the wavelength of the light as measured in the rest frame of the source is the proper wavelength A. The detected wavelength A is either longer (a red shift) or shorter (a blue shift) depending on whether the source-detector separation is increasing or decreasing. When the separation is increasing, the wavelengths are related by
λ= λο
(source and detector separating),
(37-32)
1+ B 1-B where ẞ = v/c and v is the relative radial speed (along a line con- necting the source and detector). If the separation is decreasing, the signs in front of the ẞ symbols are reversed. For speeds much less than c, the magnitude of the Doppler wavelength shift (Aλ = λ -λ) is approximately related to v by
Momentum and Energy The following definitions of linear momentum p, kinetic energy K, and total energy E for a particle of mass m are valid at any physically possible speed:
p = ymv
(momentum), (total energy),
(kinetic energy).
(37-42) (37-47, 37-48)
(37-52)
E = mc2 + Kymc2 K = mc2(y-1) Here y is the Lorentz factor for the particle's motion, and mc2 is the mass energy, or rest energy, associated with the mass of the par- ticle. These equations lead to the relationships
and
(37-36)
(pc)2= K2 + 2Kmc2
E2 = (pc)2 + (mc2)2.
(37-54) (37-55)
스시
C
(vc).
λο
Transverse Doppler Effect If the relative motion of the light source is perpendicular to a line joining the source and detector, the detected frequency fis related to the proper frequency fo by
When a system of particles undergoes a chemical or nuclear reaction, the Q of the reaction is the negative of the change in the system's total mass energy:
Q=Mic2 - Mc2 = -AM c2,
(37-50)
(37-37)
where M, is the system's total mass before the reaction and M, is its total mass after the reaction.

''',

'''


Light Quanta-Photons An electromagnetic wave (light) is quantized, and its quanta are called photons. For a light wave of frequency ƒ and wavelength A, the energy E and momentum mag- nitude p of a photon are
and
p =
Ehf (photon energy)
hf
с
=
h
(photon momentum).
λ
(38-2)
(38-7)
Photoelectric Effect When light of high enough frequency falls on a clean metal surface, electrons are emitted from the sur- face by photon-electron interactions within the metal. The gov- erning relation is hf = Kmax + Þ, (38-5)
in which hf is the photon energy, Kmax is the kinetic energy of the most energetic emitted electrons, and Þ is the work function of the target material—that is, the minimum energy an electron must have if it is to emerge from the surface of the target. If hf is less than P, electrons are not emitted.
Compton Shift When x rays are scattered by loosely bound electrons in a target, some of the scattered x rays have a longer wavelength than do the incident x rays. This Compton shift (in wavelength) is given by
h mc
Δλ= (1 - cos +),
(38-11)
in which is the angle at which the x rays are scattered. Light Waves and Photons When light interacts with matter, energy and momentum are transferred via photons. When light is in transit, however, we interpret the light wave as a probability wave, in which the probability (per unit time) that a photon can be detected is proportional to E, where Em is the amplitude of the oscillating electric field of the light wave at the detector.
Ideal Blackbody Radiation
As a measure of the emission
of thermal radiation by an ideal blackbody radiator, we define the spectral radiancy S(A) in terms of the emitted intensity per unit wavelength at a given wavelength A. For the Planck radiation law,
1180
CHAPTER 38 PHOTONS AND MATTER WAVES
in which atomic oscillators produce the thermal radiation, we have
S(A)
=
2πс2h 15
1 ehc/AKT - 1'
(38-14)
where h is the Planck constant, k is the Boltzmann constant, and T is the temperature of the radiating surface. Wien's law relates the temperature T of a blackbody radiator and the wavelength Amax at which the spectral radiancy is maximum:
AmaxT=2898 μm · K.
(38-15)
Matter Waves A moving particle such as an electron or a pro- ton can be described as a matter wave; its wavelength (called the de Broglie wavelength) is given by λ=h/p, where p is the magni- tude of the particle's momentum.
The Wave Function A matter wave is described by its wave function (x, y, z, t), which can be separated into a space- dependent part (x, y, z) and a time-dependent part e-it. For a particle of mass m moving in the x direction with constant total en- ergy E through a region in which its potential energy is U(x), (x) can be found by solving the simplified Schrödinger equation:
d24 8π2m dx2 h2
+
[E- U(x)] = 0.
(38-19)
A matter wave, like a light wave, is a probability wave in the sense that if a particle detector is inserted into the wave, the probability that the detector will register a particle during any specified time in- terval is proportional to l2, a quantity called the probability density.
For a free particle—that is, a particle for which U(x) = 0— moving in the x direction, 2 has a constant value for all positions along the x axis.
Heisenberg's Uncertainty Principle The probabilistic nature of quantum physics places an important limitation on de- tecting a particle's position and momentum. That is, it is not possi- ble to measure the position and the momentum p of a particle si- multaneously with unlimited precision. The uncertainties in the components of these quantities are given by
Ax Apx = h
Ay Ap, ≥ h
Az Ap2 = h.
(38-28)
Potential Step This term defines a region where a particle's potential energy increases at the expense of its kinetic energy. According to classical physics, if a particle's initial kinetic energy exceeds the potential energy, it should never be reflected by the re- gion. However, according to quantum physics, there is a reflection coefficient R that gives a finite probability of reflection. The proba- bility of transmission is T = 1-R.
Barrier Tunneling According to classical physics, an incident particle will be reflected from a potential energy barrier whose height is greater than the particle's kinetic energy. According to quantum physics, however, the particle has a finite probability of tunneling through such a barrier, appearing on the other side unchanged. The probability that a given particle of mass m and en- ergy E will tunnel through a barrier of height U, and thickness L is given by the transmission coefficient 7:
(38-38)
T≈e-2bL
where
b =
8π2m(UE) h2
(38-39)

''',

'''


Confinement Confinement of waves (string waves, matter waves any type of wave) leads to quantization—that is, discrete states with certain energies. States with intermediate energies are not allowed.
Electron in an Infinite Potential Well Because it is a matter wave, an electron confined to an infinite potential well can exist in only certain discrete states. If the well is one-dimensional with length L, the energies associated with these quantum states are
h2 8mL2
for n = 1,2,3,...,
(39-4)
where m is the electron mass and n is a quantum number. The low- est energy, said to be the zero-point energy, is not zero but is given by n = 1. The electron can change (jump) from one state to an- other only if its energy change is
AE = Ehigh - Elow,
(39-5) where Ehigh is the higher energy and Elow is the lower energy. If the change is done by photon absorption or emission, the energy of the photon must be equal to the change in the electron's energy:
hc λ
hf == AE = Ehigh - Elow
(39-6)
where frequency f and wavelength A are associated with the photon. The wave functions for an electron in an infinite, one-dimen- sional potential well with length L along an x axis are given by
(x)
2 L
for n = 1,2,3,...,
L
(39-10) where n is the quantum number and the factor √2/L comes from normalizing the wave function. The wave function (x) does not have physical meaning, but the probability density
(x) does have physical meaning: The product (x) dx is the probability that the electron will be detected in the interval between x and x + dx. If the probability density of an electron is integrated over the entire x axis, the total probability must be 1, which means that the electron will be detected somewhere along the x axis:
[*_46(x) dx = 1.
(39-14)
Electron in a Finite Well The wave function for an electron in a finite, one-dimensional potential well extends into the walls. Compared to the states in an infinite well of the same size, the states in a finite well have a limited number, longer de Broglie wavelengths, and lower energies.
Two-Dimensional Electron Trap The quantized energies
for an electron trapped in a two-dimensional infinite potential well that forms a rectangular corral are
h2
Енхлу
+
8m L
n L
(39-20)
where n is a quantum number for which the electron's matter wave fits in well width L, and n, is a quantum number for which it fits in well width L. The wave functions for an electron in a two-dimensional well are given by
Unx,ny
√
2
sin Lx
2
() ()
sin
Ly
(39-19)
The Hydrogen Atom The Bohr model of the hydrogen atom successfully derived the energy levels for the atom, to explain the emission/absorption spectrum of the atom, but it is incorrect in al- most every other aspect. It is a planetary model in which the elec- tron orbits the central proton with an angular momentum L that is limited to values given by
L = nh, for n = 1,2,3,...,
(39-23)
where n is a quantum number. The equation is, however, incorrect. Application of the Schrödinger equation gives the correct values of L and the quantized energies:
En
me4 1 Beth 2
13.60 eV n2
for n = 1,2,3,.... (39-34)
The atom (or, the electron in the atom) can change energy only by jumping between these allowed energies. If the jump is by photon absorption (the atom's energy increases) or photon emission (the atom's energy decreases), this restriction in energy changes leads to
1 = R λ
2
1 Wow
1
(39-37)
for the wavelength of the light, where R is the Rydberg constant,
me1 R = 8eh c
= 1.097 373 × 107 m ̄1.
(39-38)
The radial probability density P(r) for a state of the hydrogen atom is defined so that P(r) is the probability that the electron will be de- tected somewhere in the space between two spherical shells of radii r and r + dr that are centered on the nucleus. The probability that the electron will be detected between any two given radii r1 and r2 is
(probability of detection) = [^P(r) dr.
(39-45)

''',

'''


Some Properties of Atoms Atoms have quantized ener- gies and can make quantum jumps between them. If a jump be- tween a higher energy and a lower energy involves the emission or absorption of a photon, the frequency associated with the light is given by
hf=Eigh-B
(40-1)
States with the same value of quantum number n form a shell. States with the same values of quantum numbers and € form a subshell.
Orbital Angular Momentum and Magnetic Dipole Moments The magnitude of the orbital angular momentum of an electron trapped in an atom has quantized values given by
0,1,2,
(n-1), (40-2)
L= Vece+1) A. for where A is h/2w, is the orbital magnetic quantum number, and nis the electron's principal quantum number. The component L, of the orbital angular momentum on a z axis is quantized and given by L= mk, form, = 0, 1, 2,...,,
(40.3) where m, is the orbital magnetic quantum number. The magnitude Man of the orbital magnetic moment of the electron is quantized with the values given by
Mu-Vece+1) A,
201
(40-6)
where m is the electron mass. The component on a z axis is also quantized according to
e
Ma
2m
where is the Bohr magneton:
(40-7)
eh
9.274 x 10-J/T.
(40-8)
4mm
2m
Spin Angular Momentum and Magnetic Dipole Moment Every electron, whether trapped or free, has an intrin- sic spin angular momentum 3 with a magnitude that is quantized as S= √(+1), fors (40-9) where s is the spin quantum number. An electron is said to be a
spin-particle. The component S, on a z axis is also quantized ac- cording to
S=m,h, form,====
(40-10)
where m, is the spin magnetic quantum number. Every electron, whether trapped or free, has an intrinsic spin magnetic dipole mo- ment, with a magnitude that is quantized as
The component, on a z axis is also quantized according to H-2m form, +
(40-12)
(40-13) Stern-Gerlach Experiment The Stern-Gerlach experi- ment demonstrated that the magnetic moment of silver atoms is quantized, experimental proof that magnetic moments at the atomic level are quantized. An atom with magnetic dipole mo- ment experiences a force in a nonuniform magnetic field. If the field changes at the rate of dB/dz along a z axis, then the force is along the z axis and is related to the component, of the dipole dB (40-17)
moment
A proton has an intrinsic spin angular momentum and an intrin sic magnetic dipole moment that are in the same direction. Magnetic Resonance The magnetic dipole moment of a proton in a magnetic field along a z axis has two quantized components on that axis: spin up (, is in the direction B) and spin down (4, is in the opposite direction). Contrary to the situa tion with an electron, spin up is the lower energy orientation; the difference between the two orientations is 24,B. The energy re- quired of a photon to spin-flip the proton between the two orien tations is
hf-2.B.
(40-22)
The field is the vector sum of an external field set up by equipment and an internal field set up by the atoms and nuclei surrounding the proton. Detection of spin-flips can lead to nuclear magnetic resonance spectra by which specific substances can be identified.
1246
CHAPTER 40 ALL ABOUT ATOMS
Pauli Exclusion Principle Electrons in atoms and other traps obey the Pauli exclusion principle, which requires that no two electrons in a trap can have the same set of quantum numbers. Building the Periodic Table In the periodic table, the ele ments are listed in order of increasing atomic number Z, where Z is the number of protons in the nucleus. For a neutral atom, Z is also the number of electrons. States with the same value of quan- tum number a form a shell. States with the same values of quantum numbers and form a subshell. A closed shell and a closed sub- shell contain the maximum number of electrons as allowed by the Pauli exclusion principle. The net angular momentum and net mag- netic moment of such closed structures is zero.
X Rays and the Numbering of the Elements When a beam of high-energy electrons impacts a target, the electrons can lose their energy by emitting x rays when they scatter from atoms in the target. The emission is over a range of wavelengths, said to be a continuous spectrum. The shortest wavelength in the spec- trum is the cutoff wavelength A which is emitted when an inci- dent electron loses its full kinetic energy K, in a single scattering event, with a single x-ray emission:

The characteristic x-ray spectrum is produced when incident elec- trons eject low-lying electrons in the target atoms and electrons from upper levels jump down to the resulting holes, emitting light. A Moseley plot is a graph of the square root of the charac teristic-emission frequencies Vf versus atomic number Z of the target atoms. The straight-line plot reveals that the position of an element in the periodic table is set by Z and not by the atomic weight.
Lasers In stimulated emission, an atom in an excited state can be induced to de-excite to a lower energy state by emitting a pho- ton if an identical photon passes the atom. The light emitted in stimulated emission is in phase with and travels in the direction of the light causing the emission.
A laser can emit light via stimulated emission provided that its atoms are in population inversion. That is, for the pair of levels in- volved in the stimulated emission, more atoms must be in the up- per level than the lower level so that there is more stimulated emis- sion than just absorption.

''',

'''

Metals, Semiconductors, and Insulators Three electrical properties that can be used to distinguish among crystalline solids are resistivity p, temperature coefficient of resistivity a, and num- ber density of charge carriers n. Solids can be broadly divided into insulators (very high p), metals (low p, positive and low a, large n), and semiconductors (high p, negative and high a, small n).
Energy Levels and Gaps in a Crystalline Solid An isolated atom can exist in only a discrete set of energy levels. As atoms come together to form a solid, the levels of the individual atoms merge to form the discrete energy bands of the solid. These energy bands are separated by energy gaps, each of which corresponds to a range of energies that no electron may possess.
Any energy band is made up of an enormous number of very closely spaced levels. The Pauli exclusion principle asserts that only one electron may occupy each of these levels.
Insulators In an insulator, the highest band containing electrons is completely filled and is separated from the vacant band above it by an energy gap so large that electrons can essentially never become thermally agitated enough to jump across the gap.
Metals In a metal, the highest band that contains any electrons is only partially filled. The energy of the highest filled level at a temperature of 0 K is called the Fermi energy EF for the metal.
The electrons in the partially filled band are the conduction electrons and their number is
(number of conduction)
electrons in sample
(number of atoms
in sample
(number of valence)
electrons per atom/
(41-2)
The number of atoms in a sample is given by
(number of atoms
in sample
sample mass Mam
atomic mass
sample mass Mam
(molar mass M)/NA
material's
sample
density
volume
(41-4)
(molar mass M)/NA


The number density n of the conduction electrons is
number of conduction electrons in sample
sample volume V
(41-3)
The density of states function N(E) is the number of available energy levels per unit volume of the sample and per unit energy in- terval and is given by
N(E)
8√2πm3/2 h3
El/2 (density of states, m'J'),
(41-5)
where m (=9.109 × 10-31 kg) is the electron mass, h (= 6.626 X 10-34 J-s) is the Planck constant, and E is the energy in joules at which N(E) is to be evaluated. To modify the equation so that the value of E is in eV and the value of N(E) is in m3 eV, multiply the right side by e3/2 (where e = 1.602 X 10-19 C).
The occupancy probability P(E), the probability that a given available state will be occupied by an electron, is
P(E)
1
e(E-Ep)/kT +1
(occupancy probability).
(41-6)
The density of occupied states N.(E) is given by the product of the two quantities in Eqs. (41-5) and (41-6):
N.(E) = N(E) P(E) (density of occupied states).
(41-7)
The Fermi energy for a metal can be found by integrating N,(E) for T = 0 from E = 0 to E = Ep. The result is
Ex = (1632m
123 h
0.121/2
n2/3
n2/3
(41-9)
16√2
m
m
Semiconductors The band structure of a semiconductor is like that of an insulator except that the gap width E, is much smaller in the semiconductor. For silicon (a semiconductor) at room temperature, thermal agitation raises a few electrons to the conduction band, leaving an equal number of holes in the va- lence band. Both electrons and holes serve as charge carriers. The number of electrons in the conduction band of silicon can be increased greatly by doping with small amounts of phosphorus, thus forming n-type material. The number of holes in the va lence band can be greatly increased by doping with aluminum, thus forming p-type material.

The p-n Junction Ap-n junction is a single semiconducting crys- tal with one end doped to form p-type material and the other end doped to form n-type material, the two types meeting at a junction plane. At thermal equilibrium, the following occurs at that plane: The majority carriers (electrons on the n side and holes on the p side) diffuse across the junction plane, producing a diffusion current
The minority carriers (holes on the n side and electrons on the p side) are swept across the junction plane, forming a drift cur- rent Idrift. These two currents are equal in magnitude, making the net current zero.
A depletion zone, consisting largely of charged donor and acceptor ions, forms across the junction plane.

A contact potential difference Vo develops across the depletion zone.
Applications of the p-n Junction When a potential difference is applied across a p-n junction, the device conducts electricity more readily for one polarity of the applied potential difference than for the other. Thus, a p-n junction can serve as a junction rectifier.
When a p-n junction is forward biased, it can emit light, hence can serve as a light-emitting diode (LED). The wavelength of the emitted light is given by
hc
λ
f E
(41-11)
A strongly forward-biased p-n junction with parallel end faces can op- erate as a junction laser, emitting light of a sharply defined wavelength.
''',

'''


The Nuclides Approximately 2000 nuclides are known to exist. Each is characterized by an atomic number Z (the number of pro- tons), a neutron number N, and a mass number A (the total number of nucleons-protons and neutrons). Thus, A = Z+N. Nuclides with the same atomic number but different neutron numbers are isotopes of one another. Nuclei have a mean radius r given by
where ro≈ 1.2 fm.
r = roA1/3,
(42-3)
Mass and Binding Energy Atomic masses are often re-
ported in terms of mass excess
AM-A (mass excess),
(42-6) where M is the actual mass of an atom in atomic mass units and A is the mass number for that atom's nucleus. The binding energy of a nucleus is the difference
AEbe (mc2) Mc2 (binding energy),
(42-7)
where (mc2) is the total mass energy of the individual protons and neutrons. The binding energy per nucleon is

AEbe
A
AEben Mass-Energy Exchanges The energy equivalent of one mass unit (u) is 931.494 013 MeV. The binding energy curve shows that middle-mass nuclides are the most stable and that en- ergy can be released both by fission of high-mass nuclei and by fusion of low-mass nuclei.
(binding energy per nucleon). (42-8)
The Nuclear Force Nuclei are held together by an attractive force acting among the nucleons, part of the strong force acting between the quarks that make up the nucleons.
Radioactive Decay Most known nuclides are radioactive; they spontaneously decay at a rate R (= -dN/dt) that is proportional to the number N of radioactive atoms present, the proportionality constant being the disintegration constant λ. This leads to the law of exponential decay:
N = NoeTM, R = AN = Roe At (radioactive decay).
(42-15, 42-17, 42-16) The half-life T1/2 = (In 2)/A of a radioactive nuclide is the time re- quired for the decay rate R (or the number N) in a sample to drop to half its initial value.
Alpha Decay Some nuclides decay by emitting an alpha parti- cle (a helium nucleus, 'He). Such decay is inhibited by a potential energy barrier that cannot be penetrated according to classical physics but is subject to tunneling according to quantum physics. The barrier penetrability, and thus the half-life for alpha decay, is very sensitive to the energy of the emitted alpha particle.
Beta Decay In beta decay either an electron or a positron
is emitted by a nucleus, along with a neutrino. The emitted particles share the available disintegration energy. The electrons and positrons emitted in beta decay have a continuous spectrum of en- ergies from near zero up to a limit Kmax (= Q = -Am c2). Radioactive Dating Naturally occurring radioactive nuclides provide a means for estimating the dates of historic and prehistoric events. For example, the ages of organic materials can often be found by measuring their 14C content; rock samples can be dated using the radioactive isotope 40K.
Radiation Dosage Three units are used to describe exposure to ionizing radiation. The becquerel (1 Bq = 1 decay per second) measures the activity of a source. The amount of energy actually absorbed is measured in grays, with 1 Gy corresponding to 1 J/kg. The estimated biological effect of the absorbed energy is measured in sieverts; a dose equivalent of 1 Sv causes the same biological ef- fect regardless of the radiation type by which it was acquired. Nuclear Models The collective model of nuclear structure as- sumes that nucleons collide constantly with one another and that rel- atively long-lived compound nuclei are formed when a projectile is captured. The formation and eventual decay of a compound nucleus are totally independent events.
The independent particle model of nuclear structure assumes that each nucleon moves, essentially without collisions, in a quantized state within the nucleus. The model predicts nucleon levels and magic nucleon numbers (2, 8, 20, 28, 50, 82, and 126) associated with closed shells of nucleons; nuclides with any of these numbers of neutrons or protons are particularly stable.
The combined model, in which extra nucleons occupy quan- tized states outside a central core of closed shells, is highly success- ful in predicting many nuclear properties.

''',

'''


Energy from the Nucleus Nuclear processes are about a million times more effective, per unit mass, than chemical pro- cesses in transforming mass into other forms of energy.
Nuclear Fission Equation 43-1 shows a fission of 236U induced by thermal neutrons bombarding 235U. Equations 43-2 and 43-3 show the beta-decay chains of the primary fragments. The energy released in such a fission event is Q≈ 200 MeV.
Fission can be understood in terms of the collective model, in which a nucleus is likened to a charged liquid drop carrying a cer- tain excitation energy. A potential barrier must be tunneled through if fission is to occur. The ability of a nucleus to undergo fis- sion depends on the relationship between the barrier height E, and the excitation energy En.
The neutrons released during fission make possible a fission chain reaction. Figure 43-5 shows the neutron balance for one cycle of a typical reactor. Figure 43-6 suggests the layout of a complete nuclear power plant.
Nuclear Fusion The release of energy by the fusion of two light nuclei is inhibited by their mutual Coulomb barrier (due to
the electric repulsion between the two collections of protons). Fusion can occur in bulk matter only if the temperature is high enough (that is, if the particle energy is high enough) for apprecia- ble barrier tunneling to occur.
The Sun's energy arises mainly from the thermonuclear burning of hydrogen to form helium by the proton-proton cycle outlined in Fig. 43-11. Elements up to A≈ 56 (the peak of the binding energy curve) can be built up by other fusion processes once the hydrogen fuel supply of a star has been exhausted. Fusion of more massive elements requires an input of energy and thus cannot be the source of a star's energy output.
Controlled Fusion Controlled thermonuclear fusion for energy generation has not yet been achieved. The d-d and d-t reactions are the most promising mechanisms. A successful fusion reactor must satisfy Lawson's criterion,
nT> 1020 s/m3,
and must have a suitably high plasma temperature T.
(43-16)
In a tokamak the plasma is confined by a magnetic field. In laser fusion inertial confinement is used.

''',

'''

Leptons and Quarks Current research supports the view that
all matter is made of six kinds of leptons (Table 44-2), six kinds of quarks (Table 44-5), and 12 antiparticles, one corresponding to each lepton and each quark. All these particles have spin quantum numbers equal to and are thus fermions (particles with half- integer spin quantum numbers).
The Interactions Particles with electric charge interact through the electromagnetic force by exchanging virtual photons. Leptons can also interact with each other and with quarks through the weak force, via massive W and Z particles as messengers. In ad- dition, quarks interact with each other through the color force. The electromagnetic and weak forces are different manifestations of the same force, called the electroweak force.
Leptons Three of the leptons (the electron, muon, and tau) have electric charge equal to -1e. There are also three uncharged neutrinos (also leptons), one corresponding to each of the charged leptons. The antiparticles for the charged leptons have positive charge.
Quarks The six quarks (up, down, strange, charm, bottom, and top, in order of increasing mass) each have baryon number + and charge equal to either +e ore. The strange quark has strange-
ness -1, whereas the others all have strangeness 0. These four alge- braic signs are reversed for the antiquarks.
Hadrons: Baryons and Mesons Quarks combine into strongly interacting particles called hadrons. Baryons are hadrons with half-integer spin quantum numbers ( or). Mesons are hadrons with integer spin quantum numbers (0 or 1) and thus are bosons. Baryons are fermions. Mesons have baryon number equal to zero; baryons have baryon number equal to +1 or -1. Quantum chromodynamics predicts that the possible combinations of quarks are either a quark with an antiquark, three quarks, or three anti- quarks (this prediction is consistent with experiment). Expansion of the Universe Current evidence strongly sug- gests that the universe is expanding, with the distant galaxies mov- ing away from us at a rate v given by Hubble's law:
v = Hr (Hubble's law).
Here we take H, the Hubble constant, to have the value H=71.0 km/s Mpc21.8 mm/s⚫ly.
(44-19)
(44-21)
The expansion described by Hubble's law and the presence of ubiquitous background microwave radiation reveal that the uni- verse began in a “big bang” 13.7 billion years ago.

'''

]

ess_text = [

    '''


2.1 Minerals: Building Blocks of Rocks
KEY TERMS: mineralogy, mineral, rock
In Earth science, the word mineral refers to naturally occurring inorganic solids that possess an orderly crystalline structure and a characteristic chemical composition. The study of minerals is called mineralogy.
Minerals are the building blocks of rocks. Rocks are naturally occurring masses of minerals or mineral-like matter such as natural glass or organic material.

''',

'''

2.2 Atoms: Building Blocks of Minerals 

KEY TERMS: atom, nucleus, proton, neutron, electron, valence electron, atomic number, element, periodic table, chemical compound
Minerals are composed of atoms of one or more elements. All atoms consist of the same three basic components: protons, neutrons, and electrons. The atomic number represents the number of protons found in the nucleus of an atom of a particular element. For example, an oxygen atom has eight protons, so its atomic number is eight. Protons and neutrons have approximately the same size and mass, but protons are positively charged, whereas neutrons have no charge.
Electrons weigh only about 1/2000 as much as protons or neutrons. They occupy the space around the nucleus, where they form what can be thought of as a cloud that is structured into several distinct energy levels called principal shells. The electrons in the outermost principal shell, called valence electrons, are responsible for the bonds that hold atoms together to form chemical compounds.
Elements that have the same number of valence electrons tend to behave similarly. The periodic table is organized so that elements with the same number of valence electrons form a column, called a group.

''',

'''
2.3 Why Atoms Bond
KEY TERMS: octet rule, chemical bond, ionic bond, ion, covalent bond, metallic bond
When atoms are attracted to other atoms, they can form chemical bonds, which generally involve the transfer or sharing of valence electrons. The most stable arrangement for most atoms is to have eight electrons in the outermost principal shell. This concept is called the octet rule.
To form ionic bonds, atoms of one element give up one or more valence electrons to atoms of another
element, forming positively and negatively charged. atoms called ions. The ionic bond results from the attraction between oppositely charged ions.
• Covalent bonds form when adjacent atoms share valence electrons. • In metallic bonds, the sharing is more extensive: The shared valence electrons can move freely through the substance.

''',

'''
2.4 Properties of Minerals
KEY TERMS: diagnostic property, ambiguous property, luster, color, streak, crystal shape (habit), hardness, Mohs scale, cleavage, fracture, tenacity, density, specific gravity
The composition and internal crystalline structure of a mineral give it specific physical properties. Mineral properties useful in identifying minerals are termed diagnostic properties.
- Luster is a mineral's ability to reflect light. The terms transparent, translucent, and opaque describe the degree to which a mineral can transmit light. Color can be unreliable for mineral identification, as impurities can "stain" minerals with diverse colors. A more reliable identifier is streak, the color of the powder generated by scraping a mineral against a porcelain streak plate.
- Crystal shape, also called crystal habit, is often useful for mineral identification.


Variations in the strength of chemical bonds give minerals properties such as hardness (resistance to being scratched) and tenacity (response to deforming stress, such as whether the mineral tends to undergo brittle breakage like quartz, bend elastically like mica, or deform malleably like gold). Cleavage, the preferential breakage of a mineral along planes of weakly bonded atoms, is very useful in identifying minerals.
The amount of matter packed into a given volume determines a mineral's density. To compare the densities of minerals, mineralogists use a related quantity, known as specific gravity, which is the ratio between a mineral's density and the density of water.
Other properties are diagnostic for certain minerals but rare in most others; examples include smell, taste, feel, reaction to hydrochloric acid, magnetism, and double refraction.

''',

'''
2.5 Mineral Groups
KEY TERMS: rock-forming mineral, economic mineral, silicate, nonsilicate, silicon-oxygen tetrahedron, light silicate mineral, potassium feldspar, plagio- clase feldspar, quartz, muscovite, clay, dark silicate mineral, olivine, augite, hornblende, biotite, garnet, calcite, dolomite, halite, gypsum
Silicate minerals have a basic building block in common: a small pyramid- shaped structure called the silicon-oxygen tetrahedron, which consists of one silicon atom surrounded by four oxygen atoms. Neighboring tetrahedra can share some of their oxygen atoms, causing them to develop long chains, sheet structures, and three-dimensional networks. Silicate minerals are the most common mineral class on Earth. They are subdivided into minerals that contain iron and/or magnesium (dark silicates) and those that do not (light silicates). The light silicate minerals are generally light in color and have relatively low specific gravities. Feldspar, quartz, muscovite, and clay minerals are examples. The dark silicate minerals are generally dark in color and relatively dense. Olivine, pyroxene, amphibole, biotite, and garnet are examples. Nonsilicate minerals include oxides, which contain oxygen ions that bond to other elements (usually metals); carbonates, which have CO2- as a critical part of their crystal structure; sulfates, which have SO 2- as their basic building block; and halides, which contain a nonmetal ion such as chlorine, bromine, or fluorine that bonds to a metal ion such as sodium or calcium.
Nonsilicate minerals are often economically important. Hematite is an important source of industrial iron, while calcite is an essential component of cement.

''',

'''
2.6 Minerals: A Nonrenewable Resource
KEY TERMS: renewable, nonrenewable, mineral resource, ore deposit Resources are classified as renewable when they can be replenished over short time spans and nonrenewable when they can't.
Ore deposits are naturally occurring concentrations of one or more metallic minerals that can be extracted economically using current technology. A mineral resource can be upgraded to an ore deposit if the price of the commodity increases sufficiently or if the cost of extraction decreases. The reverse can also happen.

''',

'''


3.1 Earth as a System: The Rock Cycle
KEY TERM: rock cycle
The rock cycle is a good model for thinking about the transformation of one rock to another due to Earth processes. Igneous rocks form when molten rock solidifies. Sedimentary rocks are made from weathered products of other rocks. Metamorphic rocks are the products of preexisting rocks subjected to conditions of high temperatures and/or pressures. Given the right sequence of conditions, any rock type can be transformed into any other type of rock.

''',

'''

3.2 Igneous Rocks: "Formed by Fire"
KEY TERMS: igneous rock, magma, lava, extrusive (volcanic) rock, intrusive (plutonic) rock, granitic (felsic) composition, basaltic (mafic) composition, andesitic (intermediate) composition, ultramafic, peridotite, texture, fine- grained texture, coarse-grained texture, porphyritic texture, phenocryst, groundmass, vesicular texture, glassy texture, pyroclastic (fragmental) texture, granite, rhyolite, obsidian, pumice, andesite, diorite, basalt, gabbro, Bowen's reaction series, crystal settling, magmatic differentiation
vapor,
Completely or partly molten rock is called magma if it is below Earth's surface and lava if it has erupted onto the surface. It consists of a liquid melt that contains gases (volatiles) such as water and it may contain solids (mineral crystals). Magmas that cool at depth produce intrusive igneous rocks, whereas those that erupt onto Earth's surface produce extrusive igneous rocks. In geology, texture refers to the size, shape, and arrangement of mineral grains in a rock. Careful observation of the texture of igneous rocks can lead to insights about the conditions under which they formed. Lava on or near the surface cools rapidly, resulting in a large number of very small crystals that gives the rock a fine-grained texture. Magma at depth is insulated by the surrounding rock and cools very slowly. This allows sufficient time for the magma's ions to organize into larger crystals, resulting in a rock with a coarse-grained texture. If crystals begin to form at depth and then the magma rises to a shallow depth or erupts at the surface, it has a two-stage cooling history. The result is a rock with a porphyritic texture.
Pioneering experimentation by N. L. Bowen revealed that as magma cools, minerals crystallize in a specific order. The dark-colored silicate minerals, such as olivine, crystallize first, at the highest temperatures (1250°C (2300°F]), whereas the light silicates, such as quartz, crystallize last, at the lowest temperatures (650°C [1200°F]). Separation of minerals by mechanisms such as crystal settling results in igneous rocks having a wide variety of chemical compositions.
Igneous rocks are classified into compositional groups based on the percentage of dark and light silicate minerals they contain. Granític (or felsic) rocks such as granite and rhyolite are composed mostly of the light-colored silicate minerals potassium feldspar and quartz. Rocks of andesitic (or intermediate) composition such as andesite contain plagioclase feldspar and amphibole. Basaltic (or mafic) rocks such as basalt contain abundant pyroxene and calcium-rich plagioclase feldspar

''',

'''
3.3 Sedimentary Rocks: Compacted and Cemented Sediment
KEY TERMS: sedimentary rock, sediment, detrital sedimentary rock, conglom- erate, breccia, sandstone, shale, siltstone, chemical sedimentary rock, bio- chemical sedimentary rock, limestone, coquina, travertine, evaporite deposit, coal, lithification, compaction, cementation, strata (beds), fossil ⚫Although igneous and metamorphic rocks make up most of Earth's crust by volume, sediment and sedimentary rocks are concentrated near the surface.
Detrital sedimentary rocks are made of solid particles, mostly quartz grains and microscopic clay minerals. Common detrital sedimentary rocks include shale (the most abundant sedimentary rock), sandstone, and conglomerate.
Chemical and biochemical sedimentary rocks are derived from mineral matter (ions) that is carried in solution to lakes and seas. Under certain conditions, ions in solution precipitate (settle out) to form chemical sediments as a result of physical processes, such as evaporation. Precipitation may also occur indirectly through life processes of water- dwelling organisms that form materials called biochemical sediments. Many water-dwelling animals and plants extract dissolved mineral matter to form shells and other hard parts. After the organisms die, their skeletons may accumulate on the floor of a lake or an ocean.
Limestone, an abundant sedimentary rock, is composed chiefly of the mineral calcite (CaCO3). Rock gypsum and rock salt are chemical rocks that form as water evaporates.
Coal forms from the burial of large amounts of plant matter in low- oxygen depositional environments such as swamps and bogs
The transformation of sediment into sedimentary rock is called lithification. The two main processes that contribute to lithification are compaction (a reduction in pore space that results from packing grains more tightly together) and cementation (a reduction in pore space that results from adding new mineral material that acts as a "glue" to bind the grains to each other).

''',

'''
3.4 Metamorphic Rocks: New Rock from Old
KEY TERMS: metamorphic rock, metamorphism, contact metamorphism, regional metamorphism, confining pressure, differential stress, foliation, non- foliated, slate, phyllite, schist, gneiss, marble, quartzite
When rocks are subjected to elevated temperatures and pressures, they can change form, producing metamorphic rocks. Every metamorphic rock has a parent rock-the rock it used to be prior to metamorphism. When the minerals in parent rocks are subjected to heat and pressure, new minerals can form. Depending on the intensity of alteration, metamorphism ranges from low grade to high grade.
Heat, confining pressure, differential stress, and chemically active fluids are four agents that drive metamorphic reactions. Any one alone may trigger metamorphism, or all four may act simultaneously.
Confining pressure results from burial. The force it exerts is the same in all directions, like the pressure exerted by water on a diver. An increase in confining pressure causes rocks to compact into more dense configurations. Differential stresses, which occur during mountain building, are greater in one direction than in others. Rocks subjected to differential stress under ductile conditions deep in the crust tend to shorten in
the direction of greatest stress and elongate in the direction(s) of least stress, producing flattened or stretched grains. In the shallow crust, most rocks respond to differential stress with brittle deformation, breaking into pieces.
A common kind of texture is foliation, the planar arrangement of mineral grains. Common foliated metamorphic rocks include (in order of increasing metamorphic grade) slate, phyllite, schist, and gneiss.
Common nonfoliated metamorphic rocks include quartzite and marble, recrystallized rocks that form from quartz sandstone and limestone, respectively.

''',

'''
3.5 Resources from Rocks and Minerals
KEY TERMS: pegmatite, vein deposit, disseminated deposit, nonmetallic min- eral resource, building material, industrial mineral, fossil fuel, source rock, oil trap, reservoir rock, cap rock, hydraulic fracturing
Igneous processes concentrate some economically important elements through both magmatic differentiation and the emplacement of pegmatites. Magmas may also release hydrothermal (hot-water) solutions that penetrate surrounding rock, carrying dissolved metals in them. The metal ores may be precipitated as fracture-filling deposits (veins) or may penetrate the surrounding strata, producing countless tiny deposits disseminated throughout the host rock.
• Earth materials that are not used as fuels or processed for the metals they contain are referred to as nonmetallic resources. The two broad groups of nonmetallic resources are building materials (such as gypsum, used for plaster) and industrial minerals (including sylvite, a potassium- rich mineral used to make fertilizers).
Coal, oil, and natural gas are all fossil fuels. In each, the
energy
of ancient sunlight, captured by photosynthesis, is stored in the hydrocarbons of plants or other living things buried by sediments.
Coal is formed from compressed plant fragments, originally deposited in ancient swamps. Coal mining can be risky and environmentally damaging, and burning coal generates several kinds of pollution. Oil and natural gas are formed from the heated remains of marine plankton. Together, they account for more than 60 percent of U.S. energy use. Both oil and natural gas leave their source rock (typically shale) and migrate to an oil trap made up of other, more porous rocks, called reservoir rock, covered by a suitable impermeable cap rock. Hydraulic fracturing (or "fracking") is a method of opening pore space in otherwise impermeable rocks, permitting
natural gas to flow out into wells.

''',

'''


4.1 Continental Drift: An Idea Before Its Time
KEY TERMS: continental drift, supercontinent, Pangaea
- German meteorologist Alfred Wegener formulated the continental drift hypothesis in 1915. He suggested that Earth's continents are not fixed in place but move slowly over geologic time.
• Wegener proposed a supercontinent called Pangaea that existed about 200 million years ago, during the late Paleozoic and early Mesozoic eras.
•Wegener's evidence that Pangaea existed and later broke into pieces that drifted apart included (1) the shape of the continents, (2) continental fossil organisms that matched across oceans, (3) matching rock types and modern mountain belts on separate continents, and (4) sedimentary rocks that recorded ancient climates, including glaciers on the southern portion of Pangaea.
• Wegener's hypothesis suffered from two flaws: It proposed tidal forces as the mechanism for the motion of continents, and it implied that the continents would have plowed their way through weaker oceanic crust, like boats cutting through a thin layer of sea ice. Most geologists rejected the idea of continental drift when Wegener proposed it, and it wasn't resurrected for another 50 years.

''',

'''


4.2 The Theory of Plate Tectonics
KEY TERMS: theory of plate tectonics, lithosphere, asthenosphere, lithospheric plate (plate)
Research conducted after World War II led to new insights that helped revive Wegener's hypothesis of continental drift. Exploration of the seafloor uncovered previously unknown features, including an extremely long mid-ocean ridge system. Sampling of the oceanic crust revealed that it was quite young relative to the continents.
The lithosphere, Earth's outermost rocky layer, is relatively stiff and deforms by bending or breaking. The lithosphere consists both of crust (either oceanic or continental) and underlying upper mantle. Beneath the lithosphere is the asthenosphere, a relatively weak layer that deforms by flowing. The lithosphere consists of numerous segments of irregular size and shape. There are seven large lithospheric plates, another seven intermediate-size plates, and many relatively small microplates. Plates meet along boundaries that may be divergent (moving apart from each other), convergent (moving toward each other), or transform (moving laterally past each other).

''',

'''
4.3 Divergent Plate Boundaries and Seafloor Spreading
KEY TERMS: divergent plate boundary (spreading center), oceanic ridge system, rift valley, seafloor spreading, continental rift
Seafloor spreading leads to the formation of new oceanic lithosphere at mid-ocean ridge systems. As two plates move apart from one another, tensional forces open cracks in the plates, allowing magma to well up and generate new slivers of seafloor. This process generates new oceanic lithosphere at a rate of 2 to 15 centimeters (1 to 6 inches) each year.
As it ages, oceanic lithosphere cools and becomes denser. It therefore subsides as it is transported away from the mid-ocean ridge. At the same time, the underlying asthenosphere cools, adding new material to the underside of the plate, which consequently thickens
Divergent boundaries are not limited to the seafloor. Continents can break apart, too, starting with a continental rift (as in modern-day east Africa) and potentially producing a new ocean basin between the two sides of the rift.

''',

'''
4.4 Convergent Plate Boundaries and Subduction
KEY TERMS: convergent plate boundary (subduction zone), deep-ocean trench, partial melting, continental volcanic arc, volcanic island arc (island arc) When plates move toward one another, oceanic lithosphere is subducted into the mantle, where it is recycled. Subduction manifests itself on the ocean floor as a deep linear trench. The subducting slab of oceanic lithosphere can descend at a variety of angles, from nearly horizontal to nearly vertical. Aided by the presence of water, the subducted oceanic lithosphere triggers melting in the mantle, which produces magma. The magma is less dense than the surrounding rock and will rise. It may cool at depth, thickening the crust, or it may make it all the way to Earth's surface, where it erupts as a volcano.
A line of volcanoes that emerge through continental crust is termed a continental volcanic arc, while a line of volcanoes that emerge through an overriding plate of oceanic lithosphere is a volcanic island arc.
Continental crust resists subduction due to its relatively low density, and so when an intervening ocean basin is completely destroyed through subduction, the continents on either side collide, generating a new mountain range.

''',

'''
4.5 Transform Plate Boundaries
KEY TERMS: transform plate boundary (transform fault), fracture zone.
At a transform boundary, lithospheric plates slide horizontally past one another. No new lithosphere is generated, and no old lithosphere is consumed. Shallow earthquakes signal the movement of these slabs of rock as they grind past their neighbors. 
The San Andreas Fault in California is an example of a transform boundary in continental crust, while the fracture zones between segments of the Mid-Atlantic Ridge are transform faults in oceanic
crust.

''',

'''


4.6 From Continental Drift to Plate Tectonics Summarize the view that most geologists held prior to the 1960s regard- ing the geographic positions of the ocean basins and continents.
Fifty years ago, most geologists thought that ocean basins were very old and that continents were fixed in place. Those ideas were discarded with a scientific revolution that revitalized geology: the theory of plate tectonics. Supported by multiple kinds of evidence, plate tectonics is the foundation of modern Earth science.

''',

'''
4.7 How Do Plates and Plate Boundaries Change?
Although the total surface area of Earth does not change, the shape and size of individual plates are constantly changing as a result of subduction and seafloor spreading Plate boundaries can also be created or destroyed in response to changes in the forces acting on the lithosphere. The breakup of Pangaea and the collision of India with Eurasia are two examples of how plates change through geologic time.

''',

'''
4.8 Testing the Plate Tectonics Model
KEY TERMS: mantle plume, hot spot, hot-spot track, Curie point, paleomag- netism (preserved magnetism), magnetic reversal, normal polarity, reverse polarity, magnetic time scale, magnetometer
Multiple lines of evidence have verified the plate tectonics model. For instance, the Deep Sea Drilling Project found that the age of 
the seafloor increases with distance from a mid-ocean ridge. The thickness of sediment atop this seafloor is also proportional to distance from the ridge: Older lithosphere has had more time to accumulate sediment.
A hot spot is an area of volcanic activity where a mantle plume reaches Earth's surface, Volcanic rocks generated by hot-spot volcanism provide evidence of both the direction and rate of plate movement over
time.
Magnetic minerals such as magnetite align themselves with Earth's magnetic field as rock forms. These preserved magnets are records of the ancient orientation of Earth's magnetic field. This is useful to geologists in two ways: (1) It allows a given stack of rock layers to be interpreted in terms of their orientation relative to the magnetic poles through time, and (2) reversals in the orientation of the magnetic field are preserved as "stripes" of normal and reversed polarity in the oceanic crust. Magnetometers reveal this signature of seafloor spreading as a symmetrical pattern of magnetic stripes parallel to the axis of the mid- ocean ridge.

''',

'''
4.9 How Is Plate Motion Measured?
Describe two methods researchers use to measure relative plate motion. Data collected from the ocean floor has established the direction and rate of motion of lithospheric plates. Transform faults point in the direction the plate is moving Establishing dates for seafloor rocks helps to calibrate the rate of motion.
GPS satellites can be used to accurately measure the motion of special receivers to within a few millimeters. These "real-time" data support the inferences made from seafloor observations. On average, plates move at about the same rate human fingernails grow: about 5 centimeters (2 inches) per year.

''',

'''

4.10 What Drives Plate Motions?
Describe plate-mantle convection and explain two of the primary driving forces of plate motion.
KEY TERMS: convection, slab pull, ridge push,
In general, convection (upward movement of less dense material and downward movement of more dense material) appears to drive the motion of plates.
Slabs of oceanic lithosphere sink at subduction zones because the subducted slab is denser than the underlying asthenosphere. In this process, called slab pull, Earth's gravity tugs at the slab, drawing the rest of the plate toward the subduction zone. As oceanic lithosphere slides down the mid-ocean ridge, it exerts a small additional force, called ridge push.
• Convection may occur throughout the entire mantle, as suggested by the whole-mantle model. Alternatively, it may occur in two layers within the mantle-an active upper mantle and a sluggish lower mantle-as proposed in the layer cake model.

''',

'''




5.1 What Is an Earthquake?
KEY TERMS: earthquake, fault, hypocenter (focus), epicenter, seismic wave, elastic rebound, aftershock, foreshock, megathrust fault, fault creep
The sudden movements of large blocks of rock on opposite sides of faults cause most earthquakes. The location where the rock begins to slip is called the hypocenter, or focus. During an earthquake, seismic waves radiate outward from the hypocenter into the surrounding rock. The point on Earth's surface directly above the hypocenter is the epicenter.
The ultimate cause of earthquakes is differential stress that gradually bends Earth's crust over tens to hundreds of years. Up to a point, frictional resistance along the fault keeps the rock from rupturing and slipping. Once that point is reached, the fault slips, allowing the bent rock to "spring back" to its original shape, generating an earthquake. The springing back is called elastic rebound.
Convergent plate boundaries and associated subduction zones are marked by megathrust faults. These large faults are responsible for most of the largest earthquakes in recorded history. Megathrust earthquakes may also generate tsunamis.


''',

'''


5.2 Seismology: The Study of Earthquake Waves Compare and contrast the types of seismic waves and describe the prin-
ciple of the seismograph.
KEY TERMS: seismology, seismograph (seismometer), inertia, seismogram, body waves, surface waves, primary (P) waves, secondary (S) waves
Seismology is the study of seismic waves. A seismograph measures these waves, using the principle of inertia. While the body of the instrument moves with the waves, the inertia of a suspended weight keeps a sensor A seismogram, a record of seismic waves, reveals two main categories stationary to record the displacement between the two.
of earthquake
waves: body waves (P waves and S waves), which are
capable of moving through Earth's interior, and surface waves, which travel only along the upper layers of the crust. P waves are the fastest,
S waves are intermediate in speed, and surface waves are the slowest. However, surface waves tend to have the greatest amplitude, S waves are intermediate, and P waves have the lowest amplitude. Large-amplitude waves produce the most shaking, so surface waves usually account for most damage during earthquakes.
⚫P waves and S waves exhibit different kinds of motion. P waves momentarily push (compress) and pull (stretch) rocks as they travel through a rock body, thereby changing the volume of the rock. S waves impart a shaking motion as they pass through rock, changing the rock's shape but not its volume. Because fluids do not resist forces that change their shape, S waves cannot travel through fluids, whereas P waves can. ? How could you physically demonstrate the difference between P waves and S waves to a friend who hasn't taken a geology course? (Caution: Don't hurt your friend!)


''',

'''


5.3 Locating the Source of an Earthquake
Explain how seismographs are used to locate the epicenter of an earthquake.
The distance separating a recording station from an earthquake's epicenter can be determined by using the difference in arrival times between P and S waves. When the distances are known from three or more seismic stations, the epicenter can be located using a method called triangulation.

''',

'''


5.4 Determining the Size of an Earthquake

KEY TERMS: intensity, magnitude, Modified Mercalli Intensity scale, Richter scale, moment magnitude

• Intensity and magnitude are different measures of earthquake strength. Intensity measures the amount of ground shaking at a location due to an earthquake, and magnitude is an estimate of the amount of energy released during an earthquake.

• The Modified Mercalli Intensity scale is a tool for measuring an earthquake's intensity at different locations. The scale is based on verifiable physical evidence that is used to quantify intensity on a 12-point scale.

The Richter scale takes into account both the maximum amplitude of the seismic waves measured at a given seismograph and that seismograph's distance from the earthquake. The Richter scale is logarithmic, meaning that the next higher number on the scale represents seismic amplitudes that are 10 times greater than those represented by the number below. Furthermore, each larger number on the Richter scale represents the release of about 32 times more energy than the number below it.

Because the Richter scale does not effectively differentiate between very large earthquakes, the moment magnitude scale was devised. This scale measures the total energy released from an earthquake by considering the strength of the faulted rock, the amount of slippage, and the area of the fault that slipped. Moment magnitude is the modern standard for measuring the size of earthquakes.

''',

'''

5.5 Earthquake Destruction

KEY TERMS: liquefaction, tsunami

• Factors influencing how much destruction an earthquake might inflict on a human-made structure include (1) intensity of the shaking, (2) how long shaking persists, (3) the nature of the ground that underlies the structure, and (4) building construction. Buildings constructed of unreinforced bricks and blocks are more likely than other types of structures to be severely damaged in a quake.

In general, bedrock-supported buildings fare best in an earthquake, as loose sediments amplify seismic shaking.

Liquefaction may occur when water-logged sediment or soil is severely shaken during an earthquake. Liquefaction can reduce the strength of the ground to the point that it may not support buildings.

Earthquakes may also trigger landslides or ground subsidence, and they may break gas lines, which can initiate devastating fires. Tsunamis are large ocean waves that form when water is displaced, usually by a megathrust fault rupturing on the seafloor. Traveling at the speed of a jet aircraft, a tsunami is hardly noticeable in deep water. However, upon arrival in shallower coastal waters, the tsunami slows down and piles up, producing a wall of water sometimes more than 30 meters (100 feet) in height. Tsunamis cause major destruction in coastal areas if they strike the shoreline. Tsunami warning systems have been established in most of the large ocean basins.

''',

'''

5.6 Where Do Most Earthquakes Occur?

• Most earthquake energy is released in the circum-Pacific belt, the ring of megathrust faults rimming the Pacific Ocean. Another earthquake belt is the Alpine-Himalayan belt, which runs along the zone where the Eurasia plate collides with the Indian subcontinent and African plates. • Earth's oceanic ridge system produces another belt of earthquake activity. Seafloor spreading and active transform faults that separate ridge segments generate many frequent small-magnitude quakes. Transform faults in the continental crust, including the San Andreas Fault, can produce large earthquakes.

Although most destructive earthquakes are produced along plate boundaries, some occur at considerable distances from plate boundaries. Examples include the 1811-1812 New Madrid, Missouri, earthquakes and the 1886 Charleston, South Carolina, earthquake.

''',

'''

6.2 The Nature of Volcanic Eruptions

KEY TERMS: magma, lava, effusive eruption, viscosity, eruption column

The two primary factors determining the nature of a volcanic eruption are the viscosity (resistance to flow) of the magma and its gas content. In general, magmas that contain more silica are more viscous, while those with lower silica content are more fluid. Temperature also influences viscosity. Hot lavas are more fluid, while cool lavas are more viscous.

Basaltic magmas, which are fluid and have low gas content, tend to generate effusive (nonexplosive) eruptions. In contrast, silica-rich magmas (andesitic and rhyolitic). which are the most viscous and contain the greatest quantity of gases, are the most explosive.

''',

'''

6.3 Materials Extruded During an Eruption

List and describe the three categories of materials extruded during vol- canic eruptions.

KEY TERMS: aa flow, pahoehoe flow, lava tube, pillow lava, volatile, pyroclas- tic material, tephra, scoria, pumice

• Volcanoes erupt molten lava, gases, and solid pyroclastic materials. • Low-viscosity basaltic lava flows can extend great distances from a volcano. On the surface, they travel as pahoehoe or aa flows. Sometimes the surface

of the flow congeals, and lava continues to flow below in tunnels called lava tubes. When lava erupts underwater, the outer surface is chilled instantly to obsidian, while the inside continues to flow, producing pillow lavas. The gases most commonly emitted by volcanoes are water vapor and carbon dioxide. Upon reaching the surface, these gases rapidly expand, leading to explosive eruptions that can generate a mass of lava fragments called pyroclastic materials.

• Pyroclastic materials come in several sizes. From smallest to largest, they are ash, lapilli, and blocks or bombs. Blocks exit the volcano as solid fragments, whereas bombs exit as liquid blobs.


If bubbles of gas in lava don't pop before the lava solidifies, they are preserved as voids called vesicles. Especially frothy, silica-rich lava can cool to make lightweight pumice, while basaltic lava with lots of bubbles

cools to make scoria.

''',

'''
6.4 Anatomy of a Volcano

KEY TERMS: fissure, conduit, vent, volcanic cone, crater, caldera, parasitic cone, fumarole

• Volcanoes vary in size and form but share a few common features. Most are roughly conical piles of extruded material that collect around a central vent. The vent is usually within a summit crater or caldera. On the flanks of the volcano, there may be smaller vents marked by small parasitic cones, or there may be fumaroles, spots where gas is expelled. ? Label the diagram using the following terms: conduit, vent, lava, parasitic cone, bombs, pyroclastic material.

''',

'''
6.5 Shield Volcanoes

KEY TERMS: shield volcano, seamount

⚫ Shield volcanoes consist of many successive lava flows of low-viscosity basaltic lava but lack significant amounts of pyroclastic debris. Lava tubes help transport lava far from the main vent, resulting in very gentle, shield-like profiles.

⚫ Most shield volcanoes begin as seamounts that grow from Earth's seafloor. Mauna Loa, Mauna Kea, and Kilauea in Hawaii are classic examples of the low, wide form characteristic of shield volcanoes.
''',

'''
6.6 Cinder Cones

KEY TERMS: cinder cone, (scoria cone)

emerge

Cinder cones are steep-sided structures composed mainly of pyroclastic debris, typically having a basaltic composition. Lava flows sometimes from the base of a cinder cone but typically do not flow out of the crater. • Cinder cones are small relative to the other major kinds of volcanoes, reflecting the fact that most form quickly, as single eruptive events. Because they are unconsolidated, cinder cones easily succumb to weathering and erosion.

''',

'''

6.7 Composite Volcanoes


KEY TERMS: composite volcano, (stratovolcano)

magmas

• Composite volcanoes are called "composite" because they consist of both pyroclastic material and lava flows. They typically erupt silica-rich of andesitic or rhyolitic composition. They are much larger than cinder cones and form from multiple eruptions over millions of years. • Because andesitic and rhyolitic lavas are more viscous than basaltic lava, they accumulate at a steeper angle than does the lava from shield volcanoes. Over time, a composite volcano's combination of lava and cinders produces a towering volcano with a classic symmetrical shape. • Mount Rainier and the other volcanoes of the Cascade Range in the northwestern United States are good examples of composite volcanoes.

''',

'''

6.8 Volcanic Hazards

KEY TERMS: pyroclastic flow (nuée ardente), lahar, tsunami

The greatest volcanic hazard to human life is the pyroclastic flow, or nuée ardente. This dense mix of hot gas and pyroclastic fragments races downhill at great speed and incinerates everything in its path. A pyroclastic flow can travel many kilometers from its source volcano. Because pyroclastic flows are hot, their deposits frequently "weld" together into a solid rock called welded tuff.

Lahars are mudflows that form on volcanoes. These rapidly moving slurries of ash and debris suspended in water tend to follow stream valleys and can result in loss of life and/or significant damage to structures. • Volcanic ash in the atmosphere can be a risk to air travel when it is sucked into airplane engines. Volcanoes at sea level can generate tsunamis when they erupt or when their flanks collapse into the ocean. Those that spew large amounts of gas such as sulfur dioxide can cause respiratory problems. If volcanic gases reach the stratosphere, they screen out a portion of incoming solar radiation and can trigger short- term cooling at Earth's surface.

''',

'''

6.9 Other Volcanic Landforms

List volcanic landforms other than shield, cinder, and composite volca- noes and describe their formation.

KEY TERMS: fissure eruption, basalt plateau, flood basalt, volcanic neck, (plug) Calderas, which can be among the largest volcanic structures, form when the rigid, cold rock above a magma chamber cannot be supported and collapses, creating a broad, roughly circular depression. On shield

volcanoes, calderas form slowly as lava drains from the magma chamber beneath the volcano. On a composite volcano, caldera collapse often follows an explosive eruption that can result in significant loss of life and destruction of property.

Fissure eruptions occasionally produce massive floods of fluid basaltic lava from large cracks, called fissures, in the crust. Layer upon layer of these flood basalts may accumulate to significant thicknesses and blanket a wide area. The Columbia Plateau in the northwestern United States is an example.

Shiprock, New Mexico, is an example of a volcanic neck where the lava in the "throat" of an ancient volcano congealed to form a plug of solid rock that weathered more slowly than the surrounding volcanic rocks. The surrounding pyroclastic debris eroded, and the resistant neck remains as a distinctive landform.

''',

'''

6.10 Intrusive Igneous Activity

Compare and contrast these intrusive igneous structures: dikes, sills, batholiths, stocks, and laccoliths.

KEY TERMS: host (country) rock, intrusion (pluton), tabular, massive, discord- ant, concordant, dike, sill, columnar jointing, batholith, stock, laccolith . When magma intrudes other rocks, it may cool and crystallize before reaching the surface to produce intrusions called plutons. Plutons come in many shapes. They may cut across the host rocks without regard for preexisting structures, or the magma may flow along weak zones in the host rock, such as between the horizontal layers of sedimentary bedding. .Tabular intrusions may be concordant (sills) or discordant (dikes). Massive plutons may be small (stocks) or very large (batholiths). A blister- like intrusion that lifts the overlying rock layers is a laccolith. As solid igneous rock cools, its volume decreases. Contraction can produce a distinctive fracture pattern called columnar jointing.

''',

'''

6.11 Partial Melting and the Origin of Magma 

KEY TERMS: partial melting, geothermal gradient, decompression melting • Solid rock may melt under three geologic circumstances: when heat is added to the rock, raising its temperature; when already hot rock experiences lower pressures (decompression, as seen at mid-ocean ridges); and when water is added (as occurs at subduction zones).

''',

'''
6.12 Plate Tectonics and Volcanism

KEY TERMS: Ring of Fire, volcanic island arc (island arc), continental volcanic arc, intraplate volcanism, mantle plume, hot spot, superplume

• Volcanoes occur at both convergent and divergent plate boundaries, as well as in intraplate settings.

• At divergent plate boundaries, where lithosphere is being rifted apart, decompression melting is the dominant generator of magma. As warm rock rises, it can begin to melt without the addition of heat.

• Convergent plate boundaries that involve the subduction of oceanic crust are the most common site for explosive volcanoes-most prominently in the Pacific Ring of Fire. The release of water from the subducting plate triggers melting in the overlying mantle. The ascending magma interacts with the lower crust of the overlying plate and can form a volcanic are at the surface. • In intraplate settings, the source of magma is a mantle plume-a column of mantle rock that is warmer and more buoyant than the surrounding mantle.

''',

'''


7.1 Crustal Deformation
Describe the three types of differential stress and identify the tectonic setting most commonly associated with each. Differentiate stress from strain and brittle from ductile deformation.
KEY TERMS: deformation, tectonic structure (geologic structure), stress, confining pressure, differential stress, compressional stress, tensional stress, shear, strain, elastic deformation, brittle deformation, ductile deformation
• Tectonic (geologic) structures are structures generated when rocks are deformed by bending or breaking; they include folds, faults, and joints. Stress is the force that drives rock deformation. When stress acts equally from all directions, we call it confining pressure. When the stress is greatest in one direction, we call it differential stress. There are three main types of differential stress: compressional, tensional, and shear.
⚫ A rock's strength is its ability to resist permanent deformation. When the stresses on a rock exceed its strength, the rock deforms, usually by folding or faulting.
Elastic deformation is caused by a temporary stretching of the chemical bonds in a rock. When the stress is released, the rock returns to its original shape. When the rock's strength is exceeded, bonds break, and the rock deforms in either a brittle or ductile fashion. Brittle deformation fractures rocks, whereas ductile deformation changes a rock's shape. . Whether a rock deforms in a brittle or ductile manner depends on its temperature and its confining pressure. The hotter a rock, the more likely it is to experience ductile deformation. Greater confining pressure makes a rock stronger and less likely to break. Thus, rock deformation tends to be brittle in the shallow crust and ductile at deeper levels.
⚫ Whether deformation is brittle or ductile also depends on the type of rock. For example, shale is weaker than granite, so it is more prone to ductile deformation. If a rock is forced to deform more quickly than can be accommodated by the slow processes of ductile deformation, it will break.

''',

'''
7.2 Folds: Rock Structures Formed by Ductile Deformation
List and describe five types of folds.
KEY TERMS: fold, anticline, syncline, dome, basin, monocline
• Folds are wavelike undulations in layered rocks that develop through ductile deformation caused by compressional stresses.
• Anticlines usually arise by upfolding, or arching, of sedimentary layers, whereas synclines are downfolds. or troughs. Anticlines and synclines may be symmetrical, asymmetrical, overturned, or recumbent.
• When folded rocks erode to form a series of ridges and valleys, the ridges represent resistant beds (not anticlines), and the valleys represent softer beds (not synclines). A fold is said to plunge when its axis penetrates the ground at an angle. This results in a V-shaped outcrop pattern.
• Domes and basins are large bowl- or saucer-shaped folds that produce roughly circular outcrop patterns. When eroded, a dome has the oldest beds in the middle, and a basin has the oldest beds around the margin.
• Monoclines are large steplike folds in otherwise horizontal strata that develop when beds drape over a vertical offset produced by subsurface faulting.

''',

'''
7.3 Faults and Joints: Rock Structures Formed by Brittle Deformation
Sketch and briefly describe the relative motion of rock bodies located on opposite sides of normal, reverse, and thrust faults as well as both types of strike-slip faults.
KEY TERMS: fault, dip-slip fault, hanging wall block, footwall block, fault scarp, normal fault, fault-block mountain, horst, graben, half-graben, detach- ment fault, reverse fault, thrust fault, strike-slip fault, transform fault, joint Faults and joints are fractures in rock that form through brittle deformation.
A fault is a fracture along which motion occurs, offsetting the rocks on either side. If the movement is in the direction of the fault's dip (or inclination), the rock above the fault plane is the hanging wall block, and the rock below the fault is the footwall block. If the hanging wall moves down relative to the footwall, the fault is a normal fault. If the hanging wall moves up relative to the footwall, the fault is a reverse fault. Large normal faults with low dip angles are called detachment faults. Large reverse faults with low dip angles are thrust faults.
⚫ Faults that intersect Earth's surface may produce a "step" in the land known as a fault scarp. Areas of tectonic extension, such as the Basin and Range Province, produce fault-block mountains-horsts separated by neighboring grabens or half-grabens.
• Areas of tectonic compression, such as mountain belts, are dominated by reverse faults that shorten the crust horizontally while thickening it vertically.
Strike-slip faults have most of their movement in a horizontal direction along the trend of the fault trace. Transform faults are strike-slip faults that serve as tectonic boundaries between lithospheric plates. Joints form in the shallow crust when rocks are stressed under brittle conditions. They facilitate groundwater movement and mineralization of economic resources, and they may result in hazards to humans.

''',

'''

7.4 Mountain Building
Locate and name Earth's major mountain belts on a world map.
KEY TERMS: orogenesis, orogeny, collisional mountain
• Orogenesis is the making of mountains. An episode of orogenesis is an orogeny. Most orogenesis occurs along convergent plate boundaries, where compressional forces cause folding and faulting, thickening the crust vertically and shortening it horizontally.

''',

'''
7.5 Subduction and Mountain Building
Sketch a cross section of an Andean-type mountain belt and describe how its major features are generated.
KEY TERMS: accretionary wedge, forearc basin
The type of convergent margin determines the type of mountains that form. Where one oceanic plate overrides another, a volcanic island arc forms. Where an oceanic plate subducts under a continent, Andean-type mountain building occurs.
In either case, release of water from the subducted slab triggers melting in the overlying mangle wedge, generating basaltic magmas
that rise to the base of the continental crust where they often pond. The hot basaltic magma may heat the overlying crustal rocks sufficiently to generate a silica-rich magma of intermediate or felsic (granitic) composition.
.Sediment scraped off the subducting plate builds an accretionary wedge. Between the accretionary wedge and the volcanic arc is a relatively calm site of sedimentary deposition, the forearc basin.
The geophy of central California preserves an accretionary wedge (Coast Ranges), a foreare basin (Great Valley), and the roots of an Andean-style mountain belt (Sierra Nevada).


''',

'''


7.6 Collisional Mountain Belts
Summarize the stages in the development of an Alpine-type mountain belt such as the Appalachians.
KEY TERMS: terrane, microcontinent, suture • A terrane is a relatively small crustal fragment (microcontinent, volcanic island arc, or oceanic plateau) that has been carried by an oceanic plate to a continental subduction zone and then accreted onto the continental margin. The North American Cordillera formed by the accretion of many successive terranes.
The Himalayas and Appalachians were formed by collisions between continents when the intervening ocean basin subducted completely. The Appalachians were caused by e collision of ancestral North America with ancestral rica more than 250 million years ago. The Himalayas were med by the collision of India and Eurasia starting around million years ago, and they are still rising.

''',

'''
7.7 Vertical Motions of the Crust
Explain the principle of isostasy and how it contributes to the elevated topography of mountain belts.
KEY TERMS: isostasy, isostatic adjustment, gravitational collapse
• Earth's crust floats in the denser material of the mantle the way wood floats in water. This principle is termed isostasy. If additional weight is placed on the crust (an ice sheet, for example), the crust sinks, and if weight is removed (glacial melting), the crust rebounds. This process of maintaining gravitational equilibrium is called isostatic adjustment. For a mountain belt, isostasy partially offsets the effect of erosion, pushing the mountains up as erosion wears them down.
When compressional forces raise a mountain belt too high, the rock at the belt's core becomes warm and weak, and the belt spreads, becoming broader
and lower.

''',

'''


8.1 Earth's External Processes
List three types of external processes and discuss the role each plays in the rock cycle.
KEY TERMS: external process, internal process, weathering, mass movement, erosion
⚫ Weathering, mass movement, and erosion are responsible for creating, transporting, and depositing sediment. They are called external processes because they occur at or near Earth's surface and are powered by gravity and by energy from the Sun.
• Internal processes lead to volcanic activity and mountain building and derive their energy from Earth's interior.

''',

'''
8.2 Weathering
Define weathering and distinguish between the two main categories of weathering. Summarize the factors that influence the type and rate of rock weathering.
KEY TERMS: mechanical weathering, chemical weathering, frost wedging, sheeting, exfoliation dome, carbonic acid, spheroidal weathering, differential weathering
Mechanical weathering is the physical breaking up of rock into smaller pieces. Rocks can be broken into smaller fragments by frost wedging, salt crystal growth, unloading, and biological activity.
⚫ Chemical weathering alters a rock's chemistry, changing it into different substances.
Water is by far the most important agent of chemical weathering. Oxygen in water can oxidize some materials, while carbon dioxide (CO2) dissolved in water forms carbonic acid. The chemical weathering of silicate minerals produces soluble products containing sodium, calcium, potassium, and magnesium, as well as insoluble iron oxides and clay minerals.
Mechanical weathering aids chemical weathering; the smaller the particles into which rock is
broken, the faster the rock will weather.
The mineral composition of a rock affects the rate of weathering. For example, calcite readily dissolves in mildly acidic solutions. Among the silicate minerals, those that crystallize earlier as magma cools are less resistant to chemical weathering than those that crystallize later.
Masses of rock do not weather uniformly. Differential weathering refers to the variation in the rate and degree of weathering caused by factors such as rock type, climate, and degree of jointing. Rock weathers most rapidly in an environment with lots of heat to drive reactions and water to facilitate those reactions.
''',

'''

8.3 Soil: An Indispensable Resource
Define soil and explain why soil is referred to as an interface.
KEY TERMS: regolith, soil, soil texture
Soils are vital combinations of organic and nonorganic components found at the interface where
regolith's rocky debris, mixed with humus, water, and air.
the
Soil texture refers to the proportions of different particle sizes (clay, silt, and sand) found in soil.

''',

'''

8.4 Controls of Soil Formation
List and briefly discuss five controls of soil formation. KEY TERMS: parent material
Residual soils form in place due to the weathering of bedrock, whereas transported soils develop on unconsolidated sediment. Soils form slowly and
change in character as they mature.
The type of parent material influences the rate of weathering and the soil's fertility but only weakly affects the type of mature soil that develops.
Climate (particularly temperature and precipitation) exerts the strongest control over soil type.
The types and abundance of organisms in a locality strongly influence the physical and chemical properties of the soil, particularly by furnishing The steepness of the slope on which a soil is forming is a key variable, with shallow slopes retaining their soils and steeper slopes shedding them to d organic matter and breaking it down to yield nutrients, humus, and organic acids, as well as by mixing and aerating soil. AM to 280
accumulate elsewhere.
''',

'''
8.5 Describing and Classifying Soils
Describe an idealized soil profile. Explain the need for classifying soils. KEY TERMS: soil horizon, soil profile, eluviation, leaching, solum, Soil Taxonomy
Despite the great diversity of soils around the world, there are some broad patterns to the vertical anatomy of soil layers. Organic material, called humus, is added at the top (O horizon), mainly from plant sources. There, it mixes with mineral matter (A horizon). At the bottom, bedrock breaks down and contributes mineral matter (C horizon). In between, some materials are leached out (eluviated) from higher levels (E horizon) and transported to lower levels (B horizon), where they may form an impermeable layer called hardpan.
The need to bring order to huge quantities of data motivated the establishment of a classification scheme for the world's soils. This Soil Taxonomy features 12 broad orders.

''',

'''
8.6 Soil Erosion: Losing a Vital Resource
Discuss the detrimental impact of human activities on soil and some ways that soil erosion is controlled.
• Soil erosion is a natural process; it is part of the constant recycling of Earth materials that we call the rock cycle.
• Because of human activities, soil erosion rates have increased over the past several hundred years. Natural soil production rates are constant, so there is a net loss of soil at a time when a record- breaking number of people live on the planet. Using windbreaks, terracing the land, installing grassed waterways, and plowing the land along horizontal contour lines are all practices that have been shown to reduce soil erosion.

''',


'''
8.7 Mass Movement on Slopes:
The Work of Gravity
Discuss the role that mass movements play in the development of land- scapes. Summarize the factors that control and trigger mass movement processes.
KEY TERMS: mass movement, trigger, angle of repose
• After weathering breaks apart rock, gravity moves the debris downslope, in a process called mass movement. Sometimes this occurs rapidly as a landslide, and at other times the movement is slower. Landslides are a significant geologic hazard, taking many lives and destroying property every year. • Mass movement serves an important role in landscape development. It widens stream-cut valleys and helps tear down mountains thrust up by internal processes.
• An event that initiates a mass movement process is referred to as a trigger. The addition of water, oversteepening of the slope, removal of vegetation, and shaking due to an earthquake are four important
examples. Not all landslides are triggered by one of these four but many are.
processes,
• Water added to a slope can expand the pore space between grains, causing them to lose their cohesion. Water also adds a significant amount of mass to a wetted slope.
⚫ Loose granular materials can form a stable slope only up to a specific angle of repose, which is typically between 25 and 40 degrees from horizontal and is steeper for coarser or more angular particles. Cohesive materials do not have a defined angle of repose but eventually respond to oversteepening with mass movement.
The roots of plants (especially plants with deep roots) act as a three- dimensional "net" that holds soil and regolith particles in place. The removal of vegetation such as by wildfires or various human activities that clear the land on steep slopes can set the stage for significant mass
movement.
• Earthquakes are significant triggers that deliver an energetic jolt to slopes poised on the brink of failure.

''',

'''


8.8 Types of Mass Movement
List and explain the criteria that are commonly used to classify mass movement processes. Distinguish among six different types of mass movement.
KEY TERMS: fall, slide, flow, rock avalanche, slump, rockslide, debris flow, mudflow, lahar, earthflow, creep, solifluction, permafrost
⚫ Mass movements can be classified by the type of material involved (e.g., rocks, debris, mud), the type of motion (fall, slide, flow), and the rate of motion (from very fast to centimeters or millimeters per year).
• Rockfalls occur when pieces of bedrock detach and fall freely through the air. Repeated rockfalls are the primary means by which talus slopes are built and maintained.
. Many slides occur when a mass of material moves along a well-defined, flattish surface, such as a bedding plane that tilts into a valley. A rockslide consists of blocks of rock; a debris slide consists mainly of unconsolidated soil and regolith. Motion is generally rapid; rock avalanches can reach speeds exceeding 200 kilometers (125 miles) per hour.
In a slump, a mass of rock or unconsolidated material (such as clay) slides as a unit along a curved, often spoon-shaped surface. Slumping is a common response to slopes becoming oversteepened.
In a flow, material moves downslope as a viscous, often turbulent fluid (rather than coherently, as in a slide). Most flows are saturated with water; they range in consistency from very thick to soupy. A debris flow consists of soil and regolith; in a mudflow, the material is mainly fine grained. A lahar is a particularly deadly type of debris flow that develops on steep volcanic slopes. Thick flows may pick up and carry large boulders and trees.
Earthflows are usually much slower than debris flows and form on
hillsides in humid regions. They are associated with silt- and clay-rich
materials. Typically, sites of earthflow show an uphill scarp and a lobe of viscous soil on the downhill side.
• Creep is a widespread and important form of mass movement that is very slow. It occurs mainly when freezing (or wetting) causes soil particles to be pushed out away from the slope, only to drop down to a lower position following thawing (or drying)
Solifluction is the gradual flow of a saturated surface layer that is underlain by an impermeable zone. In arctic regions, the impermeable zone is permafrost. privasi

''',

'''


9.1 Earth as a System: The Hydrologic Cycle
List the hydrosphere's major reservoirs and describe the different paths that water takes through the hydrologic cycle.
KEY TERMS: hydrologic cycle, evaporation, infiltra- tion, runoff, transpiration, evapotranspiration • Water moves through the hydrosphere's many reservoirs by evaporating, condensing into clouds, and falling as precipitation. Once it reaches the ground, rain can either soak in, evaporate, be returned to the atmosphere by plant transpiration, or run off. Running water is the most important agent sculpting Earth's varied landscapes.

''',

'''
9.2 Running Water
Describe the nature of drainage basins and river sys- tems. Sketch four basic drainage patterns.
KEY TERMS: drainage basin (watershed), divide, head- ward erosion, dendritic pattern, radial pattern, rectangular pattern, trellis pattern
The land area that contributes water to a stream is its drainage basin. Drainage basins are separated by imaginary lines called divides.
As a generalization, river systems tend to erode at the upstream end, transport sediment through the middle section, and deposit sediment at the downstream end. A stream erodes most effectively in a headward direction, thereby lengthening its course.
? Identify each of the drainage patterns depicted in the accompanying sketch.
''',

'''

9.3 Streamflow Characteristics Discuss streamflow and the factors that cause it to change. KEY TERMS: laminar flow, turbulent flow, gradient, discharge, longitu-
dinal profile
The flow of water in a stream may be laminar or turbulent. A stream's flow velocity is influenced by the channel's gradient; the size, shape, and roughness of the channel; and the stream's
discharge.
A cross-sectional view of a stream from head to mouth is a longitudinal profile. Usually the gradient and roughness of the stream channel decrease going downstream, whereas the size of the channel, stream discharge, and flow velocity increase in the downstream direction.

''',

'''
9.4 The Work of Running Water
Summarize the ways in which streams erode, transport, and deposit
sediment.
KEY TERMS: pothole, dissolved load, suspended load, bed load, settling velocity, saltation, capacity, competence, sorting, alluvium
• Streams erode when turbulent water lifts loose particles from the streambed. The focused "drilling" of the stream armed with swirling particles also creates potholes in solid rock.
Streams transport their load of sediment dissolved in water, in suspension, and along the bottom (bed) of the channel.
A stream's ability to transport solid particles is described using two criteria: Capacity refers to how much sediment a stream is transporting, and competence refers to the particle sizes the stream is capable of moving.
• Streams deposit sediment when velocity slows and competence is reduced. This results in sorting, the process by which like-size particles are deposited together.
''',

'''
9.5 Stream Channels
KEY TERMS: meander, cut bank, point bar, cutoff, oxbow lake, braided channel
Bedrock channels are cut into solid rock and are most common in headwaters areas where gradients are steep. Rapids and waterfalls are common features. •Alluvial channels are dominated by streamflow through alluvium previously deposited by the stream. A floodplain usually covers the valley floor, with the river meandering or moving through braided channels.
⚫ Meanders change shape through erosion at the cut bank (the outer edge of the meander) and deposition of sediment on point bars (the inside of a meander). A meander may become cut off and form an oxbow lake.
? The town of Carter Lake is the only portion of the state of lowa that lies on the west side of the Missouri River. It is bounded on the north by its namesake, Carter Lake, on the south by the Missouri River, and on the east and west by Nebraska. After examining the map, prepare a hypothesis that explains how this unusual situation could have developed.
''',

'''
9.6 Shaping Stream Valleys
Contrast narrow V-shaped valleys, broad valleys with floodplains, and valleys that display incised meanders.
KEY TERMS: stream valley, base level, floodplain, incised meander, stream
terrace
• A stream valley includes the channel itself, the adjacent floodplain, and the relatively steep valley walls. Streams erode downward until they approach base level, the lowest point to which a stream can
de its channel. A river flowing toward the ocean (the ultimate se level) may encounter several local base levels along its route. 1ese could be lakes or resistant rock layers that retard downcutting by the stream.
A stream valley is widened through the meandering action of the stream, which erodes the valley walls and widens the floodplain. If base level drops or if the land is uplifted, a stream downcuts. If it is underlain by bedrock, the stream may develop incised meanders. Streams underlain by deep alluvium are likely to develop terraces.
''',

'''

9.7 Depositional Landforms
Discuss the formation of deltas, natural levees, and alluvial fans. KEY TERMS: bar, delta, distributary, natural levee, back swamp, yazoo tribu-
tary, alluvial fan
• A delta may form where a river deposits sediment in another water body at its mouth. The partitioning of streamflow into multiple distributaries spreads sediment in different directions.
• Natural levees result from sediment deposited along the margins of a stream channel by many flooding events. Because the levees slope gently away from the channel, the adjacent floodplain is poorly drained, resulting in back swamps and yazoo tributaries flowing parallel to the main river. ⚫ Alluvial fans are fan-shaped deposits of alluvium that form where steep mountain fronts drop down into adjacent valleys.

''',


'''
9.8 Floods and Flood Control
Distinguish between regional floods and flash floods. Describe some
common flood control measures.
KEY TERMS: flood
Floods are usually triggered by heavy rains and/or snowmelt. Sometimes human interference can worsen or even cause floods. Flood control measures include the building of artificial levees and dams. y involve creating artificial cutoffs. Many scientists
Channelization may
and engineers advocate a nonstructural approach to flood control that
involves more appropriate land use.

''',

'''
9.9 Groundwater: Water Beneath the Surface
Discuss the importance of groundwater and describe its distribution and movement. KEY TERMS: groundwater, zone of saturation, water table, unsaturated zone, porosity, perme- ability, aquitard, aquifer
Groundwater represents the largest reservoir of freshwater that is readily available to humans. Geologically, groundwater is an equalizer of streamflow, and the dissolving action of groundwater produces caverns and sinkholes.
Groundwater is water that occupies the pore spaces in sediment and rock in a zone beneath the surface called the zone of saturation. The upper limit of this zone is called the water table. The zone above the water table where the material is not saturated is called the unsaturated zone.
The quantity of water that can be stored in the open spaces in rock or sediment is termed porosity. Permeability, the ability of a material to transmit a fluid through interconnected pore spaces, is a key factor affecting the movement of groundwater. Aquifers are permeable materials that transmit groundwater freely, whereas aquitards are impermeable materials. ? Examine this profile view showing the distribution of water in relatively uniform unconsolidated sediments and label the various portions of the groundwater complex.
''',

'''
9.10 Wells, Artesian Systems, and Springs
Compare and contrast wells, artesian systems, and springs. KEY TERMS: well, drawdown, cone of depression, artesian system, confined aquifer, spring, perched water table, hot spring, geyser • Wells, which are openings bored into the zone of saturation, withdraw groundwater and may create roughly conical depressions in the water table known as cones of depression. • Artesian wells tap into inclined aquifers bounded above and below by aquitards. For a system to qualify as artesian, the water in the well must be under sufficient pressure for the water to rise above the top of the confined aquifer. Artesian wells may be flowing or nonflowing, depending on whether the pressure e surface is above or below the ground surface. •Springs occur where the water table intersects the land surface and a natural flow of groundwater results. When groundwater circulates deep below the surface, it may become heated and emerge at the surface as a hot spring. Geysers occur when groundwater is heated in underground chambers and expands, with some water quickly changing to steam and causing the geyser to erupt. The source of heat for most hot springs and geysers is hot igneous rock.

''',

'''
9.11 Environmental Problems Related to Groundwater
List and discuss three important environmental problems associated with groundwater. • Groundwater can be "mined" by being extracted at a rate that is greater than the rate of replenishment. When groundwater is treated as a nonrenewable resource, as it is in parts of the High Plains aquifer, the water table drops, in some cases by 60 meters (200 feet The extraction of groundwater can cause pore
space to decrease in volume and the grains of loose Earth materials to pack more closely together. This overall compaction of sediment volume results in the
subsidence of the land surface.
Contamination of groundwater with sewage, highway salt, fertilizer, or industrial chemicals is another issue of critical concern. Once groundwater is
contaminated, the problem is very difficult to solve
requiring expensive remediation or even abandonment of the aquifer.

''',

'''


9.12 The Geologic Work of Groundwater
Explain the formation of caverns and the development of karst topography. KEY TERMS: cavern, stalactite, stalagmite, karst topography, sinkhole (sink),
⚫ Groundwater dissolves rock, in particular limestone, leaving behind void spaces in the rock. Caverns form at the zone of saturation, but later dropping of the water table may leave them open and dry--and available for people to explore.
• Dripstone is rock deposited by dripping of water containing dissolved calcium carbonate inside caverns. Features made of dripstone include stalactites, stalagmites, and columns.
Karst topography develops in limestone regions and exhibits irregular terrain punctuated with many depressions called sinkholes. Some sinkholes form when the cavern roofs collapse.
Identify the three cavern deposits labeled in this photograph.
''',
'''


10.1 Glaciers and the Earth System
Explain the role of glaciers in the hydrologic and rock cycles. Describe the different types of glaciers, their characteristics, and their present- day distribution.
KEY TERMS: glacier, valley, (alpine) glacier, ice sheet, sea ice, ice shelf, ice cap, piedmont glacier, outlet glacier
A glacier is a thick mass of ice that originates on land from the compaction and recrystallization of snow and that shows evidence of past or present flow. Glaciers are part of both the hydrologic cycle and the rock cycle. They store and release freshwater, and they transport and deposit large quantities of sediment.
Valley glaciers flow down mountain valleys, whereas ice sheets are very large masses, such as those that cover Greenland and Antarctica. During the Last Glacial Maximum, around 18,000 years ago, large areas of Earth were covered by glacial ice.
. When valley glaciers exit confining mountains, they may spread out into broad lobes called piedmont glaciers. Similarly, ice shelves form when glaciers flow into the ocean, producing a layer of floating ice.
• Ice caps are like small ice sheets. Both ice sheets and ice caps may be drained by outlet glaciers, which often resemble valley glaciers.

''',

'''


10.2 How Glaciers Move
Describe how glaciers move, the rates at which they move, and the significance of the glacial budget.
KEY TERMS: zone of fracture, crevasse, zone of accumulation, snowline, (equilibrium line), zone of wastage, calving, iceberg, glacial budget
Glaciers move in part by flowing under pressure. On the surface of a glacier, ice is brittle. Below about 50 meters (165 feet), pressure is great, and ice flows like a plastic material. In addition, the bottom of a glacier may slide along its bed.
• Fast glaciers may move 800 meters (2600 feet) per year, while slow glaciers may move only 2 meters (6.5 feet) per year. Some glaciers experience periodic surges of rapid movement. 238 8.0
A glacier's budget is the balance between formation of new ice from snow in the zone of accumulation and loss of ice in the zone of wastage. When the budget is positive, the glacier's terminus advances; when the budget is negative, the terminus retreats.

''',

'''
10.3 Glacial Erosion
Discuss the processes of glacial erosion. Identify and describe the major topographic features sculpted by glacial erosion.
KEY TERMS: plucking, abrasion, rock flour, glacial striations, glacial trough, hanging valley, cirque, arête, horn, fiord
⚫ Glaciers acquire sediment through plucking from the bedrock beneath the glacier, by abrasion of the bedrock using sediment already in the ice, and when mass-wasting processes drop debris on top of the glacier. Grinding of the bedrock produces grooves and scratches called glacial
striations.
⚫ Erosional features produced by valley glaciers include glacial troughs, hanging valleys, cirques, arêtes, horns, and fiords.
''',

'''
10.4 Glacial Deposits
Distinguish between the two basic types of glacial deposits and briefly describe the features associated with each type.
KEY TERMS: glacial drift, till, glacial erratic, stratified drift, lateral moraine, medial moraine, end moraine, ground moraine, outwash plain, valley train, kettle, drumlin, esker, kame
Any sediment of glacial origin is called drift. The two distinct types of glacial drift are till, which is unsorted material deposited directly by the ice, and stratified drift, which is sediment sorted and deposited by meltwater from a glacier.
The most widespread features created by glacial deposition are layers or ridges of till, called moraines. Associated with valley glaciers are lateral moraines, formed along the sides of the valley, and medial moraines, formed between two valley glaciers that have merged. End moraines, which mark the former position of the front of a glacier, and ground moraines, undulating layers of till deposited as the ice front retreats, are common to both valley glaciers and ice sheets.
''',

'''

10.5 Other Effects of Ice Age Glaciers
Describe and explain several important effects of Ice Age glaciers other than the formation of erosional and depositional landforms.
KEY TERMS: proglacial lake, pluvial lake
In addition to erosional and depositional features, other effects of Ice Age glaciers include the forced migration of organisms and adjustments of the crust by rebounding upward after removal of the immense load of ice. Ice sheets are nourished by water that ultimately comes from the ocean, so when ice sheets grow, sea level falls, and when they melt, sea level rises. Advance and retreat of ice sheets caused significant changes to the paths followed by rivers. Proglacial lakes formed when glaciers acted as dams to create lakes by trapping glacial meltwater or blocking rivers. In response to the cooler and wetter glacial climate, pluvial lakes formed in areas such as present-day Nevada.
''',

'''

10.6 The Ice Age
Discuss the extent of glaciation and climate variability during the Quaternary Ice Age. Summarize some of the current ideas about the causes of ice ages.
KEY TERMS: Quaternary period
The Ice Age that began between 2 and 3 million years ago is a complex period characterized by numerous advances and withdrawals of glacial ice. Most of the major glacial episodes occurred during a span on the geologic time scale called the Quaternary period, which continues today. The existence of multiple layers of drift on land and an uninterrupted record of climate cycles preserved in seafloor sediments provide evidence of the occurrence of several glacial advances during the Ice Age. While rare, Ice Ages have occurred in Earth history prior to the recent glaciations we call the Ice Age. Lithified till, called tillite, is a major line of evidence for these ancient ice ages. There are several reasons glacial ice might accumulate globally, including the position of the continents, which is driven by plate tectonics. Antarctica's position over the South Pole is doubtless a key reason for its massive ice sheets, for instance. • The Quaternary period is marked by not only glacial advances but also intervening episodes of glacial retreat. One way to explain these oscillations is through variations in Earth's orbit, which lead to seasonal variations in the distribution of solar radiation. The orbit's shape varies (eccentricity), the tilt of the planet's rotational axis varies (obliquity), and the axis slowly "wobbles" over time (precession). These three effects, which occur on different time scales, collectively account for alternating colder and warmer periods during the Quaternary.
Additional factors that may be important for initiating or ending glaciations include rising or falling levels of greenhouse gases, changes in the reflectivity of Earth's surface, and variations in the ocean currents that redistribute heat energy from warmer to colder regions.
''',

'''
10.7 Deserts
Describe the general distribution and extent of Earth's dry lands and the role that water plays in modifying desert landscapes.
KEY TERMS: dry climate, desert, steppe, ephemeral stream
• Dry climates cover about 30 percent of Earth's land area. These regions have yearly precipitation totals that are less than the potential loss of water through evaporation. Deserts are drier than steppes, but both climate types are considered water deficient.
Dry regions in the lower latitudes coincide with the zones of subsiding air and high air pressure known as subtropical highs. Middle-latitude continents far removed from oceans. Mountains also act to shield these deserts exist because of their positions in the deep interiors of large
regions from humid marine air masses.
Nevertheless, running water is responsible for most of the erosional work Practically all desert streams are dry most of the time (ephemeral). in a desert. Although wind erosion is more significant in dry areas tha elsewhere, the main role of wind in a desert is to transport and deposit
sediment.

''',

'''
10.8 Basin and Range: The Evolution of a Mountainous Desert Landscape
Discuss the stages of landscape evolution in the Basin and Range region of the western United
States.
KEY TERMS: interior drainage, alluvial fan, bajada, playa lake
The Basin and Range region of the western United States is characterized by interior drainage, with streams eroding uplifted mountain blocks and depositing sediment in interior basins. Alluvial fans, bajadas, playas, playa lakes, salt flats, and inselbergs are features often associated with these landscapes.
''',

'''
10.9 Wind Erosion
Describe the ways that wind transports sediment and the features created by wind erosion.
KEY TERMS: deflation, blowout, desert pavement
• For wind erosion to be effective, dryness and scant vegetation are essential. Deflation, the lifting and removal of loose material, often produces shallow depressions called blowouts.
• Abrasion, the sandblasting effect of wind, is often given too much credit for producing desert features. However, abrasion does cut and polish rock near the surface.
''',

'''

10.10 Wind Deposits
Explain how loess deposits differ from deposits of sand. Discuss the movement of dunes and distinguish among different dune types. KEY TERMS: loess, dune, slip face, cross bed, barchan dunes, transverse dunes, barchanoid dunes, longitudinal dunes, parabolic dunes, star dunes • Wind deposits are of two distinct types: extensive blankets of silt, called loess, carried by wind in suspension, and mounds and ridges of sand, called dunes, which are formed from sediment that is carried as part the wind's bed load.
of
⚫ Most loess is derived from either deserts or areas that have recently been glaciated. In the latter case, wind blowing across stratified drift picks up silt-size grains.
⚫ Dunes accumulate due to the difference in wind energy on the upwind and downwind sides of the dune (or an object that initiates dune formation). Sand that is blown up the gently sloping upwind side settles out on the downwind slip face, where it periodically avalanches down to maintain the angle of repose. These processes cause the dune to
migrate downwind. Inside the dune, the buried slip faces may be preserved as cross beds.
. There are six major kinds of dunes. Their shapes result from the pattern of prevailing winds, the amount of available sand, and the presence of vegetation.
? This close-up photo shows a small portion of one side of a barchan dune. What term is applied to this side of the dune? Is the prevailing wind direction "coming out" of the photo or "going into" the photo? Explain. Why did some of the sand break away and slide?

''',

'''


11.1 A Brief History of Geology
Explain the principle of uniformitarianism and discuss how it differs from catastrophism.
KEY TERMS: catastrophism, uniformitarianism
Early ideas about the nature of Earth were based on religious traditions and notions of great catastrophes.
In the late 1700s, James Hutton emphasized that the same slow processes have acted over great spans of time and are responsible for Earth's rocks, mountains, and landforms. This similarity of processes over vast spans of time led to this principle being called uniformitarianism.

''',

'''
11.2 Creating a Time Scale: Relative Dating Principles
Distinguish between numerical and relative dating and apply relative dating principles to determine a time sequence of geologic events.
KEY TERMS: numerical date, relative date, principle of superposition, principle of original horizontality, principle of lateral continuity, principle of cross-cutting relationships, principle of inclusions, conformable, uncon- formity, angular unconformity, disconformity, nonconformity
The two types of dates that geologists use to interpret Earth history are (1) relative dates, which put events in their proper sequence of formation, and (2) numerical dates, which pinpoint the time in years when an event took place.
• Relative dates can be established using the principles of superposition, original horizontality, cross-cutting relationships, and inclusions. Unconformities, gaps in the geologic record, may be identified during the relative dating process.

''',

'''
11.3 Fossils: Evidence of Past Life
Define fossil and discuss the conditions that favor the preser- vation of organisms as fossils. List and describe various types of fossils.
KEY TERMS: fossil, paleontology
• Fossils are remains or traces of ancient life. Paleontology is the branch of science that studies fossils.
Fossils can form through many processes. For an organism to be preserved as a fossil, it usually needs to be buried rapidly. Also, an organism's hard
parts are most likely to be preserved because soft tissue decomposes rapidly in most circumstances.

''',

'''
11.4 Correlation of Rock Layers
Explain how rocks of similar age that are in different places can be matched up. KEY TERMS: correlation, principle of fossil succession, index fossil, fossil assemblage • Matching up exposures of rock that are the same age but are in different places is called correlation. By correlating rocks from around the world, geologists e developed the geologic time scale and obtained a fuller perspective on Earth history.
Fossils can be used to correlate sedimentary rocks in widely separated places by using the rocks' distinctive fossil content and applying the principle of fossil succession. This principle states that fossil organisms succeed one another in a definite and determinable order, and, therefore, a time period can be recognized by examining its fossil content. Index fossils are particularly useful in correlation because they are widespread it aipoload art bo polonim and associated with a relatively narrow time span. The overlapping ranges fossils in an assemblage may be used to establish an age for a rock layer that contains multiple fossils.
of
Fossils may be used to establish ancient environmental conditions that existed when sediment was deposited.
''',

'''
11.5 Numerical Dating with Nuclear Decay
Discuss three ways that atomic nuclei change and explain how unstable isotopes are used to determine numerical dates. KEY TERMS: nuclear, (radioactive) decay, radiometric dating, half-life, radiocarbon dating
Nuclear decay is the spontaneous breaking apart of certain unstable atomic nuclei. Three common forms of nuclear decay are (1) emission of an alpha particle from the nucleus, (2) emission of a beta particle (electron) from the nucleus, and (3) capture of an electron by the nucleus. Radiometric dating refers to the procedure by which unstable isotopes are used to determine numerical ages of rocks and minerals. It is reliable
because the rates of decay for the isotopes that are used have been precisely measured and do not vary.
The length of time it takes for one-half of the nuclei of an unstable parent isotope to change into its stable daughter product is called the half-life of that

''',

'''
11.6 Determining Numerical Dates for Sedimentary Strata
Explain how reliable numerical dates are determined for layers of sedimentary rock.
Sedimentary strata are usually not directly datable using radiometric techniques because they consist
of the material produced by the weathering of other rocks. A particle in a sedimentary rock comes from some older source rock. If you were to date the particle using unstable isotopes, you would get the age of the source rock, not the age of the sedimentary rock.
One way geologists assign numerical dates to sedimentary rocks is to use relative dating principles to relate them to datable igneous masses, such as dikes and volcanic ash beds. A layer may be older than one igneous feature and younger than another.

''',

'''
11.7 The Geologic Time Scale
Sandstone Basalt dike dated at 570 million years old
Unconformity
Granite dated at 1.4 billion years old
Distinguish among the four basic time units that make up the geologic time scale and explain why the time scale is considered to be a dynamic tool. KEY TERMS: geologic time scale, eon, Phanerozoic eon, era, Paleozoic era, Mesozoic era, Cenozoic era, period, epoch, Archean, Proterozoic, Precambrian Earth history is divided into units of time on the geologic time scale. Eons are divided into eras, which each contain multiple periods. Periods are divided into epochs.
⚫ Precambrian time includes the Archean and Proterozoic eons. It is followed by the Phanerozoic eon, which is well documented by abundant fossil evidence, resulting in many subdivisions.
The geologic time scale is a work in progress, continually being refined as new information becomes available.
''',

'''


12.1 What Makes Earth Habitable?
List the principal characteristics that make Earth habitable.
KEY TERMS: exoplanet, habitable zone
As far as we know, Earth is unique among planets in hosting life. The planet's size, composition, and distance from the Sun all contribute to conditions
that support life.

''',

'''
12.2 Birth of a Planet
Outline the major stages in Earth's evolution, from the Big Bang to the formation of our planet's layered
internal structure.
KEY TERMS: supernova, solar nebula, planetesimal, protoplanet, Hadean
• The universe is thought to have formed about 13.8 billion years ago, with the Big Bang, which generated space, time, energy, and matter, including the elements hydrogen and helium. Elements heavier than hydrogen and helium were synthesized by nuclear reactions that occur in stars.
Earth and the solar system formed around 4.6 billion years ago, with the contraction of a solar nebula. Collisions between clumps of matter in this spinning disk resulted in the growth of planetesimals and then protoplanets. Over time, the matter of the solar nebula was concentrated into a smaller number of larger bodies: the Sun, the rocky inner planets, the icy outer planets, moons, comets, and asteroids.
The early Earth was hot enough for rock and iron to melt, thanks to the kinetic energy of impacting asteroids and planetesimals as well as the decay of radioactive isotopes. This allowed iron to sink to form Earth's core and rocky material to rise to form the mantle and crust.

''',

'''
12.3 Origin and Evolution of the Atmosphere and Oceans
Describe how Earth's atmosphere and oceans formed and evolved through time. KEY TERMS: outgassing, photosynthesis, banded iron formation, Great Oxygenation Event Earth's atmosphere formed as volcanic outgassing added mainly water vapor and carbon dioxide to the primordial atmosphere of gases common in the early solar system: methane and ammonia.
Free oxygen began to accumulate through photosynthesis by cyanobacteria, which released oxygen as a waste product. Much of this early oxygen immediately reacted with iron dissolved in seawater and settled to the ocean floor as chemical sediments called banded iron formations. The Great Oxygenation Event of 2.5 billion years ago marks the first evidence of significant amounts of free oxygen in the atmosphere.
⚫ Earth's oceans formed after the planet's surface had cooled. Soluble ions weathered from the crust were carried to the ocean, making it salty. The oceans also absorbed tremendous amounts of carbon dioxide from the atmosphere.

''',

'''
12.4 Precambrian History: The Formation of Earth's Continents
Explain the formation of continental crust, how continental crust becomes assembled into continents, and the role that the supercontinent cycle has played in this process.
KEY TERMS: craton, shield, supercontinent, supercontinent cycle
The Precambrian includes the Archean and Proterozoic eons. Our knowledge of these eons is limited because erosion has destroyed much of the rock
record.
Continental crust was produced over time through the recycling of ultramafic and mafic crust in an early version of plate tectonics. Small crustal fragments formed and amalgamated into large crustal provinces called cratons. Over time, North America and other continents grew through the accretion of new
terranes around the edges of this central "nucleus" of crust.
Over time, these ocean basins also closed to form a new supercontinent called Pangaea around 250 million years ago. Early cratons not only merged but sometimes rifted apart. The supercontinent Rodinia formed around 1.1 billion years ago and then rifted apart, opening new ocean basins. Like Rodinia before it, Pangaea broke up as part of the ongoing supercontinent cycle.
The formation of elevated oceanic ridges following the breakup of a supercontinent displaced enough water that sea level rose, and shallow seas flooded the continents. The breakup of continents can also influence the direction of ocean currents, with important consequences for climate.

''',

'''
12.5 Geologic History of the Phanerozoic: The Formation of Earth's Modern Continents
List and discuss the major geologic events in the Paleozoic, Mesozoic, and Cenozoic eras.
KEY TERMS: Pangaea, Laurasia, Gondwana
The Phanerozoic eon began 545 million years ago and is divided into the Paleozoic, Mesozoic, and Cenozoic eras.
In the Paleozoic era, North America experienced a series of collisions that resulted in the rise of the young Appalachian mountain belt, as part of the assembly of Pangaea. High sea levels caused the ocean to cover vast areas of the continent and resulted in a thick sequence of sedimentary strata. During the Mesozoic, Pangaea broke up, and the Atlantic Ocean began to form. As the North American continent moved westward, the Cordillera began to rise due to subduction and the accretion of terranes along the west coast. In the Southwest, vast deserts accumulated thick layers of dune sand, while environments in the East were conducive to the formation and subsequent burial of coal swamps.
In the Cenozoic era, a thick sequence of sediments was deposited along North America's Atlantic margin and the Gulf of Mexico. Meanwhile, western North America experienced an extraordinary episode of crustal extension; the Basin and Range Province resulted.

''',

'''

12.6 Earth's First Life
Describe some of the hypotheses on the origin of life and the character- istics of early prokaryotes, eukaryotes, and multicellular organisms. KEY TERMS: protein, prokaryote, stromatolite, eukaryote
Life began from nonlife. Amino acids, a necessary building block for proteins, may have been assembled with energy from ultraviolet light or lightning, or in a hot spring, or may have been delivered later to Earth
via meteorites.
The first organisms were relatively simple single-celled prokaryotes that thrived in the absence of oxygen. They may have formed by 3.8 billion years ago. The advent of photosynthesis allowed microbial mats to build up and form stromatolites.
Eukaryotes have larger, more complex cells than prokaryotes. The oldest- known eukaryotic cells date from around 2.1 billion years ago. Eukaryotic cells gave rise to the great diversity of multicellular organisms.

''',

'''
12.7 Paleozoic Era: Life Explodes
List the major developments in the history of life during the Paleozoic era. KEY TERMS: invertebrate, Cambrian explosion, vertebrate, amphibian, reptile, amniotic egg, mass extinction
Abundant fossil hard parts appear in sedimentary rocks at the beginning of the Cambrian period. These shells and other skeletal material came from a profusion of new animals, including trilobites and cephalopods. Plants colonized the land around 400 million years ago and soon diversified into forests.
In the Devonian, some lobe-finned fishes gradually evolved into the first amphibians. A subset of the amphibian population evolved waterproof skin and shelled eggs and split off to become the reptile line. The Paleozoic era ended with the largest mass extinction in the geologic record. This deadly event may have been related to the eruption of the Siberian Traps flood basalts.

''',

'''
12.8 Mesozoic Era: Dinosaurs Dominate the Land Briefly explain the major developments in the history of life during the Mesozoic era.
KEY TERMS: seed, gymnosperm
• Plants diversified during the Mesozoic. The flora of that time was dominated by gymnosperms, the first plants with seeds.
The dinosaurs came to dominate the land, pterosaurs took to the air, and a suite of marine reptiles swam the seas. The first birds evolved during the Mesozoic, as evidenced by Archaeopteryx, a transitional fossil. Like the Paleozoic, the Mesozoic ended with a mass extinction. This extinction was due to a massive meteorite impact and a period of extensive volcanism, both of which released particulate matter into the atmosphere and dramatically altered Earth's climate and disrupted its food chain.

''',

'''


13.1 The Vast World Ocean
Discuss the extent and distribution of oceans and continents on Earth. Identify Earth's four main ocean basins.
KEY TERM: oceanography
• Oceanography is an interdisciplinary science that draws on the methods and knowledge of biology, chemistry, physics, and geology to study all aspects of the world ocean.
Earth's surface is dominated by oceans. Nearly 71 percent of the planet's surface area is oceans and marginal seas. In the Southern Hemisphere, about 81 percent of the surface is water.
Of the three major oceans-the Pacific, Atlantic, and Indian-the Pacific Ocean is the largest, contains slightly more than half of the water in the world ocean, and has the greatest average depth-3940 meters (12,927 feet).

''',

'''
13.2 An Emerging Picture of the Ocean Floor Define bathymetry and summarize the various techniques used to map
the ocean floor.
KEY TERMS: bathymetry, sonar, echo sounder
map
⚫ Seafloor mapping is done with sonar-shipboard instruments that emit pulses of sound that "echo" off the bottom. Satellites are also used to the ocean floor. Their instruments measure slight variations in sea level that result from differences in the gravitational pull of features on the seafloor. Accurate maps of seafloor topography can be made using these data. Mapping efforts have revealed three major areas of the ocean floor: continental margins, deep-ocean basins, and oceanic ridges.

''',

'''
13.3 Continental Margins
Compare a passive continental margin with an active continental margin and list the major features of each.
KEY TERMS: continental margin, passive continental margin, continental shelf, continental slope, continental rise, deep-sea fan, submarine canyon, turbidity current, active continental margin, accretionary wedge, subduction erosion ⚫ Continental margins are transition zones between continental and oceanic crust. Active continental margins occur where a plate boundary and the edge of a continent coincide, usually on the leading edge of plate. Passive continental margins are on the trailing edges of continent far from plate boundaries.

Heading offshore from the shoreline of a passive margin, a submarine traveler would first encounter the crust and the beginning of the oceanic crust. Beyond the continental slope is another gently sloping section, gently sloping continental shelf and then the steeper continental slope, marking the end of the continental the continental rise, made of sediment transported by turbidity currents through submarine canyons and piled up in deep-sea fans atop the oceanic crust.
Submarine canyons are deep, steep-sided valleys that originate on the continental slope and may extend to the deep-ocean basin. Many submarine canyons have been excavated by turbidity currents (downslope
movements of dense, sediment-laden water).
At an active continental margin, material may be added to the leading edge of a continent in the form of an accretionary wedge (common at shallow-angle subduction zones), or material may be scraped off the
edge of a continent by subduction erosion (common at steeply dipping subduction zones).

''',

'''
13.4 Features of Deep-Ocean Basins
Overriding continental crust
KEY TERMS: deep-ocean basin, deep-ocean trench, volcanic island arc, continental volcanic arc, abyssal plain, seamount, guyot, oceanic plateau The deep-ocean basin makes up about half of the ocean floor's area. Much of it is abyssal plain (deep, featureless sediment-draped crust). Subduction zones and deep-ocean trenches also occur in deep-ocean basins. Paralleling trenches are volcanic island arcs (if the subduction goes underneath oceanic lithosphere) or continental volcanic arcs (if the overriding plate has continental lithosphere on its leading edge
There are a variety of volcanic structures on the deep-ocean floor. Seamounts are submarine volcanoes; if they pierce the surface of the ocean, we call them volcanic islands. Guyots are old volcanic islands that have had their tops eroded off before they sink below sea level. Oceanic plateaus are unusually thick sections of oceanic crust formed by massive underwater eruptions of lava.

''',

'''
13.5 The Oceanic Ridge System Summarize the basic characteristics of oceanic ridges. KEY TERMS: oceanic ridge or rise (mid-ocean ridge), rift valley
The oceanic ridge system is the longest topographic feature on Earth, wrapping around the world through all major ocean basins. It is a few kilometers tall, a few thousand kilometers wide, and a few tens
''',

'''
13.6 Seafloor Sediments
of thousands of kilometers long. The summit is the place where new oceanic crust is generated, often marked by a rift valley. Oceanic ridges are elevated features because they are warm and therefore less dense than older, colder oceanic lithosphere. As oceanic crust moves away from the ridge crest, heat loss causes the oceanic crust to become denser and subside. After 80 million years, crust that was once part of an oceanic ridge is in the deep-ocean basin, far from the ridge.
Distinguish among three categories of seafloor sediment and explain how biogenous sediment can be used to study climate change.
KEY TERMS: terrigenous sediment, biogenous sediment, hydrogenous sediment
There are three broad categories of seafloor sediments. Terrigenous sediment consists primarily of mineral grains that were weathered from continental rocks and transported to the ocean; biogenous sediment consists of shells and skeletons of marine animals and plants; and hydrogenous sediment includes minerals that crystallize directly from seawater through various chemical reactions.
Seafloor sediments are helpful in studying worldwide climate change because they often contain the remains of organisms that once lived near the sea surface. The numbers and types of these organisms change as the climate changes, and their remains in seafloor sediments record these changes.

''',

'''



14.1 Composition of Seawater

Define salinity and list the main elements that contribute to the ocean's salinity. Describe the sources of dissolved substances in seawater and causes of variations in salinity.

KEY TERM: salinity

•

Salinity is the proportion of dissolved salts to pure water, usually expressed in parts per thousand (%). The average salinity in the open ocean is about 35%. The principal elements that contribute to the ocean's salinity are chlorine (55 percent) and sodium (31 percent). The primary sources for the elements in sea salt are chemical weathering of rocks on the continents and volcanic outgassing on the ocean floor. ⚫Variations in seawater salinity are primarily caused by gain or loss of water. The main causes of reduced salinity are precipitation, runoff from land, and the melting of icebergs and sea ice. The main causes of increased salinity are evaporation and the formation of sea ice.

''',

'''
14.2 Variations in Temperature and Density with Depth

Discuss temperature, salinity, and density changes with depth in the open ocean.

KEY TERMS: thermocline, density, pycnocline

The ocean's surface temperature is related to the amount of solar energy received and varies as a function of latitude. Low-latitude regions have relatively warm surface water and distinctly colder water at depth, creating a thermocline, which is a layer of rapid temperature change. No thermocline exists in high-latitude regions because there is little temperature difference between the top and bottom of the water column (that is, the water column is isothermal). • The density of seawater depends mainly on its temperature and secondarily on salinity. Cold, high-salinity water is densest. Low-latitude regions have distinctly denser (colder) water at depth than at the surface, creating a pycnocline, which is a layer of rapidly changing density. No pycnocline exists in high-latitude regions (that is, the water column is isopycnal).

• At low latitudes, most regions of the open ocean exhibit a three-layered structure based on water density.

The shallow surface mixed zone has warm and nearly uniform temperatures. The transition zone includes a

''',

'''
14.3 The Diversity of Ocean Life

Distinguish among plankton, nekton, and benthos. Summarize the factors used to divide the

ocean into marine life zones.

KEY TERMS: photosynthesis, plankton, phytoplankton, zooplankton, biomass, nekton, benthos, photic zone, euphotic zone, aphotic zone, intertidal zone, neritic zone, oceanic zone, pelagic zone, benthic zone, abyssal zone

Marine organisms can be classified into one of three groups, based on habitat and mobility. Plankton are free-floating forms with little power of locomotion, nekton are swimmers, and benthos are bottom dwellers. Most of the ocean's biomass is planktonic.

Three criteria are frequently used to establish marine life zones. Based on availability of sunlight, the ocean can be divided into the photic zone (which includes the euphotic zone) and the aphotic zone. Based on distance from shore, the ocean can be divided into the intertidal zone, the neritic zone, and the oceanic zone. Based on water depth, the ocean can be divided into the pelagic zone and the benthic zone (which includes the abyssal zone).

''',

'''

14.4 Oceanic Productivity

Contrast ocean productivity in polar, midlatitude, and tropical settings.

KEY TERM: primary productivity

• Primary productivity is the amount of carbon fixed by organisms through the synthesis of organic matter using energy derived from solar radiation (photosynthesis) or chemical reactions (chemosynthesis). Chemosynthesis is much less significant than photosynthesis in worldwide oceanic productivity. Photosynthetic productivity in the ocean varies due to the availability of nutrients and amount of solar radiation.

Oceanic photosynthetic productivity varies at different

latitudes because of seasonal changes and the development of a thermocline. In polar oceans, the availability of solar radiation limits productivity even though nutrient levels are high. In tropical oceans, a strong thermocline exists year-round, so the lack of nutrients generally limits productivity. In midlatitude oceans, productivity peaks in the spring and fall and is limited by the lack of solar radiation in winter and by the lack of nutrients

in summer.

''',

'''

14.5 Oceanic Feeding Relationships

Define trophic level and discuss the efficiency of energy transfer between different trophic levels.

KEY TERMS: trophic level, food chain, food web

The Sun's energy is utilized by phytoplankton and converted to chemical energy, which is passed through different trophic levels. On average, only about 10 percent of the mass taken in at one trophic level is passed on to the next. As a result, the size

of individuals increases but the number of individuals decreases with each trophic level of a food chain or food web. Overall, the total biomass of populations decreases at successive trophic levels.

''',

'''



15.1 The Ocean's Surface Circulation

Discuss the factors that create and influence surface-ocean currents and describe the effect these ocean currents have on climate.

KEY TERMS: gyre, Coriolis effect

The ocean's surface pattern of the world's major wind belts. Surface currents are parts of huge, slowly moving loops of water called gyres that are centered in the subtropics of each ocean basin. The positions of the continents and the Coriolis effect also influence the movement of ocean water within gyres. Because of the Coriolis effect, subtropical gyres move clockwise in the Northern Hemisphere and counterclockwise in the Southern Hemisphere. Generally, four main currents comprise each subtropical gyre.

⚫ Ocean currents can have a significant effect on climate. Poleward-moving warm ocean currents moderate winter temperatures in the middle latitudes. Cold currents exert their greatest influence during summer in middle latitudes and year-round in the tropics. In addition to cooler temperatures, cold currents are associated with greater fog frequency and drought

''',

'''

15.2 Upwelling and Deep-Ocean Circulation

KEY TERMS: upwelling, thermohaline circulation

Upwelling, the rising of colder water from deeper layers, is a wind-induced movement that brings cold, nutrient-rich water to the surface. Coastal upwelling is most characteristic along the west coasts of continents. In contrast to surface currents, deep-ocean circulation is governed by gravity and driven by density differences. The two factors that can create a dense mass of water are temperature and salinity, so the movement of deep-ocean water is often termed thermohaline circulation. Most water involved in thermohaline circulation begins in high latitudes at the surface, when the salinity of the cold water increases as a result of sea ice formation. This dense water sinks, initiating deep-ocean currents.

''',

'''

15.3 The Shoreline: A Dynamic Interface

KEY TERMS: shoreline, shore, coast, coastline, foreshore, backshore, near-shore zone, offshore zone, beach, berm, beach face

The shore is the area extending between the lowest tide level and the highest elevation on land that is affected by storm waves. The coast extends inland from the shore as far as ocean-related features can be found. The shore is divided into the foreshore and backshore. Seaward of the foreshore are the near- shore and offshore zones.

A beach is an accumulation of sediment along the landward margin of the ocean or a lake. Among its parts are one or more berms and the beach face. Beaches are composed of whatever material is locally abundant and can be thought of as material in transit along the shore.


''',

'''
15.4 Ocean Waves


KEY TERMS: wave height, wavelength, wave period, circular orbital motion, wave base, surf

Waves are moving energy, and most ocean waves are initiated by wind. The three factors that influence the height, wavelength, and period of a wave are (1) wind speed, (2) length of time the wind has blown (duration), and (3) fetch, the distance that the wind has traveled across open water. Once waves leave a storm area, they are termed swells, which are symmetrical, longer-wavelength waves.

As waves travel, water particles transmit energy by circular orbital motion, which extends to a depth equal to one-half the wavelength (the wave base).

When a wave enters water that is shallower than the wave base, it slows down, which allows waves farther from shore to catch up. As a result, wavelength decreases and wave height increases. Eventually the wave breaks, creating turbulent surf in which water rushes toward the shore.

''',

'''



15.5 The Work of Waves

Describe how waves erode and move sediment along the shore.

KEY TERMS: abrasion, wave refraction, beach drift, longshore current, rip current

Waves provide most of the energy that modifies shorelines. Wave erosion is caused by wave impact pressure and abrasion (the sawing and grinding action of water armed with rock fragments).

As they approach the shore, waves refract (bend) to align nearly parallel to the shore. Refraction occurs because a wave travels more slowly in shallower water, allowing the part still in deeper water to catch up. Wave refraction causes wave erosion to be concentrated against the sides and ends of headlands and dispersed in bays.

• Waves that approach the shore at an angle transport sediment parallel to the shoreline. On the beach face, this movement of sediment, called beach drift, is due to the fact that the incoming swash pushes sediment obliquely upward, whereas the backwash pulls it directly downslope. Longshore currents are a similar phenomenon in the surf zone, capable of transporting very large quantities of sediment parallel to a shoreline.

''',

'''

15.6 Shoreline Features

KEY TERMS: wave-cut cliff, wave-cut platform, marine terrace, sea arch, sea stack, spit, bay- mouth bar, tombolo, barrier island

Erosional features include wave-cut cliffs (which originate from the cutting action of the surf against the base of coastal land), wave-cut platforms (relatively flat, bench- like surfaces left behind by receding cliffs), and marine terraces (uplifted wave-cut platforms). Erosional features also include sea arches (formed when a headland is eroded and two sea caves from opposite sides unite) and sea stacks (formed when the roof of a sea arch collapses).

• Some of the depositional features that form when sediment is moved by beach drift and longshore currents are spits (elongated ridges of sand that project from the land into the mouth of an adjacent bay), baymouth bars (sandbars that completely cross a bay), and tombolos (ridges of sand that connect an island to the mainland or to another island). Along the Atlantic and Gulf coastal plains, the coastal region is characterized by offshore barrier islands, which are low ridges of sand that parallel the coast.

''',

'''
15.7 Contrasting America's Coasts

Distinguish between emergent and submergent coasts. Contrast the erosion problems faced on the Atlantic and Gulf coasts with those along the Pacific Coast.

KEY TERMS: emergent coast, submergent coast, estuary

• Coasts may be classified by their changes relative to sea level. Emergent coasts are sites of either land uplift or sea-level fall. Marine terraces are features of emergent coasts. Submergent coasts are sites of land subsidence or sea-level rise. One characteristic of submergent coasts is drowned river valleys called estuaries. In the United States, the Pacific coast is emergent, and the Atlantic and Gulf coasts are submergent. The Atlantic and Gulf coasts of the United States are lined in many places by barrier islands-dynamic expanses of sand that see a lot of change during storm events. Many of these low and narrow islands have also been prime sites for real estate development. The Pacific coast's big issue is the narrowing of beaches due to sediment starvation. Rivers that drain to the coast (bringing it sand) have been dammed, resulting in reservoirs that trap sand before it can make it to the coast. Narrower beaches offer less resistance to incoming waves, often leading to erosion of bluffs behind the beach.

''',

'''

15.8 Stabilizing the Shore

Summarize the ways in which people deal with shoreline erosion problems.

KEY TERMS: hard stabilization, jetty, groin, breakwater, seawall, beach nourishment

open.

⚫ Hard stabilization refers to any structures built along the coastline to prevent movement of sand or shoreline erosion. Jetties project out from the coast, with the goal of keeping inlets Groins are also oriented perpendicular to the coast, but with the goal of slowing beach erosion by longshore currents. Breakwaters are parallel to the coast but located some distance offshore. Their goal is to blunt the force of incoming ocean waves, often to protect boats. Like breakwaters, seawalls are parallel to the coast, but they are built on the shoreline itself. Often the installation of hard stabilization results in increased erosion elsewhere. ⚫ Beach nourishment is an expensive alternative to hard stabilization. Sand is pumped onto a beach from some other area, temporarily replenishing the sediment supply. Another possibility is relocating buildings away from high-risk areas and leaving the beach to be shaped by natural processes.
''',

'''

15.9 Tides

Explain the cause of tides and their monthly cycles. Describe the hori- zontal flow of water that accompanies the rise and fall of tides.

KEY TERMS:, tide, spring tide, neap tide, diurnal tidal pattern, semidiurnal tidal pattern, mixed tidal pattern, tidal current, tidal flat

Tides are daily changes in ocean-surface elevation. They are caused by gravitational pull on ocean water by the Moon and, to a lesser extent, the Sun. When the Sun, Earth, and Moon all line up about every 2 weeks (full moon or new moon), the tides are most exaggerated. When a quarter moon is in the sky, the Moon is pulling on Earth's water at a right angle relative to the Sun, and the daily tidal range is minimized as the two forces partially counteract one another.

mb

Tides are strongly influenced by local conditions, including the shape of the local coastline and the depth of the ocean basin. Tidal patterns may be diurnal (one high tide per day), semidiurnal (two high tides per day), or mixed (similar to semidiurnal but with significant inequality between high tides).

A flood current is the landward movement of water during the shift between low tide and high tide. When high tide transitions to low tide again, the movement of water away from the land is an ebb current. Ebb currents may expose tidal flats to the air. If a tide passes through an inlet, the current may carry sediment that gets deposited as a tidal delta. ? Would spring tides and neap tides occur on an Earth-like planet that had no moon? Explain.

''',

'''

16.1 Focus on the Atmosphere

Distinguish between weather and climate and name the basic elements of weather and climate.

KEY TERMS: weather, climate, elements (of weather and climate)

• Weather is the state of the atmosphere at a particular place for a short period of time. Climate, on the other hand, is a generalization of the weather conditions of a place over a long period of time.

• The most important elements-quantities or properties that are measured regularly of weather and climate are (1) air temperature, (2) humidity, (3) type and amount of cloudiness, (4) type and amount of precipitation, (5) air pressure, and (6) the speed and direction of the wind.

''',

'''

16.2 Composition of the Atmosphere

List the major gases composing Earth's atmosphere and identify the components that are most important to understanding weather and climate.

KEY TERMS: air, aerosols, ozone

Air is a mixture of many discrete gases, and its composition varies from time to time and from place to place. If water vapor, dust, and other variable components of the atmosphere are removed, clean, dry air is composed almost entirely of nitrogen (N2) and oxygen (O2). Carbon dioxide (CO2), although present only in minute amounts, is important because it has the ability to absorb heat radiated by Earth and thus helps keep the atmosphere warm. Among the variable components of air, water vapor is important because it is the source of all clouds and precipitation. Like carbon dioxide, water vapor can absorb heat emitted by Earth. When water changes from one state to another, it absorbs or releases heat. In the atmosphere, water vapor transports this latent ("hidden") heat from place to place; latent heat provides the energy that helps drive many storms.

• Aerosols are tiny solid and liquid particles that are important because they may act as surfaces on which water vapor can condense and are also absorbers and reflectors of incoming solar radiation.

Ozone, a form of oxygen that combines three oxygen atoms into each molecule (O3), is concentrated in the 10- to 50-kilometer (6- to 31-mile) height range in the atmosphere. This gas is important to life because of its ability to absorb potentially harmful ultraviolet radiation from the Sun.

''',

'''

16.3 Vertical Structure of the Atmosphere

Interpret a graph that shows changes in air pressure from Earth's surface to the top of the atmosphere. Sketch and label a graph that shows atmospheric layers based on temperature.

KEY TERMS: troposphere, environmental lapse rate, radiosonde, stratosphere, mesosphere, thermosphere

Because the atmosphere gradually thins with increasing altitude, it has no sharp upper boundary but simply blends into outer

space.

Based on temperature, the atmosphere is divided vertically into four layers. The troposphere is the lowermost layer. In the troposphere, temperature usually decreases with increasing altitude. This environmental lapse rate is variable but averages about 6.5°C per kilometer (3.5°F per 1000 feet). Essentially, all important weather phenomena occur in the troposphere.

Beyond the troposphere is the stratosphere, which warms with increasing altitude because of absorption of UV radiation by

ozone. In the mesosphere, temperatures again decrease with increasing altitude. Above the mesosphere is the thermosphere, a

layer with only a tiny fraction of the atmosphere's mass and no well-defined upper limit.

''',

'''

16.4 Earth-Sun Relationships

Explain what causes the Sun angle and length of daylight to change during the year and describe how these changes produce the seasons. KEY TERMS: rotation, circle of illumination, inclination of the axis, Tropic of Cancer, summer solstice, Tropic of Capricorn, winter solstice, autumnal (fall) equinox, spring equinox

The two principal motions of Earth are (1) rotation about its axis, which produces the daily cycle of daylight and darkness, and (2) orbital motion around the Sun, which produces yearly variations.

The seasons are caused by changes in the angle at which the Sun's rays strike Earth's surface and the changes in the length of daylight at each latitude. These seasonal changes are the result of the tilt of Earth's axis as it orbits the Sun.

''',

'''
16.5 Energy, Heat, and Temperature

Distinguish between heat and temperature. List and describe the three mechanisms

of heat transfer.

KEY TERMS: heat, temperature, conduction, convection, radiation, electromagnetic radiation, visible light, infrared, ultraviolet (UV)

⚫ Heat refers to the quantity of energy present in a material, whereas temperature refers to intensity, or the degree of "hotness."

The three mechanisms of heat transfer are (1) conduction, the transfer of heat through matter by molecular activity; (2) convection, the transfer of heat by the movement of a mass or substance from one place to another; and (3) radiation, the transfer of heat by electromagnetic waves.

• Electromagnetic radiation is energy emitted in the form of rays, or waves, called electromagnetic waves. All radiation is capable of transmitting energy through the vacuum of space. One of the most important differences between electromagnetic waves is their wavelengths, which range from very long for radio waves to very short gamma rays. Visible light is the only portion of the electromagnetic spectrum

for

we can see.

Some basic laws that relate to radiation are (1) all objects emit radiant energy; (2) hotter objects radiate more total energy than do colder objects;

(3) the hotter the radiating body, the shorter the wavelengths of maximum radiation; and (4) objects that are good absorbers of radiation are good

emitters as well.

''',

'''
16.6 Heating the Atmosphere

Sketch and label a diagram that shows the paths taken by incoming solar radiation. Summarize the greenhouse effect.

stergeom/A erit to stufount Isathey car

KEY TERMS: reflection, scattering, albedo, diffused light, selective absorbers, greenhouse effect

About 50 percent of the solar radiation that strikes the atmosphere reaches Earth's surface. About 30 percent is reflected back to space. The remaining 20 percent of incoming solar energy is absorbed by clouds and the atmosphere's gases. The fraction of radiation reflected by a surface is called the

albedo of that surface.

⚫ Radiant energy absorbed at Earth's surface is eventually radiated skyward. Because Earth has a much lower surface temperature than the Sun, its radiation is in the form of long-wave infrared radiation. Because atmospheric gases, primarily water vapor and carbon dioxide, are more efficient absorbers of long-wave radiation than of short-wave radiation, the atmosphere is heated from the ground up.

⚫ Greenhouse effect is the term for the selective absorption of Earth's long-wave radiation by water vapor and carbon dioxide, which results in Earth's average temperature being warmer than it would be otherwise.

''',

'''
16.7 For the Record: Air Temperature Data

Calculate five commonly used types of temperature data and interpret a map that depicts temperature data using isotherms. KEY TERMS: daily mean temperature, daily range, monthly mean, annual mean, annual temperature range, isotherm, temperature gradient • Daily mean temperature is an average of the daily maximum and daily minimum temperatures, whereas the daily range is the difference b daily maximum and daily minimum temperatures. The monthly mean is determined by averaging the daily means for a particular month. mean is an average of the 12 monthly means, whereas the annual temperature range is the difference between the highest and lowest mon Temperature distribution is shown on a map by using isotherms, which are lines of equal temperature. Temperature gradient is the amount temperature change per unit of distance. Closely spaced isotherms indicate a rapid rate of change.

''',

'''
16.8 Why Temperatures Vary: The Controls

of Temperature

Discuss the principal controls of temperature and use examples to describe their effects.

KEY TERMS: temperature control, specific heat, windward coast, leeward coast

Controls of temperature are factors that cause temperature to vary from place to place and from time to time. Latitude (Earth-Sun relationships) is one example. Ocean currents (discussed in Chapter 10) provide another example.

Unequal heating of land and water is a temperature control. Because land and water heat and cool differently, land areas experience greater temperature extremes than do water-dominated areas. Altitude is an easy-to-visualize control: The higher up you go, the colder it gets; therefore, mountains are cooler than adjacent lowlands.

Geographic position as a temperature control involves factors such as mountains acting as barriers to marine influence and a place being on a windward coast or a leeward coast.

''',

'''

16.9 World Distribution of Temperature

Interpret the patterns depicted on world maps of January and July temperatures.

On world maps showing January and July mean temperatures, isotherms generally trend east-west and show a decrease in temperature from the equator to the poles. When the two maps are compared, a latitudinal shifting of temperatures is seen. Bending isotherms reveal the locations of ocean

currents.

• Annual temperature range is small near the equator and increases with an increase in latitude. Outside the tropics, annual temperature range a increases as marine influence diminishes.

''',

'''
17.1 Water's Changes of State



KEY TERMS: calorie, latent heat, evaporation, condensation, sublimation, deposition ⚫ Water exists in all three states of matter (solid, liquid, or gas) at the temperatures and pressures near Earth's surface. The gaseous form of water is water vapor. The processes by which matter changes state are evaporation (liquid to gas), condensation (gas to liquid), melting (solid to liquid), freezing (liquid to solid), b sublimation (solid to gas), and deposition (gas to solid). During each change, latent (hidden, or stored) heat is either absorbed or released.

''',

'''



17.2 Humidity: Water Vapor in the Air

Write a generalization relating air temperature and the amount of water vapor needed to satu-

rate air.

KEY TERMS: humidity, saturation, vapor pressure, mixing ratio, relative humidity, dew-point tempera- ture (dew point), hygrometer, psychrometer

⚫ Humidity is the amount of water vapor in the air. The methods used to express humidity quantitatively include (1) mixing ratio, the mass of water vapor in a unit of air compared to the remaining mass of dry air; (2) relative humidity, the ratio of the air's actual water-vapor content to the amount of water vapor required for saturation at that temperature; and (3) dew-point temperature.

• Relative humidity can be changed in two ways: by adding or subtracting water vapor or by changing the air's temperature.

The dew-point temperature (or simply dew point) is the temperature to which a parcel of air must be cooled to reach saturation. Unlike relative humidity, dew-point temperature is a measure of the air's actual moisture content.

''',

'''

17.3 Adiabatic Temperature Changes and Cloud Formation

Describe adiabatic temperature changes and explain why the wet adiabatic rate of cooling is less than the dry adiabatic rate.

KEY TERMS: adiabatic temperature change, parcel, dry adiabatic rate, lifting condensation level (condensation level), sensible heat, wet adiabatic rate ⚫ Cooling of air as it rises and expands due to decreasing air pressure is the basic cloud-forming process. Temperature changes that result when air is compressed or when air expands are called adiabatic temperature changes.

⚫ Unsaturated air warms by compression and cools by expansion at the rather constant rate of 10°C per 1000 meters (5.5°F per 1000 feet) of altitude change, a quantity called the dry adiabatic rate. When air rises high enough, it cools sufficiently to cause condensation and form clouds. Air that continues to rise above the condensation level cools at the wet adiabatic rate, which varies from 5°C to 9°C per 1000 meters of ascent. The difference between the wet and dry adiabatic rates is due to the latent heat released by condensation, which slows the rate at which air cools as it ascends.

''',

'''
17.4 Processes That Lift Air

List and describe the four mechanisms that cause air to rise.

KEY TERMS: orographic lifting, rainshadow desert, front, frontal lifting (wedging), convergence, localized convective lifting (convective lifting)

⚫ Four mechanisms that cause air to rise are (1) orographic lifting, where air is forced to rise over elevated terrain such as a mountain barrier; (2) frontal lifting, where warmer, less-dense air is forced over cooler, denser air along a front; (3) convergence, a pileup of horizontal airflow resulting in an upward flow; and (4) localized convective lifting, where unequal surface heating causes localized pockets of air to rise because of their buoyancy.
''',

'''

17.5 The Critical Weathermaker: Atmospheric Stability

Describe how atmospheric stability is determined and compare conditional

instability with absolute instability.

KEY TERMS: stable air, unstable air, environmental lapse rate, absolute stability, abso- lute instability, conditional instability

Stable air resists vertical movement, whereas unstable air rises because of its buoyancy. The stability of a parcel of air is determined by the local environmental lapse rate (the temperature of the atmosphere at various heights). The three fundamental conditions of the atmosphere are (1) absolute stability, when the environmental lapse rate is less than the wet adiabatic rate; (2) absolute instability, when the environmental lapse rate is greater than the dry adiabatic rate; and (3) conditional instability, when moist air has an environmental lapse rate between the dry and wet adiabatic rates.

In general, when stable air is forced aloft, the associated clouds have little vertical thickness, and precipitation, if any, is light. In contrast, clouds associated with unstable air are towering and can produce heavy precipitation.

''',

'''

17.6 Condensation and Cloud Formation

Name and describe the 10 basic cloud types, based on form and height. Contrast nimbostratus and cumulonimbus clouds and their associated weather.

KEY TERMS: cloud condensation nuclei, hygroscopic nuclei, cloud, cirrus, stratus, cumulus, nimbus, high clouds, middle clouds, low clouds, clouds of vertical development, cirrocumulus, cirrostratus, altocumulus, altostratus, stratocumulus,

nimbostratus, cumulonimbus

. For water vapor to condense into cloud droplets, the air must reach saturation, and there must be a surface on which the water vapor can condense. The resulting cloud droplets are tiny and are held aloft by the slightest updrafts.

⚫ Clouds are classified on the basis of their form and height. The three basic cloud forms are cirrus (high, white, thin wisps or sheets), cumulus (globular, individual cloud masses), and stratus (sheets or layers).

Cloud heights can be high, with bases above 6000 meters (20,000 feet); middle, from 2000 (6500 feet) to 6000 meters; or low, below 2000 meters. Clouds of vertical development have bases in the low height range and extend upward into the middle or high range.
''',

'''
17.7 Types of Fog

Identify the basic types of fog and describe how each forms.

KEY TERMS: fog, radiation fog, advection fog, upslope fog, steam fog, frontal (precipitation) fog

Fog is a cloud with its base at or very near the ground. Fogs form when air is cooled below its dew point or when enough water vapor is added to the air to cause saturation.

Fogs formed by cooling include radiation fog, advection fog, and upslope fog. Fogs formed by the addition of water vapor are steam fog and frontal fog.

''',

'''

17.8 How Precipitation Forms

Describe the Bergeron process and explain how it differs from the collision-coalescence process.

KEY TERMS: Bergeron process, supercooled, ice (freezing) nuclei, collision-coalescence process

For precipitation to form, millions of cloud droplets must join together into drops that are large enough to reach the ground before evaporating. The two mechanisms that generate precipitation are the Bergeron process, which produces precipitation from cold clouds primarily in the middle and high latitudes, and the collision-coalescence process, which occurs in warm clouds and primarily in the tropics.

''',

'''
17.9 Forms of Precipitation

Describe the atmospheric conditions that produce sleet, freezing rain (glaze), and hail.

KEY TERMS: rain, drizzle, mist, snow, sleet, freezing rain (glaze), hail, rime

The two most common and familiar forms of precipitation are rain and snow. Rain can form in either warm or cold clouds. When it falls from cold clouds, it begins as snow that melts before reaching the ground.

Sleet consists of spherical to lumpy ice particles that form when raindrops freeze while falling through a thick layer of subfreezing air. Freezing

rain results when supercooled raindrops freeze upon contact with cold objects. Rime consists of delicate frostlike accumulations that form as supercooled fog droplets encounter objects and freeze on contact. Hail consists of hard, rounded pellets or irregular lumps of ice produced in towering cumulonimbus clouds, where frozen ice particles and supercooled water coexist.

''',

'''

17.10 Measuring Precipitation

List the advantages of using weather radar versus a standard rain gauge to measure precipitation.

KEY TERMS: standard rain gauge, tipping-bucket gauge, weather radar

Two instruments commonly used to measure rain are the standard rain gauge and the automated tipping-bucket gauge. The two most common

measurements of snow are depth and water equivalent.

a federn weather radar has given meteorologists an important tool to track storm systems and precipitation patterns, even when the storms are as far as

a few hundred kilometers away.

''',

'''
18.1 Understanding Air Pressure
Define air pressure and describe the instruments used to measure this weather element.
KEY TERMS: air pressure, mercury barometer, aneroid barometer, barograph
Air has weight: At sea level, it exerts a pressure of 1 kilogram per square centimeter (14.7 pounds per square inch), or 1 atmosphere.
with
Air pressure is the force exerted by the weight of air above. With increasing altitude, there is less air above to exert a force, and thus air pressure decreases altitude-rapidly at first and then much more slowly.
The unit meteorologists use to measure atmospheric pressure is the millibar. Standard sea-level pressure is expressed as 1013.2 millibars. Isobars are lines on a weather map that connect places of equal air pressures.
A mercury barometer measures air pressure using a column of mercury in a glass tube sealed at one end and inverted in a dish of mercury. It measures atmospheric pressure based on the height of the column of mercury in the barometer. Standard atmospheric pressure at sea level equals 29.92 inches of mercury. As air pressure increases, the mercury in the tube rises, and when air pressure decreases, so does the height of the column of mercury. Aneroid ("without liquid") barometers consist of partially evacuated metal chambers that compress as air pressure increases and expand as pressure decreases.
''',
'''
18.2 Factors Affecting Wind
Discuss the three forces that act on the atmosphere to either create or alter winds.
KEY TERMS: wind, isobar, pressure gradient force, Coriolis effect, geostrophic wind, jet stream Wind is controlled by a combination of (1) the pressure gradient force, (2) the Coriolis effect, and (3) friction. The pressure gradient force, which results from pressure differences, is the primary force that drives wind. It is depicted by the spacing of isobars on a map. Closely spaced isobars indicate a steep pressure gradient and strong winds; widely spaced isobars indicate a weak pressure gradient and light winds.
The Coriolis effect, which is due to Earth's rotation, produces deviation in the path of wind due to Earth's rotation (to the right in the Northern Hemisphere and to the left in the Southern Hemisphere). Friction, which significantly influences airflow near Earth's surface, is negligible above a height of a few kilometers.
Above a height of a few kilometers, the Coriolis effect is equal to and opposite the pressure gradient force, which results in geostrophic winds. Geostrophic winds follow a path parallel to the isobars, with velocities proportional to the pressure gradient force.
''',

'''

18.3 Highs and Lows
Contrast the weather associated with low-pressure centers (cyclones) and high-pressure centers (anticyclones).
KEY TERMS: cyclone (low), anticyclone (high), convergence, divergence, pressure (barometric) tendency The two types of pressure centers are (1) cyclones, or lows (centers of low pressure), and (2) anticyclones, or highs (centers of high pressure). In the Northern Hemisphere, winds around a low (cyclone) are counterclockwise and inward. Around a high (anticyclone), they are clockwise and outward. In the Southern Hemisphere, the Coriolis effect causes winds to be clockwise around a low and counterclockwise around a high.
• Because air rises and cools adiabatically in a low-pressure center, cloudy conditions and precipitation are often associated with their passage. In a high-pressure center, descending air is compressed and warmed; therefore, cloud formation and precipitation are unlikely in an anticyclone, and "fair" weather is usually expected.

''',

'''
18.4 General Circulation of the Atmosphere
Summarize Earth's idealized global circulation. Describe how continents and seasonal temperature changes complicate the idealized patter
KEY TERMS: equatorial low, intertropical convergence zone (ITCZ), subtropical high, trade winds, westerlies, polar easterlies, subpolar low, polar from olar
high, monsoon
• If Earth's surface were uniform, four belts of pressure oriented east to west would exist in each bemisphere. Beginning at the equator, the four belts would be the (1) equatorial low, also referred to as the intertropical convergence zone (ITCZ), (2) subtropical high at about 25° to 35° on either side of the equator, (3) subpolar low, situated at about 50° to 60° latitude, and (4) polar high, near Earth's poles.
Particularly in the Northern Hemisphere, large seasonal temperature differences over continents disrupt the idealized, or zonal, global patterns of pressure and wind. In winter, large, cold landmasses develop a seasonal high-pressure system from which surface airflow is directed off the land. In summer, landmasses are heated, and a low-pressure system develops over them, which permits air to flow onto the land. These seasonal changes in wind direction are known as
monsoons.
In the middle latitudes, between 30° and 60° latitude, the general west-to-east flow of the westerlies is interrupted by the migration of cyclones and anticyclones. The paths taken by these cyclonic and anticyclonic systems is closely correlated to upper-level airflow and the polar jet stream. The average position of the polar jet stream, and hence the paths followed by cyclones, migrates southward with the approach of winter and northward as summer nears.
''',
'''
18.5 Local Winds
List three types of local winds and describe their formation.
KEY TERMS: local wind, sea breeze, land breeze, valley breeze, mountain breeze, chinook, Santa Ana
Local winds are small-scale winds produced by a locally generated pressure gradient. Sea and land breezes form along coasts and are brought about by temperature contrasts between land and water. Valley and mountain breezes occur in mountainous areas where the air along slopes heats differently than does the air at the same elevation over the valley floor. Chinook and Santa Ana winds are warm, dry winds created when air descends the leeward side of a mountain and warms by compression.
''',

'''
18.6 Measuring Wind
Describe the instruments used to measure wind. Explain how wind direc- tion is expressed using compass directions.
KEY TERMS: wind vane, cup anemometer, prevailing wind
The two basic wind measurements are direction and speed. Winds are always labeled by the direction from which they blow. Wind direction is measured with a wind vane, and wind speed is measured using a cup anemometer.

''',


'''

18.7 El Niño, La Niña, and the Southern Oscillation
Describe the Southern Oscillation and its relationship to El Niño and La Niña. List the climate impacts of El Niño and La Niña on North America.
KEY TERMS: El Niño, La Niña, Southern Oscillation
El Niño refers to episodes of ocean warming in the eastern Pacific along the coasts of Ecuador and Peru. It is associated with weak trade winds, a strong eastward-moving equatorial countercurrent, a weakened Peru Current, and diminished upwelling along the western margin of South America.
A La Niña event is associated with colder-than-average surface temperatures in the eastern Pacific. La Niña is linked to strong trade winds, a strong westward-moving equatorial current, and a strong Peru Current with significant coastal upwelling
El Niño and La Niña events are part of the global circulation and are related to a seesaw pattern of atmospheric pressure between the eastern and western Pacific called the Southern Oscillation. El Niño and La Niña events influence weather on both sides of the tropical Pacific Ocean as well as weather in the United States.

''',

'''
18.8 Global Distribution of Precipitation
Discuss the major factors that influence the global distribution of precipitation.
The general features of the global distribution of precipitation can be explained by global winds and pressure systems. In general, regions influenced by high pressure, with its associated subsidence and divergent winds, experience dry conditions. Regions under the influence of low pressure, with its converging winds and ascending air, receive ample precipitation.
Air temperature, the distribution of continents and oceans, and the location of mountains also influence the distribution of precipitation.
''',

'''


19.1 Air Masses
Discuss air masses, their classification, and associated weather.
KEY TERMS: air mass, air-mass weather, source region, polar (P) air mass, arctic (A) air mass, tropical (1) air mass, continental (c) air mass, maritime (m) air mass, lake-effect snow, nor'easter
An air mass is a large body of air, usually 1600 kilometers (1000 miles) or more across, that is characterized by a sameness of temperature and moisture at any given altitude. When this air moves out of its region of origin, called the source region, it carries these temperatures and moisture conditions elsewhere, perhaps eventually affecting a large portion of a continent.
Air masses are classified according to the nature of the surface in the source region and the latitude of the source region. Continental (c) designates an air mass of land origin, with the air likely to be dry; at maritime (m) air mass originates over water and, therefore, will be relatively humid. Polar (P) and arctic (A) air masses originate in high
latitudes and are cold. Tropical (T) air masses form in low latitudes and are warm. According to this classification scheme, the four main types of air masses are continental polar (cP), continental tropical (cT), maritime polar (mP), and maritime tropical (mT).
Continental polar (CP) and maritime tropical (mT) air masses influence the weather of North America most, especially east of the Rocky Mountains. Maritime tropical
air is the source of much, if not most, of the precipitation received in the eastern two- thirds of the United States. ? Identify the source region associated with each letter on this map. One letter is not associated with a source region. Which one is it?

''',

'''


19.2 Fronts
Compare and contrast typical weather associated with a warm front and a cold front. Describe an occluded front and a stationary front.
KEY TERMS: front, overrunning, warm front, cold front, stationary front, occluded front
Fronts are boundary surfaces that separate air masses of different densities, one usually warmer and more humid than the other. As one air mass moves into another, the warmer, less dense air mass is forced aloft in a process called overruming
Along a warm front, a warm air mass overrides a retreating mass of cooler air. As the warm air ascends, it cools adiabatically to produce clouds and, frequently, light to moderate precipitation over a large area
A cold front forms where cold air is actively advancing into a region occupied by warmer air. Cold fronts are about twice as steep as and move more rapidly than warm fronts. Because of these two differences, precipitation along a cold front is generally more intense and of shorter duration than precipitation associated with a warm front.
''',
'''
19.3 Midlatitude Cyclones
Summarize the weather associated with the passage of a mature mid- latitude cyclone. Describe how airflow aloft is related to cyclones and anticyclones at the surface.
KEY TERMS: midlatitude (middle-latitude) cyclone
The primary weather producers in the middle latitudes are large centers of low pressure that generally travel from west to east, called midlatitude cyclones. These bearers of stormy weather, which last from a few days to a week, have a counterclockwise circulation pattern in the Northern Hemisphere, with an inward flow of air toward their centers.
Most midlatitude cyclones have a cold front and frequently a warm front extending from the central area of low pressure. Convergence and forceful lifting along the fronts initiate cloud development and frequently cause precipitation. The particular weather experienced by an area depends on the path of the cyclone.
Guided by west-to-east-moving jet streams, cyclones generally move eastward across the United States. Airflow aloft (divergence and convergence) plays an important role in maintaining cyclonic and anticyclonic circulation. In cyclones, divergence aloft supports the inward flow at the surface.
''',

'''
19.4 Thunderstorms
List the basic requirements for thunderstorm formation and locate places on a map that exhibit frequent thunderstorm activity. Describe the stages in the development of a thunderstorm. KEY TERMS: thunderstorm
Thunderstorms are caused by the upward movement of warm, moist, unstable air. They are associated with cumulonimbus clouds that generate heavy rainfall, lightning, thunder, and occasionally hail and tornadoes.
Air-mass thunderstorms frequently occur in maritime tropical (mT) air during spring and summer in the middle latitudes. Generally, three stages are involved in the development of these storms: the cumulus stage, mature stage, and dissipating stage.
''',

'''
19.5 Tornadoes
Summarize the atmospheric conditions and locations that are favorable to the formation of tornadoes. Discuss tornado destruction and tornado forecasting.
KEY TERMS: tornado, mesocyclone, wind shear, Enhanced Fujita intensity scale (EF-scale), tornado watch, tornado warning, Doppler radar
A tornado is a violent windstorm that takes the form of a rotating column of air called a vortex that extends downward from a cumulonimbus cloud. Many strong tornadoes contain smaller internal vortices. Because of the tremendous pressure gradient associated with a strong tornado, maximum winds can approach 480 kilometers (300 miles) per hour.
⚫ Tornadoes are most often spawned along the cold front of a midlatitude cyclone or in association with a supercell thunderstorm. Tornadoes also form in association with tropical cyclones (hurricanes). In the United States, April through June is the period of greatest tornado activity, but tornadoes can occur during any month of the year.
Most tornado damage is caused by the tremendously strong winds. One commonly used guide to tornado intensity is the Enhanced Fujita intensity scale (EF-scale). A rating on the EF-scale is determined by assessing damage produced by the storm.
Because severe thunderstorms and tornadoes are small and short-lived phenomena, they are among the most difficult weather features to forecast precisely. When weather conditions favor the formation of tornadoes, a tornado watch is issued. The National Weather Service issues a tornado warning when a tornado has been sighted in an area or is indicated on Doppler radar.

''',

'''


19.6 Hurricanes
Identify areas of hurricane formation on a world map and discuss the conditions that promote hurricane formation. List the three broad cat- egories of hurricane destruction.
KEY TERMS: hurricane, eye wall, eye, tropical depression, tropical storm, Saf- fir-Simpson hurricane scale, storm surge
Hurricanes, the greatest storms on Earth, are tropical cyclones with wind speeds in excess of 119 kilometers (74 miles) per hour. These complex tropical disturbances develop over tropical ocean waters and are fueled by the latent heat that is liberated when huge quantities of water vapor condense.
.Hurricanes form most often in late summer, when ocean-surface temperatures reach 27°C (80°F) or higher and thus are able to provide the necessary heat and moisture to the air. Hurricanes diminish in intensity when they move over cool ocean water that cannot supply adequate heat and moisture, move onto land, or reach a location where large-scale flow aloft is unfavorable.
The Saffir-Simpson scale ranks the relative intensities of hurricanes. A 5 on the scale represents the strongest storm possible, and a 1 indicates
the lowest severity. Damage caused by hurricanes is divided into three categories: (1) storm surge, (2) wind damage, and (3) heavy rains and inland flooding,

''',

'''
20.1 The Climate System
List the five parts of the climate system and provide examples of each.
KEY TERMS: climate system, cryosphere
Climate is the aggregate of weather conditions for a place or region over a long period of time.
Earth's climate system involves the exchanges of energy and moisture that occur among the atmosphere, hydrosphere, solid Earth, biosphere, and cryosphere (the ice and snow that exist at Earth's surface).
''',
'''
20.2 World Climates
Explain why classification is a necessary process when studying world climates. Discuss the criteria used in the Köppen system of climate classification.
KEY TERM: Köppen classification
Climate classification brings order to large quantities of information, which aids comprehension and understanding and facilitates analysis and explanation.
The most important elements in climate descriptions are temperature and precipitation because they have the greatest influence on people and their activities, and they also have an important impact on the distribution of vegetation and the development of soils.
''',

'''
20.3 Humid Tropical (A) Climates
Compare the two broad categories of tropical climates.
KEY TERMS: tropical rain forest, tropical wet and dry,
savanna
Humid tropical (A) climates are winterless, with all months having a mean temperature above 18°C (64°F).
Wet tropical climates (Af and Am), which lie near the equator, have constantly high temperatures and enough rainfall to support the most luxuriant vegetation (tropical rain forest) found in any climatic realm..
•Tropical wet and dry climates (Aw) are found
to
poleward of the wet tropics and equatorward of the subtropical deserts, where the rain forest gives way the tropical grasslands and scattered drought-tolerant trees of the savanna. The most distinctive feature of this climate is the seasonal character of the rainfall. ? When does the rainy season occur in a tropical wet and dry climate: winter or summer? Explain.
An early attempt at climate classification by the Greeks divided each hemisphere into three zones: torrid, temperate, and frigid. Many climate classifications have been devised, with the value of each determined by its intended use.
The Köppen classification, which uses mean monthly and annual values of temperature and precipitation, is a widely used system. The boundaries Köppen chose were largely based on the limits of certain plant associations. The Köppen classification uses five principal climate groups, each with subdivisions. Four of the climate groups-A, C, D, and E-are defined on the basis of temperature characteristics, and the fifth, the B group, has precipitation as its primary criterion.

''',

'''
20.4 Dry (B) Climates
Contrast low-latitude dry climates and middle-latitude dry climates.
KEY TERMS: arid (desert), semiarid (steppe)
Dry (B) climates, in which the yearly precipitation is less than the potential loss of water by evaporation, are subdivided into two types: arid or desert (BW) and semiarid or steppe (BS).
Differences between desert and steppe are primarily a matter of degree, with semiarid being a marginal and more humid variant of arid. Low-latitude deserts and steppes coincide with the clear skies caused by subsiding air beneath the subtropical high-pressure belts.
Middle-latitude deserts and steppes exist principally because of their position in the deep interiors of large landmasses far removed from the ocean. Because many middle-latitude deserts occupy sites on the leeward sides of mountains, they can also be classified as rainshadow deserts. ? This photo was taken in Nevada's Great Basin Desert, looking west toward the Sierra Nevada. What is the basic cause of the arid conditions in this region?
''',

'''
20.5 Humid Middle-Latitude Climates (C and D Climates)
Distinguish among five different humid middle-latitude climates.
KEY TERMS: humid subtropical climate, marine west coast climate, dry-summer subtropical climate, humid continental climate, subarctic climate, taiga • Middle-latitude climates with mild winters (C. climates) occur where the average temperature of the coldest month is below 18°C (64°F) but above -3°C (27 F) Three C climate subgroups exist
• Humid subtropical climates (Cfa) are located on the eastern sides of the continents, in the 25° to 40° latitude range. Summer weather is hot and sultry, and winters are mild. In North America, the marine west coast climate (Cfb. Cfe) extends from near the U.S.-Canada border northward as a narrow belt into southern Alaska. The prevalence of maritime air masses means that mild winters and cool summers are the rule. Dry-summer subtropical climates (Csa, Csb) are typically located along the west sides of continents between latitudes 30° and 45°. In summer, the regions are dominated by stable, dry conditions associated with the oceanic subtropical highs. In winter, they are within range of the cyclonic storms of the polar front. Humid middle-latitude climates with severe winters (D climates) are land-controlled climates that are absent in the Southern Hemisphere. The average temperature of the coldest month is -3°C (27°F) or below, and the warmest monthly mean exceeds 10°C (50°F).
⚫ Humid continental climates (Dfa, Dfb, Dwa, Dwb) are confined to the eastern portions of North America and Eurasia in the latitude range between approximately 40 and 50° north latitude. Both winter and summer temperatures are relatively severe. Precipitation is generally greater in summer than in winter. Subarctic climates (Dfc, Dfd, Dwc, Dwd) are situated north of the humid continental climates and south of the polar tundras. The outstanding feature of subarctic climates is the dominance of winter, summers are short but remarkably warm. The highest annual temperature ranges on Earth occur here.
''',
'''
20.6 Polar (E) Climates
Contrast ice cap and tundra climates.
KEY TERMS: polar climate, tundra climate, ice cap climate
Polar climates (ET, EF) are those in which the mean temperature of the warmest month is below 10°C (50°F). Annual temperature ranges are extreme, with the lowest annual means on the planet. Although polar climates are classified as humid, precipitation is generally meager, with many nonmarine stations receiving less than 25 centimeters (10 inches) annually. Two types of polar climates are recognized. The tundra climate (ET) is found almost exclusively in the Northern Hemisphere. The 10°C (50°F) summer isotherm represents its equatorward limit. It is a treeless region of grasses, sedges, mosses, and lichens with permanently frozen subsoil, called permafrost. The ice cap climate (EF) does not have a single monthly mean above 0°C (32°F). Consequently, the growth of vegetation is prohibited, and the landscape is one of permanent ice and snow. The ice sheets of Greenland and Antarctica are important examples.
''',
'''
20.7 Highland Climates
Summarize the characteristics associated with highland climates.
KEY TERM: highland climate
Highland climates are characterized by a great diversity of climatic conditions over a small area. Although the best-known climatic effect of increased altitude is lower temperatures, greater precipitation due to orographic lifting is also common. Variety and changeability best. describe highland climates. Because atmospheric conditions fluctuate with altitude and exposure to the Sun's rays, a nearly limitless variety of local climates occur in mountainous regions.
''',
'''
20.8 Human Impact on Global Climate
Summarize the nature and cause of the atmosphere's changing composition since about 1750. Describe the climate's response. KEY TERMS: aerosols, black carbon
. Humans have been modifying the environment for thousands of years. By burning vegetation and allowing domestic animals to overgraze the land. people have modified such important climatic factors as surface albedo, evaporation rates, and surface winds.
Human activities produce climate change in large part by releasing carbon dioxide (CO2) and trace gases. Humans release CO2 when they cut down forests and when they burn fossil fuels such as coal, oil, and natural gas. A steady rise in atmospheric CO, levels has been documented at Mauna Loa, Hawaii, and other locations around the world.
More than half of the carbon released by humans is absorbed by new plant matter or dissolved in the oceans. About 45 percent remains in the atmosphere, where it can influence climate for decades. Air bubbles trapped in glacial ice reveal that there is currently about 30 percent more CO2 than the atmosphere has contained in the past 800,000 years.
As a result of the extra heat retained by added CO2, Earth's atmosphere has warmed by about 0.8°C (1.4°F) in the past 100 years, most of it since 1980. Temperatures are projected to increase by another 2°C to 4.5°C (3.6°F to 8.1°F) in the future.
Trace gases such as methane, nitrous oxide, and CFCs also play a significant role in increasing global temperature.
Aerosols-tiny liquid and solid particles suspended in the air-are produced by human and natural sources and affect global climate. Many aerosols reflect a portion of incoming solar radiation back to space and therefore have a cooling effect. Some aerosols, called black carbon, absorb incoming solar radiation and warm the atmosphere. When black carbon is deposited on snow and ice, it reduces surface albedo and increases the amount of light absorbed at the surface.
''',
'''
20.9 Climate-Feedback Mechanisms
Contrast positive- and negative-feedback mechanisms and provide examples of each.
KEY TERMS: climate-feedback mechanism, positive-feedback mechanism, negative-feedback mechanism A change in one part of the climate system may trigger changes in other parts of the climate system that amplify or diminish the initial effect. These climate-feedback mechanisms are called positive- feedback mechanisms if they reinforce the initial change and negative-feedback mechanisms if they counteract the initial effect.
The melting of sea ice due to global warming (decreasing albedo and hence increasing the initial effect of warming) is one example of a positive-feedback mechanism. The production of more clouds (blotting out incoming solar radiation, leading to cooling) is an example of a negative-feedback
mechanism.
Computer models of climate give scientists a tool for testing hypotheses about climate change. Although these models are far simpler than the real climate system, they are useful tools for predicting the future climate.
''',

'''
20.10 Some Possible Consequences of Global Warming
Summarize some of the possible consequences of global warming.
In the future, Earth's surface temperature is likely to continue to rise. The temperature increase will likely be greatest in the polar regions and least in the tropics. Some areas will get drier, and other areas will get wetter.
Sea level is predicted to rise for several reasons, including the melting of glacial ice and thermal expansion (a given mass of seawater takes up more volume when it is warm than when it is cool). Low-lying, gently sloped coastal areas (which are often highly populated) are most at risk. The extent and thickness of sea ice in the Arctic have been declining since satellite observations began in 1979.
Because of the warming of the Arctic, permafrost is melting, releasing CO2 and methane to the atmosphere in a positive-feedback loop. Because the climate system is complicated, dynamic, and imperfectly understood, it could produce sudden, unexpected changes with little warning.
''',

'''

21.1 Ancient Astronomy
Explain the geocentric view of the solar system and describe how it differs from the heliocentric view.
KEY TERMS: geocentric, heliocentric, Ptolemaic system, retrograde motion
The early Greeks held a geocentric ("Earth-centered") view of the universe, in which Earth is a motionless sphere at the center of the universe, orbited by the Moon, the Sun, and the planets that were known at the time-Mercury, Venus, Mars, Jupiter, and Saturn.
The early Greeks believed that the stars traveled daily around Earth on a transparent, hollow celestial sphere. In 141 C.E. Claudius Ptolemy it to not documented this geocentric view, now called the Ptolemaic system, which became the dominant view of the solar system for over 15 centuries.

''',

'''


21.2 The Birth of Modern Astronomy
List and describe the contributions to modern astronomy of Nicolaus Copernicus, Tycho Brahe, Johannes Kepler, Galileo Galilei, and Isaac
Newton.
KEY TERMS: astronomical unit (AU), inertia, law of universal gravitation Modern astronomy evolved during the 1500s and 1600s, facilitated by scientists going beyond merely describing what is observed to explaining why the universe behaves as it does,
Nicolaus Copernicus (1473-1543) proposed that the Sun, rather than Earth, is the center of the solar system, although he perpetuated the erroneous view that orbits must be circular. His Sun-centered view was rejected by the establishment of his day.
Tycho Brahe's (1546-1601) observations of the planets were far more precise than any made previously and are his legacy to astronomy. Johannes Kepler (1571-1630) used Tycho Brahe's observations to usher in a new astronomy with the formulation of his three laws of planetary
motion.
⚫ After constructing his own telescope, Galileo Galilei (1564-1642) made many important discoveries that supported the Copernican view of a Sun- centered solar system. This included discovering moons around Jupiter, thus proving that Earth was not the center of all planetary motion. Sir Isaac Newton (1642-1727) demonstrated that the orbit of a planet is a result of the planet's inertia (its tendency to move in a straight line) and the Sun's gravitational attraction, which bends the planet's path into an elliptical orbit.

''',

'''
21.3 Patterns in the Night Sky
Describe how constellations are used in modern astronomy.
KEY TERMS: constellation, celestial sphere, direction, altitude, angular size (angular diameter), angular distance
As early as 5000 years ago, people began naming the configurations of stars, called constellations, in honor of mythological characters or great heroes. Today, 88 constellations are recognized that divide the sky into regions, just as state boundaries divide the United States.
Although we realize that the stars are not fixed to a celestial sphere that surrounds Earth, we use this convenient idea to describe the locations of the stars and other celestial objects.
The location of any object in the sky can be described by its direction along the horizon and its altitude above the horizon. The direction is usually measured in degrees clockwise from due north. The apparent size of a celestial object can be described as the angle of view its spans (angular size); the same measure is used for apparent distances.
''',

'''
21.4 The Motions of Earth
Describe the two primary motions of Earth and explain the difference between a solar day and a sidereal day.
KEY TERMS: rotation, orbit (revolution), mean solar day, sidereal day, perihe- lion, aphelion, ecliptic, plane of the ecliptic
The most basic motions of Earth are its daily rotation on its axis (spin) and its yearly orbit, or revolution, around the Sun.
Earth's rotation can be measured in two ways, making two kinds of days. The mean solar day is the time interval from one noon (the time of day when the Sun is highest in the sky) to the next, which averages about
''',

'''
21.5 Motions of the Earth-Moon System
24 hours. In contrast, the sidereal day is the time it takes for Earth to make one complete rotation with respect to a star other than the Sun, a period of 23 hours, 56 minutes, and 4 seconds.
Earth travels around the Sun in an elliptical orbit at an average distance from the Sun of 150 million kilometers (93 million miles). At perihelion (closest to the Sun), which occurs in January, Earth is 147 million kilometers (91.5 million miles) from the Sun. At aphelion (farthest from the Sun), which occurs in July, Earth is 152 million kilometers (94.5 million miles) distant. The imaginary plane that connects Earth's orbit with the celestial sphere is called the plane of the ecliptic.
Sketch the changing configuration of the Earth-Moon system that produces the regular cycle we call the phases of the Moon.
KEY TERMS: synodic month, sidereal month, phases of the Moon
One of the first astronomical phenomena to be understood was the regular cycle of the phases of the Moon. The phases of the Moon are a result of the motion of the Moon around Earth and the portion of the bright side of the Moon that is visible to an
observer on Earth.
The cycle of the Moon through its phases requires 291⁄2 days, a time span called the synodic month. However, the true period of the Moon's orbit around Earth is 27/3 days and is known as the sidereal month. The difference of nearly 2 days is due to the fact that as the Moon orbits Earth, the Earth-Moon system also advances in its orbit around
the Sun.
NASA's Goddard Space Flight Center
''',

'''


21.6 Eclipses of the Sun and Moon
Sketch the configuration of the Earth-Moon-Sun system that produces a lunar eclipse and the configuration that produces a solar eclipse.
KEY TERMS: solar eclipse, lunar eclipse
• In addition to understanding the Moon's phases, the early Greeks also realized that eclipses are simply shadow effects. When the Moon passes directly between Earth and the Sun, which can occur only during the new-Moon phase, it casts a dark shadow on Earth, producing a solar eclipse.
A lunar eclipse takes place when the Moon moves within the shadow of Earth during the full-Moon phase.
• Because the Moon's orbit is inclined about 5 degrees to the plane that contains Earth and the Sun (the plane of the ecliptic), during most new- and full-Moon phases, no eclipse occurs. Only if a new- or full-Moon phase occurs as the Moon crosses the plane of the ecliptic can an eclipse take place. The usual number of eclipses is four per year.

''',

'''


22.1 Our Solar System: An Overview
Describe the formation of the solar system according to the nebular theory. Compare and contrast the terrestrial and Jovian planets.
KEY TERMS: nebular theory, solar nebula, planetesimal, protoplanet, terrestrial (Earth-like) planet, Jovian (Jupiter-like) planet, escape velocity, impact crater Our Sun is the most massive body in our solar system, which includes planets, dwarf planets, moons, and other small bodies. The planets orbit in the same direction and at speeds proportional to their distance from the Sun, with inner planets moving faster and outer planets moving more slowly. The solar system began as a solar nebula before condensing due to gravity. While most of the matter ended up in the Sun, some material formed a thick disk around the early Sun and later clumped together into larger and larger bodies. Planetesimals collided to form protoplanets, and protoplanets grew into planets.
The four terrestrial planets are enriched in rocky and metallic materials, whereas the Jovian planets have a higher proportion of ice and gas. The terrestrial planets are relatively dense, with thin atmospheres, while the Jovian planets are less dense and have thick atmospheres.oyo Smaller planets have less gravity to retain gases in their atmosphere. Lightweight gases such as hydrogen and helium more easily reach escape velocity, so the atmospheres of the terrestrial planets tend to be enriched in heavier gases, such as water vapor, carbon dioxide, and nitrogen.

''',

'''

22.2 Earth's Moon: A Chip Off the Old Block
List and describe the major features of Earth's Moon and explain how maria basins were formed.
KEY TERMS: maria, lunar highlands, lunar regolith
The Moon has a composition that is approximately the same as that of Earth's mantle. The Moon likely formed from a collision between a Mars-sized protoplanet and the early Earth.
The lunar surface is dominated by light-colored lunar highlands (or terrae) and darker lowlands called maria, the latter formed primarily from flood basalts. Both terrae and maria are partially covered by lunar regolith produced by micrometeorite bombardment.
''',

'''
22.3 Terrestrial Planets
Outline the principal characteristics of Mercury, Venus, and Mars. Describe their similarities to and differences from Earth.
Mercury has a very thin atmosphere and a weak magnetic field. Like Earth's moon, Mercury has both heavily cratered areas and smooth plains; the smooth plains are similar to lunar maria.
• Venus has a very dense atmosphere, dominated by carbon dioxide. The resulting extreme greenhouse effect produces surface temperatures around 450°C (900°F). The topography of Venus has been resurfaced by active volcanism.
Mars has about 1 percent as much atmosphere as Earth, so it is
relatively cold (-140°C to 20°C [-220°F to 68°F]). Mars appears to be the closest planetary analog to Earth, showing surface evidence of rifting, volcanism, and
modification by flowing water. Volcanoes on Mars are much bigger than volcanoes on Earth because of the lack of plate motion on Mars.
''',

'''
22.4 Jovian Planets
Summarize and compare the features of Jupiter, Saturn, Uranus, and Neptune, including their ring systems.
KEY TERMS: cryovolcanism
• Jupiter's mass is several times larger than the combined mass of everything else in the solar system except for the Sun. Convective flow, combined with its three cloud layers, produces its characteristic banded appearance. Persistent, giant rotating storms exist between these bands. Many moons orbit Jupiter, including Io, which shows active volcanism, and Europa, which is believed to have a liquid ocean under its icy shell. Saturn, like Jupiter, is big, gaseous, and endowed with dozens of moons. Some moons show evidence of tectonics, while Titan has its own atmosphere. Saturn's well-developed rings are made of many particles of water ice and rocky debris.
• Uranus, like its "twin" Neptune, has a blue atmosphere dominated by methane, and its diameter is about four times greater than Earth's.
Uranus rotates sideways relative to the plane of the solar system. It has a relatively thin ring system and at least five moons.
Neptune has an active atmosphere, with fierce wind speeds and
giant storms. It has 1 large moon, Triton, which shows evidence of cryovolcanism, as well as 13 smaller moons and a ring system.

''',

'''
22.5 Small Solar System Bodies
List and describe the principal characteristics of the small bodies that inhabit the solar system.
KEY TERMS: small solar system body, dwarf planet, asteroid, asteroid belt, comet, nucleus, coma, Kuiper belt, Oort cloud, meteor, meteoroid, meteor shower, meteorite
• Small solar system bodies include rocky asteroids and icy comets. Both are basically scraps left over from the formation of the solar system or fragments from later impacts.
. Most asteroids are concentrated in a wide belt between the orbits of Mars and Jupiter. Some are rocky, some are metallic, and some are basically "piles of rubble," loosely held together by their own weak gravity. • Comets are dominated by ices, "dirtied" by rocky material and dust. Most originate in either the Kuiper belt beyond Neptune or the Oort cloud. When a comet's orbit brings it through the inner solar system, solar radiation causes its ices to vaporize, generating the coma and its characteristic "tail."
. A meteoroid is a small rocky or metallic body traveling through space. When it enters Earth's atmosphere, it flares briefly as a meteor before either burning up or striking Earth's surface to become a meteorite. Asteroids and material lost from comets as they travel through the inner solar system are the most common sources of meteoroids.
• Bodies massive enough to have a spherical shape but not so massive as to have cleared their orbits of debris are classified as dwarf planets. They include the rocky asteroid Ceres as well as the icy worlds Pluto and Eris, which are located in the Kuiper belt.
''',

'''


23.1 Light: Messenger from Space
Compare and contrast the wave properties of light with the particle properties of light.
KEY TERMS: electromagnetic radiation, wavelength, frequency, photon, radiation pressure
⚫ Electromagnetic radiation occurs in a spectrum of wavelengths. From short to long, these are gamma rays, x-rays, ultraviolet light, visible light, infrared radiation (heat), and radio waves. The shorter the wavelength, the more energy the radiation carries.
⚫ Electromagnetic radiation can be described as behaving either like waves or like a stream of particles known as photons. Both descriptions are valid; they apply in different circumstances.
''',

'''
23.2 What Can We Learn from Light?
Explain how the three types of spectra are generated and what they tell astronomers about the radiating object that produced them.
KEY TERMS: spectroscopy, spectroscope, continuous spectrum, emission line spectrum, absorption line spectrum, intensity, Doppler effect, redshift
• Spectroscopy is the study of the interaction of matter and light.
The three types of spectra are called (1) continuous spectra, (2) absorption line spectra, and (3) emission line spectra. A continuous spectrum provides information about the radiating object's energy output and surface temperature. Absorption and emission spectra provide information about the object's composition. Emission spectra are produced by incandescent (glowing) gases; absorption spectra are produced when light passes through a gas. The spectra of most stars are absorption spectra.
⚫ Spectroscopy can also be used to determine the motion of an object by measuring the Doppler effect.
''',

'''
23.3 Collecting Light Using Optical Telescopes
Describe the two properties that make telescopes with large mirrors more useful than those with small mirrors.
KEY TERMS: refracting telescope, reflecting telescope, light-gathering area, resolution, turbulence, active optics, interferometer, adaptive optics
There are two types of optical telescopes: (1) the refracting telescope, which uses a lens to bend or refract light, and (2) the reflecting telescope, which uses a curved mirror to focus light. Most large modern telescopes are reflectors.
Telescopes simply collect light. When analyzed, the collected light can be used to determine the temperature, composition, relative motion, and distance to a celestial object.
Historically, astronomers relied on their eyes to collect light. Then photographic film was developed. Now, light is collected using charge-coupled devices (CCDs).
Advances such as active optics, interferometry, and adaptive optics have great improved the resolution of images acquired by modern telescopes. Still, Earth-bound optical telescopes can only "view" a tiny portion of the electromagnetic spectrum.
''',

'''
23.4 Radio- and Space-Based Astronomy
List the advantages of radio-wave and orbiting observatories over ground-based optical telescopes.
KEY TERMS: radio telescope, very-long-baseline interferometer (VLBI)
• Much of the radiation produced by celestial objects cannot penetrate our atmosphere, so other types of observatories have been developed.
• The detection of radio waves is accomplished by "big dishes" known as radio telescopes. A parabolic-shaped dish, often made of wire mesh, operates in a manner similar to the mirror of a reflecting telescope.
• Orbiting observatories, like the Hubble Space Telescope, circumvent many of the problems caused by Earth's atmosphere and have led to numerous significant discoveries in astronomy.
''',

'''
23.5 Our Star: The Sun
Sketch the Sun's structure and describe each of its major layers. Summarize the process called the proton-proton chain reaction.
KEY TERMS: photosphere, granule, chromosphere, corona, solar wind, core, radiation zone, convection zone, nuclear fusion, proton-proton chain reaction The photosphere (visible surface) of the Sun radiates most of the light we see. Unlike most surfaces to which we are accustomed, it consists of a layer of incandescent gas less than 500 kilometers (300 miles) thick and has a grainy texture consisting of numerous relatively small, bright markings called granules.
Just above the photosphere lies the chromosphere, a relatively thin layer of hot incandescent gases a few thousand kilometers thick.
At the uppermost edge of the solar atmosphere, called the corona, ionized gases escape the gravitational pull of the Sun and stream toward Earth at high speeds, producing the solar wind.
Deep in the solar interior, a type of nuclear fusion called the proton-proton chain reaction converts four hydrogen nuclei into the nucleus of a helium atom. During the reaction, some of the matter is converted into the energy that the Sun ultimately radiates into space.
''',

'''
23.6 The Active Sun
List and describe four types of solar storms that occur on the Sun.
KEY TERMS: sunspot, prominence, solar flare, coronal mass ejection, aurora
• Sunspots are the most common type of solar activity. The number of sunspots observable on the solar disk varies in an 11-year cycle.
• Prominences, huge cloudlike structures best observed when they are on the Sun's edge, or limb, are produced by ionized chromospheric gases trapped by magnetic fields that extend from regions of intense solar activity.
One of the most explosive events associated with sunspots is large solar flares, which are brief outbursts that release enormous quantities of energy. Solar flares and other solar storms can sometimes produce coronal mass ejections, which consist of radiation and fast-moving particles that cause the solar wind to intensify. If the ejected particles reach Earth, they can disrupt radio communication and produce the auroras, also called the Northern and Southern Lights.

''',

'''


24.1 Classifying Stars
Explain the criteria used to classify stars and define main-sequence star.
KEY TERMS: apparent magnitude, absolute magnitude (luminosity), light-year, Hertzsprung- Russell diagram (H-R diagram), main-sequence star, giant, red giant, supergiant, white dwarf Hertzsprung-Russell diagrams are constructed by plotting the absolute magnitudes (luminosity) and temperatures of stars on graphs.
Stars are positioned within H-R diagrams as follows: (1) Main-sequence stars, 90 percent of all stars, are in the band that runs from the upper-left corner (massive, hot blue stars) to the lower-right corner (low-mass, red stars); (2) red giants and supergiants, very luminous stars with large diameters, are located in the upper- right position; and (3) white dwarfs, which are small stars, are located in the lower portion.

''',

'''
24.2 Stellar Evolution
List and describe the stages in the evolution of a typical Sun-like star.
KEY TERMS: nebula, molecular cloud, protostar, hydrogen fusion, planetary nebula, supernova
Stars originate from the gravitational collapse of a molecular cloud. The energy released by collapse causes the cloud's center to become a hot, luminous protostar.
The protostar becomes a star when its core reaches a temperature of about 10 million K, igniting hydrogen fusion by the proton-proton chain. Hydrogen fusion involves the conversion of four hydrogen nuclei into a single helium nucleus with the release of thermal nuclear
energy.
•Two opposing forces act on a star: gravity, which tries to contract it into the smallest possible ball, and gas pressure (created by thermal nuclear energy), which tries to expand it. When the forces come into balance, the star becomes a stable main-sequence star.
A star's main-sequence lifetime ends when the hydrogen fuel in the core is exhausted. In all but low-mass (red dwarf) stars, other types of nuclear fusion then cause the outer envelope to expand enormously (hundreds to thousands of times), making the star a red giant or supergiant. When a star exhausts all of its usable nuclear fuel, gravity takes over, and the stellar remnant collapses into a small, dense body.
''',

'''
24.3 Stellar Remnants
Compare and contrast the final state of Sun-like stars to the remnants of the most massive stars.
KEY TERMS: neutron star, pulsar, black hole
The final fate of a star is determined primarily by its mass.
Low-mass and intermediate-mass stars end up as white dwarfs. In the case of intermediate-mass stars such as our Sun, the newborn white dwarf is typically surrounded by an expanding clouds of glowing gas called a planetary nebula.
Massive stars terminate in a brilliant explosion called a supernova. Supernova events can produce small, extremely dense neutron stars composed largely of neutrons, or smaller, even denser black holes-objects that have such immense gravity that light cannot escape
from them.

''',

'''
24.4 Galaxies and Galaxy Clusters
List the three major types of galaxies. Explain the formation of large elliptical galaxies.
KEY TERMS: galaxy, spiral galaxy, barred spiral galaxy, elliptical galaxy, dwarf galaxy, irregular galaxy, galaxy cluster, Local Group
The various types of galaxies include (1) irregular galaxies, which lack symmetry and account for about 25 percent of the known galaxies; (2) spiral galaxies, which are disk-shaped and have a greater concentration of stars near their centers and arms extending from their central nucleus; and (3) elliptical galaxies, which have an ellipsoidal shape and may be nearly spherical. Some spiral galaxies, called barred spirals, have a central bar connecting the spiral arms.
Galaxies can be grouped into galaxy clusters, some containing thousands of galaxies. Our own, called the Local Group, contains at least 40 galaxies.

''',

'''
24.5 The Universe
Describe Edwin Hubble's discoveries about the nature of the universe and summarize the Big Bang theory.
KEY TERMS: cosmology, Big Bang theory, cosmological redshift, Hubble's law, dark matter, dark energy
• Cosmology is the study of the universe, including its properties, structure, and evolution.
The universe consists of hundreds of billions of galaxies, most containing billions of stars.
Evidence for an expanding universe came from the study of redshifts in the spectra of galaxies. Edwin Hubble concluded that the observed redshifts result from the expansion of space.
The model that most accurately describes the birth and current state of the universe is the Big Bang theory. According to this model, the universe began about 13.8 billion years ago, in a cataclysmic explosion, and then it continued to expand, cool, and evolve to its current state.
One question that remains is whether the universe will expand forever in a Big Chill or gravitationally contract in a Big Crunch. Dark matter
works to slow the expansion of the universe, while dark energy exerts a force that pushes matter outward and causes the expansion to speed up. Most cosmologists favor an endless, ever-expanding universe.
'''

]

chem_text = [

    '''

    Fundamental Laws of Chemistry
Conservation of Mass – In any chemical reaction, the total mass of reactants equals the total mass of products. Matter is neither created nor destroyed.
Law of Definite Proportions – A given chemical compound always contains its component elements in fixed, definite ratios by mass, regardless of sample size or source.
Law of Multiple Proportions – When two elements form multiple compounds, the mass of one element that combines with a fixed mass of the other follows simple whole-number ratios.
Dalton’s Atomic Theory
Atomic Composition – All elements consist of indivisible, fundamental particles called atoms.
Elemental Identity – Atoms of the same element are identical in mass and properties, while atoms of different elements have distinct characteristics.
Compound Formation – Chemical compounds result from the combination of atoms in fixed, whole-number ratios.
Chemical Reactions – Atoms are neither created nor destroyed in chemical reactions; they rearrange to form new substances, maintaining mass conservation.

''',

'''
Early Atomic Models and Experiments
Thomson’s Plum Pudding Model – Proposed that atoms consist of negatively charged electrons embedded within a diffuse, positively charged sphere.
Millikan’s Oil Drop Experiment – Determined the charge of a single electron by measuring the behavior of tiny oil droplets in an electric field.
Rutherford’s Gold Foil Experiment – Demonstrated that atoms have a dense, positively charged nucleus, disproving the plum pudding model by showing that most of an atom’s volume is empty space.
Nuclear Model of the Atom – Proposed by Rutherford, describing the atom as a small, central nucleus surrounded by electrons moving in empty space.

''',

'''
Atomic Structure
Nucleus – A compact, dense region at the center of the atom containing:
Protons – Positively charged particles, each with a relative mass of 1 atomic mass unit (amu).
Neutrons – Electrically neutral particles with nearly the same mass as protons.
Electrons – Negatively charged particles residing in the space around the nucleus, with a mass approximately 1/1840 that of a proton.
Isotopes – Variants of an element with the same number of protons but different numbers of neutrons, leading to different mass numbers.

''',

'''
Chemical Bonding and Molecular Structure
Covalent Bonds – Formed when atoms share electrons to create molecules.
Molecular Representation:
Chemical Formula – Denotes the number and type of atoms in a molecule.
Structural Formula – Shows the specific arrangement of atoms.
Ball-and-Stick Model – Illustrates spatial relationships between atoms.
Space-Filling Model – Represents the actual relative sizes of atoms in a molecule.

''',

'''
Formation of Ions and Ionic Bonding
Cation Formation – An atom loses one or more electrons, acquiring a positive charge.
Anion Formation – An atom gains one or more electrons, acquiring a negative charge.
Ionic Bonds – Strong electrostatic forces between oppositely charged cations and anions, forming ionic compounds.

''',

'''
The Periodic Table and Element Classification
Elements are arranged by increasing atomic number, grouping those with similar properties into columns (groups).
Metals – Form cations, generally conductive, malleable, and ductile.
Nonmetals – Form anions, often brittle solids or gases, poor conductors.

''',

'''
Naming Chemical Compounds
Binary Compounds – Composed of two elements:
Type I – Metal with a fixed oxidation state (e.g., NaCl, MgO).
Type II – Metal with variable oxidation states, indicated by Roman numerals (e.g., FeCl₂ = Iron(II) chloride).
Type III – Two nonmetals, named using Greek prefixes (e.g., CO₂ = Carbon dioxide).
Polyatomic Ions – Charged species consisting of multiple atoms bonded together, forming ionic compounds (e.g., NH₄⁺, SO₄²⁻).

''',

'''

Stoichiometry: Quantitative Relationships in Chemical Reactions
Definition – Stoichiometry examines the numerical relationships between reactants and products in chemical reactions, determining the amounts of substances consumed or produced.
Counting Atoms by Mass – Since individual atoms are too small to count directly, their quantity is inferred by measuring mass.
Mass-Number Relationship – To convert between mass and the number of atoms, the average atomic mass (weighted based on isotopic abundance) is essential.
''',

'''
The Mole: The Fundamental Counting Unit in Chemistry
Definition – A mole represents 6.022 × 10²³ (Avogadro’s number) of any specified particles (atoms, molecules, ions, or formula units).
Carbon-12 Standard – One mole is defined as the number of carbon atoms in exactly 12 g of pure carbon-12.
Mass-Mole Relationship – The molar mass of an element, measured in grams per mole (g/mol), is numerically equivalent to its atomic mass in atomic mass units (amu).
Molar Mass: Mass of One Mole of a Substance
Definition – The mass of 1 mole of a substance (element or compound) in grams.
Calculation for Compounds – Determined by summing the atomic masses of constituent atoms based on their chemical formula.

''',

'''
Percent Composition: Elemental Distribution in a Compound
Definition - The mass percent of each element in a given compound.
Formula: \text{Mass percent} = \left( \frac{\text{Mass of element in 1 mole of substance}}{\text{Mass of 1 mole of substance}} \right) \times 100\%

 ''',

 '''
Empirical and Molecular Formulas
Empirical Formula: Simplest Atomic Ratio

Definition – Represents the simplest whole-number ratio of different types of atoms in a compound.
Derivation – Can be determined using the percent composition of the compound.

''',

'''
Molecular Formula: Actual Molecular Composition

For Molecular Substances – Specifies the actual number of atoms in a single molecule. It is always a whole-number multiple of the empirical formula.
For Ionic Substances – The molecular formula is identical to the empirical formula, as ionic compounds do not form discrete molecules.
Chemical Reactions: Transformation of Substances
Definition – A process where reactants are converted into products through the breaking and formation of chemical bonds.
Law of Conservation of Mass – Atoms cannot be created or destroyed in a reaction; all atoms in the reactants must also appear in the products.

''',

'''
Chemical Equations: Representation of Reactions
Definition – A symbolic representation of a chemical reaction.
Structure:
Reactants are listed on the left side.
Products are listed on the right side.
The arrow (→) signifies the direction of the reaction.
Balanced Chemical Equation – Ensures the law of conservation of mass by maintaining equal numbers of each atom on both sides.

''',

'''
Stoichiometric Calculations: Determining Reactant and Product Quantities
Balanced Equations as Conversion Factors – The coefficients in a balanced chemical equation provide the mole ratio between reactants and products.
Limiting Reactant Concept:
The limiting reactant is the first reactant to be fully consumed, restricting the maximum amount of product formed.
The excess reactant remains after the reaction is complete.
Yield: Efficiency of a Chemical Reaction
Theoretical Yield – The maximum amount of product that could be produced based on complete reaction of the limiting reactant.
Actual Yield – The measured amount of product obtained from the reaction, which is always lower than the theoretical yield due to inefficiencies.
Percent Yield Formula:
\text{Percent yield} = \left( \frac{\text{Actual yield}}{\text{Theoretical yield}} \right) \times 100\%

''',

'''

Alkanes: Saturated Hydrocarbons

Definition – Alkanes are hydrocarbons that contain only carbon-carbon single bonds (C–C).
General Formula – Given by CₙH₂ₙ₊₂, where n represents the number of carbon atoms.
Saturation – Called saturated hydrocarbons because each carbon atom forms four single bonds, ensuring the maximum possible number of hydrogen atoms.
Hybridization – Carbon atoms in alkanes exhibit sp³ hybridization, forming tetrahedral molecular geometries.
Isomerism – Alkanes can form structural isomers, where the same molecular formula corresponds to different branching arrangements.
Reactivity:
Combustion Reaction – Alkanes react with oxygen (O₂) to form carbon dioxide (CO₂) and water (H₂O), releasing energy.
Substitution Reactions – Alkanes can undergo halogenation, where a hydrogen atom is replaced by a halogen (e.g., chlorine or bromine).

''',

'''
Alkenes: Unsaturated Hydrocarbons with Double Bonds

Definition – Alkenes contain at least one carbon-carbon double bond (C=C).
Simplest Example – Ethene (C₂H₄, also called ethylene), where carbon atoms are sp² hybridized and arranged in a trigonal planar geometry.
Isomerism – The double bond prevents free rotation, leading to the formation of cis-trans (geometric) isomers based on the arrangement of substituents around the double bond.
Reactivity –
Addition Reactions – Alkenes readily react with substances such as hydrogen (H₂), halogens (Br₂, Cl₂), and hydrogen halides (HCl, HBr) by breaking the double bond and forming new single bonds.

''',

'''
Alkynes: Unsaturated Hydrocarbons with Triple Bonds

Definition – Alkynes contain at least one carbon-carbon triple bond (C≡C).
Simplest Example – Ethyne (C₂H₂, also called acetylene), where carbon atoms exhibit sp hybridization, forming a linear geometry.
Reactivity – Like alkenes, alkynes undergo addition reactions, breaking the triple bond to form more saturated products.

''',

'''
Aromatic Hydrocarbons: Resonance-Stabilized Rings

Definition – These hydrocarbons contain ring structures with delocalized π electrons, following Hückel’s Rule (4n+2 π electrons).
Reactivity – Unlike alkenes and alkynes, they undergo substitution reactions (e.g., electrophilic aromatic substitution) rather than addition, preserving the aromatic ring stability.
Hydrocarbon Derivatives: Functional Groups and Reactivity
Hydrocarbon derivatives are organic compounds that contain additional functional groups, modifying their chemical properties.

''',

'''
Common Functional Groups

Alcohols – Contain the –OH (hydroxyl) group, making them polar and capable of hydrogen bonding.
Aldehydes – Characterized by the carbonyl group (C=O) at the end of a carbon chain.
Carboxylic Acids – Contain both carbonyl (C=O) and hydroxyl (–OH) groups, contributing to acidity.
Polymers: Macromolecules from Repeating Units
Polymers are large molecules formed by linking small repeating units (monomers).

''',

'''
Types of Polymerization

Addition Polymerization – Monomers with double bonds undergo a chain reaction mechanism, leading to polymer growth (e.g., polyethylene, polypropylene).
Condensation Polymerization – Monomers link together while eliminating a small molecule (e.g., water), forming polymers like proteins and polyesters.
Proteins: Biological Polymers and Structural Organization
Proteins are essential natural polymers with molar masses ranging from 600 to over 1,000,000 g/mol.

''',

'''

Electrolytes
Strong Electrolyte:
Completely dissociates in solution to produce separate ions (e.g., NaCl → Na⁺ + Cl⁻).
Conducts electricity very efficiently due to the high concentration of ions.
Common examples include soluble salts (like NaCl), strong acids (like HCl), and strong bases (like NaOH).
Weak Electrolyte:
Only a small fraction of dissolved molecules dissociate into ions (e.g., CH₃COOH ↔ CH₃COO⁻ + H⁺).
Conducts electricity poorly, as there are fewer ions present in solution.
Common examples include weak acids (like acetic acid) and weak bases (like ammonia).
Nonelectrolyte:
Dissolved substances that do not produce ions in solution (e.g., sugar, ethanol).
Does not conduct electricity as there are no free ions present.

''',

'''
Acids and Bases
Arrhenius Model:
Acid: A substance that, when dissolved in water, produces hydrogen ions (H⁺).
Base: A substance that, when dissolved in water, produces hydroxide ions (OH⁻).
Brønsted–Lowry Model:
Acid: A proton donor, which can transfer a hydrogen ion to another substance.
Base: A proton acceptor, which can accept a hydrogen ion from another substance.
Strong Acid:
Completely dissociates in solution to yield H⁺ ions and anions (e.g., HCl → H⁺ + Cl⁻).
High conductivity due to a large number of ions.
Weak Acid:
Only partially dissociates in solution, resulting in an equilibrium between undissociated acid and ions (e.g., CH₃COOH ⇌ CH₃COO⁻ + H⁺).

''',

'''

Molarity
Definition: Molarity (M) is a way to express the concentration of a solution.
Formula: Molarity (M) = moles of solute / volume of solution (L).
Standard Solution:
A solution whose concentration is precisely known, often used as a reference in titrations and calculations.

''',

'''
Dilution
Process: Involves adding solvent to a solution to decrease its concentration.
Moles of Solute:
The number of moles of solute remains constant before and after dilution:
Dilution Equation: M₁V₁ = M₂V₂, where M is molarity and V is volume.

''',

'''
Types of Equations that Describe Solution Reactions
Formula Equation:
Represents all reactants and products in their complete formulas, showing the overall reaction without indicating ionic dissociation.
Complete Ionic Equation:
Breaks down strong electrolytes into their constituent ions, showing all ions present in the reaction.
Net Ionic Equation:
Displays only the ions and compounds that undergo a change during the reaction, excluding spectator ions that do not participate.

''',

'''
Solubility Rules
General Observations:
Based on experimental data to predict whether a compound will dissolve in water.
Help in anticipating the formation of precipitates in reactions.

''',

'''
Important Types of Solution Reactions
Acid–Base Reactions:
Characterized by the transfer of H⁺ ions between reactants, often resulting in the formation of water and a salt.
Precipitation Reactions:
Involve the formation of an insoluble solid (precipitate) from the reaction of two soluble reactants.
Oxidation–Reduction Reactions:
Involve the transfer of electrons between substances, resulting in changes to their oxidation states.

''',

'''
Titrations
Definition: A laboratory technique used to determine the concentration of a solution by reacting it with a standard solution of known concentration (the titrant).
Stoichiometric (Equivalence) Point:
The point in the titration at which the amount of titrant added is exactly enough to react with the substance being analyzed.
Endpoint:
The stage in a titration where a visible change occurs, often indicated by a color change due to a chemical indicator.

''',

'''

Oxidation–Reduction Reactions
Oxidation States:
Assigned according to a set of rules to track electron movement during reactions.
Oxidation:
The process where an atom or ion loses electrons, resulting in an increase in oxidation state.
Reduction:
The process where an atom or ion gains electrons, resulting in a decrease in oxidation state.
Oxidizing Agent:
The species that gains electrons in a redox reaction and is thereby reduced.
Reducing Agent:
The species that loses electrons in a redox reaction and is thereby oxidized.
Balancing Equations:
Equations for oxidation-reduction reactions can be balanced using the oxidation states method to ensure mass and charge conservation.

''',

'''

State of a Gas
The state of a gas can be fully described by the following parameters:
Pressure (P): The force exerted by gas particles colliding with the walls of their container per unit area.
Volume (V): The space occupied by the gas.
Temperature (T): A measure of the average kinetic energy of gas particles, expressed in Kelvin (K).
Amount of Gas (n): The quantity of gas present, measured in moles.
Pressure
Common Units of Pressure:
SI Unit: Pascal (Pa)
Other Units:
1 torr = 1 mm Hg
1 atm = 760 torr
1 atm = 101,325 Pa

''',

'''

Gas Laws
Gas laws describe the relationships between pressure, volume, temperature, and amount of gas based on empirical observations.
Boyle’s Law:
Describes the inverse relationship between pressure and volume at constant temperature.
Equation: 
PV = k (where k is a constant).
Charles’s Law:
Describes the direct relationship between volume and temperature at constant pressure.
Equation: 
V = b T (where b is a constant).
Avogadro’s Law:
States that the volume of a gas is directly proportional to the number of moles of gas at constant temperature and pressure.
Equation: 
V = an (where a is a constant).
Ideal Gas Law:
Combines the previous laws into one equation that relates pressure, volume, temperature, and the number of moles of gas.
Equation: PV = nRT (where R is the ideal gas constant).
Partial Pressure:
P_{\text{total}} = P_1 + P_2 + P_3 + \dots
\text{where } P_n \text{ represents the partial pressure of each gas.}

''',

'''
Assumptions of Ideal Gases
The ideal gas model makes several key assumptions:
The volume of gas particles is negligible (considered zero).
There are no intermolecular forces or interactions between gas particles.
Gas particles are in constant, random motion and collide elastically with the walls of the container, producing pressure.
The average kinetic energy of gas particles is directly proportional to the absolute temperature of the gas in Kelvin.

''',

''''
Gas Properties
Velocity Distribution:
The particles in a gas sample have a range of velocities, which can be described by the root mean square (rms) velocity.
Root Mean Square (rms) Velocity:
Represents the square root of the average of the squares of the particle velocities.
Equation: u_{\text{rms}} = \sqrt{\frac{3RT}{M}}, \text{where } R \text{ is the ideal gas constant, } T \text{ is the temperature in Kelvin, and } M \text{ is the molar mass of the gas.}
Diffusion:
The process in which gas particles intermingle due to random motion, leading to the gradual mixing of different gases.
Effusion:
The process in which gas particles escape through a small hole into an empty chamber, dependent on the speed of the particles.

''',

'''
Real Gas Behavior
Deviation from Ideal Behavior:
Real gases deviate from ideal behavior at high pressures and low temperatures due to increased particle interactions and volume effects.
Modifications to Ideal Gas Equation:
To accurately describe real gas behavior, modifications must be made to the ideal gas equation to account for:
Intermolecular forces between gas particles.
The actual volume occupied by gas particles.
Van der Waals Equation:
Van der Waals developed an equation that adjusts the ideal gas law to account for these factors: \left( P + \frac{a n^2}{V^2} \right) \left( V - n b \right) = n R T, \text{where } a \text{ accounts for attractive forces between particles, and } b \text{ accounts for the volume occupied by the gas particles themselves.}

''',

'''

Electromagnetic Radiation
Definition: Electromagnetic radiation is energy that travels through space as waves. It is characterized by three key properties:
Wavelength (λ): The distance between successive peaks of the wave, usually measured in meters (m).
Frequency (ν): The number of wave cycles that pass a point in one second, measured in hertz (Hz).
Speed (c): The speed of light in a vacuum, c = 3*10^8 m/s.
Relationship: The wavelength and frequency are inversely related by the equation: c=λν
Photons: Electromagnetic radiation can also be viewed as a stream of particles known as photons. Each photon carries a quantized amount of energy, given by the equation: E = hf where  h h is Planck's constant ( h = 6.626 × 10 − 34   J*s h=6.626×10  −34  J s).

''',

'''
Photoelectric Effect
Definition: The photoelectric effect is the phenomenon where electrons are emitted from a metal surface when it is illuminated by light of sufficient frequency.
Observations:
The kinetic energy of the emitted electrons is dependent on the frequency of the incident light, not its intensity.
This effect demonstrated that light has particle-like properties, leading to the concept that electromagnetic radiation can be considered as a stream of photons.

''',

'''
Hydrogen Spectrum
Emission Spectrum: The emission spectrum of hydrogen consists of distinct lines corresponding to specific wavelengths of light emitted when electrons transition between energy levels.
Significance: The presence of discrete wavelengths indicates that hydrogen has quantized energy levels, where electrons can occupy specific states without intermediate values.

''',

'''
Bohr Model of the Hydrogen Atom
Development: Using data from the hydrogen spectrum and assuming that angular momentum is quantized, Niels Bohr developed a model of the hydrogen atom where:
Electrons travel in fixed circular orbits around the nucleus.
The energy of each orbit is quantized, with electrons emitting or absorbing energy in discrete amounts when transitioning between orbits.
Limitations: Although revolutionary at the time, the Bohr model was ultimately found to be incorrect and insufficient for explaining more complex atoms.

''',

'''
Wave (Quantum) Mechanical Model
Electron Behavior: In this model, electrons are treated as standing waves rather than particles, leading to a more comprehensive understanding of their behavior in atoms.
Wave Function: The square of the wave function describes the probability distribution of an electron's position, providing a statistical interpretation of electron locations rather than definitive paths.
Heisenberg Uncertainty Principle: This principle states that it is impossible to simultaneously know both the exact position and momentum of a particle, which reinforces the probabilistic nature of the quantum mechanical model.

''',

'''
Orbitals: Probability maps derived from the wave function define the shapes and orientations of orbitals, characterized by the quantum numbers:
n (principal quantum number): Indicates the energy level and size of the orbital.
l (azimuthal quantum number): Indicates the shape of the orbital.
mₗ (magnetic quantum number): Indicates the orientation of the orbital in space.

''',

'''
Electron Spin
Spin Quantum Number: Spin Quantum Number ( m s m  s ​   ): Describes the intrinsic angular momentum of an electron, with possible values of  + 1 2 +  2 1 ​    or  − 1 2 −  2 1 ​   . Pauli Exclusion Principle: States that no two electrons in an atom can have the same set of quantum numbers ( n , l , m l , m s n,l,m  l ​   ,m  s ​   ), meaning that only two electrons with opposite spins can occupy the same orbital.

''',

'''
Aufbau Principle: The order in which orbitals are filled with electrons follows the Aufbau principle, which explains the structure of the periodic table based on the arrangement of electrons in orbitals.
Valence Electrons: Atoms in the same group of the periodic table have the same valence electron configuration, which contributes to their similar chemical properties.
Trends in Properties: Trends such as ionization energy and atomic radius can be explained through concepts of:
Nuclear Attraction: The attractive force between protons in the nucleus and electrons.
Electron Repulsions: The repulsive forces between electrons in the same atom.
Shielding: The effect of inner-shell electrons reducing the effective nuclear charge felt by outer-shell electrons.
Penetration: The ability of an electron in a given orbital to get close to the nucleus, influencing its energy and stability.

''',

'''

Chemical Bonds
Definition: Chemical bonds are the forces that hold groups of atoms together in a compound. They occur when a group of atoms can lower its total energy by aggregating.
Types of Chemical Bonds:
Ionic Bonds: Formed when electrons are transferred from one atom to another, resulting in the formation of charged ions (cations and anions).
Covalent Bonds: Formed by the equal sharing of electrons between two nonmetal atoms.
Polar Covalent Bonds: Occur when electrons are shared unequally between two atoms, leading to a partial positive charge on one atom and a partial negative charge on the other.
Percent Ionic Character: The degree of ionic character in a bond

''',

'''

Electronegativity: A measure of the relative ability of an atom to attract shared electrons in a chemical bond. The difference in electronegativity between two bonded atoms determines the polarity of the bond:
A larger difference indicates a more polar bond, while a smaller difference suggests a nonpolar bond.
Dipole Moment: The spatial arrangement of polar bonds in a molecule determines whether the molecule has an overall dipole moment, affecting its physical and chemical properties.

''',

'''
Ionic Bonding
Ionic Compounds: Formed from the electrostatic attraction between cations and anions.
Ionic Size:
Anion: An ion formed by the gain of electrons; it is larger than its parent atom due to increased electron-electron repulsion.
Cation: An ion formed by the loss of electrons; it is smaller than its parent atom due to decreased electron-electron repulsion and increased nuclear charge effect.
Lattice Energy: The energy change that occurs when ions are packed together to form an ionic solid. It is a measure of the stability of the ionic compound, with higher lattice energies indicating stronger ionic bonds.

''',

'''
Bond Energy
Definition: The amount of energy required to break a covalent bond between two atoms in a molecule.
Trends:
Bond energy increases with the number of shared electron pairs (e.g., triple bonds have higher bond energy than double bonds, which in turn are stronger than single bonds).
Application: Bond energy can be used to estimate the enthalpy change (ΔH) for a chemical reaction by summing the bond energies of the bonds broken and formed during the reaction.

''',

'''
Lewis Structures
Purpose: Lewis structures visually represent how the valence electron pairs are arranged among atoms in a molecule or polyatomic ion.
Key Concepts:
Stable molecules generally have filled valence orbitals.
Duet Rule: For hydrogen, stability is achieved with two electrons (a filled 1s orbital).
Octet Rule: For second-row elements, stability is typically achieved with eight electrons in the valence shell.
Atoms of elements in the third row and beyond can exceed the octet rule by accommodating more than eight electrons due to available d orbitals.
Resonance: Some molecules can be represented by multiple equivalent Lewis structures, indicating delocalized electrons.
Formal Charge: When multiple nonequivalent Lewis structures can be drawn, formal charge calculations help identify the most stable structure(s) by minimizing formal charges across atoms.
VSEPR Model (Valence Shell Electron Pair Repulsion)
Principle: The VSEPR model is based on the idea that electron pairs (bonding and lone pairs) will arrange themselves around a central atom to minimize electron-electron repulsions, resulting in specific molecular geometries.
Application: The VSEPR model can be used to predict the geometric structure of most molecules, including:
Linear (180°)
Trigonal planar (120°)
Tetrahedral (109.5°)
Trigonal bipyramidal (90° and 120°)
Octahedral (90°)

''',

'''
Two Widely Used Bonding Models
Localized Electron Model
Molecular Orbital Model
Localized Electron Model
Concept: The localized electron model visualizes a molecule as a collection of atoms that share electron pairs between their atomic orbitals. This model emphasizes the role of hybridization in determining molecular structure.
Hybrid Orbitals: To explain the geometry of molecules, hybrid orbitals—combinations of the native atomic orbitals—are often employed. The required hybrid orbitals depend on the number of electron pairs surrounding the central atom:
Six Electron Pairs (Octahedral Arrangement): Require d²sp³ hybrid orbitals.
Five Electron Pairs (Trigonal Bipyramidal Arrangement): Require dsp³ hybrid orbitals.
Four Electron Pairs (Tetrahedral Arrangement): Require sp³ hybrid orbitals.
Three Electron Pairs (Trigonal Planar Arrangement): Require sp² hybrid orbitals.
Two Electron Pairs (Linear Arrangement): Require sp hybrid orbitals.

''',

'''
Types of Bonds:
Sigma (σ) Bonds: Formed when electrons are shared in an area centered along the line connecting the two atoms. This bond type allows for free rotation about the bond axis.
Pi (π) Bonds: Formed when a shared electron pair occupies regions above and below the line connecting the two atoms. These bonds do not allow for free rotation due to their orientation.
Molecular Orbital Model
Concept: The molecular orbital model treats a molecule as a new entity made up of positively charged nuclei and electrons. Instead of focusing solely on localized electron pairs, this model considers electrons to be distributed in molecular orbitals (MOs) that are formed from the atomic orbitals of the constituent atoms.
Key Features:
Delocalization: Electrons in the molecular orbital model are depicted as being delocalized across the entire molecule, which provides a more accurate representation of bonding in polyatomic molecules.
Predictive Power: This model effectively predicts relative bond strength, magnetism, and bond polarity.
Disadvantages: The primary drawback of the molecular orbital model is that it can be challenging to apply qualitatively to polyatomic molecules due to its complexity.
Classification of Molecular Orbitals
Molecular orbitals can be classified based on two main criteria: energy and shape.

''',

'''
Energy:
Bonding Molecular Orbitals (MOs): These MOs are lower in energy than the atomic orbitals from which they are formed. Electrons in bonding MOs are lower in energy within the molecule than in the separated atoms, favoring molecule formation.
Antibonding Molecular Orbitals: These MOs are higher in energy than the atomic orbitals from which they are formed. Electrons in antibonding MOs are higher in energy in the molecule than in the separated atoms, which does not favor molecule formation.
Shape (Symmetry):
Sigma (σ) MOs: These orbitals have their electron probability concentrated along a line passing through the nuclei of the atoms.
Pi (π) MOs: These orbitals have their electron probability distributed above and below the line connecting the nuclei, indicating the presence of a nodal plane.
Bond Order and Resonance
Bond Order: An index of bond strength calculated using the formula:
Bond Order
=
Number of Bonding Electrons
−
Number of Antibonding Electrons
2
Bond Order= 
2
Number of Bonding Electrons−Number of Antibonding Electrons

A higher bond order indicates a stronger bond between atoms.
Combining Models: For molecules requiring resonance in the localized electron model, a more accurate description can be achieved by integrating both the localized electron and molecular orbital models:
σ Bonds: Considered localized.
π Bonds: Treated as delocalized.

''',

'''
General Properties: Liquids and solids are held together by intermolecular forces among their constituent molecules, atoms, or ions. These forces dictate various physical properties, such as surface tension, capillary action, and viscosity in liquids.
Intermolecular Forces
Dipole-Dipole Forces:
Definition: Attractions that occur between molecules with permanent dipole moments.
Hydrogen Bonding: A particularly strong type of dipole-dipole interaction that occurs in molecules where hydrogen is bonded to highly electronegative elements such as nitrogen, oxygen, or fluorine. Hydrogen bonds contribute to unusually high boiling points in substances like water.
London Dispersion Forces:
Definition: Weak attractions that arise from instantaneous dipoles that occur in atoms or nonpolar molecules due to temporary fluctuations in electron distribution. These forces increase with the size of the molecule.

''',

'''
Crystalline Solids
Structure: Crystalline solids are characterized by a regular arrangement of their components, often depicted as a lattice. The smallest repeating unit of the lattice is known as the unit cell.
Classification by Component Types:
Atomic Solids: Composed of individual atoms.
Ionic Solids: Comprised of ions held together by ionic bonds.
Molecular Solids: Formed from molecules held together by intermolecular forces.
Analysis: The arrangement of components in crystalline solids can be determined using X-ray analysis.

''',

'''
Metals
Structure: Metallic solids are modeled by assuming atoms are uniform spheres arranged in a closely packed structure.
Packing Types:
Hexagonal Closest Packing
Cubic Closest Packing
Metallic Bonding Models:
Electron Sea Model: Valence electrons are delocalized and move freely among the metal cations, contributing to conductivity and malleability.
Band Model: Electrons occupy molecular orbitals, forming bands.
Conduction Bands: Closely spaced molecular orbitals with available electron states that facilitate electrical conductivity.
Alloys: Mixtures of metals that exhibit metallic properties.
Types:
Substitutional Alloys: Atoms of one metal are replaced by atoms of another metal of similar size.
Interstitial Alloys: Smaller atoms occupy the spaces between larger metal atoms.

''',

'''
Network Solids
Description: Network solids are characterized by extensive networks of atoms that are covalently bonded together.
Examples:
Diamond: A form of carbon where each atom is tetrahedrally bonded to four other carbon atoms, resulting in a very hard structure.
Graphite: Composed of layers of carbon atoms arranged in a planar hexagonal structure, allowing for slip between layers.
Silicates: Network solids containing silicon-oxygen (Si-O) bridges that form the basis of many rocks, clays, and ceramics.

''',

'''
Semiconductors
Doping Process: Very pure silicon is doped with other elements to modify its electrical properties.
n-type Semiconductors: Created by doping silicon with atoms that have five valence electrons, resulting in excess electrons.
p-type Semiconductors: Created by doping silicon with atoms that have three valence electrons, resulting in "holes" that can carry a positive charge.
Application: Modern electronics rely on devices that utilize p-n junctions formed by combining n-type and p-type materials.

''',

'''
Molecular Solids
Definition: Composed of discrete molecules held together by relatively weak intermolecular forces, resulting in lower boiling and melting points compared to other solid types.
Ionic Solids
Characteristics: Composed of ions held together by strong ionic bonds, resulting in high melting and boiling points. The arrangement typically involves the closest packing of larger ions, with smaller ions occupying tetrahedral or octahedral holes.

''',

'''
Equilibrium Vapor Pressure: The pressure exerted by a vapor in equilibrium with its liquid or solid phase in a closed system when the rate of evaporation equals the rate of condensation.
Properties of Liquids: Liquids with high intermolecular forces exhibit relatively low vapor pressures.
Normal Boiling Point: The temperature at which the vapor pressure of a liquid equals one atmosphere.
Normal Melting Point: The temperature at which a solid and its liquid phase have the same vapor pressure at one atmosphere of external pressure.

''',

'''
Phase Diagrams
Function: Illustrate the state of a substance (solid, liquid, gas) at various temperatures and pressures in a closed system.
Key Points:
Triple Point: The unique temperature and pressure at which all three phases coexist in equilibrium.
Critical Point: Defined by critical temperature and pressure, beyond which a gas cannot be liquefied regardless of the pressure applied.
Critical Temperature: The highest temperature at which a substance can exist as a liquid.

''',

'''

Molarity (M):
Defined as the number of moles of solute per liter of solution.
Formula: mol/L.

Mass Percent:
The ratio of the mass of the solute to the mass of the solution, expressed as a percentage.
Formula: 
Mass percent
=
(
mass of solute
mass of solution
)
×
100
%
Mass percent=( 
mass of solution
mass of solute
​	
 )×100%

Mole Fraction (x):
The ratio of the number of moles of a given component to the total number of moles of all components in the solution.
Formula: 
x
=
moles of component
total moles of all components
x= 
total moles of all components
moles of component
​	
 
Molality (m):
Defined as the number of moles of solute per kilogram of solvent.
Formula: 
m
=
moles of solute
mass of solvent (kg)
m= 
mass of solvent (kg)
moles of solute
​	
 
Normality (N):
The number of equivalents of solute per liter of solution.
Useful in acid-base reactions and redox reactions.
Enthalpy of Solution (
Δ
H
s
o
l
n
ΔH 
soln
​	
 )

''',

'''
Definition: The enthalpy change that occurs when a solution is formed from its components.
Components:
The energy required to overcome solute-solute interactions.
The energy required to create space (or "holes") in the solvent.
The energy associated with the interactions between solute and solvent.

''',

'''
Factors Affecting Solubility
Polarity of Solute and Solvent:
General Rule: “Like dissolves like,” meaning polar solutes dissolve well in polar solvents, while nonpolar solutes dissolve in nonpolar solvents.
Pressure:
Increasing pressure enhances the solubility of gases in a solvent.
Henry’s Law: 
C
=
k
P
C=kP
Where 
C
C is the concentration of the gas, 
k
k is Henry’s law constant, and 
P
P is the partial pressure of the gas.
Temperature Effects:
Increased temperature generally decreases the solubility of gases in water.
Most solids are more soluble at higher temperatures, although there are important exceptions (e.g., certain salts).
Vapor Pressure of Solutions
A solution containing a nonvolatile solute will have a lower vapor pressure compared to that of the pure solvent.
Raoult’s Law:
Defines an ideal solution:
P
s
o
l
n
=
x
⋅
P
p
u
r
e
P 
soln
​	
 =x⋅P 
pure
​	
 
Where 
P
s
o
l
n
P 
soln
​	
  is the vapor pressure of the solution, 
x
x is the mole fraction of the solvent, and 
P
p
u
r
e
P 
pure
​	
  is the vapor pressure of the pure solvent.
Solutions where solute-solvent attractions differ significantly from solute-solute and solvent-solvent attractions will violate Raoult’s law.

''',

'''
Colligative Properties
Definition: Properties that depend on the number of solute particles in a solution rather than their identity.
Key Properties:
Boiling-Point Elevation:
Δ
T
b
=
K
b
⋅
m
s
o
l
u
t
e
ΔT 
b
​	
 =K 
b
​	
 ⋅m 
solute
​	
 
Where 
K
b
K 
b
​	
  is the boiling point elevation constant and 
m
s
o
l
u
t
e
m 
solute
​	
  is the molality of the solute.
Freezing-Point Lowering:
Δ
T
f
=
K
f
⋅
m
s
o
l
u
t
e
ΔT 
f
​	
 =K 
f
​	
 ⋅m 
solute
​	
 
Where 
K
f
K 
f
​	
  is the freezing point depression constant.
Osmotic Pressure:
P
=
M
R
T
P=MRT
Where 
P
P is the osmotic pressure, 
M
M is the molarity, 
R
R is the ideal gas constant, and 
T
T is the temperature in Kelvin.

''',

'''
Osmosis: Occurs when a solution and pure solvent are separated by a semipermeable membrane that allows solvent molecules to pass but not solute particles.
Reverse Osmosis: Happens when pressure applied to the solution exceeds its osmotic pressure, causing solvent to flow from the solution to the pure solvent side.
Van’t Hoff Factor (i):
Represents the number of ions produced by each formula unit of solute when it dissolves.
Colligative properties are affected proportionally to the number of ions produced.
Colloids
Definition: A colloid is a suspension of tiny particles dispersed throughout a continuous medium (liquid, gas, or solid).
Stabilization: Colloids are stabilized by electrostatic repulsion among the charged layers surrounding individual particles, preventing them from coalescing.
Coagulation: Colloids can be destroyed (coagulated) through processes such as heating or the addition of electrolytes, leading to the aggregation of particles.

''',

'''

Chemical Kinetics
Definition: The study of the factors that control the rate (speed) of a chemical reaction.
Rate Definition: The rate of a reaction is defined in terms of the change in concentration of a given reaction component per unit time.
Kinetic Measurements: Often conducted under conditions where the reverse reaction is insignificant, allowing for simpler analysis.
Relationship to Thermodynamics: The kinetic and thermodynamic properties of a reaction are not fundamentally related; they provide different information about the reaction.
Rate Laws
Rate Constant (k): A proportionality constant in the rate law that is specific to each reaction and varies with temperature.
Order of Reaction (n): Indicates the power to which the concentration of a reactant is raised in the rate law; it is not necessarily related to the coefficients in the balanced equation.
Integrated Rate Law: Describes how the concentration of reactants changes over time.
Differential Rate Law: Describes the rate of the reaction as a function of the concentration of reactants.
General form:
Rate
=
k
[
A
]
n
Rate=k[A] 
n
 
Special Cases of Integrated Rate Laws

Zero-Order Reaction (
n
=
0
n=0):
Rate Law:
Rate
=
k
[
A
]
0
=
k
Rate=k[A] 
0
 =k
Integrated Form:
[
A
]
=
[
A
]
0
−
k
t
[A]=[A] 
0
​	
 −kt
Half-Life:
t
1
/
2
=
[
A
]
0
2
k
t 
1/2
​	
 = 
2k
[A] 
0
​	
 
​	
 
First-Order Reaction (
n
=
1
n=1):
Rate Law:
Rate
=
k
[
A
]
1
Rate=k[A] 
1
 
Integrated Form:
ln
⁡
[
A
]
=
−
k
t
+
ln
⁡
[
A
]
0
ln[A]=−kt+ln[A] 
0
​	
 
Half-Life:
t
1
/
2
=
0.693
k
t 
1/2
​	
 = 
k
0.693
​	
 
Second-Order Reaction (
n
=
2
n=2):
Rate Law:
Rate
=
k
[
A
]
2
Rate=k[A] 
2
 
Integrated Form:
1
[
A
]
=
k
t
+
1
[
A
]
0
[A]
1
​	
 =kt+ 
[A] 
0
​	
 
1
​	
 
Half-Life:
t
1
/
2
=
1
k
[
A
]
0
t 
1/2
​	
 = 
k[A] 
0
​	
 
1
​	
 
The value of 
k
k can be determined from the plot of the appropriate function of 
[
A
]
[A] versus time.
Reaction Mechanisms
Elementary Steps: A series of individual steps through which an overall reaction occurs. The rate law for each elementary step can be derived from its molecularity.
Requirements for Acceptable Mechanisms:
The elementary steps must sum to give the correct overall balanced equation.
The mechanism must agree with the experimentally determined rate law.
Rate-Determining Step: In a sequence of elementary steps, the slowest step controls the overall rate of the reaction.
Kinetic Models
Collision Model: The simplest model for reaction kinetics, which states that molecules must collide to react.
Collision Energy: The kinetic energy from the collision provides the potential energy necessary for the reactants to rearrange and form products.
Activation Energy (
E
a
E 
a
​	
 ): A threshold energy that must be exceeded for a reaction to occur.
Orientation: The relative orientations of the colliding reactants are critical; certain orientations may be more favorable for reaction.
Arrhenius Equation:
k
=
A
e
−
E
a
/
R
T
k=Ae 
−E 
a
​	
 /RT
 
A
A: The frequency factor, which depends on the collision frequency and the relative orientation of the molecules.
The value of 
E
a
E 
a
​	
  can be determined by measuring 
k
k at different temperatures.
Catalysts
Definition: Substances that speed up a reaction without being consumed in the process.
Mechanism: Catalysts provide an alternative pathway for the reaction with a lower activation energy.
Types of Catalysts:
Homogeneous Catalysts: Exist in the same phase (solid, liquid, gas) as the reactants, facilitating reactions by interacting with them directly.
Heterogeneous Catalysts: Exist in a different phase than the reactants, often solid catalysts in liquid or gas reactions.
Biological Catalysts: Enzymes are specialized catalysts that speed up biochemical reactions.
Acids and Bases: Can also function as catalysts in certain reactions.

''',

'''

Chemical Equilibrium
Definition: When a reaction occurs in a closed system, it eventually reaches a state where the concentrations of reactants and products remain constant over time.
Dynamic State: Although the concentrations are constant, the reactants and products are continually interconverted, meaning that both the forward and reverse reactions are occurring simultaneously.
Forward and Reverse Rates: At equilibrium, the rate of the forward reaction equals the rate of the reverse reaction.
The Law of Mass Action
For the reaction:
j
A
+
k
B
⇌
m
C
+
n
D
jA+kB⇌mC+nD
The equilibrium constant 
K
K is expressed as:
K
=
[
C
]
m
[
D
]
n
[
A
]
j
[
B
]
k
K= 
[A] 
j
 [B] 
k
 
[C] 
m
 [D] 
n
 
​	
 
Exclusion of Pure Substances: Pure liquids and solids are not included in the equilibrium expression.
Equilibrium Constant for Gases: For gas-phase reactions, the equilibrium constant can also be expressed in terms of partial pressures, denoted as 
K
p
K 
p
​	
 :
K
p
=
K
c
(
R
T
)
Δ
n
K 
p
​	
 =K 
c
​	
 (RT) 
Δn
 
where 
Δ
n
Δn is the difference in the sum of the coefficients of gaseous products and reactants, and 
R
R is the universal gas constant.
Equilibrium Position
Definition: A specific set of reactant and product concentrations that satisfies the equilibrium constant expression.
Constant 
K
K: For a given system at a specified temperature, there is one equilibrium constant 
K
K. However, there can be an infinite number of equilibrium positions at that temperature, depending on the initial concentrations.
Magnitude of 
K
K:
A small value of 
K
K indicates that the equilibrium lies to the left (favoring reactants).
A large value of 
K
K indicates that the equilibrium lies to the right (favoring products).
Independence from Reaction Rate: The size of 
K
K does not indicate the speed at which equilibrium is reached.
Reaction Quotient (
Q
Q): Applies the law of mass action to the initial concentrations rather than at equilibrium.
If 
Q
>
K
Q>K, the system will shift to the left (toward reactants) to reach equilibrium.
If 
Q
<
K
Q<K, the system will shift to the right (toward products) to reach equilibrium.
Finding Equilibrium Concentrations:
Start with the initial concentrations (or partial pressures).
Define the changes needed to reach equilibrium.
Apply these changes to the initial concentrations and solve for the equilibrium concentrations.
Le Châtelier’s Principle
Principle Statement: This principle provides a qualitative way to predict how a system at equilibrium will respond to changes in concentration, pressure, and temperature.
Response to Stress: If an external change (stress) is applied to a system at equilibrium, the system will adjust (shift) in a direction that counteracts or relieves the stress.
Types of Stresses:
Change in Concentration: Adding or removing reactants or products will shift the equilibrium position to favor the side that counteracts the change.
Change in Pressure: Increasing pressure favors the side of the reaction with fewer gas molecules, while decreasing pressure favors the side with more gas molecules.
Change in Temperature: For exothermic reactions, increasing temperature shifts the equilibrium to favor reactants (left), while decreasing temperature favors products (right). For endothermic reactions, the reverse is true.

''',

'''

Models for Acids and Bases
1. Arrhenius Model

Definition:
Acids: Substances that produce hydrogen ions (
H
+
H 
+
 ) in solution.
Bases: Substances that produce hydroxide ions (
OH
−
OH 
−
 ) in solution.
2. Brønsted–Lowry Model

Acid: Defined as a proton donor.
Base: Defined as a proton acceptor.
Reaction with Water: An acid reacts with a water molecule (acting as a base):
HA (aq)
+
H
2
O (l)
⇌
H
3
O
+
(
a
q
)
+
A
−
(
a
q
)
HA (aq)+H 
2
​	
 O (l)⇌H 
3
​	
 O 
+
 (aq)+A 
−
 (aq)
This reaction produces a conjugate acid (
H
3
O
+
H 
3
​	
 O 
+
 ) and a conjugate base (
A
−
A 
−
 ).
3. Lewis Model

Lewis Acid: An electron-pair acceptor.
Lewis Base: An electron-pair donor.
Acid–Base Equilibrium
Equilibrium Constant (
K
a
K 
a
​	
 ): The equilibrium constant for an acid dissociating (ionizing) in water is called 
K
a
K 
a
​	
 .
Expression for 
K
a
K 
a
​	
 :
K
a
=
[
H
3
O
+
]
[
A
−
]
[
HA
]
K 
a
​	
 = 
[HA]
[H 
3
​	
 O 
+
 ][A 
−
 ]
​	
 
Simplified as:
K
a
=
[
H
3
O
+
]
[
HA
]
K 
a
​	
 = 
[HA]
[H 
3
​	
 O 
+
 ]
​	
 
Note: The concentration of water 
[
H
2
O
]
[H 
2
​	
 O] is not included as it is assumed to be constant.
Acid Strength
Strong Acids:
Have very large 
K
a
K 
a
​	
  values.
Completely dissociate (ionize) in water.
The dissociation equilibrium position lies far to the right.
Strong acids have very weak conjugate bases.
Common strong acids:
Nitric acid 
[
HNO
3
(
a
q
)
]
[HNO 
3
​	
 (aq)]
Hydrochloric acid 
[
HCl
(
a
q
)
]
[HCl(aq)]
Sulfuric acid 
[
H
2
SO
4
(
a
q
)
]
[H 
2
​	
 SO 
4
​	
 (aq)]
Perchloric acid 
[
HClO
4
(
a
q
)
]
[HClO 
4
​	
 (aq)]
Weak Acids:
Have small 
K
a
K 
a
​	
  values.
Dissociate (ionize) to a slight extent.
The dissociation equilibrium position lies far to the left.
Weak acids have relatively strong conjugate bases.
Percent Dissociation:
Percent Dissociation
=
(
Amount Dissociated (mol/L)
Initial Concentration (mol/L)
)
×
100
%
Percent Dissociation=( 
Initial Concentration (mol/L)
Amount Dissociated (mol/L)
​	
 )×100%
A smaller percent dissociation indicates a weaker acid.
Dilution of a weak acid increases its percent dissociation.
Autoionization of Water
Amphoteric Nature: Water can act as both an acid and a base.
Self-Reaction:
H
2
O (l)
+
H
2
O (l)
⇌
H
3
O
+
(
a
q
)
+
OH
−
(
a
q
)
H 
2
​	
 O (l)+H 
2
​	
 O (l)⇌H 
3
​	
 O 
+
 (aq)+OH 
−
 (aq)
Equilibrium Expression:
K
w
=
[
H
3
O
+
]
[
OH
−
]
K 
w
​	
 =[H 
3
​	
 O 
+
 ][OH 
−
 ]
Ion-Product Constant for Water: At 25°C, 
[
H
+
]
=
[
O
H
−
]
=
1.0
×
10
−
7
[H 
+
 ]=[OH 
−
 ]=1.0×10 
−7
 , so 
K
w
=
1.0
×
10
−
14
K 
w
​	
 =1.0×10 
−14
 .
Solution Classifications:
Acidic Solution: 
[
H
+
]
>
[
O
H
−
]
[H 
+
 ]>[OH 
−
 ]
Basic Solution: 
[
O
H
−
]
>
[
H
+
]
[OH 
−
 ]>[H 
+
 ]
Neutral Solution: 
[
H
+
]
=
[
O
H
−
]
[H 
+
 ]=[OH 
−
 ]
The pH Scale
Definition:
pH
=
−
log
⁡
[
H
+
]
pH=−log[H 
+
 ]
Logarithmic Scale:
pH changes by 1 unit for every 10-fold change in 
[
H
+
]
[H 
+
 ].
Similar log scales apply for 
[
OH
−
]
[OH 
−
 ] and 
K
a
K 
a
​	
 :
pOH
=
−
log
⁡
[
OH
−
]
,
pK
a
=
−
log
⁡
K
a
pOH=−log[OH 
−
 ],pK 
a
​	
 =−logK 
a
​	
 
Bases
Strong Bases: Typically hydroxide salts such as sodium hydroxide 
[
NaOH
]
[NaOH] and potassium hydroxide 
[
KOH
]
[KOH].
Weak Bases: React with water to produce hydroxide ions:
B (aq)
+
H
2
O (l)
⇌
BH
+
(
a
q
)
+
OH
−
(
a
q
)
B (aq)+H 
2
​	
 O (l)⇌BH 
+
 (aq)+OH 
−
 (aq)
Equilibrium Constant for Weak Bases (
K
b
K 
b
​	
 ):
K
b
=
[
BH
+
]
[
OH
−
]
[
B
]
K 
b
​	
 = 
[B]
[BH 
+
 ][OH 
−
 ]
​	
 
In water, a weak base 
B
B is always competing with hydroxide ions for protons, leading to generally small 
K
b
K 
b
​	
  values.

Polyprotic Acids
Definition: A polyprotic acid is an acid that can donate more than one proton (
H
+
H 
+
 ) per molecule.
Dissociation Process:
Polyprotic acids dissociate one proton at a time through multiple ionization steps.
Characteristic 
K
a
K 
a
​	
  Values:
Each step of dissociation has a specific equilibrium constant, denoted as 
K
a
1
K 
a1
​	
 , 
K
a
2
K 
a2
​	
 , etc.
Typically, for a weak polyprotic acid:
K
a
1
>
K
a
2
>
K
a
3
K 
a1
​	
 >K 
a2
​	
 >K 
a3
​	
 
Unique Case of Sulfuric Acid:
Sulfuric acid (
H
2
SO
4
H 
2
​	
 SO 
4
​	
 ) is notable because:
The first dissociation step is strong (
K
a
1
K 
a1
​	
  is very large), leading to complete ionization.
The second dissociation step is weak, characterized by a smaller 
K
a
2
K 
a2
​	
 .
Acid–Base Properties of Salts
Solution Types: Salts can produce acidic, basic, or neutral solutions in water based on their constituent ions.
Neutral Solutions:
Formed by salts that contain:
Cations from strong bases and anions from strong acids.
Basic Solutions:
Formed by salts that contain:
Cations from strong bases and anions from weak acids.
Acidic Solutions:
Formed by salts that contain:
Cations from weak bases and anions from strong acids.
Also produced by salts containing highly charged metal cations, such as:
Al
3
+
Al 
3+
  and 
Fe
3
+
Fe 
3+
 .
Effect of Structure on Acid–Base Properties
Functional Group: Many substances that act as acids or bases contain the 
HOOX
HOOX grouping, where 
X
X represents another atom or group.
Acid Behavior:
Molecules with a strong and covalent 
OX
OX bond tend to exhibit acidic behavior, effectively donating protons.
As the electronegativity of 
X
X increases, the strength of the acid generally increases.
Base Behavior:
When the 
OX
OX bond is more ionic, the substance tends to behave as a base, releasing hydroxide ions (
OH
−
OH 
−
 ) when dissolved in water.

''',

'''

Buffered Solutions
Definition: A buffered solution contains either a weak acid (
HA
HA) and its salt (e.g., 
NaA
NaA) or a weak base (
B
B) and its salt (e.g., 
BHCl
BHCl).
Function: Buffered solutions resist changes in pH when small amounts of 
H
+
H 
+
  or 
OH
−
OH 
−
  are added.
Henderson–Hasselbalch Equation:
For a buffered solution containing 
HA
HA and its conjugate base 
A
−
A 
−
 , the pH can be calculated using the Henderson–Hasselbalch equation:
pH
=
p
K
a
+
log
⁡
(
[
A
−
]
[
HA
]
)
pH=pK 
a
​	
 +log( 
[HA]
[A 
−
 ]
​	
 )
Buffer Capacity:
The capacity of the buffered solution depends on the concentrations of 
HA
HA and 
A
−
A 
−
 present.
The most efficient buffering occurs when the ratio of 
[
HA
]
[HA] to 
[
A
−
]
[A 
−
 ] is close to 1.
Mechanism of Buffering:
Buffering works because the amounts of 
HA
HA (which reacts with added 
OH
−
OH 
−
 ) and 
A
−
A 
−
 (which reacts with added 
H
+
H 
+
 ) are large enough to maintain the 
[
HA
]
[HA] to 
[
A
−
]
[A 
−
 ] ratio, preventing significant changes in pH upon the addition of strong acids or bases.
Acid-Base Titrations
Titration Process:
The progress of a titration is represented by plotting the pH of the solution versus the volume of added titrant. The resulting graph is called a pH curve or titration curve.
Strong Acid–Strong Base Titrations:
These titrations exhibit a sharp change in pH near the equivalence point, where stoichiometric amounts of acid and base have reacted.
Titration Curve Shapes:
The shape of the pH curve for a strong base–weak acid titration differs significantly from that of a strong acid–strong base titration.
For a strong base–weak acid titration, the pH at the equivalence point is greater than 7 due to the basic properties of the conjugate base 
A
−
A 
−
 .
Indicators:
Indicators are substances used to mark the equivalence point of an acid-base titration.
The end point of the titration is where the indicator changes color.
The goal is to have the end point and the equivalence point coincide as closely as possible to ensure accurate titration results.

''',

'''

Solids Dissolving in Water
Slightly Soluble Salts:
For a slightly soluble salt (e.g., 
MX
MX), an equilibrium is established between the excess solid and the ions in solution:
MX (s)
⇌
M
+
(
a
q
)
+
X
−
(
a
q
)
MX (s)⇌M 
+
 (aq)+X 
−
 (aq)
Solubility Product Constant (
K
s
p
K 
sp
​	
 ):
The corresponding equilibrium constant for this dissolution is known as the solubility product constant (
K
s
p
K 
sp
​	
 ):
K
s
p
=
[
M
+
]
[
X
−
]
K 
sp
​	
 =[M 
+
 ][X 
−
 ]
Common Ion Effect:
The solubility of 
MX
(
s
)
MX(s) is decreased by the presence of another source of either 
M
+
M 
+
  or
X
−
X 
−
 . This phenomenon is referred to as the common ion effect.
Predicting Precipitation:
To determine whether precipitation will occur when two solutions are mixed, calculate the reaction quotient (
Q
Q) for the initial concentrations:
If 
Q
>
K
s
p
Q>K 
sp
​	
 , precipitation occurs.
If 
Q
≤
K
s
p
Q≤K 
sp
​	
 , no precipitation occurs.
Qualitative Analysis
Selective Precipitation:
A mixture of ions can be separated through selective precipitation, which involves the following steps:
Group Separation:
Ions are first grouped by adding hydrochloric acid (
HCl (aq)
HCl (aq)), followed by hydrogen sulfide (
H
2
S (aq)
H 
2
​	
 S (aq)), sodium hydroxide (
NaOH (aq)
NaOH (aq)), and sodium carbonate (
Na
2
CO
3
(
a
q
)
Na 
2
​	
 CO 
3
​	
 (aq)).
Identification:
The ions in each group are then further separated and identified using additional selective dissolution and precipitation methods.
Complex Ions
Definition:
Complex ions are formed from a metal ion surrounded by attached ligands.
Ligands:
A ligand is a Lewis base that donates a pair of electrons to the metal ion.
Coordination Number:
The number of ligands attached to the metal ion is known as the coordination number, which is typically 2, 4, or 6.
Equilibria in Solution:
Complex ion equilibria in solution are described by formation (stability) constants, indicating the stability of the complex ion.
Application in Qualitative Analysis:
The formation of complex ions can be utilized to selectively dissolve solids within the qualitative analysis framework, aiding in the separation and identification of ions.

''',

'''

First Law of Thermodynamics
Energy Conservation:
The first law states that the energy of the universe is constant. It emphasizes that energy cannot be created or destroyed, only transformed from one form to another.
Energy Tracking:
This law provides a framework to keep track of energy changes as they occur in various processes.
Direction of Processes:
It does not provide information regarding why a particular process occurs in a specific direction.
Second Law of Thermodynamics
Entropy and Spontaneous Processes:
The second law states that for any spontaneous (thermodynamically favored) process, there is always an increase in the entropy of the universe.
Entropy (
S
S):
Entropy is a thermodynamic function that quantifies the number of arrangements (positions and/or energy levels) available to a system in a given state.
Natural Progression:
Nature tends to spontaneously move toward states with the highest probability of occurring, indicating a preference for disorder or higher entropy.
Predicting Direction:
Using entropy, thermodynamics can predict the direction in which a process will spontaneously occur:
Δ
S
u
n
i
v
=
Δ
S
s
y
s
+
Δ
S
s
u
r
r
ΔS 
univ
​	
 =ΔS 
sys
​	
 +ΔS 
surr
​	
 
For a spontaneous process, 
Δ
S
u
n
i
v
ΔS 
univ
​	
  must be positive.
Entropy Contributions:
At constant temperature and pressure:
Δ
S
s
y
s
ΔS 
sys
​	
  is primarily influenced by “positional” entropy.
For chemical reactions, 
Δ
S
s
y
s
ΔS 
sys
​	
  is dominated by changes in the number of gaseous molecules.
Surroundings and Heat:
Δ
S
s
u
r
r
ΔS 
surr
​	
  is determined by heat:
Δ
S
s
u
r
r
=
−
Δ
H
T
ΔS 
surr
​	
 =− 
T
ΔH
​	
 
Δ
S
s
u
r
r
ΔS 
surr
​	
  is positive for exothermic processes (where 
Δ
H
ΔH is negative).
Temperature Dependency:
Since 
Δ
S
s
u
r
r
ΔS 
surr
​	
  depends inversely on temperature, exothermicity becomes a more significant driving force at lower temperatures.
Rate of Processes:
Thermodynamics cannot predict the rate at which a system will spontaneously change; principles of kinetics are required for that.
Third Law of Thermodynamics
Entropy at Absolute Zero:
The third law states that the entropy of a perfect crystal at absolute zero (0 K) is zero, indicating that there is only one microstate available at this temperature.
Free Energy (
G
G)
Definition and Spontaneity:
Free energy is a state function that indicates the spontaneity of processes at constant temperature and pressure:
G
=
H
−
T
S
G=H−TS
A process is spontaneous in the direction in which its free energy decreases (
Δ
G
<
0
ΔG<0).
Standard Free Energy Change:
The standard free energy change (
Δ
G
∘
ΔG 
∘
 ) is the change in free energy that occurs when reactants in their standard states are converted to products in their standard states.
Calculating Standard Free Energy Change:
The standard free energy change for a reaction can be calculated from the standard free energies of formation (
Δ
G
f
∘
ΔG 
f
∘
​	
 ):
Δ
G
∘
=
∑
Δ
G
p
r
o
d
u
c
t
s
∘
−
∑
Δ
G
r
e
a
c
t
a
n
t
s
∘
ΔG 
∘
 =∑ΔG 
products
∘
​	
 −∑ΔG 
reactants
∘
​	
 
Temperature and Pressure Dependence:
Free energy also depends on temperature and pressure:
G
=
G
∘
+
R
T
ln
⁡
P
G=G 
∘
 +RTlnP
Relationship with Equilibrium Constant:
This relationship allows for the derivation of the connection between 
Δ
G
∘
ΔG 
∘
  for a reaction and its equilibrium constant (
K
K):
Δ
G
∘
=
−
R
T
ln
⁡
K
ΔG 
∘
 =−RTlnK
Where:
Δ
G
∘
=
0
ΔG 
∘
 =0 implies 
K
=
1
K=1
Δ
G
∘
<
0
ΔG 
∘
 <0 implies 
K
>
1
K>1
Δ
G
∘
>
0
ΔG 
∘
 >0 implies 
K
<
1
K<1
Maximum Work:
The maximum possible useful work obtainable from a process at constant temperature and pressure is equal to the change in free energy:
w
m
a
x
=
Δ
G
w 
max
​	
 =ΔG
Energy Use in Real Processes:
When energy is utilized to do work in a real process, the total energy of the universe remains constant, but the usefulness of that energy diminishes.
Energy Distribution:
Concentrated energy disperses in the surroundings as thermal energy.

''',

'''

Electrochemistry
❯ The study of the interchange of chemical and electrical energy
❯ Uses oxidation–reduction reactions
❯ Galvanic cell: chemical energy is transformed into electrical energy by separating the oxi- dizing and reducing agents and forcing the electrons to travel through a wire
❯ Electrolytic cell: electrical energy is used to produce a chemical change Galvanic cell
❯ Anode: the electrode where oxidation occurs
❯ Cathode: the electrode where reduction occurs
❯ The driving force behind the electron transfer is called the cell potential (%cell)
❯ The potential is measured in units of volts (V), defined as a joule of work per coulomb of charge:
2work 1J2 w %1V2 5 charge 1C2 5 2q
❯ A system of half-reactions, called standard reduction potentials, can be used to calculate the potentials of various cells
❯ The half-reaction 2H1 1 2e2 h H2 is arbitrarily assigned a potential of 0 V Free energy and work
❯ The maximum work that a cell can perform is
2wmax 5 q%max
where %max represents the cell potential when no current is flowing
❯ The actual work obtained from a cell is always less than the maximum because energy is lost
through frictional heating of the wire when current flows
❯ For a process carried out at constant temperature and pressure, the change in free energy equals the maximum useful work obtainable from that process:
DG 5 wmax 5 2q%max 5 2nF%
where F (faraday) equals 96,485 C and n is the number of moles of electrons transferred in
the process
Concentration cell
❯ A galvanic cell in which both compartments have the same components but at different concentrations
❯ The electrons flow in the direction that tends to equalize the concentrations Nernst equation
❯ Shows how the cell potential depends on the concentrations of the cell components: %5%0 20.0591logQ at25°C
n
❯ When a galvanic cell is at equilibrium, % 5 0 and Q 5 K
Batteries
❯ A battery consists of a galvanic cell or group of cells connected in series that serve as a source of direct current.
❯ Lead storage battery
❯ Anode: lead
❯ Cathode: lead coated with PbO2
❯ Electrolyte: H2SO4(aq)
❯ Dry cell battery
❯ Contains a moist paste instead of a liquid electrolyte
❯ Anode: usually Zn
❯ Cathode: carbon rod in contact with an oxidizing agent (which varies depending on the
application)
Fuel cells
❯ Galvanic cells in which the reactants are continuously supplied
❯ The H2/O2 fuel cell is based on the reaction between H2 and O2 to form water
Corrosion
❯ Involves the oxidation of metals to form mainly oxides and sulfides
❯ Some metals, such as aluminum and chromium, form a thin, protective oxide coating that
prevents further corrosion
❯ The corrosion of iron to form rust is an electrochemical process
❯ The Fe21 ions formed at anodic areas of the surface migrate through the moisture layer to cathodic regions, where they react with oxygen from the air
❯ Iron can be protected from corrosion by coating it with paint or with a thin layer of metal such as chromium, tin, or zinc; by alloying; and by cathodic protection
Electrolysis
❯ Used to place a thin coating of metal onto steel
❯ Used to produce pure metals such as aluminum and copper

''',

'''

Radioactivity
❯ Certain nuclei decay spontaneously into more stable nuclei ❯ Types of radioactive decay:
❯ a-particle 142He2 production ❯ b-particle 1 0e2 production
21
❯ Positron 10e2 production
1
❯ g rays are usually produced in a radioactive decay event
❯ A decay series involves several radioactive decays to finally reach a stable nuclide ❯ Radioactive decay follows first-order kinetics
❯ Half-life of a radioactive sample: the time required for half of the nuclides to decay
❯ The transuranium elements (those beyond uranium in the periodic table) can be synthesized
by particle bombardment of uranium or heavier elements
❯ Radiocarbon dating uses the 146C@126C ratio in an object to establish its date of origin
Thermodynamic stability of a nucleus
❯ Compares the mass of a nucleus to the sum of the masses of its component nucleons
❯ When a system gains or loses energy, it also gains or loses mass as described by the relation-
ship E 5 mc2
❯ The difference between the sum of the masses of the component nucleons and the actual mass
of a nucleus (called the mass defect) can be used to calculate the nuclear binding energy
Nuclear energy production
❯ Fusion: the process of combining two light nuclei to form a heavier, more stable nucleus
❯ Fission: the process of splitting a heavy nucleus into two lighter, more stable nuclei
❯ Current nuclear power reactors use controlled fission to produce energy Radiation damage
❯ Radiation can cause direct (somatic) damage to a living organism or genetic damage to the organism’s offspring
❯ The biological effects of radiation depend on the energy, the penetrating ability, the ionizing ability of the radiation, and the chemical properties of the nuclide producing the radiation

''',

'''

Representative elements
❯ Chemical properties are determined by their s and p valence-electron configurations
❯ Metallic character increases going down the group
❯ The properties of the first element in a group usually differ most from the properties of the other elements in the group due to a significant difference in size
❯ In Group 1A, hydrogen is a nonmetal and the other members of the group are active metals
❯ The first member of a group forms the strongest p bonds, causing nitrogen and oxygen to exist as N2 and O2 molecules
Elemental abundances on earth
❯ Oxygen is the most abundant element, followed by silicon
❯ The most abundant metals are aluminum and iron, which are found as ores
Group 1A elements (alkali metals)
❯ Have valence configuration ns1
❯ Except for hydrogen, readily lose one electron to form M1 ions in their compounds with
nonmetals
❯ React vigorously with water to form M1 and OH2 ions and hydrogen gas
❯ Form a series of oxides of the types M2O (oxide), M2O2 (peroxide), and MO2 (superoxide)
❯ Not all metals form all types of oxide compounds
❯ Hydrogen forms covalent compounds with nonmetals
❯ With very active metals, hydrogen forms hydrides that contain the H2 ion
Group 2A (alkaline earth metals)
❯ Have valence configuration ns2
❯ React less violently with water than alkali metals
❯ The heavier alkaline earth metals form nitrides and hydrides
❯ Hard water contains Ca21 and Mg21 ions
❯ Form precipitates with soap
❯ Usually removed by ion-exchange resins that replace the Ca21 and Mg21 ions with Na1
Group 3A
❯ Have valence configuration ns2np1
❯ Show increasing metallic character going down the group
❯ Boron is a nonmetal that forms many types of covalent compounds, including boranes, which are highly electron-deficient and thus are very reactive
❯ The metals aluminum, gallium, and indium show some covalent tendencies Group 4A
❯ Have valence configuration ns2np2
❯ Lighter members are nonmetals; heavier members are metals
❯ All group members can form covalent bonds to nonmetals
❯ Carbon forms a huge variety of compounds, most of which are classified as organic compounds
Group 5A
❯ Elements show a wide variety of chemical properties
❯ Nitrogen and phosphorus are nonmetals
❯ Antimony and bismuth tend to be metallic, although no ionic compounds containing Sb51 and
Bi51 are known; the compounds containing Sb(V) and Bi(V) are molecular rather than ionic
❯ All group members except N form molecules with five covalent bonds
❯ The ability to form p bonds decreases dramatically after N
❯ Chemistry of nitrogen
❯ Most nitrogen-containing compounds decompose exothermically, forming the very stable
N2 molecule, which explains the power of nitrogen-based explosives
❯ The nitrogen cycle, which consists of a series of steps, shows how nitrogen is cycled in the natural environment
❯ Nitrogen fixation changes the N2 in air into compounds useful to plants
❯ The Haber process is a synthetic method of nitrogen fixation
❯ In the natural world, nitrogen fixation occurs through nitrogen-fixing bacteria in the
root nodules of certain plants and through lightning in the atmosphere
❯ Ammonia is the most important hydride of nitrogen
❯ Contains pyramidal NH3 molecules
❯ Widely used as a fertilizer
❯ Hydrazine (N2H4) is a powerful reducing agent
❯ Nitrogen forms a series of oxides including N2O, NO, NO2, and N2O5
❯ Nitric acid (HNO3) is a very important strong acid manufactured by the Ostwald process
❯ Chemistry of phosphorus
❯ Exists in three elemental forms: white (contains P4 molecules), red, and black
❯ Phosphine (PH3) has bond angles close to 90 degrees
❯ Phosphorus forms oxides including P4O6 and P4O10 (which dissolves in water to form
phosphoric acid, H3PO4)
Group 6A
❯ Metallic character increases going down the group but no element behaves as a typical metal
❯ The lighter members tend to gain two electrons to form X22 ions in compounds with metals
❯ Chemistry of oxygen
❯ Elemental forms are O2 and O3
❯ Oxygen forms a wide variety of oxides
❯ O2 and especially O3 are powerful oxidizing agents
❯ Chemistry of sulfur
❯ The elemental forms are called rhombic and monoclinic sulfur, both of which contain S8
molecules
❯ The most important oxides are SO2 (which forms H2SO3 in water) and SO3 (which forms H2SO4 in water)
❯ Sulfur forms a wide variety of compounds in which it shows the oxidation states 16, 14, 12, 0, and 22
Group 7A (halogens)
❯ All nonmetals
❯ Form hydrides of the type HX that behave as strong acids in water except for HF, which is a
weak acid
❯ The oxyacids of the halogens become stronger as more oxygen atoms are present
Group 8A (noble gases)
❯ All elements are monatomic gases and are generally very unreactive
❯ The heavier elements form compounds with electronegative elements such as fluorine and
oxygen
''',

'''

First-row transition metals (scandium–zinc)
❯ All have one or more electrons in the 4s orbital and various numbers of 3d electrons ❯ All exhibit metallic properties
❯ A particular element often shows more than one oxidation state in its compounds
❯ Most compounds are colored, and many are paramagnetic
❯ Most commonly form coordination compounds containing a complex ion involving ligands (Lewis bases) attached to a central transition metal ion
❯ The number of attached ligands (called the coordination number) can vary from 2 to 8, with 4 and 6 being most common
❯ Many transition metal ions have major biological importance in molecules such as enzymes and those that transport and store oxygen
❯ Chelating ligands form more than one bond to the transition metal ion
Isomerism
❯ Isomers: two or more compounds with the same formula but different properties
❯ Coordination isomerism: the composition of the coordination sphere varies
❯ Linkage isomerism: the point of attachment of one or more ligands varies
❯ Stereoisomerism: isomers have identical bonds but different spatial arrangements
❯ Geometric isomerism: ligands assume different relative positions in the coordination sphere; examples are cis and trans isomers
❯ Optical isomerism: molecules with nonsuperimposable mirror images rotate plane- polarized light in opposite directions
Spectral and magnetic properties
❯ Usually explained in terms of the crystal field model
❯ Model assumes the ligands are point charges that split the energies of the 3d orbitals
❯ Color and magnetism are explained in terms of how the 3d electrons occupy the split 3d energy levels
❯ Strong-field case: relatively large orbital splitting
❯ Weak-field case: relatively small orbital splitting
Metallurgy
❯ The processes connected with separating a metal from its ore
❯ The minerals in ores are often converted to oxides (roasting) before being reduced to the
metal (smelting)
❯ The metallurgy of iron: most common method for reduction uses a blast furnace; process involves iron ore, coke, and limestone
❯ Impure product (,90% iron) is called pig iron
❯ Steel is manufactured by oxidizing the impurities in pig iron

'''

]

bio_text = [

'''

Concept 3.1: Carbon atoms can form diverse molecules by bonding to four other atoms Carbon, with a valence of 4, can bond to various other atoms, including O, H, N. Carbon can also bond to other carbon atoms, forming the carbon skeletons of organic compounds. These skeletons vary in length and shape.
Chemical groups attached to the carbon skeletons of organic molecules participate in chemical reactions (functional groups) or contribute to function by affecting molecular shape.
ATP (adenosine triphosphate) can react with water, releasing energy that can be used by the cell.

''',

'''

Concept 3.2: Macromolecules are polymers, built from monomers
Proteins, nucleic acids, and large carbohydrates (polysaccharides) are polymers, which are chains of monomers. Monomers form larger molecules by dehydration reactions, in which water molecules are released.
Polymers can disassemble by the reverse process, hydrolysis. In cells, dehydration reactions and hydrolysis are catalyzed by enzymes. An immense variety of polymers can be built from a small set of monomers.

''',

'''
Concept 3.3: Carbohydrates serve as fuel and building material
Monosaccharides: glucose, fructose → Fuel; carbon sources that can be converted to other molecules or combined into polymers.
Disaccharides: lactose, sucrose.
Polysaccharides:
Cellulose (plants) → Strengthens plant cell walls.
Starch (plants) → Stores glucose for energy in plants.
Glycogen (animals) → Stores glucose for energy in animals.
Chitin (animals and fungi) → Strengthens exoskeletons and fungal cell walls.

''',

'''
Concept 3.4: Lipids are a diverse group of hydrophobic molecules
Triacylglycerols (fats or oils): glycerol + 3 fatty acids → Important energy source.
Phospholipids: phosphate group + glycerol + 2 fatty acids → Lipid bilayers of membranes.
Steroids: four fused rings with attached chemical groups → Component of cell membranes (cholesterol), signaling molecules that travel through the body (hormones).

''',

'''
Concept 3.5: Proteins include a diversity of structures, resulting in a wide range of functions
Proteins are composed of amino acid monomers (20 types).
Functions of proteins:
Enzymes → Catalyze chemical reactions.
Structural proteins → Provide structural support.
Storage proteins → Store amino acids.
Transport proteins → Transport substances.
Hormones → Coordinate organismal responses.
Receptor proteins → Receive signals from outside the cell.
Motor proteins → Function in cell movement.
Defensive proteins → Protect against disease.

''',

'''
Concept 3.6: Nucleic acids store, transmit, and help express hereditary information

DNA:
Sugar = deoxyribose.
Nitrogenous bases = C, G, A, T.
Usually double-stranded.
Function: Stores hereditary information.
RNA:
Sugar = ribose.
Nitrogenous bases = C, G, A, U.
Usually single-stranded.
Function: Various functions in gene expression, including carrying instructions from DNA to ribosomes.

''',

'''
CONCEPT 4.1
Biologists use microscopes and the tools of
biochemistry to study cells (pp. 67–69)
• Improvements in microscopy that affect the parameters of mag- nification, resolution, and contrast have catalyzed progress in the study of cell structure. The light microscope (LM) and electron microscope (EM), as well as other types, remain important tools.
• Cell biologists can obtain pellets enriched in particular cellular com- ponentsbycentrifugingdisruptedcellsatsequentialspeeds,apro- cess known as cell fractionation. Larger cellular components are in the pellet after lower-speed centrifugation, and smaller components are in the pellet after higher-speed centrifugation.

''',

'''

CONCEPT 4.2
Eukaryotic cells have internal membranes that
compartmentalize their functions (pp. 69–74)
• All cells are bounded by a plasma membrane.
• Prokaryotic cells lack nuclei and other membrane-enclosed
organelles, while eukaryotic cells have internal membranes that
compartmentalize cellular functions.
• The surface-to-volume ratio is an important parameter affecting
cell size and shape.
• Plantandanimalcellshavemostofthesameorganelles:anucleus,
endoplasmic reticulum, Golgi apparatus, and mitochondria. Some organelles are found only in plant or in animal cells. Chloroplasts are present only in cells of photosynthetic eukaryotes.

''',

'''

CONCEPT 4.3
The eukaryotic cell’s genetic instructions are housed in the nucleus and carried out by the ribosomes (pp. 74–76)


Nucleus structure: Surrounded by nuclear envelope (double membrane) perforated by nuclear pores; nuclear envelope continuous with endoplasmic reticulum (ER)

Nucleus function: Houses chromosomes, which are made of chromatin (DNA and proteins); contains nucleoli, where ribosomal subunits are made; pores regulate entry and exit of materials.

Ribosome structure: Two subunits made of ribosomal RNA and proteins; can be free in cytosol or bound to ER

Ribosome function: Protein synthesis

''',

'''

CONCEPT 4.4: The endomembrane system

Endoplasmic Reticulum
- Structure: Extensive network of membrane-bounded tubules and sacs; membrane separates lumen from cytosol; continuous with nuclear envelope
- Function: Smooth ER: synthesis of lipids, metabolism of carbohydrates, Ca2+ storage, detoxification of drugs and poisons, Rough ER: aids in synthesis of secretory and other proteins
from bound ribosomes; adds carbohydrates to proteins to make glycoproteins; produces new membrane

''',

'''

CONCEPT 4.5 Mitochondria and Chloroplasts

Mitochondrion
Bounded by double membrane; inner membrane has infoldings (cristae)
Function: Cellular respiration
Chloroplast
Typically two membranes around fluid stroma, which contains thylakoids stacked into grana (in cells of photosynthetic eukaryotes, including plants)
Function: Photosynthesis
Peroxisome
Specialized metabolic compartment bounded by a single membrane
Function: Contains enzymes that transfer hydrogen atoms from certain molecules to oxygen, producing hydrogen peroxide (H₂O₂) as a by-product; H₂O₂ is converted to water by another enzyme

''',

'''

CONCEPT 4.6

The cytoskeleton is a network of fibers that organizes structures and activities in the cell (pp. 84–88)
• The cytoskeleton functions in structural support for the cell and in motility and signal transmission.
• Microtubules shape the cell, guide organelle movement, and separate chromosomes in dividing cells. Cilia and flagella are motile appendages containing microtubules. Primary cilia play sensory and signaling roles. Microfilaments are thin rods func- tioning in muscle contraction, amoeboid movement, cytoplasmic streaming, and support of microvilli. Intermediate filaments support cell shape and fix organelles in place.

''',

'''

CONCEPT 4.7

Extracellular components and connections between
cells help coordinate cellular activities (pp. 88–91)
• Plant cell walls are made of cellulose fibers embedded in other polysaccharides and proteins.
• Animal cells secrete glycoproteins and proteoglycans that form the extracellular matrix (ECM), which functions in support, adhesion, movement, and regulation.
• Cell junctions connect neighboring cells in plants and animals. Plants have plasmodesmata that pass through adjoining cell walls. Animal cells have tight junctions, desmosomes, and gap junctions.

''',

'''

Concept 5.1

Cellular membranes are fluid mosaics of lipids and proteins (pp. 94–98)

In the fluid mosaic model, amphipathic proteins are embedded in the phospholipid bilayer.
Phospholipids and some proteins move laterally within the membrane. The unsaturated hydrocarbon tails of some phospholipids keep membranes fluid at lower temperatures, while cholesterol helps membranes resist changes in fluidity caused by temperature changes.
Membrane proteins function in transport, enzymatic activity, attachment to the cytoskeleton and extracellular matrix, cell-cell recognition, intercellular joining, and signal transduction.
Short chains of sugars linked to proteins (in glycoproteins) and lipids (in glycolipids) on the exterior side of the plasma membrane interact with surface molecules of other cells.
Membrane proteins and lipids are synthesized in the ER and modified in the ER and Golgi apparatus. The inside and outside faces of membranes differ in molecular composition.


''',

'''

Concept 5.2

Membrane structure results in selective permeability (p. 99)

A cell must exchange substances with its surroundings, a process controlled by the selective permeability of the plasma membrane.
Hydrophobic molecules pass through membranes rapidly, whereas polar molecules and ions usually need specific transport proteins.

''',

'''

Concept 5.3

Passive transport is diffusion of a substance across a membrane with no energy investment (pp. 99–103)

Diffusion is the spontaneous movement of a substance down its concentration gradient.
Water diffuses out through the permeable membrane of a cell (osmosis) if the solution outside has a higher solute concentration than the cytosol (is hypertonic), whereas water enters the cell if the solution has a lower solute concentration (is hypotonic).
If the concentrations are equal (isotonic), no net osmosis occurs. Cell survival depends on balancing water uptake and loss.
In facilitated diffusion, a transport protein speeds the movement of water or a solute across a membrane down its concentration gradient.
Ion channels facilitate the diffusion of ions across a membrane. Carrier proteins can undergo changes in shape that transport bound solutes.

''',

'''

Concept 5.4

Active transport uses energy to move solutes against their gradients (pp. 103–106)

Specific membrane proteins use energy, usually in the form of ATP, to do the work of active transport.
Ions can have both a concentration (chemical) gradient and an electrical gradient (voltage). These combine in the electrochemical gradient, which determines the net direction of ionic diffusion.
Cotransport of two solutes occurs when a membrane protein enables the “downhill” diffusion of one solute to drive the “uphill” transport of the other.

''',

'''

Concept 5.5

Bulk transport across the plasma membrane occurs by exocytosis and endocytosis (pp. 106–107)

Three main types of endocytosis are phagocytosis, pinocytosis, and receptor-mediated endocytosis.

''',

'''

Concept 5.6

The plasma membrane plays a key role in most cell signaling (pp. 108–113)

In local signaling, animal cells may communicate by direct contact or by secreting local regulators.
For long-distance signaling, both animals and plants use hormones; animals also signal electrically.
Signaling molecules that bind to membrane receptors trigger a three-stage cell-signaling pathway:
Reception
Transduction
Response
In reception, a signaling molecule binds to a receptor protein, causing the protein to change shape.
Two major types of membrane receptors are G protein-coupled receptors (GPCRs), which work with the help of cytoplasmic G proteins, and ligand-gated ion channels, which open or close in response to binding by signaling molecules. Signaling molecules that are hydrophobic cross the plasma membrane and bind to receptors inside the cell.
At each step in a signal transduction pathway, the signal is transduced into a different form, which commonly involves a change in a protein’s shape. Many pathways include phosphorylation cascades, in which a series of protein kinases each add a phosphate group to the next one in line, activating it. The balance between phosphorylation and dephosphorylation, by protein phosphatases, regulates the activity of proteins in the pathway.
Second messengers, such as the small molecule cyclic AMP (cAMP), diffuse readily through the cytosol and thus help broadcast signals quickly. Many G proteins activate the enzyme that makes cAMP from ATP.
The cell’s response to a signal may be the regulation of transcription in the nucleus or of an activity in the cytoplasm.

''',

'''

CONCEPT 7.1
Cellular membranes are fluid mosaics
of lipids and proteins (pp. 127-131)
■ In the fluid mosaic model, amphipathic proteins
are embedded in the phospholipid bilayer.
■ Phospholipids and some proteins move sideways
within the membrane. The unsaturated hydrocarbon tails of some phospholipids keep membranes fluid at lower temperatures, while cholesterol helps membranes resist changes in fluidity caused by temperature changes.
■ Membrane proteins function in transport, enzymatic activity, sig- nal transduction, cell-cell recognition, intercellular joining, and attachment to the cytoskeleton and extracellular matrix. Short chains of sugars linked to proteins (in glycoproteins) and lipids (in glycolipids) on the exterior side of the plasma membrane interact with surface molecules of other cells.
■ Membrane proteins and lipids are synthesized in the ER and modified in the ER and Golgi apparatus. The inside and outside faces of membranes differ in molecular composition.

''',

'''
CONCEPT 7.2
Membrane structure results in selective permeability (pp. 131-132)
■ A cell must exchange molecules and ions with its surroundings, a process controlled by the selective permeability of the plasma membrane. Hydrophobic substances are soluble in lipids and pass through membranes rapidly, whereas polar molecules and ions generally require specific transport proteins.

''',

'''
CONCEPT 7.3
Passive transport is diffusion of a substance across a membrane with no energy investment (pp. 132-136)
■ Diffusion is the spontaneous movement of a substance down its concentration gradient. Water diffuses out through the per- meable membrane of a cell (osmosis) if the solution outside has
a higher solute concentration (hypertonic) than the cytosol; water enters the cell if the solution has a lower solute concentra- tion (hypotonic). If the concentrations are equal (isotonic), no net osmosis occurs. Cell survival depends on balancing water uptake and loss. ■In facilitated
diffusion, a transport protein speeds the movement of water or a solute across a mem- brane down its concen- tration gradient. Ion channels facilitate the diffusion of ions across a membrane. Carrier proteins can undergo changes in shape that translocate bound solutes across the membrane.
Passive transport: Facilitated diffusion
Channel protein
-Carrier protein

''',

'''
CONCEPT 7.4
Active transport uses energy to move solutes against their gradients
(pp. 136-139)
■ Specific membrane proteins use energy, usually in the form of ATP, to do the work of active transport.
■Ions can have both a concentration (chemical) gradient and an electrical gra- dient (voltage). These gradients combine in the electrochemical gradient, which determines the net direction of ionic diffusion.
■ Cotransport of two solutes occurs when a membrane protein enables the "downhill" diffusion of one solute to drive the "uphill" transport of the other.

''',

'''
CONCEPT 7.5
Bulk transport across the plasma membrane
occurs by exocytosis and endocytosis (pp. 139–141)
■In exocytosis, transport vesicles migrate to the plasma membrane, fuse with it, and release their contents. In endocytosis, molecules enter cells within vesicles that pinch inward from the plasma membrane. The three types of endocytosis are phagocytosis, pinocytosis, and receptor-mediated endocytosis.

''',

'''

CONCEPT 8.1
An organism's metabolism transforms matter and energy, subject to the laws of thermodynamics (pp. 144-147)
■ Metabolism is the collection of chemical reactions that occur in an organism. Enzymes catalyze reactions in intersecting metabolic pathways, which may be catabolic (breaking down molecules, releasing energy) or anabolic (building molecules, consuming energy). Bioenergetics is the study of the flow of energy through living organisms.
■ Energy is the capacity to cause change; some forms of energy do work by moving matter. Kinetic energy is associated with motion and includes thermal energy associated with random motion of atoms or molecules. Heat is thermal energy in transfer from one object to another. Potential energy is related to the location or structure of matter and includes chemical energy possessed by a molecule due to its structure.
The first law of thermodynamics, conservation of energy, states that energy cannot be created or destroyed, only transferred or transformed. The second law of thermodynamics states that spontaneous processes, those requiring no outside input of energy, increase the entropy (molecular disorder) of the universe.

''',

'''

CONCEPT 8.2
The free-energy change of a reaction tells us whether or not the reaction occurs spontaneously (pp. 147-150)
■ A living system's free energy is energy that can do work under cellular conditions. The change in free energy (AG) during a bio- logical process is related directly to enthalpy change (AH) and to the change in entropy (AS): AG=AH-TAS. Organisms live at the expense of free energy. A spontaneous process occurs with no energy input; during such a process, free energy decreases and the stability of a system increases. At maximum stability, the system is at equilibrium and can do no work.
■ In an exergonic (spontaneous) chemical reaction, the products have less free energy than the reactants (-AG). Endergonic (nonspontaneous) reactions require an input of energy (+AG). The addition of starting materials and the removal of end prod- ucts prevent metabolism from reaching equilibrium.

''',

'''

CONCEPT 8.3
ATP powers cellular work by coupling exergonic reactions to endergonic reactions (pp. 150-153)
■ ATP is the cell's energy shuttle. Hydrolysis of its terminal phos- phate yields ADP and D, and releases free energy.
■ Through energy coupling, the exergonic process of ATP hydro- lysis drives endergonic reactions by transfer of a phosphate group to specific reactants, forming a phosphorylated intermediate
that is more reactive. ATP hydrolysis (sometimes with protein phosphorylation) also causes changes in the shape and binding affinities of transport and motor proteins.
■ Catabolic pathways drive regeneration of ATP from ADP+℗1.

''',

'''
CONCEPT 8.4
Enzymes speed up metabolic reactions
by lowering energy barriers (pp. 153-159)
In a chemical reaction, the energy necessary to break the bonds of the reactants is the activation energy, EA.
■ Enzymes lower the activaition energy barrier.
Each enzyme has a unique active site that binds one or more substrate(s), the reactants on which it acts. It then changes shape, binding the substrate(s) more tightly (induced fit). ■ The active site can lower an E, barrier by orienting substrates correctly, straining their bonds, providing a favorable micro- environment, or even covalently bonding with the substrate. Each enzyme has an optimal temperature and pH. Inhibitors reduce enzyme function. A competitive inhibitor binds to the active site, whereas a noncompetitive inhibitor binds to a different site on the enzyme.
■ Natural selection, acting on organisms with variant enzymes, is responsible for the diversity of enzymes found in organisms.

''',

'''
CONCEPT 8.5
Regulation of enzyme activity helps control metabolism (pp. 159-161)
■Many enzymes are subject to allosteric regulation: Regulatory molecules, either activators or inhibitors, bind to specific regula- tory sites, affecting the shape and function of the enzyme. In cooperativity, binding of one substrate molecule can stimulate binding or activity at other active sites. In feedback inhibition, the end product of a metabolic pathway allosterically inhibits the enzyme for a previous step in the pathway.
Some enzymes are grouped into complexes, some are incorporated into membranes, and some are contained inside organelles, increas- ing the efficiency of metabolic processes.

''',

'''

CONCEPT 9.1
Catabolic pathways yield energy by oxidizing organic fuels (pp. 165-169)
■Cells break down glucose and other organic fuels to yield chemical energy in the form of ATP. Fermentation is a process that results in the partial degradation of glucose without the use of oxygen. The process of cellular respiration is a more complete breakdown of glucose. In aerobic respiration, oxygen is used as a reactant; in anaerobic respiration, other substances are used as reactants in a similar process that harvests chemical energy without oxygen. The cell taps the energy stored in food molecules through redox reactions, in which one substance partially or totally shifts elec- trons to another. Oxidation is the total or partial loss of electrons, while reduction is the total or partial addition of electrons. During aerobic respiration, glucose (C6H12O6) is oxidized to CO2, and O2 is reduced to H2O:
- becomes oxidized-
C6H12O6+ 602 →6 CO2+ 6H2O + Energy
■ Electrons lose potential energy during their transfer from glucose or other organic compounds to oxygen. Electrons are usually
passed first to NAD, reducing it to NADH, and are then passed from NADH to an electron transport chain, which conducts the electrons to O, in energy-releasing steps. The energy that is released is used to make ATP.
■ Aerobic respiration occurs in three stages: (1) glycolysis, (2) pyruvate oxidation and the citric acid cycle, and (3) oxidative phosphorylation (electron transport and chemiosmosis).

''',

'''

CONCEPT 9.2
Glycolysis harvests chemical energy by oxidizing glucose to pyruvate (pp. 170-171)
■ Glycolysis ("splitting of sugar") is a series of reactions that breaks down glucose into two pyruvate molecules, which may go on to enter the citric acid cycle, and nets 2 ATP and 2 NADH per glucose molecule.
GLYCOLYSIS
Glucose -> 2 Pyruvate + 2 ATP + 2 NADH

''',

'''
CONCEPT 9.3
After pyruvate is oxidized, the citric acid cycle completes the energy-yielding oxidation of organic molecules (pp. 171-174)
■In eukaryotic cells, pyruvate enters the mitochondrion and is oxidized to acetyl CoA, which is further oxidized in the citric acid cycle.

2 Acetyl CoA -> 2 ATP + 8 NADH + 6 CO2 + 2 FADH2

''',

'''

CONCEPT 9.4
During oxidative phosphorylation, chemiosmosis couples electron transport to ATP synthesis (pp. 174-179)
■ NADH and FADH2 transfer electrons to the electron transport chain. Electrons move down the chain, losing energy in several energy-releasing steps. Finally, electrons are passed to O2, reducing it to H2O.
Along the electron transport chain, electron transfer causes protein complexes to move H+ from the mitochondrial matrix (in eukaryotes) to the intermem- brane space, storing energy as a proton-motive force (H+ gradi- ent). As H+ diffuses back into the matrix through ATP synthase, its passage drives the phosphory- lation of ADP to form ATP, called chemiosmosis.
About 34% of the energy stored in a glucose molecule is trans- ferred to ATP during cellular respiration, producing a maxi- mum of about 32 ATP.

''',

'''
CONCEPT 9.5
Fermentation and anaerobic respiration enable cells to produce ATP without the use of oxygen (pp. 179–182)
■Glycolysis nets 2 ATP by substrate-level phosphorylation, whether oxygen is present or not. Under anaerobic conditions, anaerobic respiration or fermentation can take place. In anaerobic respira- tion, an electron transport chain is present with a final electron acceptor other than oxygen. In fermentation, the electrons from NADH are passed to pyruvate or a derivative of pyruvate, regen- erating the NAD* required to oxidize more glucose. Two common types of fermentation are alcohol fermentation and lactic acid fermentation.
■Fermentation and anaerobic or aerobic respiration all use glycolysis to oxidize glucose, but they differ in their final electron acceptor and whether an electron transport chain is used (respiration) or not (fermentation). Respiration yields more ATP; aerobic respira- tion, with O2 as the final electron acceptor, yields about 16 times as much ATP as does fermentation.
■ Glycolysis occurs in nearly all organisms and is thought to have evolved in ancient prokaryotes before there was O2 in the atmosphere.

''',

'''
CONCEPT 9.6
Glycolysis and the citric acid cycle connect
to many other metabolic pathways (pp. 182-184)
■ Catabolic pathways funnel electrons from many kinds of organic molecules into cellular respiration. Many carbohydrates can enter glycolysis, most often after conversion to glucose. Amino acids of proteins must be deaminated before being oxidized. The fatty acids of fats undergo beta oxidation to two-carbon frag- ments and then enter the citric acid cycle as acetyl CoA. Anabolic pathways can use small molecules from food directly or build other substances using intermediates of glycolysis or the citric acid cycle.
■ Cellular respiration is controlled by allosteric enzymes at key points in glycolysis and the citric acid cycle.

''',

'''

CONCEPT 10.1
Photosynthesis converts light energy to the chemical energy of food (pp. 189–192)
■ In eukaryotes that are autotrophs, photosynthe- sis occurs in chloroplasts, organelles containing thylakoids. Stacks of thylakoids form grana. Photosynthesis is summarized as
6 CO2+ 12 H2O + Light energy → C6H12O6 + 6 O2 + 6 H2O. Chloroplasts split water into hydrogen and oxygen, incorporating the electrons of hydrogen into sugar molecules. Photosynthesis is a redox process: H2O is oxidized, and CO2 is reduced. The light reactions in the thylakoid membranes split water, releasing O2, producing ATP, and forming NADPH. The Calvin cycle in the stroma forms sugar from CO2, using ATP for energy and NADPH for reducing power.

''',

'''
CONCEPT 10.2
The light reactions convert solar energy to the chemical energy of ATP and NADPH (pp. 192-201)
■Light is a form of electromagnetic energy. The colors we see as visible light include those wavelengths that drive photosynthe- sis. A pigment absorbs light of specific wavelengths; chlorophyll a is the main photosynthetic pigment in plants. Other accessory pig- ments absorb different wavelengths of light and pass the energy on to chlorophyll a.
■ A pigment goes from a ground state to an excited state when a photon of light boosts one of the pigment's electrons to a higher-energy orbital. This excited state is unstable. Electrons from isolated pigments tend to fall back to the ground state, giving off heat and/or light.
■ A photosystem is composed of a reaction-center complex surrounded by light-harvesting complexes that funnel the energy of photons to the reaction-center complex. When a special pair of reaction-center chlorophyll a molecules absorbs energy, one of its electrons is boosted to a higher energy level and transferred to the primary electron acceptor. Photosystem II contains P680 chlorophyll a molecules in the reaction-center complex; photosystem I contains P700 molecules.
■ Linear electron flow during the light reactions uses both photosystems and produces NADPH, ATP, and oxygen:
■ Cyclic electron flow employs only one photosystem, produc- ing ATP but no NADPH or O2.
■During chemiosmosis in both mitochondria and chloroplasts, electron transport chains generate an H* gradient across a membrane. ATP synthase uses this proton-motive force to make ATP.

''',

'''
CONCEPT 10.3
The Calvin cycle uses the chemical energy of ATP and NADPH to reduce CO2 to sugar (pp. 201-202)
■The Calvin cycle occurs in the stroma, using electrons from NADPH and energy from ATP. One molecule of G3P exits the cycle per three CO2 molecules fixed and is converted to glucose and other organic molecules.

''',

'''
CONCEPT 10.4
Alternative mechanisms of carbon fixation have evolved in hot, arid climates (pp. 203-206)
■ On dry, hot days, C3 plants close their stomata, conserving water but keeping CO2 out and O2 in. Under these conditions, photorespiration can occur: Rubisco binds O2 instead of CO2, consuming ATP and releasing CO2 without producing ATP or car- bohydrate. Photorespiration may be an evolutionary relic, and it may play a photoprotective role.
■ C4 plants minimize the cost of photorespiration by incorporat- ing CO2 into four-carbon compounds in mesophyll cells. These compounds are exported to bundle-sheath cells, where they release carbon dioxide for use in the Calvin cycle.
■ CAM plants open their stomata at night, incorporating CO2 into organic acids, which are stored in mesophyll cells. During the day, the stomata close, and the CO2 is released from the organic acids for use in the Calvin cycle.
■ Organic compounds produced by photosynthesis provide the energy and building material for Earth's ecosystems.

''',

'''

CONCEPT 11.1
External signals are converted to responses within the cell (pp. 213–217)
■ Signal transduction pathways are crucial for many processes. Signaling during yeast cell mating has much in common with processes in multicellu- lar organisms, suggesting an early evolutionary origin of signaling mechanisms. Bacterial cells can sense the local density of bacte- rial cells (quorum sensing).
■Local signaling by animal cells involves direct contact or the secre- tion of local regulators. For long-distance signaling, animal and plant cells use hormones; animals also pass signals electrically. Like epinephrine, other hormones that bind to membrane recep- tors trigger a three-stage cell-signaling pathway:
1. Reception: receptor, signaling molecule
2. Transduction: relay molecules
3. Response: activation of cellular response

''',

'''

CONCEPT 11.2
Reception: A signaling molecule binds
to a receptor protein, causing it to change shape (pp. 217-221)
The binding between signaling molecule (ligand) and receptor is highly specific. A specific shape change in a receptor is often the initial transduction of the signal.
■There are three major types of cell-surface transmembrane receptors: (1) G protein-coupled receptors (GPCRs) work with cytoplas- mic G proteins. Ligand binding activates the receptor, which then activates a specific G protein, which activates yet another pro- tein, thus propagating the signal. (2) Receptor tyrosine kinases (RTKs) react to the binding of signaling molecules by forming dimers and then adding phosphate groups to tyrosines on the cyto- plasmic part of the other monomer making up the dimer. Relay proteins in the cell can then be activated by binding to different phosphorylated tyrosines, allowing this receptor to trigger several pathways at once. (3) Ligand-gated ion channels open or close in response to binding by specific signaling molecules, regulating the flow of specific ions across the membrane.
The activity of all three types of receptors is crucial; abnormal GPCRs and RTKs are associated with many human diseases. ■ Intracellular receptors are cytoplasmic or nuclear proteins. Signaling molecules that are hydrophobic or small enough to cross the plasma membrane bind to these receptors inside the cell.


''',

'''
CONCEPT 11.3
Transduction: Cascades of molecular interactions relay signals from receptors to target molecules in the cell (pp. 221-225)
At each step in a signal transduction pathway, the signal is trans- duced into a different form, which commonly involves a shape change in a protein. Many signal transduction pathways include phosphorylation cascades, in which a series of protein kinases each add a phosphate group to the next one in line, activating it. Enzymes called protein phosphatases remove the phosphate groups. The balance between phosphorylation and dephosphorylation regulates the activity of proteins involved in the sequential steps of a signal transduction pathway.
■ Second messengers, such as the small molecule cyclic AMP (CAMP) and the ion Ca2, diffuse readily through the cytosol and thus help broadcast signals quickly. Many G proteins activate adenylyl cyclase, which makes cAMP from ATP. Cells use Ca2+ as a second messenger in both GPCR and RTK pathways. The tyro- sine kinase pathways can also involve two other second messen- gers, diacylglycerol (DAG) and inositol trisphosphate (IP3). IP, can trigger a subsequent increase in Ca2+ levels.


''',

'''
CONCEPT 11.4
Response: Cell signaling leads to regulation of transcription or cytoplasmic activities (pp. 226-229)
■Some pathways lead to a nuclear response: Specific genes are turned on or off by activated transcription factors. In others, the response involves cytoplasmic regulation.
■ Cellular responses are not simply on or off; they are regulated at many steps. Each protein in a signaling pathway amplifies the sig- nal by activating multiple copies of the next component; for long pathways, the total amplification may be over a millionfold. The combination of proteins in a cell confers specificity in the signals it detects and the responses it carries out. Scaffolding proteins increase signaling efficiency. Pathway branching further helps the cell coordinate signals and responses. Signal response can be terminated quickly because ligand binding is reversible. ? What mechanisms in the cell terminate its response to a signal and maintain its ability to respond to new signals?
''',

'''
CONCEPT 11.5
Apoptosis integrates multiple cell-signaling pathways (pp. 229-231)
Apoptosis is a type of programmed cell death in which cell components are disposed of in an orderly fashion. Studies of the soil worm Caenorhabditis elegans clarified molecular details of the relevant signaling pathways. A death signal leads to activation of caspases and nucleases, the main enzymes involved in apoptosis. ■ Several apoptotic signaling pathways exist in the cells of humans and other mammals, triggered in different ways. Signals eliciting apoptosis can originate from outside or inside the cell.

''',

'''
CONCEPT 12.1
Most cell division results in genetically identical daughter cells (pp. 235-237)
■ The genetic material (DNA) of a cell-its genome-is partitioned among chromosomes. Each eukaryotic chromosome consists of one DNA molecule associated with many proteins. Together, the complex of DNA and associated proteins is called chromatin. The chromatin of a chromosome exists in different states of condensation at different times. In animals, gametes have one set of chromosomes and somatic cells have two sets. ■ Cells replicate their genetic material before they divide, each daughter cell receiving a copy of the DNA. Prior to cell divi- sion, chromosomes are duplicated. Each one then consists of two identical sister chromatids joined along their lengths by sister chromatid cohesion and held most tightly together at a constricted region at the centromeres. When this cohesion is broken, the chromatids separate during cell division, becoming the chromosomes of the daughter cells. Eukaryotic cell division consists of mitosis (division of the nucleus) and cytokinesis (division of the cytoplasm).

''',

'''
CONCEPT 12.2
The mitotic phase alternates with interphase in the cell cycle (pp. 237-244)
■ Between divisions, a cell is in interphase: the G1, S, and G2 phases. The cell grows throughout interphase, with DNA being replicated only during the synthesis (S) phase. Mitosis and cytokinesis make up the mitotic (M) phase of the cell cycle: prophase, prometaphase, metaphase, anaphase, telophase.
The mitotic spindle, made up of microtubules, controls chro- mosome movement during mitosis. In animal cells, it arises from the centrosomes and includes spindle microtubules and asters. Some spindle microtubules attach to the kinetochores of chro- mosomes and move the chromosomes to the metaphase plate. After sister chromatids separate, motor proteins move them along kinetochore microtubules toward opposite ends of the cell. The cell elongates when motor proteins push nonkinetochore micro- tubules from opposite poles away from each other.
■ Mitosis is usually followed by cytokinesis. Animal cells carry out cytokinesis by cleavage, and plant cells form a cell plate.
During binary fission in bacteria, the chromosome replicates and the daughter chromosomes actively move apart. Some of the proteins involved in bacterial binary fission are related to eukary- otic actin and tubulin.
Since prokaryotes preceded eukaryotes by more than a billion years, it is likely that mitosis evolved from prokaryotic cell divi- sion. Certain unicellular eukaryotes exhibit mechanisms of cell division that may be similar to those of ancestors of existing eukaryotes. Such mechanisms might represent intermediate steps in the evolution of mitosis.

''',

'''
CONCEPT 12.3
The eukaryotic cell cycle is regulated
by a molecular control system (pp. 244-250)
■ Signaling molecules present in the cytoplasm regulate progress through the cell cycle.
The cell cycle control system is molecularly based. Cyclic changes in regulatory proteins work as a cell cycle clock. The key molecules are cyclins and cyclin-dependent kinases (Cdks). The clock has specific checkpoints where the cell cycle stops until a go-ahead signal is received; important check- points occur in G1, G2, and M phases. Cell culture has enabled researchers to study the molecular details of cell division. Both internal signals and external signals control the cell cycle check- points via signal transduction pathways. Most cells exhibit density-dependent inhibition of cell division as well as anchorage dependence.
■ Cancer cells elude normal cell cycle regulation and divide unchecked, forming tumors. Malignant tumors invade nearby tissues and can undergo metastasis, exporting cancer cells to other sites, where they may form secondary tumors. Recent cell cycle and cell signaling research, and new techniques for sequencing DNA, have led to improved cancer treatments.

''',

'''

CONCEPT 13.1
Offspring acquire genes from parents by inheriting chromosomes (pp. 255-256)
Each gene in an organism's DNA exists at a specific locus on a certain chromosome.
In asexual reproduction, a single parent produces genetically identical offspring by mitosis. Sexual reproduction combines genes from two parents, leading to genetically diverse offspring.

''',

'''
CONCEPT 13.2
Fertilization and meiosis alternate in sexual
life cycles (pp. 256-259)
■Normal human somatic cells are diploid. They have 46 chromo- somes made up of two sets of 23, one set from each parent. Human diploid cells have 22 pairs of homologs that are autosomes, and one pair of sex chromosomes; the latter typically determines whether the person is female (XX) or male (XY).
In humans, ovaries and testes produce haploid gametes by meiosis, each gamete containing a single set of 23 chromosomes (n = 23). During fertilization, an egg and sperm unite, forming a diploid (2n = 46) single-celled zygote, which develops into a multicellular organism by mitosis.
Sexual life cycles differ in the timing of meiosis relative to fertil- ization and in the point(s) of the cycle at which a multicellular organism is produced by mitosis.

''',

'''
CONCEPT 13.3
Meiosis reduces the number of chromosome sets from diploid to haploid (pp. 259-265)
■The two cell divisions of meiosis, meiosis I and meiosis II, pro- duce four haploid daughter cells. The number of chromosome sets is reduced from two (diploid) to one (haploid) during meiosis I.
■ Meiosis is distinguished from mitosis by three events of meiosis I:
Prophase I: Each pair of homologous chromosomes undergoes synapsis and crossing over between nonsister chromatids with the subsequent appearance of chiasmata.
Metaphase I: Chromosomes line up as homologous pairs on the metaphase plate.
Anaphase I: Homologs separate from each other; sister chromatids remain joined at the centromere.
Meiosis II separates the sister chromatids.
■ Sister chromatid cohesion and crossing over allow chiasmata to hold homologs together until anaphase I. Cohesins are cleaved along the arms at anaphase I, allowing homologs to separate, and at the centromeres in anaphase II, releasing sister chromatids. ? In prophase I, homologous chromosomes pair up and undergo synapsis and crossing over. Can this also occur during prophase II? Explain.

''',

'''
CONCEPT 13.4
Genetic variation produced in sexual life cycles contributes to evolution (pp. 265-267)
■Three events in sexual reproduction contribute to genetic variation in a population: independent assortment of chromosomes during meiosis I, crossing over during meiosis I, and random fertilization of egg cells by sperm. During crossing over, DNA of nonsister chro- matids in a homologous pair is broken and rejoined.
■ Genetic variation is the raw material for evolution by natural selec- tion. Mutations are the original source of this variation; recombi- nation of variant genes generates additional genetic diversity.

''',

'''

CONCEPT 14.1
Mendel used the scientific approach to identify two laws of inheritance (pp. 270-276)
Gregor Mendel formulated a theory of inheritance based on experiments with garden peas, proposing
that parents pass on to their offspring discrete genes that retain their identity through generations. This theory includes two "laws." The law of segregation states that genes have alternative forms, or alleles. In a diploid organism, the two alleles of a gene segregate (separate) during meiosis and gamete formation; each sperm or egg carries only one allele of each pair. This law explains the 3:1 ratio of F2 phenotypes observed when monohybrids self-pollinate. Each organism inherits one allele for each gene from each parent. In heterozygotes, the two alleles are different; expression of the dominant allele masks the phenotypic effect of the recessive allele. Homozygotes have identical alleles of a given gene and are therefore true-breeding.
The law of independent assortment states that the pair of alleles for a given gene segregates into gametes independently of the pair of alleles for any other gene. In a cross between dihybrids (individuals heterozygous for two genes), the offspring have four phenotypes in a 9:3:3:1 ratio.

''',

'''
CONCEPT 14.2
Inheritance patterns are often more complex than predicted by simple Mendelian genetics (pp. 278-283)

Complete dominance of one allele: Heterozygous phenotype same as that of homozygous dominant
Incomplete dominance: Heterozygous phenotype intermediate between the two homozygous phenotypes of either allele
Codominance: Both phenotypes expressed in heterozygotes
Multiple alleles: In the population, some genes have more than two alleles
Pleiotropy: One gene affects multiple phenotypic characters

''',

'''
CONCEPT 14.3


■ Extensions of Mendelian genetics for two or more genes:

Epistasis: The phenotypic expression of one gene affects the expression of another gene
Polygenic inheritance: A single phenotypic character is affected by two or more genes
The expression of a genotype can be affected by environmental influences, resulting in a range of phenotypes. Polygenic characters that are also influenced by the environment are called multifactorial characters.
■ An organism's overall phenotype, including its physical appear- ance, internal anatomy, physiology, and behavior, reflects its overall genotype and unique environmental history. Even in more complex inheritance patterns, Mendel's fundamental laws still apply.


''',

'''
CONCEPT 14.4
Many human traits follow Mendelian patterns of inheritance

Analysis of family pedigrees can be used to deduce the possible genotypes of individuals and make predictions about future off- spring. Such predictions are statistical probabilities rather than certainties.
Many genetic disorders are inherited as simple recessive traits. Most affected (homozygous recessive) individuals are children of phenotypically normal, heterozygous carriers.
The sickle-cell allele has probably persisted for evolutionary reasons: Homozygotes have sickle-cell disease, but heterozygotes have an advantage because one copy of the sickle-cell allele reduces both the frequency and severity of malaria attacks.
Lethal dominant alleles are eliminated from the population if affected people die before reproducing. Nonlethal dominant alleles and lethal ones that strike relatively late in life can be inherited in a Mendelian way.
Many human diseases are multifactorial—that is, they have both genetic and environmental components and do not follow simple Mendelian inheritance patterns.
Using family histories, genetic counselors help couples deter- mine the probability that their children will have genetic dis- orders. Genetic testing of prospective parents to reveal whether they are carriers of recessive alleles associated with specific disorders has become widely available. Blood tests can screen
for certain disorders in a fetus. Amniocentesis and chorionic villus sampling can indicate whether a suspected genetic dis- order is present in a fetus. Other genetic tests can be performed after birth.

''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 15.1
Morgan showed that Mendelian
inheritance has its physical basis in the behavior of chromosomes: scientific inquiry (pp. 296-297)
■ Morgan's work with an eye color gene in Drosophila led to the chromosome theory of inheritance, which states that genes are located on chromosomes and that the behavior of chromosomes during meiosis accounts for Mendel's laws.

''',

'''

CONCEPT 15.2
Sex-linked genes exhibit unique patterns of inheritance (pp. 298-300)
■ Sex is often chromosomally based. Humans and other mammals have an X-Y system in which sex is largely determined by whether a Y chromosome is present. Other systems are found in birds, fishes, and insects.
■The sex chromosomes carry sex-linked genes, virtually all of which are on the X chromosome (X-linked). Any male who inherits a recessive X-linked allele (from his mother) will express the trait, such as color blindness.
■ In mammalian females, one of the two X chromosomes in each cell is randomly inactivated during early embryonic develop- ment, becoming highly condensed into a Barr body.

''',

'''
CONCEPT 15.3
Linked genes tend to be inherited together because they are located near each other on the same chromosome (pp. 301-306)
The alleles of unlinked genes are either on separate chromosomes or so far apart on the same chromosome that they assort independently.
Genes on the same chromosome whose alleles are so close together that they do not assort independently are said to be genetically linked.
An F, dihybrid testcross yields parental types with the same combination of traits as those in the P generation parents and recombinant types (recombinants) with new combina- tions of traits not seen in either P generation parent. Because of the independent assortment of chromosomes, unlinked genes exhibit a 50% frequency of recombination in the gametes. For genetically linked genes, crossing over between nonsister chromatids during meiosis I accounts for the observed recombi- nants, always less than 50%.
The order of genes on a chromosome and the relative distances between them can be deduced from recombination frequencies observed in genetic crosses. These data allow construction of a linkage map (a type of genetic map). The farther apart genes are, the more likely their allele combinations will be recombined during crossing over.

''',

'''
CONCEPT 15.4
Alterations of chromosome number or structure cause some genetic disorders (pp. 306-309)
■ Aneuploidy, an abnormal chromosome number, can result from nondisjunction during meiosis. When a normal gamete unites with one containing two copies or no copies of a particular chromosome, the resulting zygote and its descendant cells either have one extra copy of that chromosome (trisomy, 2n + 1) or are missing a copy (monosomy, 2n − 1). Polyploidy (extra sets of chromosomes) can result from complete nondisjunction. Chromosome breakage can result in alterations of chromo- some structure: deletions, duplications, inversions, and translocations. Translocations can be reciprocal or nonreciprocal.
■Changes in the number of chromosomes per cell or in the struc- ture of individual chromosomes can affect the phenotype and, in some cases, lead to disorders. Such alterations cause Down syndrome (usually due to trisomy of chromosome 21), certain cancers associated with chromosomal translocations that occur during mitosis, and various other human disorders.

''',

'''
CONCEPT 15.5
Some inheritance patterns are exceptions to standard Mendelian inheritance (pp. 310-311)
In mammals, the phenotypic effects of a small number of particu- lar genes depend on which allele is inherited from each parent, a phenomenon called genomic imprinting. Imprints are formed during gamete production, with the result that one allele (either maternal or paternal) is not expressed in offspring.
■ The inheritance of traits controlled by the genes present in mitochondria and plastids depends solely on the maternal par- ent because the zygote's cytoplasm containing these organelles comes from the egg. Some diseases affecting the nervous and muscular systems are caused by defects in mitochondrial genes that prevent cells from making enough ATP.

''',

'''


SUMMARY OF KEY CONCEPTS
CONCEPT 16.1
DNA is the genetic material (pp. 315-320)
■ Experiments with bacteria and with phages provided the first strong evidence that the genetic material is DNA.
■ Watson and Crick deduced that DNA is a double helix and built a structural model. Two antiparallel sugar-phosphate chains wind around the outside of the molecule; the nitrogenous bases project into the interior, where they hydrogen-bond in specific pairs, A with T, G with C.

''',

'''
CONCEPT 16.3
A chromosome consists of a DNA molecule packed together with proteins (pp. 330-332)
• The chromosome of most bacterial species is a circular DNA mol- ecule with some associated proteins, making up the nucleoid. The chromatin making up a eukaryotic chromosome is composed of DNA, histones, and other proteins. The histones bind to each other and to the DNA to form nucleosomes, the most basic units of DNA packing. Histone tails extend outward from each bead-like nucleosome core. Additional coiling and folding lead ultimately to the highly condensed chromatin of the metaphase chromosome.
■ Chromosomes occupy restricted areas in the interphase nucleus. In interphase cells, most chromatin is less compacted (euchromatin), but some remains highly condensed (hetero- chromatin). Euchromatin, but not heterochromatin, is generally accessible for transcription of genes.

''',

'''
CONCEPT 16.2
Many proteins work together in DNA replication and repair (pp. 320-329)
The Meselson-Stahl experiment showed that DNA replication is semiconservative: The parental molecule unwinds, and each strand then serves as a template for the synthesis of a new strand according to base-pairing rules.
■ DNA replication at one replication fork is summarized here: DNA pol III synthesizes
leading strand continuously
DNA pol III starts DNA synthesis at 3' end of primer, continues in 5' → 3' direction
Origin of replication
Lagging strand synthesized in short Okazaki fragments, later joined by DNA ligase
3 DNA pol I replaces the RNA primer with DNA nucleotides
■ DNA polymerases proofread new DNA, replacing incorrect nucle- otides. In mismatch repair, enzymes correct errors that persist. Nucleotide excision repair is a process by which nucleases cut out and other enzymes replace damaged stretches of DNA. The ends of eukaryotic chromosomal DNA get shorter with each round of replication. The presence of telomeres, repetitive sequences at the ends of linear DNA molecules, postpones the erosion of genes. Telomerase catalyzes the lengthening of telo- meres in germ cells.

''',

'''


SUMMARY OF KEY CONCEPTS
CONCEPT 17.1
Genes specify proteins via transcription and translation (pp. 336-342)
■ Beadle and Tatum's studies of mutant strains of Neurospora led to the one gene-one polypeptide hypothesis. During gene expression, the infor- mation encoded in genes is used to make specific polypeptide chains (enzymes and other proteins) or RNA molecules. ■ Transcription is the synthesis of RNA complementary to a template strand of DNA. Translation is the synthesis of a polypeptide whose amino acid sequence is specified by the nucleotide sequence in messenger RNA (mRNA).
■ Genetic information is encoded as a sequence of nonoverlapping nucleotide triplets, or codons. A codon in mRNA either is translated into an amino acid (61 of the 64 codons) or serves as a stop signal (3 codons). Codons must be read in the correct reading frame. ? Describe the process of gene expression, by which a gene affects the
phenotype of an organism.

''',

'''
CONCEPT 17.2
Transcription is the DNA-directed synthesis of RNA: a closer look (pp. 342-344)
■ RNA synthesis is catalyzed by RNA polymerase, which links together RNA nucleotides complementary to a DNA template strand. This process follows the same base-pairing rules as DNA replication, except that in RNA, uracil substitutes for thymine.
The three stages of transcription are initiation, elongation, and termination. A promoter, often including a TATA box in eukaryotes, establishes where RNA synthesis is initiated. Transcription factors help eukaryotic RNA polymerase recog- nize promoter sequences, forming a transcription initiation complex. Termination differs in bacteria and eukaryotes.

''',

'''
CONCEPT 17.3
Eukaryotic cells modify RNA after transcription (pp. 345-347)
■ Eukaryotic mRNAs undergo RNA processing, which includes RNA splicing, the addition of a modified nucleotide 5' cap to the 5' end, and the addition of a poly-A tail to the 3' end. The pro- cessed mRNA includes an untranslated region (5' UTR or 3' UTR) at each end of the coding segment.


■ Most eukaryotic genes are split into segments: They have introns interspersed among the exons (the regions included in the mRNA). In RNA splicing, introns are removed and exons joined. RNA splicing is typically carried out by spliceosomes, but in some cases, RNA alone catalyzes its own splicing. The cata- lytic ability of some RNA molecules, called ribozymes, derives from the inherent properties of RNA. The presence of introns allows for alternative RNA splicing.
5' Cap
5' Exon Intron Exon
Pre-mRNA
mRNA
Poly-A tail
Intron
Exon 3'
RNA splicing
5' UTR Coding 3' UTR
segment

''',

'''

CONCEPT 17.4
Translation is the RNA-directed synthesis
of a polypeptide: a closer look (pp. 347-356)
■ A cell translates an mRNA message into protein using transfer RNAs (tRNAs). After being bound to a specific amino acid by an aminoacyl-tRNA synthetase, a tRNA lines up via its anticodon at the complementary codon on mRNA. A ribosome, made up of ribosomal RNAs (rRNAs) and proteins, facilitates this coupling with binding sites for mRNA and tRNA.
■ Ribosomes coordinate the three stages of translation: initiation, elongation, and termination. The formation of peptide bonds between amino acids is catalyzed by rRNAs as tRNAs move through the A and P sites and exit through the E site.
Polypeptide Amino
acid
tRNA
Anti-
codon
Codon
mRNA
Ribosome
■ After translation, during protein processing, proteins may be modified by cleavage or by attachment of sugars, lipids, phos- phates, or other chemical groups.
Free ribosomes in the cytosol initiate synthesis of all proteins, but proteins with a signal peptide are synthesized on the ER.
A gene can be transcribed by multiple RNA polymerases simulta- neously. Also, a single mRNA molecule can be translated simulta- neously by a number of ribosomes, forming a polyribosome. In bacteria, these processes are coupled, but in eukaryotes they are separated in space and time by the nuclear membrane.

''',

'''


CONCEPT 17.5
Mutations of one or a few nucleotides can affect protein structure and function (pp. 357-360)
■ Small-scale mutations include point mutations, changes in one DNA nucleotide pair, which may lead to production of non- functional proteins. Nucleotide-pair substitutions can cause missense or nonsense mutations. Nucleotide-pair insertions or deletions may produce frameshift mutations.
■ Spontaneous mutations can occur during DNA replication and recombination. Chemical and physical mutagens cause DNA damage that can alter genes.

''',

'''

CONCEPT 18.1
Bacteria often respond to environmental change by regulating transcription
(pp. 364–368)
Cells control metabolism by regulating enzyme
activity or the expression of genes coding for
enzymes. In bacteria, genes are often clustered into operons, with one promoter serving several adjacent genes. An operator site on the DNA switches the operon on or off, resulting in coordi- nate regulation of the genes.

Both repressible and inducible operons are examples of negative gene regulation. In either type of operon, binding of a specific repressor protein to the operator shuts off transcription. (The repressor is encoded by a separate regulatory gene.) In a repres- sible operon, the repressor is active when bound to a corepressor, usually the end product of an anabolic pathway.

In an inducible operon, binding of an inducer to an innately active repressor inactivates the repressor and turns on transcrip- tion. Inducible enzymes usually function in catabolic pathways

Some operons are also subject to positive gene regulation via a stimulatory activator protein, such as cAMP receptor protein (CRP), which, when activated by cyclic AMP, binds to a site within the promoter and stimulates transcription.

''',

'''

CONCEPT 18.2

Chromatin modification
• Genes in highly compacted chromatin are generally not transcribed.
• Histone acetylation loosens chromatin structure, enhancing transcription.
• DNA methylation generally reduces transcription.

Transcription
• Regulation of transcription initiation: DNA control
elements in
enhancers bind
specific tran-
scription factors.
Bending of the DNA enables activators to contact proteins at the promoter, initiating transcription.
• Coordinate regulation:
Enhancer for Enhancer for liver-specific genes lens-specific genes

RNA processing
• Alternative RNA splicing: Primary RNA
transcript
mRNA

mRNA degradation
• Each mRNA has a characteristic life span, determined in part by sequences in the 5′ and 3′ UTRs.

Translation
• Initiation of translation can be controlled via regulation of initiation factors.

Protein processing and degradation
• Protein processing and degradation are subject to regulation.

''',

'''
Concept 18.3
noncoding RnAs play multiple roles in
controlling gene expression (pp. 377–379)

Chromatin modification: Small and/or large noncoding RNAs can  promote heterochromatin formation in certain regions, which can block transcription

Translation
• miRNA or siRNA can block the translation of specific mRNAs

mRNA degradation
• miRNA or siRNA can target specific mRNAs for destruction

''',

'''

CONCEPT 18.4
A program of differential gene expression leads to the different cell types in a multicellular organism (pp. 379-386)
■ Embryonic cells become committed to a certain fate (determination), and undergo differentiation, becoming specialized in structure and function for their determined fate. Cells differ in structure and function not because they contain different genomes but because they express different genes. Morphogenesis encompasses the processes that give shape to the organism and its various structures.
Localized cytoplasmic determinants in the unfertilized egg are distributed differentially to daughter cells, where they regulate the expression of those cells' developmental fate. In the process called induction, signaling molecules from embryonic cells cause transcriptional changes in nearby target cells.
Differentiation is heralded by the appearance of tissue-specific proteins, which enable differentiated cells to carry out their specialized roles.
In animals, pattern formation, the development of a spatial organization of tissues and organs, begins in the early embryo. Positional information, the molecular cues that control pattern formation, tells a cell its location relative to the body's axes and to other cells. In Drosophila, gradients of morphogens encoded by maternal effect genes determine the body axes. For example, the gradient of Bicoid protein determines the anterior-posterior axis.

''',

'''
CONCEPT 18.5
Cancer results from genetic changes that affect cell cycle control (pp. 386–392)
The products of proto-oncogenes and tumor-suppressor genes control cell division. A DNA change that makes a proto-oncogene excessively active converts it to an oncogene, which may promote excessive cell division and cancer. A tumor-suppressor gene encodes a protein that inhibits abnormal cell division. A mutation that reduces the activity of its protein product may lead to excessive cell division and cancer.
Many proto-oncogenes and tumor-suppressor genes encode com- ponents of growth-stimulating and growth-inhibiting signaling pathways, respectively, and mutations in these genes can inter- fere with normal cell-signaling pathways. A hyperactive version of a protein in a stimulatory pathway, such as Ras (a G protein), functions as an oncogene protein. A defective version of a protein in an inhibitory pathway, such as p53 (a transcription activator), fails to function as a tumor suppressor.
Protein overexpressed
Cell cycle overstimulated
EFFECTS OF MUTATIONS
Protein absent
Increased cell division
Cell cycle not inhibited
In the multistep model of cancer development, normal cells are converted to cancer cells by the accumulation of mutations affecting proto-oncogenes and tumor-suppressor genes. Technical advances in DNA and mRNA sequencing are enabling cancer treatments that are more individually based.
Genomics-based studies have resulted in researchers proposing four subtypes of breast cancer, based on expression of genes by tumor cells.
Individuals who inherit a mutant allele of a proto-oncogene or tumor-suppressor gene have a predisposition to develop a particu- lar cancer. Certain viruses promote cancer by integration of viral DNA into a cell’s genome.
''',

'''

CONCEPT 19.1
A virus consists of a nucleic acid sur- rounded by a protein coat (pp. 397-399)
Researchers discovered viruses in the late 1800s by studying a plant disease, tobacco mosaic disease.
A virus is a small nucleic acid genome enclosed in a protein capsid and sometimes a membranous viral envelope. The genome may be single- or double-stranded DNA or RNA.

''',

'''
CONCEPT 19.2
Viruses replicate only in host cells (pp. 399-406)
■ Viruses use enzymes, ribosomes, and small molecules of host cells to synthesize progeny viruses during replication.
Each type of virus has a characteristic host range, affected by whether cell-surface proteins are present that viral surface proteins can bind to.
Phages (viruses that infect bacteria) can replicate by two alterna- tive mechanisms: the lytic cycle and the lysogenic cycle.
Lytic cycle
Phage DNA-
Virulent or temperate phage • Destruction of host DNA
• Production of new phages
• Lysis of host cell causes release of progeny phages
Bacterial chromosome
The phage attaches to a host cell and injects its DNA.
Prophage
Lysogenic cycle
Temperate phage only
• Genome integrates into bacterial chromosome as prophage, which (1) is replicated and passed on to daughter cells and
(2) can be induced to leave the chromo- some and initiate a lytic cycle
■ Bacteria have various ways of defending themselves against phage infections, including the CRISPR-Cas system.
■ Many animal viruses have an envelope. Retroviruses (such as HIV) use the enzyme reverse transcriptase to copy their RNA genome into DNA, which can be integrated into the host genome as a provirus.
■ Since viruses can replicate only within cells, they probably
evolved after the first cells appeared, perhaps as packaged frag- ments of cellular nucleic acid.

''',

'''
CONCEPT 19.3
Viruses and prions are formidable pathogens in animals and plants (pp. 406-411)
■ Symptoms of viral diseases may be caused by direct viral harm to cells or by the body's immune response. Vaccines stimulate the immune system to defend the host against specific viruses.
■ An epidemic, a widespread outbreak of a disease, can become a pandemic, a global epidemic.
■ Outbreaks of emerging viral diseases in humans are usually not new, but rather are caused by existing viruses that expand their host territory. The H1N1 2009 flu virus was a new combination of pig, human, and avian viral genes that caused a pandemic. The H5N1 avian flu virus has the potential to cause a high- mortality flu pandemic.
■ Viruses enter plant cells through damaged cell walls (hori- zontal transmission) or are inherited from a parent (vertical transmission).
■ Prions are slow-acting, virtually indestructible infectious pro- teins that cause brain diseases in mammals.

''',

'''


SUMMARY OF KEY CONCEPTS
CONCEPT 20.1
DNA sequencing and DNA cloning are valuable tools for genetic engineering and biological inquiry (pp. 414-421)
Nucleic acid hybridization, the base pairing of one strand of a nucleic acid to the complementary sequence on a strand from another nucleic acid molecule, is widely used in DNA technology.
DNA sequencing can be carried out using the dideoxy chain termination method in automated sequencing machines. ■ Next-generation (high-throughput) techniques for sequencing DNA are based on sequencing by synthesis: DNA polymerase is used to synthesize a stretch of DNA from a single-stranded template, and the order in which nucleotides are added reveals the sequence. Third-generation sequencing methods, including nanopore technology, sequence long DNA molecules one at a
time by distinguishing the nucleotide bases as they pass through a pore in a membrane.
Gene cloning (or DNA cloning) produces multiple copies of a gene (or DNA segment) that can be used to manipulate and ana- lyze DNA and to produce useful new products or organisms with beneficial traits.
■In genetic engineering, bacterial restriction enzymes are used to cut DNA molecules within short, specific nucleotide sequences (restriction sites), yielding a set of double-stranded restriction fragments with single-stranded sticky ends
The sticky ends on restriction fragments from one DNA source can base-pair with complementary sticky ends on fragments from other DNA molecules. Sealing the base-paired fragments with DNA ligase produces recombinant DNA molecules.
■ DNA restriction fragments of different lengths can be separated by gel electrophoresis.

The polymerase chain reaction (PCR) can produce many copies of (amplify) a specific target segment of DNA in vitro, using primers that bracket the desired sequence and a heat-resistant DNA polymerase.
■To clone a eukaryotic gene:
Cloning vector
EC
(often a bacterial plasmid)
DNA fragments obtained by PCR or from another source (cut by same restriction enzyme used on cloning vector)
Recombinant plasmids are returned to host cells, each of which divides to form a clone of cells.
■Several technical difficulties hinder the expression of cloned eukaryotic genes in bacterial host cells. The use of cultured eukaryotic cells as host cells, coupled with appropriate expression vectors, helps avoid these problems.

''',

'''
CONCEPT 20.2
Biologists use DNA technology to study gene expression and function (pp. 421-426)
■Several techniques use hybridization of a nucleic acid probe to detect the presence of specific mRNAs.
■In situ hybridization and RT-PCR can detect the presence of a given mRNA in a tissue or an RNA sample, respectively.
■ DNA microarrays are used to identify sets of genes co-expressed by a group of cells. Increasingly, instead, RNA sequencing (RNA-seq) is used to sequence the cDNAs corresponding to RNAs from the cells.
For a gene of unknown function, experimental inactivation of the gene (a gene knockout) and observation of the result- ing phenotypic effects can provide clues to its function. The CRISPR-Cas9 system allows researchers to edit genes in living cells in a specific, desired way. The new alleles can be altered so that they are inherited in a biased way through a population (gene drive). In humans, genome-wide association studies identify and use single nucleotide polymorphisms (SNPs) as genetic markers for alleles that are associated with particular conditions.

''',

'''
CONCEPT 20.3
Cloned organisms and stem cells are useful for basic research and other applications (pp. 426-431)
The question of whether all the cells in an organism have the same genome prompted the first attempts at organismal cloning.
■ Single differentiated cells from plants are often totipotent: capable of generating all the tissues of a complete new plant.
■ Transplantation of the nucleus from a differentiated animal cell into an enucleated egg can sometimes give rise to a new animal.
■ Certain embryonic stem cells (ES cells) from animal embryos and particular adult stem cells from adult tissues can reproduce and differentiate both in the lab and in the organism, offering the potential for medical use. ES cells are pluripotent but difficult to acquire. Induced pluripotent stem (IPS) cells resemble ES cells in their capacity to differentiate; they can be generated by repro- gramming differentiated cells. iPS cells hold promise for medical research and regenerative medicine.

''',

'''
CONCEPT 20.4
The practical applications of DNA-based biotechnology affect our lives in many ways (pp. 431-437)
■ DNA technology, including the analysis of genetic markers such as SNPs, is increasingly being used in the diagnosis of genetic and other diseases and offers potential for better treatment of genetic disorders or even permanent cures through gene therapy, or gene editing with the CRISPR-Cas9 system. It also enables more informed cancer therapies. DNA technology is used with cell cultures in the large-scale production of protein hormones and other proteins with therapeutic uses. Some therapeutic proteins are being produced in transgenic "pharm" animals.
■ Analysis of genetic markers such as short tandem repeats (STRS) in DNA isolated from tissue or body fluids found at crime scenes leads to a genetic profile. Use of genetic profiles can provide definitive evidence that a suspect is innocent or strong evidence of guilt. Such analysis is also useful in parenthood disputes and in identifying the remains of crime victims. ■Genetically engineered microorganisms can be used to extract minerals from the environment or degrade various types of toxic waste materials.
The aims of developing transgenic plants and animals are to improve agricultural productivity and food quality.
The potential benefits of genetic engineering must be carefully weighed against the potential for harm to humans or the
environment.

''',

'''
CONCEPT 21.1
The Human Genome Project fostered development of faster, less expensive sequencing techniques (pp. 441-442)
■The Human Genome Project was largely completed in 2003, aided by major advances in
sequencing technology.
■In the whole-genome shotgun approach, the whole genome is cut into many small, overlapping fragments that are sequenced; computer software then assembles the genome sequence.
''',
'''
CONCEPT 21.2
Scientists use bioinformatics to analyze genomes and their functions (pp. 442-446)
■Computer analysis of genome sequences aids gene annotation, the identification of protein-coding sequences. Methods to determine gene function include comparing sequences of newly discovered genes with those of known genes in other species and observing the effects of experimentally inactivating the genes. ■In systems biology, scientists use the computer-based tools of bioinformatics to compare genomes and study sets of genes and proteins as whole systems (genomics and proteomics). Studies include large-scale analyses of protein interactions, functional DNA elements, and genes contributing to medical conditions. ? What has been the most significant finding of the ENCODE project? Why was the project expanded to include non-human species?
''',

'''
CONCEPT 21.3
Genomes vary in size, number of genes, and gene density (pp. 446-448)
Bacteria
Archaea
Genome size
Most are 1-6 Mb
Number of
genes
Gene density
Higher than in eukaryotes
1,500-7,500
Introns
None in
protein-coding genes
Present in some genes
Other noncoding DNA
Very little
Eukarya
Most are 10-4,000 Mb, but a few are much larger
Most are 5,000-45,000
Lower than in prokaryotes (Within eukaryotes, lower density is correlated with larger genomes.)
Present in most genes of multicellular eukaryotes, but only in some genes of unicellular eukaryotes
Can exist in large amounts; generally more repetitive noncoding DNA in
multicellular eukaryotes

''',

'''
CONCEPT 21.4
Multicellular eukaryotes have a lot of noncoding DNA and many multigene families (pp. 448-451)
Only 1.5% of the human genome codes for proteins or gives rise to rRNAs or tRNAS; the rest is noncoding DNA, including pseudogenes and repetitive DNA of unknown function. ■ The most abundant type of repetitive DNA in multicellular eukaryotes consists of transposable elements and related sequences. In eukaryotes, there are two types of transposable ele- ments: transposons, which move via a DNA intermediate, and retrotransposons, which are more prevalent and move via an RNA intermediate.
■ Other repetitive DNA includes short, noncoding sequences that are tandemly repeated thousands of times (simple sequence DNA, which includes STRS); these sequences are especially prominent in centromeres and telomeres, where they probably play structural roles in the chromosome.
■ Though many eukaryotic genes are present in one copy per hap- loid chromosome set, others (most, in some species) are members of a gene family, such as the human globin gene families:
a-Globin gene family
B-Globin gene family
Chromosome 11
Chromosome 16
5
Ψς Ψα, Ψα, α, α Ψε
€
Gy Ay B δ β
''',

'''
CONCEPT 21.5
Duplication, rearrangement, and mutation of DNA contribute to genome evolution (pp. 452-457) Errors in cell division can lead to extra copies of all or part of entire chromosome sets, which may then diverge if one set accu- mulates sequence changes. Polyploidy occurs more often among plants than animals and contributes to speciation.
The chromosomal organization of genomes can be compared among species, providing information about evolutionary relationships. Within a given species, rearrangements of chromosomes are thought to contribute to the emergence of new species.
■ The genes encoding the various related but different globin pro- teins evolved from one common ancestral globin gene, which duplicated and diverged into a-globin and B-globin ancestral genes. Subsequent duplication and random mutation gave rise to the present globin genes, all of which code for oxygen-binding proteins. The copies of some duplicated genes have diverged so much that the functions of their encoded proteins (such as lyso- zyme and a-lactalbumin) are now substantially different.
■ Rearrangement of exons within and between genes during evolu- tion has led to genes containing multiple copies of similar exons and/or several different exons derived from other genes.
■ Movement of transposable elements or recombination between copies of the same element can generate new sequence combinations that are beneficial to the organism. These may alter the functions of genes or their patterns of expression and regulation.
''',
'''


CONCEPT 21.6
Comparing genome sequences provides clues to evolution and development (pp. 457-462)
Comparisons of genomes from widely divergent and closely related species provide valuable information about ancient and more recent evolutionary history, respectively. Analysis of single nucleotide polymorphisms (SNPs) and copy-number variants (CNVs) among individuals in a species can also shed light on the evolution of that species.
■ Evolutionary developmental (evo-devo) biologists have shown that homeotic genes and some other genes associated with ani- mal development contain a homeobox region whose sequence is highly conserved among diverse species. Related sequences are present in the genes of plants and yeasts.

''',

'''


SUMMARY OF KEY CONCEPTS
CONCEPT 22.1
The Darwinian revolution challenged traditional views of a young Earth inhabited by unchanging species (pp. 467-469)
VOCAB SELF-QUIZ goo.gl/6u55ks
■ Darwin proposed that life's diversity arose from ancestral species through natural selection, a departure from prevailing views.
■ Cuvier studied fossils but denied that evolution occurs; he pro- posed that sudden catastrophic events in the past caused species to disappear from an area.
■ Hutton and Lyell thought that geologic change could result from gradual mechanisms that operated in the past in the same man- ner as they do today.
■ Lamarck hypothesized that species evolve, but the underlying mechanisms he proposed are not supported by evidence.
''',

'''
CONCEPT 22.2
Descent with modification by natural selection explains the adaptations of organisms and the unity and diversity of life (pp. 469–474)
■ Darwin's experiences during the voyage of the Beagle gave rise to his idea that new species originate from ancestral forms through the accumulation of adaptations. He refined his theory for many years and finally published it in 1859 after learning that Wallace had come to the same idea.
■ In The Origin of Species, Darwin proposed that over long periods of time, descent with modification produced the rich diversity of life through the mechanism of natural selection.
Observations
Individuals in a population
Organisms produce more offspring than the environment can support.
vary in their heritable characteristics.
Inferences
Individuals that are well suited
to their environment tend to leave more offspring than other individuals.
and
Over time, favorable traits accumulate in the population.
''',

'''
CONCEPT 22.3
Evolution is supported by an overwhelming amount of scientific evidence (pp. 475-482)
Researchers have directly observed natural selection leading to adaptive evolution in many studies, including research on soapberry bug populations and on MRSA.
Organisms share characteristics because of common descent (homology) or because natural selection affects independently evolving species in similar environments in similar ways (convergent evolution).
■ Fossils show that past organisms differed from living organisms, that many species have become extinct, and that species have evolved over long periods of time; fossils also document the evolutionary origin of new groups of organisms.
■ Evolutionary theory can explain some biogeographic patterns.
''',

'''

SUMMARY OF KEY CONCEPTS
CONCEPT 23.1
Genetic variation makes evolution possible (pp. 485-487)
■ Genetic variation refers to genetic differences among individuals within a population.
■ The nucleotide differences that provide the basis of genetic variation originate when mutation and gene duplica- tion produce new alleles and new genes. New genetic variants are produced rapidly in organisms with short generation times. In sexually reproducing organisms, most of the genetic differences among individuals result from crossing over, the independent assortment of chromosomes, and fertilization.

''',

'''
CONCEPT 23.2
The Hardy-Weinberg equation can be used to test whether a population is evolving (pp. 487-491)
■ A population, a localized group of organisms belonging to one species, is united by its gene pool, the aggregate of all the alleles in the population.
For a population in Hardy-Weinberg equilibrium, the allele and genotype frequencies will remain constant if the population is large, mating is random, mutation is negligible, there is no gene flow, and there is no natural selection. For such a population, if p and q represent the frequencies of the only two possible alleles at a particular locus, then p2 is the frequency of one kind of homozygote, q2 is the frequency of the other kind of homozygote, and 2pq is the frequency of the heterozygous genotype. ? Is it circular reasoning to calculate p and q from observed genotype frequencies and then use those values of p and q to test if the population is in Hardy-Weinberg equilibrium? Explain your answer.
''',

'''
CONCEPT 23.3
Natural selection, genetic drift, and gene flow can alter allele frequencies in a population (pp. 491-495)
■ In natural selection, individuals that have certain inherited traits tend to survive and reproduce at higher rates than other individuals because of those traits.
■In genetic drift, chance fluctuations in allele frequencies over generations tend to reduce genetic variation.
■Gene flow, the transfer of alleles between populations, tends to reduce genetic differences between populations over time. ? Would two small, geographically isolated populations in very different environments be likely to evolve in similar ways? Explain.
''',

'''
CONCEPT 23.4
Natural selection is the only mechanism that consistently causes adaptive evolution (pp. 495-502)
■ One organism has greater relative fitness than another organ- ism if it leaves more fertile descendants. The modes of natural selection differ in their effect on phenotype:
Original population Evolved population
Directional selection
Disruptive selection
Stabilizing selection
■ Unlike genetic drift and gene flow, natural selection consistently increases the frequencies of alleles that enhance survival and reproduction, thus improving the degree to which organisms are well-suited for life in their environment.
■ Sexual selection can result in secondary sex characteristics that can give individuals advantages in mating.
''',

'''
CONCEPT 24.1
The biological species concept emphasizes reproductive isolation (pp. 505-508)
A biological species is a group of populations whose individuals may interbreed and produce viable, fertile offspring with each other but not with members of other species. ■ The biological species concept emphasizes reproductive isolation through prezygotic and postzygotic barriers that separate gene pools.

''',

'''
CONCEPT 24.2
Speciation can take place with or without geographic separation (pp. 509-514)
■ In allopatric speciation, gene flow is reduced when two populations of one species become geographically separated from each other. One or both populations may undergo evo- lutionary change during the period of separation, resulting in the establishment of barriers to reproduction.
Original population
Allopatric speciation
Sympatric speciation
■ In sympatric speciation, a new species originates while remaining in the same geographic area as the parent species. Plant species (and, more rarely, animal species) have evolved sympatrically through polyploidy. Sympatric speciation can also result from sexual selection and habitat shifts.
''',

'''
CONCEPT 24.3
Hybrid zones reveal factors that cause reproductive isolation (pp. 514-518)
■ Many groups of organisms form hybrid zones in which mem- bers of different species meet and mate, producing at least some offspring of mixed ancestry.
■Many hybrid zones are stable, in that hybrid offspring continue to be produced over time. In others, reinforcement strength- ens prezygotic barriers to reproduction, thus decreasing the formation of unfit hybrids. In still other hybrid zones, barriers to reproduction may weaken over time, resulting in the fusion of the species' gene pools (reversing the speciation process).
''',

'''
CONCEPT 24.4
Speciation can occur rapidly or slowly and can result from changes in few
or many genes (pp. 518–521)
■New species can form rapidly once divergence begins-but it can take millions of years for that to happen. The time interval between speciation events varies considerably, from a few thou- sand years to tens of millions of years.
■ Researchers have identified particular genes involved in some cases of speciation. Speciation can be driven by few or many genes. ? Is speciation something that happened only in the distant past, or are new species continuing to arise today? Explain.

''',

'''
CONCEPT 25.1
Conditions on early Earth made the origin of life possible (pp. 524-526)
■ Experiments simulating possible early atmospheres have produced organic molecules from inorganic precursors. Amino acids, lipids, sugars, and nitrog- enous bases have also been found in meteorites. ■ Amino acids and RNA nucleotides polymerize when dripped onto hot sand, clay, or rock. Organic compounds can spontane- ously assemble into protocells, membrane-bounded droplets that have some properties of cells.
■The first genetic material may have self-replicating, catalytic RNA. Early protocells containing such RNA would have increased through natural selection.

''',

'''
CONCEPT 25.2
The fossil record documents the history of life (pp. 526-530)
■ The fossil record, based largely on fossils found in sedimentary rocks, documents the rise and fall of different groups of organ- isms over time.
■ Sedimentary strata reveal the relative ages of fossils. The ages of fossils can be estimated by radiometric dating and other methods.
■ The fossil record shows how new groups of organisms can arise via the gradual modification of preexisting organisms.
''',

'''
CONCEPT 25.3
Key events in life's history include the origins of unicellular and multicellular organisms and the colonization of land (pp. 530-535)
3.5 billion years
ago (bya): First prokaryotes (single-celled)
4,000 3,500
1.8 bya:
First eukaryotes (single-celled)
1.2 bya: First multicellular eukaryotes
2,500
500 mya: Colonization
of land by fungi, plants, and animals
2,000
1,500
1,000
500
535-525 mya: Cambrian explosion
3,000 Millions of years ago (mya)
(great increase in diversity
''',

'''
CONCEPT 25.4
The rise and fall of groups of organisms reflect differences in speciation and extinction rates (pp. 535-542)
■ In plate tectonics, continental plates move gradually over time, altering the physical geography and climate of Earth, leading to extinctions in some groups and speciation in others. ■ Evolutionary history has been punctuated by five mass extinctions that radically altered life's history. Possible causes for these extinctions include continental drift, volcanic activity, and impacts from comets.
■Large increases in the diversity of life have resulted from adaptive radiations that followed mass extinctions. Adaptive radiations have also occurred in groups of organisms that possessed major evolutionary innovations or that colonized new regions in which there was little competition from other organisms.
''',

'''
CONCEPT 25.5
Major changes in body form can result from changes in the sequences and regulation of developmental genes (pp. 542-545)
■ Developmental genes affect morphological differences between species by influencing the rate, timing, and spatial patterns of change in an organism's form as it develops into an adult.
■ The evolution of new forms can be caused by changes in the nucleotide sequences or regulation of developmental genes.
''',

'''
CONCEPT 25.6
Evolution is not goal oriented (pp. 545-547)
■ Novel and complex biological structures can evolve through a series of incremental modifications, each of which benefits the organism that possesses it.
■ Evolutionary trends can be caused by natural selection in a chang- ing environment or species selection, resulting from interactions between organisms and their current environments.

''',

'''
CONCEPT 26.1
Phylogenies show evolutionary
relationships (pp. 552-556)
■Linnaeus's binomial classification system gives
organisms two-part names: a genus plus a specific epithet.
■Clades can be distinguished by their shared derived characters.
■ In the Linnaean system, species are grouped in increasingly broad taxa: Related genera are placed in the same family, families in orders, orders in classes, classes in phyla, phyla in kingdoms, and (more recently) kingdoms in domains.
■ Systematists depict evolutionary relationships as branching phylogenetic trees. Many systematists propose that classifica- tion be based entirely on evolutionary relationships.
■ Unless branch lengths are proportional to time or genetic change, a phylogenetic tree indicates only patterns of descent.
■ Much information can be learned about a species from its evolu- tionary history; hence, phylogenies are useful in a wide range of applications.
Humans and chimpanzees are sister species. Explain what this statement means.
''',

'''
CONCEPT 26.2
Phylogenies are inferred from morphological and molecular data (pp. 556-557)
■ Organisms with similar morphologies or DNA sequences are likely to be more closely related than organisms with very differ- ent structures and genetic sequences.
To infer phylogeny, homology (similarity due to shared ancestry) must be distinguished from analogy (similarity due to convergent evolution).
■ Computer programs are used to align comparable DNA sequences and to distinguish molecular homologies from coincidental matches between taxa that diverged long ago.
''',
'''
CONCEPT 26.3
Shared characters are used to construct phylogenetic trees (pp. 557-563)
■ A clade is a monophyletic group that includes an ancestral species and all of its descendants.
Paraphyletic group
Among phylogenies, the most parsimonious tree is the one that requires the fewest evolutionary changes. The most likely tree is the one based on the most likely pattern of changes.
■ Well-supported phylogenetic hypotheses are consistent with a wide range of data.
''',

'''
CONCEPT 26.4
An organism's evolutionary history is documented in its genome (pp. 563-564)
■ Orthologous genes are homologous genes found in dif- ferent species as a result of speciation. Paralogous genes are homologous genes within a species that result from gene duplication; such genes can diverge and potentially take on new functions.
■ Distantly related species often have many orthologous genes. The small variation in gene number in organisms of varying complexity suggests that genes are versatile and may have multiple functions.
''',

'''
CONCEPT 26.5
Molecular clocks help track evolutionary time (pp. 564-566)
■ Some regions of DNA change at a rate consistent enough to serve as a molecular clock, a method of estimating the date of past evolutionary events based on the amount of genetic change. Other DNA regions change in a less predictable way.
■ Molecular clock analyses suggest that the most common strain of HIV jumped from primates to humans in the early 1900s.
''',

'''
CONCEPT 26.6
Our understanding of the tree of life continues to change based on new data (pp. 566-568)
■ Past classification systems have given way to the current view of the tree of life, which consists of three great domains: Bacteria, Archaea, and Eukarya.
Phylogenies based in part on rRNA genes suggest that eukaryotes are most closely related to archaea, while data from some other genes suggest a closer relationship to bacteria.
Genetic analyses indicate that extensive horizontal gene transfer has occurred throughout the evolutionary history of life.
''',

'''
CONCEPT 27.1
Structural and functional adaptations
contribute to prokaryotic
success (pp. 572-576)
Fimbriae: hairlike appendages that help cells
adhere to other cells or to a substrate
Capsule: sticky layer of polysaccharide or protein that can help cell
adherence and/or evasion of a host's immune system
Internal organization: no nucleus or other membrane- enclosed organelles; usually no complex compartmentalization
Cell wall: found in nearly all prokaryotes; structure differs in gram-positive and gram-negative bacteria
Flagella: structures used by most motile bacteria for propulsion; many species can move toward or away from certain stimuli
Circular chromosome: often accompanied by smaller rings of DNA called plasmids
Pilus: appendage that facilitates conjugation
■ Many prokaryotic species can reproduce quickly by binary fission, leading to the formation of extremely large populations.
''',

'''
CONCEPT 27.2
Rapid reproduction, mutation, and genetic recombination promote genetic diversity in prokaryotes (pp. 576-579)
Because prokaryotes can often proliferate rapidly, mutations can quickly increase a population's genetic variation. As a result, prokaryotic populations often can evolve in short periods of time in response to changing conditions. Genetic diversity in prokaryotes also can arise by recombina- tion of the DNA from two different cells (via transformation, transduction, or conjugation). By transferring advantageous alleles, such as ones for antibiotic resistance, recombination can promote adaptive evolution in prokaryotic populations. ? Mutations are rare and prokaryotes reproduce asexually, yet their populations can have high genetic diversity. Explain how this can occur.
''',
'''

CONCEPT 27.3
Diverse nutritional and metabolic adaptations have evolved in prokaryotes (pp. 579-580)
■ Nutritional diversity is much greater in prokaryotes than in eukaryotes and includes all four modes of nutrition: photoautotrophy, chemoautotrophy, photoheterotrophy, and chemoheterotrophy.
■ Among prokaryotes, obligate aerobes require O2, obligate anaerobes are poisoned by O2, and facultative anaerobes can survive with or without O2.
Unlike eukaryotes, prokaryotes can metabolize nitrogen in many different forms. Some can convert atmospheric nitrogen to ammonia, a process called nitrogen fixation.
■ Prokaryotic cells and even species may cooperate metabolically. Metabolic cooperation also occurs in surface-coating biofilms that include different species.
''',

'''
CONCEPT 27.4
Prokaryotes have radiated into a diverse set of lineages (pp. 581-585)
■ Molecular systematics is helping biologists classify prokaryotes and identify new clades.
■ Diverse nutritional types are scattered among the major groups of bacteria. The two largest groups are the proteobacteria and gram-positive bacteria.
■ Some archaea, such as extreme thermophiles and extreme halophiles, live in extreme environments. Other archaea live in moderate environments such as soils and lakes.
''',

'''
CONCEPT 27.5
Prokaryotes play crucial roles in the biosphere (pp. 585-586)
■ Decomposition by heterotrophic prokaryotes and the synthetic activities of autotrophic and nitrogen-fixing prokaryotes contrib- ute to the recycling of elements in ecosystems.
■ Many prokaryotes have a symbiotic relationship with a host; the relationships between prokaryotes and their hosts range from mutualism to commensalism to parasitism.
''',

'''
CONCEPT 27.6
Prokaryotes have both beneficial and harmful impacts on humans (pp. 586-589)
■ People depend on mutualistic prokaryotes, including hundreds of species that live in our intestines and help digest food.
■ Pathogenic bacteria typically cause disease by releasing exotoxins or endotoxins. Horizontal gene transfer can spread genes associ- ated with virulence to harmless species or strains.
■ Prokaryotes can be used in bioremediation and production of plastics, vitamins, antibiotics, and other products.
''',

'''

CONCEPT 28.1
Most eukaryotes are single-celled organisms (pp. 592-597)
Domain Eukarya includes many groups of protists, along with plants, animals, and fungi. Unlike pro- karyotes, protists and other eukaryotes have a nucleus and other membrane-enclosed organelles, as well as a cytoskeleton that enables them to have asymmetric forms and to change shape as they feed, move, or grow.
Protists are structurally and functionally diverse and have a wide variety of life cycles. Most are unicellular. Protists include photo- autotrophs, heterotrophs, and mixotrophs.
■ Current evidence indicates that eukaryotes originated by endosymbiosis when an archaeal host (or a host closely related to the archaeans) engulfed an alpha proteobacterium that would evolve into an organelle found in all eukaryotes, the mitochondrion.
■ Plastids are thought to be descendants of cyanobacteria that were engulfed by early eukaryotic cells. The plastid-bearing lineage eventually evolved into red algae and green algae. Other protist groups evolved from secondary endosymbiotic events in which red algae or green algae were themselves engulfed.
In one hypothesis, eukaryotes are grouped into four supergroups, each a monophyletic clade: Excavata, SAR, Archaeplastida, and Unikonta.
''',

'''


CONCEPT 28.2
Excavates include protists with modified mitochondria and protists with unique flagella (pp. 597-599)
? What evidence indicates that the excavates form a clade?
Diplomonads and parabasalids
Euglenozoans
Kinetoplastids Euglenids
Modified mitochondria
Spiral or crystalline rod inside flagella
Giardia, Trichomonas
Trypanosoma, Euglena

''',

'''


CONCEPT 28.3
SAR is a highly diverse group of protists defined by DNA similarities (pp. 599-606) ? Although they are not photosynthetic, apicomplexan parasites such as Plasmodium have modified plastids. Describe a current hypothesis that explains this observation.
Stramenopiles Diatoms Golden algae
Brown algae Alveolates Dinoflagellates
Hairy and smooth flagella
Membrane-enclosed sacs (alveoli) beneath plasma membrane
Phytophthora, Laminaria
Pfiesteria,
Plasmodium,
Paramecium
Apicomplexans Ciliates
Rhizarians
Amoebas with threadlike pseudopodia
Globigerina
Radiolarians
Forams
Cercozoans

''',

'''


CONCEPT 28.4
Red algae and green algae are the closest relatives of plants (pp. 606-608)
Red algae
Green algae
Phycoerythrin (photosyn thetic pigment)
Plant-type chloroplasts
Plants
Porphyra
Chlamydomonas,
Ulva
Mosses, ferns, conifers,
flowering
plants

''',

'''


CONCEPT 28.5
Unikonts include protists that
are closely related to fungi
Amoebozoans
Slime molds Tubulinids
Entamoebas
Amoebas with lobe- shaped or tube-shaped pseudopodia
(Highly variable; see Chapters 31-34.)
Amoeba, Dictyostelium
Choanoflagellates, nucleariids, animals,
and animals (pp. 608-612)
Opisthokonts
? Describe a key feature for each of the main protist subgroups
of Unikonta.
fungi

''',

'''


CONCEPT 28.6
Protists play key roles in ecological communities (pp. 612-613)
■ Protists form a wide range of mutualistic and parasitic relationships that affect their symbiotic partners and many other members of the community.
■ Photosynthetic protists are among the most important producers in aquatic communities. Because they are at the base of the food web, factors that affect photosynthetic protists affect many other species in the community.

''',

'''


SUMMARY OF KEY CONCEPTS
CONCEPT 29.1
Plants evolved from green algae (pp. 617-622)
■ Morphological and biochemical traits, as well as similarities in nuclear and chloroplast genes, indi- cate that certain groups of charophytes are the clos- est living relatives of plants.
A protective layer of sporopollenin and other traits allow charo- phytes to tolerate occasional drying along the edges of ponds and lakes. Such traits may have enabled the algal ancestors of plants to survive in terrestrial conditions, opening the way to the coloniza- tion of dry land.
■ Derived traits that distinguish plants from charophytes, their closest algal relatives, include cuticles, stomata, multicellular dependent embryos, and the four shown here:

''',

'''
CONCEPT 29.2
Mosses and other nonvascular plants have life cycles dominated by gametophytes (pp. 622-626)
Lineages leading to the three extant clades of nonvascular plants, or bryophytes-liverworts, mosses, and hornworts- diverged from other plants early in plant evolution.
In bryophytes, the dominant generation consists of haploid gametophytes, such as those that make up a carpet of moss. Rhizoids anchor gametophytes to the substrate on which they grow. The flagellated sperm produced by antheridia require a film of water to travel to the eggs in the archegonia. The diploid stage of the life cycle—the sporophytes—grow out of archegonia and are attached to the gametophytes and depen- dent on them for nourishment. Smaller and simpler than vascular plant sporophytes, they typically consist of a foot, seta (stalk), and sporangium.
Sphagnum, or peat moss, is common in large regions known as peatlands and has many practical uses, including as a fuel. ? Summarize the ecological importance of mosses.

''',

'''
CONCEPT 29.3
Ferns and other seedless vascular plants were the first plants to grow tall (pp. 626-632)
■ Fossils of the forerunners of today's vascular plants date back about 425 million years and show that these small plants had independent, branching sporophytes and a vascular system. Over time, other derived traits of living vascular plants arose, such as a life cycle with dominant sporophytes, lignified vascular tissue, well-developed roots and leaves, and sporophylls.
■ Seedless vascular plants include the lycophytes (phylum Lycophyta: club mosses, spikemosses, and quillworts) and the monilophytes (phylum Monilophyta: ferns, horsetails, and whisk ferns and relatives). Current evidence indicates that seed- less vascular plants, like bryophytes, do not form a clade. ■ Ancient lineages of lycophytes included both small herbaceous plants and large trees. Present-day lycophytes are small herba- ceous plants.
Seedless vascular plants formed the earliest forests about
385 million years ago. Their growth may have contributed to a major global cooling that took place during the Carboniferous period. The decaying remnants of the first forests eventually became coal.

''',

'''


SUMMARY OF KEY CONCEPTS
CONCEPT 30.1
Seeds and pollen grains are key
adaptations for life on land (pp. 635-637)
Five Derived Traits of Seed Plants
Reduced gametophytes
Microscopic male and
female gametophytes
(n) are nourished and
protected by the
Heterospory
sporophyte (2n)
Microspore (gives rise to a male gametophyte) Megaspore (gives rise to a female gametophyte)
Integument (2n)
(gymnosperm) Megaspore (n)
Ovules
Ovule
-Male gametophyte
-Female gametophyte
Megasporangium (2n)
Pollen
Pollen grains make water
unnecessary for fertilization
Seeds
Seeds: survive
Seed coat-
better than
unprotected
Food supply
Embryo
spores, can be
transported
long distances

''',

'''
CONCEPT 30.2
Gymnosperms bear "naked" seeds, typically on cones (pp. 637-642)
• Dominance of the sporophyte generation, the development of seeds from fertilized ovules, and the role of pollen in transfer- ring sperm to ovules are key features of a typical gymnosperm life cycle.
■ Gymnosperms appear early in the plant fossil record and domi- nated many Mesozoic terrestrial ecosystems. Living seed plants can be divided into two monophyletic groups: gymnosperms and angiosperms. Extant gymnosperms include cycads, Ginkgo biloba, gnetophytes, and conifers.
''',
'''
CONCEPT 30.3
The reproductive adaptations of angiosperms include flowers and fruits (pp. 642-649)
■Flowers generally consist of four types of modified leaves: sepals, petals, stamens (which produce pollen), and carpels (which produce ovules). Ovaries ripen into fruits, which often carry seeds by wind, water, or animals to new locations.
■Flowering plants originated about 140 million years ago, and by the mid-Cretaceous (100 mya) had begun to dominate some terrestrial ecosystems. Fossils and phylogenetic analyses offer insights into the origin of flowers.
Several groups of basal angiosperms have been identified. Other major clades of angiosperms include magnoliids, monocots, and eudicots.
Pollination and other interactions between angiosperms and animals may have contributed to the success of flowering plants during the last 100 million years.
''',

'''


CONCEPT 30.4
Human welfare depends on seed plants (pp. 649-650)
Humans depend on seed plants for products such as food, wood, and many medicines.
■ Destruction of habitat threatens the extinction of many plant species and the animal species they support.

''',

'''

CONCEPT 31.1
Fungi are heterotrophs that feed by absorption (pp. 653-655)
VOCAB SELF-QUIZ goo.gl/6u55ks
. All fungi (including decomposers and symbionts) are heterotrophs that acquire nutrients by absorp- tion. Many fungi secrete enzymes that break down complex molecules. Most fungi grow as thin, multicellular filaments called hyphae; relatively few species grow only as single-celled yeasts. In their multicellular form, fungi consist of mycelia, networks of branched hyphae adapted for absorption. Mycorrhizal fungi have specialized hyphae that enable them to form a mutually benefi- cial relationship with plants.

''',

'''
CONCEPT 31.2
Fungi produce spores through sexual or asexual life cycles (pp. 655-657)
In fungi, the sexual life cycle involves cytoplasmic fusion (plasmogamy) and nuclear fusion (karyogamy), with an
intervening heterokaryotic stage in which cells have haploid nuclei from two parents. The diploid cells resulting from karyog- amy are short-lived and undergo meiosis, producing genetically diverse haploid spores.
Many fungi can reproduce asexually as filamentous fungi or yeasts.
''',

'''
CONCEPT 31.3
The ancestor of fungi was an aquatic, single-celled, flagellated protist (pp. 657-658)
Molecular evidence indicates that fungi and animals diverged over a billion years ago from a common unicellular ancestor that had a flagellum. However, the oldest fossils that are widely accepted as fungi are 460 million years old.
■ Chytrids, a group of fungi with flagellated spores, include some basal lineages.
■ Fungi were among the earliest colonizers of land; fossil evidence indicates that these colonizers included species that were symbi- onts with early plants.
''',

'''
CONCEPT 31.4
Fungi have radiated into a diverse set of lineages (pp. 658-665)
Fungal Phylum
Chytridiomycota
Distinguishing Features
Flagellated spores
Resistant zygosporangium
(chytrids)
Zygomycota
(zygomycetes)
as sexual stage
Glomeromycota
(arbuscular
mycorrhizal fungi)
Ascomycota
(ascomycetes)
Basidiomycota (basidiomycetes)
Arbuscular mycorrhizae formed with plants
Sexual spores (ascospores) borne internally in sacs called asci; vast numbers of asexual spores (conidia) produced
Elaborate fruiting body (basidiocarp) containing many basidia that produce sexual spores (basidiospores)

''',

'''
CONCEPT 31.5
Fungi play key roles in nutrient cycling, ecological interactions, and human welfare (pp. 665-669)
■Fungi perform essential recycling of chemical elements between the living and nonliving world.
■Lichens are highly integrated symbiotic associations of fungi and algae or cyanobacteria.
■ Many fungi are parasites, mostly of plants.
■ Humans use fungi for food and to make antibiotics.

''',

'''
CONCEPT 32.1
Animals are multicellular, heterotrophic eukaryotes with tissues that develop from embryonic layers (pp. 672-673)
Animals are heterotrophs that ingest their food.
Animals are multicellular eukaryotes. Their cells are supported and connected to one another by collagen and other structural proteins located outside the cell membrane. Nervous tissue and muscle tissue are key animal features.
In most animals, gastrulation follows the formation of the blastula and leads to the formation of embryonic tissue layers. Most animals have Hox genes that regulate the development of body form. Although Hox genes have been highly conserved over the course of evolution, they can produce a wide diversity of animal morphology.

''',

'''
CONCEPT 32.2
The history of animals spans more than half a billion years (pp. 673-677)
■ Fossil biochemical evidence and molecular clock analyses indicate that animals arose over 700 million years ago.
■ Genomic analyses suggest that key steps in the origin of animals involved new ways of using proteins that were encoded by genes found in choanoflagellates.
560 mya:
Ediacaran animals
365 mya: Early land vertebrates
Origin and diversification of dinosaurs
Increased
diversity of mammals
Era
Neoproterozoic
Paleozoic
Mesozoic
Ceno- zoic
1,000
541
252
66
0
Millions of years ago (mya)
''',

'''
CONCEPT 32.3
Animals can be characterized by "body plans" (pp. 677–680)
Animals may lack symmetry or may have radial or bilateral symmetry. Bilaterally symmetrical animals have dorsal and ventral sides, as well as anterior and posterior ends. Eumetazoan embryos may be diploblastic (two germ layers) or triploblastic (three germ layers). Triploblastic animals with a body cavity may have a pseudocoelom or a true coelom.
■ Protostome and deuterostome development often differ in patterns of cleavage, coelom formation, and blastopore fate.

''',

'''
SUMMARY OF KEY CONCEPTS
CONCEPT 35.1
Plants have a hierarchical organization
consisting of organs, tissues, and
cells (pp. 757-763)
Vascular plants have shoots consisting of stems, leaves, and, in angiosperms, flowers. Roots anchor
the plant, absorb and conduct water and minerals, and store food. Leaves are attached to stem nodes and are the main organs of photosynthesis. The axillary buds, in axils of leaves and stems, give rise to branches. Plant organs may be adapted for specialized functions.
■ Vascular plants have three tissue systems-dermal, vascular, and ground—which are continuous throughout the plant. The
dermal tissue is a continuous layer of cells that covers the plant exterior. Vascular tissues (xylem and phloem) facilitate the long-distance transport of substances. Ground tissues function in storage, metabolism, and regeneration.
Parenchyma cells are relatively undifferentiated and thin-walled cells that retain the ability to divide; they perform most of the metabolic functions of synthesis and storage. Collenchyma cells have unevenly thickened walls; they support young, growing parts of the plant. Sclerenchyma cells—sclereids and fibers have thick, lignified walls that help support mature, nongrowing parts of the plant. Tracheids and vessel elements, the water-conducting cells of xylem, have thick walls and are dead at functional maturity. Sieve-tube elements are living but highly modified cells that are largely devoid of internal organelles; they function in the transport of sugars through the phloem of angiosperms.

''',

'''


CONCEPT 35.3
Primary growth lengthens roots and shoots (pp. 766-769)
■ The root apical meristem is located near the tip of the root,
where it generates cells for the growing root axis and the root cap. ■ The apical meristem of a shoot is located in the apical bud, where it gives rise to alternating internodes and leaf-bearing nodes. ■ Eudicot stems have vascular bundles in a ring, whereas monocot stems have scattered vascular bundles.
■ Mesophyll cells are adapted for photosynthesis. Stomata, epi- dermal pores formed by pairs of guard cells, allow for gaseous exchange and are major avenues for water loss.
Dermal
Ground
Vascular
Stoma
Upper epidermis
Xylem
Phloem
Palisade
mesophyll
Spongy
mesophyll
Vein
Lower epidermis
Guard cells

''',

'''
CONCEPT 35.4
Secondary growth increases the diameter
of stems and roots in woody plants (pp. 770-773)
■ The vascular cambium is a meristematic cylinder that produces secondary xylem and secondary phloem during secondary growth. Older layers of secondary xylem (heartwood) become inactive, whereas younger layers (sapwood) still conduct water.
The cork cambium gives rise to a thick protective covering called the periderm, which consists of the cork cambium plus the layers of cork cells it produces.

''',

'''

CONCEPT 35.5
Growth, morphogenesis, and cell differentiation produce the plant body (pp. 773-779)
Cell division and cell expansion are the primary determinants of growth. A preprophase band of microtubules determines where a cell plate will form in a dividing cell. Microtubule orientation also affects the direction of cell elongation by controlling the orienta- tion of cellulose microfibrils in the cell wall.
■ Morphogenesis, the development of body shape and organiza- tion, depends on cells responding to positional information from their neighbors.
■ Cell differentiation, arising from differential gene activation, enables cells within the plant to assume different functions despite having identical genomes. The way in which a plant cell differentiates is determined largely by the cell's position in the developing plant.
Internal or environmental cues may cause a plant to switch from one developmental stage to another-for example, from develop- ing juvenile leaves to developing mature leaves. Such morpho- logical changes are called phase changes.
■ Research on organ identity genes in developing flowers pro- vides a model system for studying pattern formation. The ABC hypothesis identifies how three classes of organ identity genes control formation of sepals, petals, stamens, and carpels.
''',

'''
CONCEPT 36.1
Adaptations for acquiring resources were key steps in the evolution of vascular plants (pp. 783-785)
CO2
Minerals
CO2
H2O
■Leaves typically function in gathering sunlight and CO2. Stems serve as supporting structures for leaves and as conduits for the long-distance transport of water and nutrients. Roots mine the soil for water and minerals and anchor the whole plant.
■ Natural selection has produced plant architectures that optimize resource acquisition in the ecological niche in which the plant species naturally exists.

''',

'''

CONCEPT 36.2
Different mechanisms transport substances over short or long distances (pp. 785-790)
The selective permeability of the plasma membrane controls the movement of substances into and out of cells. Both active and passive transport mechanisms occur in plants.
■ Plant tissues have two major compartments: the apoplast (every- thing outside the cells' plasma membranes) and the symplast (the cytosol and connecting plasmodesmata).
■ Direction of water movement depends on the water potential, a quantity that incorporates solute concentration and physical pressure. The osmotic uptake of water by plant cells and the resulting internal pressure that builds up make plant cells turgid. ■Long-distance transport occurs through bulk flow, the move- ment of liquid in response to a pressure gradient. Bulk flow occurs within the tracheids and vessel elements of the xylem and within the sieve-tube elements of the phloem.
''',

'''
CONCEPT 36.3
Transpiration drives the transport of water and minerals from roots to shoots via the xylem (pp. 790–794)
■ Water and minerals from the soil enter the plant through the epidermis of roots, cross the root cortex, and then pass into the
vascular cylinder by way of the selectively permeable cells of the endodermis. From the vascular cylinder, the xylem sap is transported long distances by bulk flow to the veins that branch throughout each leaf.
The cohesion-tension hypothesis proposes that the move- ment of xylem sap is driven by a water potential difference cre- ated at the leaf end of the xylem by the evaporation of water from leaf cells. Evaporation lowers the water potential at the air-water interface, thereby generating the negative pressure that pulls water through the xylem.
''',

'''
CONCEPT 36.4
The rate of transpiration is regulated
by stomata (pp. 794-797)
■ Transpiration is the loss of water vapor from plants. Wilting occurs when the water lost by transpiration is not replaced by absorption from roots. Plants respond to water deficits by closing their stomata. Under prolonged drought conditions, plants can become irreversibly injured.
■ Stomata are the major pathway for water loss from plants. A stoma opens when guard cells bordering the stomatal pore take up K+. The opening and closing of stomata are controlled by light, CO2, the drought hormone abscisic acid, and a circadian rhythm.
Xerophytes are plants that are adapted to arid environments. Reduced leaves and CAM photosynthesis are examples of adaptations to arid environments.
''',

'''
CONCEPT 36.5
Sugars are transported from sources to sinks via the phloem (pp. 797-799)
Mature leaves are the main sugar sources, although storage organs can be seasonal sources. Growing organs such as roots, stems, and fruits are the main sugar sinks. The direction of phloem transport is always from sugar source to sugar sink.
■ Phloem loading depends on the active transport of sucrose. Sucrose is cotransported with H*, which diffuses down a gradient generated by proton pumps. Loading of sugar at the source and unloading at the sink maintain a pressure difference that keeps phloem sap flowing through a sieve tube.
''',

'''
CONCEPT 36.6
The symplast is highly dynamic (pp. 799–800)
■ Plasmodesmata can change in permeability and number. When dilated, they provide a passageway for the symplastic transport of proteins, RNAs, and other macromolecules over long distances. The phloem also conducts nerve-like electrical signals that help integrate whole-plant function.

''',

'''
CONCEPT 37.1
Soil contains a living, complex ecosystem (pp. 804-807)
■ Soil particles of various sizes derived from the breakdown of rock are found in soil. Soil particle size affects the availability of water, oxygen, and minerals in the soil.
■ A soil's composition encompasses its inorganic and organic components. Topsoil is a complex ecosystem teeming with bacteria, fungi, protists, animals, and the roots of plants.
■ Some agricultural practices can deplete the mineral content of soil, tax water reserves, and promote erosion. The goal of soil conservation is to minimize this damage.
''',
'''
CONCEPT 37.2
Plant roots absorb essential elements from the soil (pp. 807-810)
- Macronutrients, elements required in relatively large amounts, include carbon, oxygen, hydrogen, nitrogen, and other major ingredients of organic compounds. Micronutrients, elements required in very small amounts, typically have catalytic functions as cofactors of enzymes.
■Deficiency of a mobile nutrient usually affects older organs
more than younger ones; the reverse is true for nutrients that are less mobile within a plant. Macronutrient deficiencies are most common, particularly deficiencies of nitrogen, phosphorus, and potassium.
Rather than tailoring the soil to match the plant, genetic engineers are tailoring the plant to match the soil.
''',

'''
CONCEPT 37.3
Plant nutrition often involves relationships with other organisms (pp. 810-818)
Rhizobacteria derive their energy from the rhizosphere, a microorganism-enriched ecosystem intimately associated with roots. Plant secretions support the energy needs of the rhizo- sphere. Some rhizobacteria produce antibiotics, whereas others make nutrients more available for plants. Most are free-living, but some live inside plants. Plants satisfy most of their huge needs for nitrogen from the bacterial decomposition of humus and the fixation of gaseous nitrogen.
(from atmosphere) N2
Proteins from humus (dead organic material)
Microbial decomposition
Denitrifying
(to atmosphere) (N2
Nitrogen-fixing bacteria
NHA
Amino acids
bacteria
Ammonifying bacteria
Weathering of rock
NO2 (nitrite)
·NO3
(nitrate)
Nitrifying bacteria
Nitrifying bacteria
Root
NH3 (ammonia)
H+ (from soil) NHA (ammonium)
Nitrogen-fixing bacteria convert atmospheric N2 to nitrogenous minerals that plants can absorb as a nitrogen source for organic synthesis. The most efficient mutualism between plants and nitrogen-fixing bacteria occurs in the nodules that are formed by Rhizobium bacteria growing in the roots of legumes. These bacteria obtain sugar from the plant and supply the plant with fixed nitrogen. In agriculture, legume crops are rotated with other crops to restore nitrogen to the soil.
Mycorrhizae are mutualistic associations of fungi and roots. The fungal hyphae of mycorrhizae absorb water and minerals, which they supply to their plant hosts.
Epiphytes grow on the surfaces of other plants but acquire water and minerals from rain. Parasitic plants absorb nutrients from host plants. Carnivorous plants supplement their mineral nutri- tion by digesting animals.
''',
'''
CONCEPT 38.1
Flowers, double fertilization, and fruits are key features of the angiosperm life cycle (pp. 821-830)
Angiosperm reproduction involves an alternation of generations between a multicellular diploid sporophyte generation and a multicellular haploid gametophyte generation. Flowers, produced by the sporophyte, function in sexual reproduction.
The four floral organs are sepals, petals, stamens, and carpels. Sepals protect the floral bud. Petals help attract pollinators. Stamens bear anthers in which haploid microspores develop into pollen grains containing a male gametophyte. Carpels contain ovules (immature seeds) in their swollen bases. Within the ovules, embryo sacs (female gametophytes) develop from megaspores.
Pollination, which pre- cedes fertilization, is the placing of pollen on the stigma of a carpel.
After pollination, the pollen tube discharges two sperm into the female gametophyte. Two sperm are needed for double fertilization, a process in which one sperm fertilizes the egg, forming a zygote and eventually an embryo, while the other sperm
Tube
nucleus
One sperm will fuse with the egg, forming a zygote (2n).
One sperm cell will fuse with the two polar nuclei, forming an endosperm nucleus (3n).
combines with the polar nuclei, giving rise to the food-storing endosperm.
A seed consists of a dormant embryo along with a food supply stocked in either the endosperm or the cotyledons. Seed dormancy ensures that seeds germinate only when conditions for seedling survival are optimal. The breaking of dormancy often requires environmental cues, such as temperature or lighting changes.
The fruit protects the enclosed seeds and aids in wind dispersal or in the attraction of seed-dispersing animals.
''',

'''
CONCEPT 38.2
Flowering plants reproduce sexually, asexually, or both (pp. 831-834)
■ Asexual reproduction, also known as vegetative reproduction, enables successful plants to proliferate quickly. Sexual reproduction generates most of the genetic variation that makes evolutionary adaptation possible.
Plants have evolved many mechanisms to avoid self-fertilization, including having male and female flowers on different individu- als, nonsynchronous production of male and female parts within a single flower, and self-incompatibility reactions in which pollen grains that bear an allele identical to one in the female are rejected.
Plants can be cloned from single cells, which can be genetically manipulated before being allowed to develop into a plant.
''',
'''

CONCEPT 38.3
People modify crops by breeding and genetic
engineering (pp. 834–838)
Hybridization of different varieties and even species of plants is common in nature and has been used by breeders, ancient and modern, to introduce new genes into crops. After two plants are successfully hybridized, plant breeders select those progeny that have the desired traits.
In genetic engineering, genes from unrelated organisms are incorporated into plants. Genetically modified (GM) plants can increase the quality and quantity of food worldwide and may also become increasingly important as biofuels.
There are concerns about the unknown risks of releasing GM organisms into the environment, but the potential benefits of transgenic crops need to be considered.

''',

'''

CONCEPT 39.2
Plant hormones help coordinate growth, development, and responses to stimuli (pp. 844–853)
Hormones control plant growth and development by affecting the division, elongation, and differentiation of cells. Some also mediate the responses of plants to environmental stimuli.
Auxin
Stimulates cell elongation; regulates branching and organ bending
Cytokinins
Stimulate plant cell division; promote later bud growth; slow organ death
Gibberellins
promote stem elongation; help seeds break dormancy and use stored reserves
Abscisic acid
promotes stomatal closure in response to drought; promotes seed dormancy
Ethylene
Mediates fruit ripening and the triple response
Brassinosteroids
Chemically similar to the sex hormones of animals; induce cell elongation and division
Jasmonates
Mediate plant defenses against insect herbivores; regulate a wide range of physiological processes
Strigolactones
Regulate apical dominance, seed germina- tion, and mycorrhizal associations

''',

'''

CONCEPT 39.3
Responses to light are critical for plant
success (pp. 853–859)
Blue-light photoreceptors control hypocotyl elongation, stomatal opening, and phototropism.
Phytochromes act like molecular “on-off” switches that regulate shade avoidance and germination of many seed types. Red light turns phytochrome “on,” and far-red light turns it “off.”
Phytochrome conversion also provides information about
the day length (photoperiod) and hence the time of year. Photoperiodism regulates the time of flowering in many species. Short-day plants require a night longer than a critical length to flower. Long-day plants need a night length shorter than a critical period to flower.
Many daily rhythms in plant behavior are controlled by an internal circadian clock. Free-running circadian rhythms are approximately 24 hours long but are entrained to exactly
24 hours by dawn and dusk effects on phytochrome form.

''',

'''

CONCEPT 39.4
Plants respond to a wide variety of stimuli
other than light (pp. 859–863)
Gravitropism is bending in response to gravity. Roots
show positive gravitropism, and stems show negative gravi- tropism. Statoliths, starch-filled plastids, enable roots to detect gravity.
Thigmotropism is a growth response to touch. Rapid leaf movements involve transmission of electrical impulses.
Plants are sensitive to environmental stresses, including drought, flooding, high salinity, and extremes of temperature.
Drought
ABA production, reducing water loss by closing stomata
Flooding
Formation of air tubes that help roots survive oxygen deprivation
Salt
Avoiding osmotic water loss by producing solutes tolerated at high concentrations
Heat
Synthesis of heat-shock proteins, which reduce protein denaturation at high temperatures
Cold
Adjusting membrane fluidity; avoiding osmotic water loss; producing antifreeze proteins
''',

'''

CONCEPT 39.5
Plants respond to attacks by pathogens
and herbivores (pp. 864–867)
The hypersensitive response seals off an infection and destroys both pathogen and host cells in the region. Systemic acquired resistance is a generalized defense response in organs distant from the infection site.
In addition to physical defenses such as thorns and trichomes, plants produce distasteful or toxic chemicals, as well as attractants that recruit animals that destroy herbivores.

''',

'''
CONCEPT 41.1
An animal's diet must supply chemical energy, organic building blocks, and essential nutrients (pp. 897-900)
Food provides animals with energy for ATP production, carbon skeletons for biosynthesis, and essential nutrients-nutrients that must be supplied in preassembled form. Essential nutrients include certain amino acids and fatty acids that animals cannot synthesize; vitamins, which are organic molecules; and minerals, which are inorganic substances.
■ Malnutrition results from an inadequate intake of essential
nutrients or a deficiency in sources of chemical energy. Studies of disease at the population level help researchers determine human dietary requirements.
''',

'''
CONCEPT 41.2
Food processing involves ingestion, digestion, absorption, and elimination (pp. 900-903)
■ Animals differ in the ways they obtain and ingest food. Many ani- mals are bulk feeders, eating large pieces of food. Other strategies include filter feeding, substrate feeding, and fluid feeding. ■ Compartmentalization is necessary to avoid self-digestion. In intra- cellular digestion, food particles are engulfed by phagocytosis and digested within food vacuoles that have fused with lysosomes. In extracellular digestion, which is used by most animals, enzymatic hydrolysis occurs outside cells in a gastrovascular cavity or alimentary canal.
''',
'''
CONCEPT 41.3
Organs specialized for sequential stages of food processing form the mammalian digestive system (pp. 903-909)
Veins to heart
Hepatic portal vein
Lymphatic system
Liver
Mouth
Stomach
Absorbed food Absorbed (except lipids) water
Esophagus
Lipids
Secretions Secretions from
from salivary gastric glands
glands
Small intestine Secretions from liver
Anus
Secretions from pancreas
Large intestine
Rectum
''',
'''
CONCEPT 41.4
Evolutionary adaptations of vertebrate digestive systems correlate with diet (pp. 909-912)
■ Vertebrate digestive systems display many evolutionary adapta- tions associated with diet. For example, the assortment of teeth (dentition) generally correlates with diet. Also, many herbivores have fermentation chambers where mutualistic microorgan- isms digest cellulose. In addition, herbivores usually have longer alimentary canals than carnivores, reflecting the longer time needed to digest vegetation.
''',
'''
CONCEPT 41.5
Feedback circuits regulate digestion, energy storage, and appetite (pp. 912-916)
■ Nutrition is regulated at multiple levels. Food intake triggers nervous and hormonal responses that cause secretion of diges- tive juices and promote movement of ingested material through the canal. The hormones insulin and glucagon control the synthesis and breakdown of glycogen, thereby regulating glucose availability.
■ Vertebrates store excess calories in glycogen (in liver and muscle cells) and in fat (in adipose cells). These energy stores can be tapped when an animal expends more calories than it consumes. If, how- ever, an animal consumes more calories than it needs for normal metabolism, the resulting overnourishment can cause obesity. Several hormones, including leptin and insulin, regulate appetite by affecting the brain's satiety center.

''',

'''

CONCEPT 42.1
Circulatory systems link exchange surfaces with cells throughout the body (pp. 920–924)
In animals with simple body plans, a gastrovascular
cavity mediates exchange between the environment and cells that can be reached by diffusion. Because diffusion is slow over long distances, most complex animals have a circulatory system that
moves fluid between cells and the organs that carry out exchange with the environment. Arthropods and most molluscs have an open circulatory system, in which hemolymph bathes organs directly. Vertebrates have a closed circulatory system, in which blood circulates in a closed network of pumps and vessels.
The closed circulatory system of vertebrates consists of blood, blood vessels, and a two- to four-chambered heart. Blood pumped by a heart ventricle passes to arteries and then to the capillaries, sites of chemical exchange between blood and inter- stitial fluid. Veins return blood from capillaries to an atrium, which passes blood to a ventricle. Fishes, rays, and sharks have a single pump in their circulation. Air-breathing vertebrates have two pumps combined in a single heart. Variations in ventricle
number and separation reflect adaptations to different environ- ments and metabolic needs.

''',

'''
CONCEPT 42.2
Coordinated cycles of heart contraction drive
double circulation in mammals (pp. 924–927)
The right ventricle pumps blood to the lungs, where it loads O2 and unloads CO2. Oxygen-rich blood from the lungs enters the heart at the left atrium and is pumped to the body tissues by the left ventricle. Blood returns to the heart through the right atrium.
The cardiac cycle, a complete sequence of the heart’s pumping and filling, consists of a period of contraction, called systole, and a period of relaxation, called diastole. Heart function can be assessed by measuring the pulse (number of times the heart beats each minute) and cardiac output (volume of blood pumped by each ventricle per minute).
The heartbeat originates with impulses at the sinoatrial (SA) node (pacemaker) of the right atrium. They trigger atrial con- traction, are delayed at the atrioventricular (AV) node, and are then conducted along the bundle branches and Purkinje fibers, triggering ventricular contraction. The nervous system, hormones, and body temperature affect pacemaker activity.

''',

'''
CONCEPT 42.3
Patterns of blood pressure and flow reflect the structure and arrangement of blood vessels (pp. 927–931)
Blood vessels have structures well adapted to function. Capillaries have narrow diameters and thin walls that facilitate exchange. The velocity of blood flow is lowest in the capillary beds as a result of their large total cross-sectional area. Arteries contain thick elastic walls that maintain blood pressure. Veins contain one-way valves that contribute to the return of blood to the heart. Blood pressure is altered by changes in cardiac output and by variable constriction of arterioles.
Fluid leaks out of capillaries and is returned to blood by the lymphatic system, which also defends against infection.


''',

'''

CONCEPT 42.4
Blood components function in exchange,
transport, and defense (pp. 932–937)
Whole blood consists of cells and cell fragments (platelets) sus- pended in a liquid matrix called plasma. Plasma proteins influ- ence blood pH, osmotic pressure, and viscosity, and they function in lipid transport, immunity (antibodies), and blood clotting (fibrinogen). Red blood cells, or erythrocytes, transport O2. Five types of white blood cells, or leukocytes, function in defense against microorganisms and foreign substances in the blood. Platelets function in blood clotting, a cascade of reactions that converts plasma fibrinogen to fibrin.
A variety of diseases impair function of the circulatory system. In sickle-cell disease, an aberrant form of hemoglobin disrupts erythrocyte shape and function, leading to blockage of small blood vessels and a decrease in the oxygen-carrying capacity of the blood. In cardiovascular disease, inflammation of the arterial lining enhances deposition of lipids and cells, resulting in the potential for life-threatening damage to the heart or brain.

''',

'''
CONCEPT 42.5
Gas exchange occurs across specialized
respiratory surfaces (pp. 937–942)
At all sites of gas exchange, a gas undergoes net diffusion from where its partial pressure is higher to where it is lower. Air is more conducive to gas exchange than water because air has a higher O2 content, lower density, and lower viscosity.
The structure and organization of respiratory surfaces differ among animal species. Gills are outfoldings of the body surface special-
ized for gas exchange in water. The effectiveness of gas exchange in some gills, including those of fishes, is increased by ventilation and countercurrent exchange between blood and water. Gas exchange in insects relies on a tracheal system, a branched net- work of tubes that bring O2 directly to cells. Spiders, land snails, and most terrestrial vertebrates have internal lungs. In mammals, air inhaled through the nostrils passes through the pharynx into the trachea, bronchi, bronchioles, and dead-end alveoli, where gas exchange occurs.
''',

'''

CONCEPT 42.6
Breathing ventilates the lungs (pp. 942–944)
Breathing mechanisms vary substantially among vertebrates. An amphibian ventilates its lungs by positive pressure breathing, which forces air down the trachea. Birds use a system of air sacs as bellows to keep air flowing through the lungs in one direction only, preventing the mixing of incoming and outgoing air. Mammals ventilate their lungs by negative pressure breathing, which pulls air into the lungs when the rib muscles and diaphragm contract. Incoming and outgoing air mix, decreasing the efficiency of ventilation.
Sensors detect the pH of cerebrospinal fluid (reflecting CO2 concentration in the blood), and a control center in the brain adjusts breathing rate and depth to match metabolic demands.
Additional input to the control center is provided by sensors in the aorta and carotid arteries that monitor blood levels of O2 as well as CO2 (via blood pH).
''',

'''
CONCEPT 42.7
Adaptations for gas exchange include pigments
that bind and transport gases (pp. 945–947)
In the lungs, gradients of partial pressure favor the net diffusion of O2 into the blood and CO2 out of the blood. The opposite situ- ation exists in the rest of the body. Respiratory pigments such as hemocyanin and hemoglobin bind O2, greatly increasing the amount of O2 transported by the circulatory system. Evolutionary adaptations enable some animals to satisfy extraor- dinary O2 demands. Deep-diving mammals stockpile O2 in blood and other tissues and deplete it slowly.
''',

'''

CONCEPT 43.1
In innate immunity, recognition and response rely on traits common to groups of pathogens (pp. 951–956)
In both invertebrates and vertebrates, innate
immunity is mediated by physical and chemi-
cal barriers as well as cell-based defenses. Activation of innate immune responses relies on recognition proteins specific for broad classes of pathogens. Pathogens that penetrate barrier defenses are ingested by phagocytic cells, which in vertebrates include macrophages and dendritic cells. Additional cellular defenses include natural killer cells, which can induce the death of virus-infected cells. Complement system proteins, interferons, and other antimicrobial peptides also act against pathogens. In the inflammatory response, histamine and other chemicals that are released at the injury site promote changes in blood vessels that enhance immune cell access.
Pathogens sometimes evade innate immune defenses. For example, some bacteria have an outer capsule that prevents recognition, while others are resistant to breakdown within lysosomes.

''',

'''
CONCEPT 43.2
In adaptive immunity, receptors provide
pathogen-specific recognition (pp. 956–961)
■ Adaptive immunity relies on two types of lymphocytes that arise from stem cells in the bone marrow: B cells and T cells. Lymphocytes have cell-surface antigen receptors for foreign molecules (antigens). All receptor proteins on a single B or T cell are the same, but there are millions of B and T cells in the body that differ in the foreign molecules that their receptors recognize. Upon infection, B and T cells specific for the pathogen are activated. Some T cells help other lymphocytes; others kill infected host cells. B cells called plasma cells produce soluble proteins called antibodies, which bind to foreign molecules and cells. Activated B and T cells called memory cells defend against future infections by the same pathogen. ■Recognition of foreign molecules by B cells and T cells involves the binding of variable regions of receptors to an epitope, a small region of an antigen. B cells and antibodies recognize epitopes on the surface of antigens circulating in the blood or lymph. T cells recognize epitopes in small antigen fragments (peptides) that are presented on the surface of host cells by proteins called major histocompatibility complex (MHC) molecules This interaction activates a T cell, enabling it to participate in adaptive immunity.
The four major characteristics of B and T cell development are the generation of cell diversity, self-tolerance, proliferation, and immunological memory. Proliferation and memory are both based on clonal selection

''',

'''

CONCEPT 43.3
Adaptive immunity defends against infection of body fluids and body cells (pp. 961–968)
Helper T cells interact with antigen fragments displayed by class II MHC molecules on the surface of antigen-presenting cells: dendritic cells, macrophages, and B cells. Activated helper T cells secrete cytokines that stimulate other lymphocytes. In
the cell-mediated immune response, activated cytotoxic
T cells trigger destruction of infected cells. In the humoral immune response, antibodies help eliminate antigens by promoting phagocytosis and complement-mediated lysis. Active immunity develops in response to infection or to immunization. The transfer of antibodies in passive immunity provides immediate, short-term protection.
Tissues or cells transferred from one person to another are subject to immune rejection. In tissue grafts and organ transplants, MHC molecules stimulate rejection. Lymphocytes in bone marrow transplants may cause a graft-versus-host reaction.

''',

'''
CONCEPT 43.4
Disruptions in immune system function
can elicit or exacerbate disease
(pp. 968–972)
In allergies, such as hay fever, the interaction of antibodies and allergens triggers immune cells to release histamine and other mediators that cause vascular changes and allergic symptoms. Loss of self-tolerance can lead to autoimmune diseases, such as multiple sclerosis. Inborn immunodeficiencies
result from defects that interfere with innate, humoral, or cell- mediated defenses. AIDS is an acquired immunodeficiency caused by HIV.
Antigenic variation, latency, and direct assault on the immune system allow some pathogens to thwart immune responses. HIV infection destroys helper T cells, leaving the patient prone to disease. Immune defense against cancer appears to primarily involve action against viruses that can cause cancer and cancer cells that harbor viruses.
''',

'''
CONCEPT 44.1
osmoregulation balances the uptake
and loss of water and solutes
(pp. 976–980)
Cells balance water gain and loss through osmoregulation,
a process based on the controlled movement of solutes between internal fluids and the external environment and on the move- ment of water, which follows by osmosis.
Osmoconformers are isoosmotic with their marine envi- ronment and do not regulate their osmolarity. In contrast, osmoregulators control water uptake and loss in a hypoos- motic or hyperosmotic environment, respectively. Water- conserving excretory organs help terrestrial animals avoid desiccation, which can be life-threatening. Animals that live in temporary waters may enter a dormant state called anhydrobiosis when their habitats dry up.
Transport epithelia contain specialized epithelial cells that control the solute movements required for waste disposal and osmoregulation.

''',

'''

CONCEPT 44.2
An animal’s nitrogenous wastes reflect
its phylogeny and habitat (pp. 980–981)
Protein and nucleic acid metabolism generates ammonia. Most aquatic animals excrete ammonia. Mammals and most adult amphibians convert ammonia to the less toxic urea, which is excreted with a minimal loss of water. Insects and many reptiles, including birds, convert ammonia to uric acid, a mostly insol- uble waste excreted in a paste-like urine.
The kind of nitrogenous waste excreted depends on an animal’s habitat, whereas the amount excreted is coupled to the animal’s energy budget and dietary protein intake.

''',

'''

CONCEPT 44.3
Diverse excretory systems are variations
on a tubular theme (pp. 982–985)
Most excretory systems carry out filtration, reabsorption, secretion, and excretion. Invertebrate excretory systems include the protonephridia of flatworms, the metane- phridia of earthworms, and the Malpighian tubules of insects. Kidneys function in both excretion and osmoregulation in vertebrates.
Excretory tubules (consisting of nephrons and collecting ducts) and blood vessels pack the mammalian kidney. Blood pressure forces fluid from blood in the glomerulus into
the lumen of Bowman’s capsule. Following reabsorption and secretion, filtrate flows into a collecting duct.
The ureter conveys urine from the renal pelvis to the urinary bladder.

''',

'''

CONCEPT 44.4
the nephron is organized for stepwise processing of blood filtrate (pp. 985–991)
Within the nephron, selective secretion and reabsorption in the proximal tubule alter filtrate volume and composition. The descending limb of the loop of Henle is permeable to water but not salt; water moves by osmosis into the interstitial fluid. The ascending limb is permeable to salt but not water; salt leaves by diffusion and by active transport. The distal tubule and collecting duct regulate K+ and NaCl levels in body fluids.
In mammals, a countercurrent multiplier system involving the loop of Henle maintains the gradient of salt concentration in the kidney interior. Urea exiting the collecting duct contributes to the osmotic gradient of the kidney.
Natural selection has shaped the form and function of neph- rons in various vertebrates to the osmoregulatory challenges
of the animals’ habitats. For example, desert mammals,
which excrete the most hyperosmotic urine, have loops of Henle that extend deep into the renal medulla, whereas mammals in moist habitats have shorter loops and excrete more dilute urine.

''',

'''

CONCEPT 44.5
Hormonal circuits link kidney function, water
balance, and blood pressure (pp. 992–994)
The posterior pituitary gland releases antidiuretic hormone (ADH) when blood osmolarity rises above a set point, such as when water intake is inadequate. ADH increases the permeability to water of the collecting ducts by increasing the number of epithelial aquaporin channels.
When blood pressure or blood volume in the afferent arteriole drops, the juxtaglomerular apparatus releases renin. Angiotensin II formed in response to renin constricts arterioles and triggers release of the hormone aldosterone, raising blood pressure and reducing the release of renin. This renin-angiotensin- aldosterone system has functions that overlap with those of ADH and are opposed by atrial natriuretic peptide.

''',

'''

CONCEPT 45.1
Hormones and other signaling molecules bind to target receptors, triggering specific response pathways (pp. 998–1002)
The forms of signaling between animal cells differ in the type
of secreting cell and the route taken by the signal to its target. Endocrine signals, or hormones, are secreted into the extracellular fluid by endocrine cells or ductless glands and reach target cells via circulatory fluids. There the binding of a hormone to a receptor specific for that particular hormone trig- gers a cellular response. Paracrine signals act on neighboring cells, whereas autocrine signals act on the secreting cell itself. Neurotransmitters also act locally, but neurohormones can act throughout the body. Pheromones are released into the environment for communication between animals of the same species.
Local regulators, which carry out paracrine and autocrine signaling, include cytokines and growth factors (polypeptides), prostaglandins (modified fatty acids), and nitric oxide (a gas). Polypeptides, steroids, and amines comprise the major classes of animal hormones. Depending on whether they are water- soluble or lipid-soluble, hormones activate different response pathways. The endocrine cells that secrete hormones are often located in glands dedicated in part or in whole to endocrine signaling.

''',

'''

CONCEPT 45.2
Feedback regulation and coordination with the nervous system are common in hormone pathways (pp. 1003–1009)
In a simple endocrine pathway, endocrine cells respond directly to a stimulus. By contrast, in a simple neuroendocrine pathway a sensory neuron receives the stimulus.
Hormone pathways may be regulated by negative feedback, which dampens the stimulus, or positive feedback, which amplifies the stimulus and drives the response to completion.
In insects, molting and development are controlled by three hor- mones: PTTH; ecdysteroid, whose release is triggered by PTTH; and juvenile hormone. Coordination of signals from the nervous and endocrine systems and modulation of one hormone activ- ity by another bring about the sequence of developmental stages that lead to an adult form.
In vertebrates, neurosecretory cells in the hypothalamus pro- duce two hormones that are secreted by the posterior pituitary and that act directly on nonendocrine tissues: oxytocin, which induces uterine contractions and release of milk from mammary glands, and antidiuretic hormone (ADH), which enhances water reabsorption in the kidneys.
Other hypothalamic cells produce hormones that are transported to the anterior pituitary, where they stimulate or inhibit the release of particular hormones.
Often, anterior pituitary hormones act in a cascade. For example, the secretion of thyroid-stimulating hormone (TSH) is regulated
by thyrotropin-releasing hormone (TRH). TSH in turn induces the thyroid gland to secrete thyroid hormone, a combination of the iodine-containing hormones T3 and T4. Thyroid hormone stim- ulates metabolism and influences development and maturation.
Most anterior pituitary hormones are tropic hormones, acting on endocrine tissues or glands to regulate hormone secretion. Tropic hormones of the anterior pituitary include TSH, follicle-stimulating hormone (FSH), luteinizing hormone (LH), and adrenocorti- cotropic hormone (ACTH). Growth hormone (GH) has both tropic and nontropic effects. It promotes growth directly, affects metabolism, and stimulates the production of growth factors by other tissues.
''',

'''

CONCEPT 45.3
endocrine glands respond to diverse stimuli in regulating homeostasis, development, and behavior (pp. 1009–1014)
Parathyroid hormone (PTH), secreted by the parathyroid glands, causes bone to release Ca2+ into the blood and stimu- lates reabsorption of Ca2+ in the kidneys. PTH also stimulates the kidneys to activate vitamin D, which promotes intestinal uptake of Ca2+ from food. Calcitonin, secreted by the thyroid, has the opposite effects in bones and kidneys as PTH. Calcitonin is impor- tant for calcium homeostasis in adults of some vertebrates, but not humans.
In response to stress, neurosecretory cells in the adrenal medulla release epinephrine and norepinephrine, which mediate various fight-or-flight responses. The adrenal cortex releases glucocorticoids, such as cortisol, which influence glucose metabolism and the immune system. It also releases mineralocorticoids, primarily aldosterone, which help regulate salt and water balance.
Sex hormones regulate growth, development, reproduction, and sexual behavior. Although the adrenal cortex produces small amounts of these hormones, the gonads (testes and ovaries) serve as the major source. All three types—androgens, estrogens, and progesterone—are produced in males and females, but in different proportions.
The pineal gland, located within the brain, secretes melatonin, which functions in biological rhythms related to reproduction and sleep. Release of melatonin is controlled by the SCN,
the region of the brain that functions as a biological clock. Hormones have acquired distinct roles in different species over the course of evolution. Prolactin stimulates milk produc-
tion in mammals but has diverse effects in other vertebrates. Melanocyte-stimulating hormone (MSH) influences
fat metabolism in mammals and skin pigmentation in other vertebrates.

''',

'''

CONCEPT 46.1
Both asexual and sexual reproduction occur in the animal kingdom
(pp. 1018–1020)
Sexual reproduction requires the fusion of male
and female gametes, forming a diploid zygote.
Asexual reproduction is the production of offspring without gamete fusion. Mechanisms of asexual reproduction include bud- ding, fission, and fragmentation with regeneration. Variations on the mode of reproduction are achieved through parthenogenesis, hermaphroditism, and sex reversal. Hormones and environ- mental cues control reproductive cycles.

''',

'''

CONCEPT 46.2
Fertilization depends on mechanisms that bring together sperm and eggs of the same species (pp. 1020–1023)
Fertilization occurs externally, when sperm and eggs are both released outside the body, or internally, when sperm deposited
by the male fertilize an egg in the female reproductive system. In either case, fertilization requires coordinated timing, which may be mediated by environmental cues, pheromones, or courtship behavior. Internal fertilization is often associated with relatively fewer offspring and greater protection of offspring by the parents. Systems for gamete production and delivery range from undiffer- entiated cells in the body cavity to complex systems that include gonads, which produce gametes, and accessory tubes and glands that protect or transport gametes and embryos. Although sexual reproduction involves a partnership, it also provides an opportu- nity for competition between individuals and between gametes.

''',

'''

CONCEPT 46.3
Reproductive organs produce and transport
gametes (pp. 1023–1027)
In human males, sperm are produced in testes, which are sus- pended outside the body in the scrotum. Ducts connect the testes to internal accessory glands and to the penis. The repro- ductive system of the human female consists principally of the labia and the glans of the clitoris externally and the vagina, uterus, oviducts, and ovaries internally. Eggs are produced in the ovaries and upon fertilization develop in the uterus. Gametogenesis, or gamete production, consists of the pro- cesses of spermatogenesis in males and oogenesis in females. Human spermatogenesis is continuous and produces four sperm per meiosis. Human oogenesis is discontinuous and cyclic, generating one egg per meiosis.

''',

'''

CONCEPT 46.4
the interplay of tropic and sex hormones regulates reproduction in mammals
(pp. 1028–1032)
In mammals, GnRH from the hypothalamus regulates the release of two hormones, FSH and LH, from the anterior pituitary. In males, FSH and LH control the secretion of androgens (chiefly testosterone) and sperm production. In females, cyclic secretion of FSH and LH orchestrates the ovarian and uterine cycles via estrogens (primarily estradiol) and progesterone. The devel- oping follicle and the corpus luteum also secrete hormones, which help coordinate the uterine and ovarian cycles through positive and negative feedback.
In estrous cycles, the lining of the endometrium is reab- sorbed, and sexual receptivity is limited to a heat period. Reproductive structures with a shared origin in development underlie many features of human sexual arousal and orgasm common to males and females.

''',

'''

CONCEPT 46.5
in placental mammals, an embryo develops fully within the mother’s uterus (pp. 1032–1038)
After fertilization and the completion of meiosis in the oviduct, the zygote undergoes a series of cell divisions and develops into a blastocyst before implantation in the endometrium. All major organs start developing by 8 weeks. A pregnant woman’s accep- tance of her “foreign” offspring likely reflects partial suppression of the maternal immune response.
Contraception may prevent release of mature gametes from the gonads, fertilization, or embryo implantation. Abortion is the termination of a pregnancy in progress.
Reproductive technologies can help detect problems before birth and can assist infertile couples. Infertility may be treated through hormone therapy or in vitro fertilization.

''',

'''
CONCEPT 47.1
Fertilization and cleavage initiate embryonic development (pp. 1042-1047) ■Fertilization forms a diploid zygote and initiates embryonic development. The acrosomal reaction releases hydrolytic enzymes from the sperm head that digest material surrounding the egg.
Sperm-egg fusion and depolarization of egg membrane (fast block to polyspermy)
Cortical granule release
(cortical reaction)
Formation of fertilization envelope (slow block to polyspermy)
In mammalian fertilization, the cortical reaction modifies the
zona pellucida as a slow block to polyspermy.
Fertilization is followed by cleavage, a period of rapid cell division without growth, producing a large number of cells called blastomeres. The amount and distribution of yolk strongly influence the pattern of cleavage. In many species, the completion of the cleavage stage gener- ates a blastula contain-
ing a fluid-filled cavity, the blastocoel.
''',

'''
CONCEPT 47.2
2-cell
stage
forming
Animal pole
8-cell stage
Vegetal pole
-Blastocoel
Blastula
Morphogenesis in animals involves specific changes in cell shape, position, and survival (pp. 1047-1055)
■ Gastrulation converts the blastula to a gastrula, which has a primitive digestive cavity and three germ layers: ectoderm (blue), which forms the outer layer of the embryo, mesoderm (red), which forms the middle layer, and endoderm (yellow), which gives rise to the innermost tissues.
■ Gastrulation and organogenesis in mammals resemble the pro- cesses in birds and other reptiles. After fertilization and early cleavage in the oviduct, the blastocyst implants in the uterus. The trophoblast initiates formation of the fetal portion of the placenta, and the embryo proper develops from a cell layer, the epiblast, within the blastocyst.
The embryos of birds, other reptiles, and mammals develop within a fluid-filled sac that is contained within a shell or the uterus. In these organisms, the three germ layers produce four extraembryonic membranes: the amnion, chorion, yolk sac, and allantois.
The organs of the animal body develop from specific portions of the three embryonic germ layers. Early events in organogenesis in vertebrates include neurulation: formation of the notochord by cells of the dorsal mesoderm and development of the neural tube from infolding of the ectodermal neural plate.
Neural tube
Notochord
Coelom
Neural tube
Notochord
Coelom
■ Cytoskeletal rearrangements cause changes in the shape of cells that underlie cell movements in gastrulation and organogen- esis, including invaginations and convergent extension. The cytoskeleton is also involved in cell migration, which relies on cell adhesion molecules and the extracellular matrix to help cells reach specific destinations. Migratory cells arise both from the neural crest and from somites.
Some processes in animal development require apoptosis, programmed cell death.
''',

'''
CONCEPT 47.3
Cytoplasmic determinants and inductive signals regulate cell fate (pp. 1055-1062)
• Experimentally derived fate maps of embryos show that specific regions of the zygote or blastula develop into specific parts of older embryos. The complete cell lineage has been worked out for C. elegans, revealing that programmed cell death contributes to animal development. In all species, the developmental potential of cells becomes progressively more limited as embryonic devel- opment proceeds.
⚫ Cells in a developing embryo receive and respond to positional information that varies with location. This information is often in the form of signaling molecules secreted by cells in specific regions of the embryo, such as the dorsal lip of the blas- topore in the amphibian gastrula and the apical ectodermal ridge and zone of polarizing activity of the vertebrate limb bud.

''',

'''
CONCEPT 48.1
Neuron structure and organization
reflect function in information
transfer (pp. 1066-1068)
■ Most neurons have branched dendrites that
receive signals from other neurons and an axon
that transmits signals to other cells at synapses. Neurons rely
on glia for functions that include nourishment, insulation, and regulation.
Dendrites
Cell body
Axon hillock
Axon
potential is restored by the inactivation of sodium channels and
by the opening of many voltage-gated potassium channels, which increases K* outflow. A refractory period follows, correspond-
ing to the interval when the sodium channels are inactivated.
Action potential
Membrane potential (mV)
+50-
-Falling phase
0-
Rising phase
Threshold (-55)
-50-
Resting potential
-70
-100
-Undershoot
Presynaptic cell
Postsynaptic cell
Signal direction
Synapse
■ A central nervous system (CNS) and a peripheral nervous system (PNS) process information in three stages: sensory input, integration, and motor output to effector cells.
''',

'''
CONCEPT 48.2
lon pumps and ion channels establish the resting potential of a neuron (pp. 1068–1070)
■ Ionic gradients generate a voltage difference, or membrane potential, across the plasma membrane of cells. The concentra- tion of Na+ is higher outside than inside; the reverse is true for K+. In resting neurons, the plasma membrane has many open potas- sium channels but few open sodium channels. Diffusion of ions, principally K+, through channels generates a resting potential, with the inside more negative than the outside.
''',
'''
CONCEPT 48.3
Action potentials are the signals conducted by axons (pp. 1070-1075)
■Neurons have gated ion channels that open or close in response to stimuli, leading to changes in the membrane poten- tial. An increase in the magnitude of the membrane potential is a hyperpolarization; a decrease is a depolarization. Changes in membrane potential that vary continuously with the strength of a stimulus are known as graded potentials.
■ An action potential is a brief, all-or-none depolarization of a neuron's plasma membrane. When a graded depolarization brings the membrane potential to threshold, many voltage-gated ion channels open, triggering an inflow of Na* that rapidly brings the membrane potential to a positive value. A negative membrane
■ A nerve impulse travels from the axon hillock to the synaptic terminals by propagating a series of action potentials along the axon. The speed of conduction increases with the diameter of the axon and, in many vertebrate axons, with myelination. Action potentials in axons insulated by myelination appear to jump from one node of Ranvier to the next, a process called saltatory conduction.
''',
'''
CONCEPT 48.4
Neurons communicate with other cells at synapses (pp. 1075-1080)
■ In an electrical synapse, electrical current flows directly from one cell to another. In a chemical synapse, depolarization causes synaptic vesicles to fuse with the terminal membrane and release neurotransmitter into the synaptic cleft.
■ At many synapses, the neurotransmitter binds to ligand-gated ion channels in the postsynaptic membrane, producing an excitatory or inhibitory postsynaptic potential (EPSP or IPSP). The neurotransmitter then diffuses out of the cleft, is taken up by surrounding cells, or is degraded by enzymes. A single neuron has many synapses on its dendrites and cell body. Temporal and spatial summation of EPSPS and IPSPs at the axon hillock determine whether a neuron generates an action potential.
■ Different receptors for the same neurotransmitter produce different effects. Some neurotransmitter receptors activate signal transduc- tion pathways, which can produce long-lasting changes in post- synaptic cells. Major neurotransmitters include acetylcholine; the amino acids GABA, glutamate, and glycine; biogenic amines; neuropeptides; and gases such as NO.

''',

'''
CONCEPT 49.1
Nervous systems consist of circuits of neurons and supporting cells (pp. 1084-1088)
■ Invertebrate nervous systems range in complexity from simple nerve nets to highly centralized nervous systems having complicated brains and ventral nerve cords.
Brain-
Spinal- cord (dorsal
-Sensory ganglia
nerve
cord)
Nerve net
''',

'''
CONCEPT 49.2
The vertebrate brain is regionally specialized (pp. 1089-1094)
Cerebrum
Forebrain
Thalamus
Hypothalamus
Pituitary gland
Midbrain
Pons
Hindbrain
Medulla
oblongata
Cerebellum'
Cerebral cortex
Spinal cord
Hydra (cnidarian)
Salamander (vertebrate)
■ In vertebrates, the central nervous system (CNS), consisting of the brain and the spinal cord, integrates information, while the nerves of the peripheral nervous system (PNS) transmit sensory and motor signals between the CNS and the rest of the body. The simplest circuits control reflex responses, in which sensory input is linked to motor output without involvement of the brain.
VENTRICLE Ependy- mal
cell
Cilia
Capillary
PNS
CNS
Astrocyte
-Oligodendrocyte
Neuron
Microglial cell
Schwann cells
■ Afferent neurons carry sensory signals to the CNS. Efferent neu- rons function in either the motor system, which carries signals to skeletal muscles, or the autonomic nervous system, which regulates smooth and cardiac muscles. The sympathetic and parasympathetic divisions of the autonomic nervous system have antagonistic effects on a diverse set of target organs, while the enteric nervous system controls the activity of many digestive organs.
■ Vertebrate neurons are supported by glia, including astrocytes, oligodendrocytes, and Schwann cells. Some glia serve as stem cells that can differentiate into mature neurons.
The cerebrum has two hemispheres, each of which consists of cortical gray matter overlying white matter and basal nuclei. The basal nuclei are important in planning and learning move- ments. The pons and medulla oblongata are relay stations for information traveling between the PNS and the cerebrum. The reticular formation, a network of neurons within the brainstem, regulates sleep and arousal. The cerebellum helps coordinate motor, perceptual, and cognitive functions. The thalamus is the main center through which sensory information passes to the cerebrum. The hypothalamus regulates homeostasis and basic survival behaviors. Within the hypothalamus, a group of neurons called the suprachiasmatic nucleus (SCN) acts as the pacemaker for circadian rhythms. The amygdala plays a key role in recognizing and recalling a number of emotions.
''',

'''
CONCEPT 49.3
The cerebral cortex controls voluntary movement and cognitive functions (pp. 1094-1097)
Each side of the cerebral cortex has four lobes-frontal, tem- poral, occipital, and parietal-that contain primary sensory areas and association areas. Association areas integrate information from different sensory areas. Broca's area and Wernicke's area are essential for generating and understanding language. These func- tions are concentrated in the left cerebral hemisphere, as are math and logic operations. The right hemisphere appears to be stronger at pattern recognition and nonverbal thinking. In the somatosensory cortex and the motor cortex, neurons are distributed according to the part of the body that generates sensory input or receives motor commands.
■ Primates and cetaceans, which are capable of higher cognition, have an extensively convoluted cerebral cortex. In birds, a brain region called the pallium contains clustered nuclei that carry out functions similar to those performed by the cerebral cortex of mammals. Some birds can solve problems and understand abstractions in a manner indicative of higher cognition.

''',

'''

CONCEPT 49.4
Changes in synaptic connections underlie
memory and learning (pp. 1097–1099)
During development, more neurons and synapses form than will exist in the adult. The programmed death of neurons and elimina- tion of synapses in embryos establish the basic structure of the nervous system. In the adult, reshaping of the nervous system can involve the loss or addition of synapses or the strengthening or weakening of signaling at synapses. This capacity for remodeling is termed neuronal plasticity. Short-term memory relies on temporary links in the hippocampus. In long-term memory, these temporary links are replaced by connections within the cerebral cortex.

''',

'''

CONCEPT 49.5
Many nervous system disorders can now be
explained in molecular terms (pp. 1100–1102)
Schizophrenia, which is characterized by hallucinations, delusions, and other symptoms, affects neuronal pathways that use dopamine as a neurotransmitter. Drugs that increase the activity of biogenic amines in the brain can be used to treat bipolar disorder and major depressive disorder. The compulsive drug use that characterizes addiction reflects altered activity of the brain’s reward system, which normally provides motivation for actions that enhance survival or reproduction. Alzheimer’s disease and Parkinson’s disease are neuro- degenerative and typically age related. Alzheimer’s disease is a dementia in which neurofibrillary tangles and amyloid plaques form in the brain. Parkinson’s disease is a motor disorder caused by the death of dopamine-secreting neurons and associated with the presence of protein aggregates.

''',

'''

COnCept 50.1
sensory receptors transduce stimulus
energy and transmit signals to the central nervous system (pp. 1106–1110)
The detection of a stimulus precedes sensory
transduction, the change in the membrane
potential of a sensory receptor in response to a stimulus. The resulting receptor potential controls transmission of action potentials to the CNS, where sensory information is integrated
to generate perceptions. The frequency of action potentials in an axon and the number of axons activated determine stimulus strength. The identity of the axon carrying the signal encodes the nature or quality of the stimulus.
Mechanoreceptors respond to stimuli such as pressure, touch, stretch, motion, and sound. Chemoreceptors detect either total solute concentrations or specific molecules. Electromagnetic receptors detect different forms of electromagnetic radiation. Thermoreceptors signal surface and core temperatures of the body. Pain is detected by a group of nociceptors that respond to excess heat, pressure, or specific classes of chemicals.

''',

'''

COnCept 50.2
In hearing and equilibrium, mechanoreceptors detect moving fluid or settling particles
(pp. 1110–1114)
Most invertebrates sense their orientation with respect to gravity by means of statocysts. Specialized hair cells form the basis for hearing and balance in mammals and for detection of water movement in fishes and aquatic amphibians. In mammals, the tympanic membrane (eardrum) transmits sound waves to bones of the middle ear, which transmit the waves through the oval window to the fluid in the coiled cochlea of the inner ear. Pressure waves in the fluid vibrate the basilar membrane, depolarizing hair cells and triggering action potentials that travel via the auditory nerve to the brain. Receptors in the inner ear function in balance and equilibrium.

''',

'''

COnCept 50.3
the diverse visual receptors of animals depend on light-absorbing pigments (pp. 1115–1121)
Invertebrates have varied light detectors, including simple light- sensitive eyespots, image-forming compound eyes, and single- lens eyes. In the vertebrate eye, a single lens is used to focus light on photoreceptors in the retina. Both rods and cones con- tain a pigment, retinal, bonded to a protein (opsin). Absorption of light by retinal triggers a signal transduction pathway that hyperpolarizes the photoreceptors, causing them to release less neurotransmitter. Synapses transmit information from photore- ceptors to cells that integrate information and convey it to the brain along axons that form the optic nerve.

''',

'''

COnCept 50.4
the senses of taste and smell rely on similar
sets of sensory receptors (pp. 1121–1123)
Taste (gustation) and smell (olfaction) depend on stimulation of chemoreceptors by small dissolved molecules. In humans, sen- sory cells in taste buds express a receptor type specific for one
of the five taste perceptions: sweet, sour, salty, bitter, and umami (elicited by glutamate). Olfactory receptor cells line the upper part of the nasal cavity. More than 1,000 genes code for membrane pro- teins that bind to specific classes of odorants, and each receptor cell appears to express only one of those genes.

''',

'''

COnCept 50.5
the physical interaction of protein filaments is required for muscle function (pp. 1123–1130)
The muscle cells (fibers) of vertebrate skeletal muscle contain myofibrils composed of thin filaments of (mostly) actin and thick filaments of myosin. These filaments are organized into repeating units called sarcomeres. Myosin heads, energized
by the hydrolysis of ATP, bind to the thin filaments, form cross- bridges, and then release upon binding ATP anew. As this cycle repeats, the thick and thin filaments slide past each other, shortening the sarcomere and contracting the muscle fiber.
Motor neurons release acetylcholine, triggering action poten- tials in muscle fibers that stimulate the release of Ca2+ from the sarcoplasmic reticulum. When the Ca2+ binds the troponin complex, tropomyosin moves, exposing the myosin-binding sites on actin and thus initiating cross-bridge formation. A motor unit consists of a motor neuron and the muscle fibers it controls. A twitch results from one action potential. Skeletal muscle fibers are slow-twitch or fast-twitch and oxidative or glycolytic. Cardiac muscle, found in the heart, consists of striated cells electrically connected by intercalated disks. Nervous system input controls the rate at which the heart contracts, but is not strictly required for cardiac muscle contraction. In smooth muscles, contractions are initiated by the muscles or by stimulation from neurons in the autonomic nervous system.
''',

'''

COnCept 50.6
skeletal systems transform muscle contraction
into locomotion (pp. 1130–1134)
Skeletal muscles, often in antagonistic pairs, contract and pull against the skeleton. Skeletons may be hydrostatic and main- tained by fluid pressure, as in worms; hardened into exoskeletons, as in insects; or in the form of endoskeletons, as in vertebrates. Each form of locomotion—swimming, movement on land,
or flying—presents a particular challenge. For example, swimmers need to overcome friction, but face less of a challenge from gravity than do animals that move on land or fly.

''',

'''

CONCEPT 51.1
Discrete sensory inputs can stimulate both simple and complex behaviors (pp. 1138–1141)
Behavior is the sum of an animal’s responses to
external and internal stimuli. In behavior studies,
proximate, or “how,” questions focus on the stimuli that trigger a behavior and on genetic, physiological, and anatomical mecha- nisms underlying a behavioral act. Ultimate, or “why,” questions address evolutionary significance.
A fixed action pattern is a largely invariant behavior trig- gered by a simple cue known as a sign stimulus. Migratory movements involve navigation, which can be based on orien- tation relative to the sun, the stars, or Earth’s magnetic field. Animal behavior is often synchronized to the circadian cycle of light and dark in the environment or to cues that cycle over the seasons.
The transmission and reception of signals constitute animal communication. Animals use visual, auditory, chemical, and tactile signals. Chemical substances called pheromones trans- mit species-specific information between members of a species in behaviors ranging from foraging to courtship.

''',

'''

CONCEPT 51.2
Learning establishes specific links between
experience and behavior (pp. 1141–1146) Cross-fostering studies can be used to measure the influence
of social environment and experience on behavior.
Learning, the modification of behavior as a result of experience, can take many forms: imprinting, cognition, spatial learning, associative learning, social learning

''',

'''
CONCEPT 51.3
selection for individual survival and reproductive success can explain diverse behaviors (pp. 1146–1152)
Controlled experiments in the laboratory can give rise to inter- pretable evolutionary changes in behavior.
An optimal foraging model is based on the idea that natural selection should favor foraging behavior that minimizes the costs of foraging and maximizes the benefits.
Sexual dimorphism correlates with the types of mating relation- ship, which include monogamous and polygamous mating systems. Variations in mating system and mode of fertilization affect certainty of paternity, which in turn has a significant influence on mating behavior and parental care.
Game theory provides a way of thinking about evolution in situations where the fitness of a particular behavioral phe- notype is influenced by other behavioral phenotypes in the population.
''',

'''
CONCEPT 51.4
Genetic analyses and the concept of inclusive fitness provide a basis for studying the evolution of behavior (pp. 1152–1158)
Genetic studies in insects have revealed the existence of master regulatory genes that control complex behaviors. Within the underlying hierarchy, multiple genes influence specific behav- iors, such as a courtship song. Research on voles illustrates how variation in a single gene can determine differences in complex behaviors.
Behavioral variation within a species that corresponds to envi- ronmental variation may be evidence of past evolution. Altruism can be explained by the concept of inclusive fitness, the effect an individual has on proliferating its genes
by producing its own offspring and by providing aid that enables close relatives to reproduce. The coefficient of relatedness and Hamilton’s rule provide a way of measuring the strength of the selective forces favoring altruism against the potential cost of the “selfless” behavior. Kin selection
favors altruistic behavior by enhancing the reproductive success of relatives.
''',

'''
CONCEPT 52.1
earth’s climate varies by latitude and season and is changing rapidly (pp. 1165–1168)
Global climate patterns are largely determined
by the input of solar energy and Earth’s revolution
around the sun.
The changing angle of the sun over the year, bodies of water, and mountains exert seasonal, regional, and local effects on climate. Fine-scale differences in certain abiotic (nonliving) factors, such as sunlight and temperature, determine microclimate. Increasing greenhouse gas concentrations in the air are warming Earth and altering the distributions of many species. Some species will not be able to shift their ranges quickly enough to reach suit- able habitat in the future.
''',

'''

CONCEPT 52.2
the distribution of terrestrial biomes is controlled
by climate and disturbance (pp. 1168–1174)
Climographs show that temperature and precipitation are correlated with biomes. Because other factors also play roles
in biome location, biomes overlap.
Terrestrial biomes are often named for major physical or climatic factors and for their predominant vegetation. Vertical layering is an important feature of terrestrial biomes.
Disturbance, both natural and human-induced, influences the type of vegetation found in biomes. Humans have altered much of Earth’s surface, replacing the natural terrestrial com- munities described and depicted in Figure 52.12 with urban and agricultural ones.
The pattern of climatic variation is as important as the average climate in determining where biomes occur.

''',

'''
CONCEPT 52.3
Aquatic biomes are diverse and dynamic systems
that cover most of earth (pp. 1175–1176)
Aquatic biomes are characterized primarily by their physical envi- ronment rather than by climate and are often layered with regard to light penetration, temperature, and community structure. Marine biomes have a higher salt concentration than freshwater biomes.
In the ocean and in most lakes, an abrupt temperature change called a thermocline separates a more uniformly warm upper layer from more uniformly cold deeper waters.
Many temperate lakes undergo a turnover, or mixing of water in spring and fall, that sends deep, nutrient-rich water to the surface and shallow, oxygen-rich water to deeper layers.
''',

'''
CONCEPT 52.4
interactions between organisms and the environment limit the distribution of species (pp. 1176–1185)
Ecologists want to know not only where species occur but also why those species occur where they do.
''',

'''
CONCEPT 52.5
ecological change and evolution affect one another over long and short periods of time (p. 1185)
Ecological interactions can cause evolutionary change, as when predators cause natural selection in a prey population. Likewise, an evolutionary change, such as an increase in the frequency of a new defensive mechanism in a prey population, can alter the outcome of ecological interactions.

''',

'''
CONCEPT 53.1
Biotic and abiotic factors affect population density, dispersion, and demographics (pp. 1189–1193)
Population density—the number of individuals per
unit area or volume—reflects the interplay of births,
deaths, immigration, and emigration. Environmental and social factors influence the dispersion of individuals.
Populations increase from births and immigration and decrease from deaths and emigration. Life tables and survivorship curves summarize specific trends in demography.
''',

'''
CONCEPT 53.2
the exponential model describes population growth in an idealized, unlimited environment (pp. 1194–1195)
If immigration and emigration are ignored, a population’s per capita growth rate equals its birth rate minus its death rate.
The exponential growth equation dN/dt = rN represents a population’s growth when resources are relatively abundant, where r is the intrinsic rate of increase and N is the number of individuals in the population.
''',

'''
CONCEPT 53.3
the logistic model describes how a population grows more slowly as it nears its carrying capacity (pp. 1195–1198)
Exponential growth cannot be sustained in any population. Amorerealisticpopulationmodellimitsgrowthbyincorporat- ing carrying capacity (K), the maximum population size the environment can support.
According to the logistic growth equation dN/dt = rN
(K - N)/K, growth levels off as population size approaches
the carrying capacity.
The logistic model fits few real populations perfectly, but it is useful for estimating possible growth.
''',

'''
CONCEPT 53.4
Life history traits are products of natural
selection (pp. 1198–1200)
Life history traits are evolutionary outcomes reflected in the development, physiology, and behavior of organisms. Big-bang, or semelparous, organisms reproduce once and die. Iteroparous organisms produce offspring repeatedly.
Life history traits such as brood size, age at maturity, and parental caregiving represent trade-offs between conflicting demands
for time, energy, and nutrients. Two hypothetical life history patterns are K-selection and r-selection.
''',

'''
CONCEPT 53.5
Density-dependent factors regulate population growth (pp. 1200–1205)
In density-dependent population regulation, death rates rise and birth rates fall with increasing density. A birth or death rate that does not vary with density is said to be density independent.
Density-dependent changes in birth and death rates curb popula- tion increase through negative feedback and can eventually sta- bilize a population near its carrying capacity. Density-dependent limiting factors include intraspecific competition for limited food or space, increased predation, disease, intrinsic physiological factors, and buildup of toxic substances.
Because changing environmental conditions periodically disrupt them, all populations exhibit some size fluctuations. Many populations undergo regular boom-and-bust cycles that are influenced by complex interactions between biotic and abiotic factors. A metapopulation is a group of populations linked by immigration and emigration.
''',

'''

CONCEPT 53.6
the human population is no longer growing exponentially but is still increasing
rapidly (pp. 1205–1209)
Since about 1650, the global human population has grown exponentially, but within the last 50 years, the rate of growth
has fallen by half. Differences in age structure show that while some nations’ populations are growing rapidly, those of oth-
ers are stable or declining in size. Infant mortality rates and life expectancy at birth vary widely in different countries. Ecological footprint is the aggregate land and water area needed to produce all the resources a person or group of people consume and to absorb all of their waste. It is one measure of how close we are to the carrying capacity of Earth, which is uncertain. With a world population of more than 7.2 billion people, we are already using many resources in an unsustainable manner.

''',

'''

CONCEPT 54.1
Community interactions are classified by whether they help, harm, or have no effect on the species involved
(pp. 1213–1219)
Interspecific interactions affect the survival
and reproduction of the species that engage in them. As shown in the table, these interactions can be grouped into three broad categories: competition, exploitation, and positive interactions.
Competition (-/-)
two or more species compete for a resource that is in short supply.
Exploitation (+/-) predation
herbivory parasitism
One species benefits by feeding upon the other species, which is harmed. exploitation includes the following:
One species, the predator, kills and eats the other, the prey.
An herbivore eats part of a plant or alga.
the parasite derives its nourishment from a second organism, its host, which is harmed.
Positive interactions
(+/+ or 0/+) Mutualism (+/+)
commensalism (+/0)
One species benefits, while the other species benefits or is not harmed. positive interactions include the following:
Both species benefit from the interaction.
One species benefits, while the other is not affected.

''',

'''
CONCEPT 54.2
Diversity and trophic structure characterize
biological communities (pp. 1220–1225)
Species diversity is affected by both the number of species
in a community—its species richness—and their relative abundance.
More diverse communities typically produce more biomass and show less year-to-year variation in growth than less diverse com- munities and are more resistant to invasion by exotic species. Trophic structure is a key factor in community dynamics. Food chains link the trophic levels from producers to top carnivores. Branching food chains and complex trophic interactions form food webs.
Dominant species are the most abundant species in a com- munity. Keystone species are usually less abundant species that exert a disproportionate influence on community structure. Ecosystem engineers influence community structure through their effects on the physical environment.
The bottom-up model proposes a unidirectional influence from lower to higher trophic levels, in which nutrients and other abiotic factors primarily determine community structure. The top-down model proposes that control of each trophic level comes from the trophic level above, with the result that predators control herbivores, which in turn control primary producers.
''',

'''
CONCEPT 54.3
Disturbance influences species diversity
and composition (pp. 1226–1229)
Increasing evidence suggests that disturbance and lack of equilibrium, rather than stability and equilibrium, are the norm for most communities. According to the intermediate disturbance hypothesis, moderate levels of disturbance can foster higher species diversity than can low or high levels of disturbance.
Ecological succession is the sequence of community and ecosystem changes after a disturbance. Primary succession occurs where no soil exists when succession begins; secondary succession begins in an area where soil remains after a disturbance.
''',

'''
CONCEPT 54.4
Biogeographic factors affect community
diversity (pp. 1229–1232)
Species richness generally declines along a latitudinal gradient from the tropics to the poles. Climate influences the diversity gradient through energy (heat and light) and water. The greater age of tropical environments also may contribute to their greater species richness.
Species richness is directly related to a community’s geographic size, a principle formalized in the species-area curve.
Species richness on islands depends on island size and distance from the mainland. The island equilibrium model maintains that species richness on an ecological island reaches an equilibrium where new immigrations are balanced by extinctions.
''',

'''
CONCEPT 54.5
pathogens alter community structure locally
and globally (pp. 1232–1233)
Recent work has highlighted the role that pathogens play
in structuring terrestrial and marine communities.
Zoonotic pathogens are transferred from other animals to humans and cause the largest class of emerging human diseases. Community ecology provides the framework for identifying key species interactions associated with such pathogens and for help- ing us track and control their spread.
''',
'''
CONCEPT 55.1
physical laws govern energy flow
and chemical cycling in ecosystems
(pp. 1237–1239)
An ecosystem consists of all the organisms in a
community and all the abiotic factors with which
they interact. Energy is conserved but released as heat during ecosystem processes. As a result, energy flows through ecosystems (rather than being recycled).
Chemical elements enter and leave an ecosystem and cycle within it, subject to the law of conservation of mass. Inputs and outputs are generally small compared to recycled amounts, but their balance determines whether the ecosystem gains or loses an element over time.
''',

'''

CONCEPT 55.2
energy and other limiting factors
control primary production in ecosystems (pp. 1239–1243)
Primary production sets the spending limit for the global energy budget. Gross primary production is the total energy assimilated by an ecosystem in a given period. Net primary production, the energy accumulated in autotroph biomass, equals gross primary production minus the energy used by the primary producers for respiration. Net ecosystem production is the total biomass accumulation of an ecosystem, defined as the difference between gross primary production and total ecosystem respiration.
In aquatic ecosystems, light and nutrients limit primary produc- tion. In terrestrial ecosystems, climatic factors such as tempera- ture and moisture affect primary production at large scales, but a soil nutrient is often the limiting factor locally.

''',

'''

CONCEPT 55.3
energy transfer between trophic levels
is typically only 10% efficient (pp. 1244–1246)
The amount of energy available to each trophic level is determined by the net primary production and the production efficiency, the efficiency with which food energy is converted to biomass at each link in the food chain.
The percentage of energy transferred from one trophic level to the next, called trophic efficiency, is typically 10%. Pyramids of energy and biomass reflect low trophic efficiency.

''',
'''
CONCEPT 55.4
Biological and geochemical processes cycle
nutrients and water in ecosystems (pp. 1246–1251)
Water moves in a global cycle driven by solar energy. The car- bon cycle primarily reflects the reciprocal processes of photo- synthesis and cellular respiration. Nitrogen enters ecosystems through atmospheric deposition and nitrogen fixation by prokaryotes.
The proportion of a nutrient in a particular form varies
among ecosystems, largely because of differences in the rate of decomposition.
Nutrient cycling is strongly regulated by vegetation. The Hubbard Brook case study showed that logging increases water runoff and can cause large losses of minerals.

''',

'''
CONCEPT 55.5
Restoration ecologists return degraded
ecosystems to a more natural state (pp. 1251–1255)
Restoration ecologists harness organisms to detoxify polluted ecosystems through the process of bioremediation.
In biological augmentation, ecologists use organisms to add essential materials to ecosystems.
''',

'''
CONCEPT 56.1
Human activities threaten earth’s
biodiversity (pp. 1259–1264)
Biodiversity can be considered at three main levels: genetic, species, ecosystem.
Our biophilia enables us to recognize the value of biodiversity for its own sake. Other species also provide humans with food, fiber, medicines, and ecosystem services.
Four major threats to biodiversity are habitat loss, introduced species, overharvesting, and global change.

''',

'''
CONCEPT 56.2
population conservation focuses on population size, genetic diversity, and critical habitat
(pp. 1264–1268)
When a population drops below a minimum viable popula- tion (MVP) size, its loss of genetic variation due to nonrandom mating and genetic drift can trap it in an extinction vortex. The declining-population approach focuses on the environmental factors that cause decline, regardless of absolute population size. It follows a step-by-step conservation strategy.
Conserving species often requires resolving conflicts between the habitat needs of endangered species and human demands.
''',

'''
CONCEPT 56.3
Landscape and regional conservation
help sustain biodiversity (pp. 1268–1272)
The structure of a landscape can strongly influence biodiversity. As habitat fragmentation increases and edges become more extensive, biodiversity tends to decrease. Movement corridors can promote dispersal and help sustain populations. Biodiversity hot spots are also hot spots of extinction and thus prime candidates for protection. Sustaining biodiversity in parks and reserves requires management to ensure that human activities in the surrounding landscape do not harm the protected habitats. The zoned reserve model recognizes that conservation efforts often involve working in landscapes that are greatly affected by human activity.
Urban ecology is the study of organisms and their environment in primarily urban settings.
''',

'''
CONCEPT 56.4
earth is changing rapidly as a result
of human actions (pp. 1272–1281)
Agriculture removes plant nutrients from ecosystems, so large supplements are usually required. The nutrients in fertilizer can pollute groundwater and surface-water aquatic ecosystems, where they can stimulate excess algal growth (eutrophication).
The release of toxic wastes and pharmaceuticals has polluted the environment with harmful substances that often persist for long periods and become increasingly concentrated in successively higher trophic levels of food webs (biological magnification). Because of the burning of fossil fuels and other human activities, the atmospheric concentration of CO2 and other greenhouse gases has been steadily increasing. These increases have caused climate change, including significant global warming and changing patterns of precipitation. Climate change has already affected many ecosystems.
The ozone layer reduces the penetration of UV radiation through the atmosphere. Human activities, notably the release of chlorine- containing pollutants, have eroded the ozone layer, but govern- ment policies are helping to solve the problem.
''',

'''
CONCEPT 56.5
sustainable development can improve human
lives while conserving biodiversity (pp. 1281–1282)
The goal of the Sustainable Biosphere Initiative is to acquire the ecological information needed for the development, manage- ment, and conservation of Earth’s resources.
Costa Rica’s success in conserving tropical biodiversity has involved a partnership among the government, other organiza- tions, and private citizens. Human living conditions in Costa Rica have improved along with ecological conservation.
By learning about biological processes and the diversity of life, we become more aware of our close connection to the environment and the value of other organisms that share it.
'''
]

math_prompt = "This is a math question. Unlike other kinds of questions, you will not be asking for terms like 'what method allows you to do this' or 'what is the name of this formula.' Everything is centered around calculations and computations."

import time

import os

from groq import Groq

os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def llama_math(category, topic):
        prompt = "The question should be difficult. The meaning of difficult is that it is intellectually challenging."
        
        prompt +=  f"""

        DON'T EVER MENTION THE TOPIC IN THE QUESTION (e.g. use the law of sines or some shit).

        The question must consist of both a toss-up and a bonus.

        It must be in this format **TOSSUP** {category} **(whether it is Short Answer or Multiple Choice)**, then **BONUS** {category} **(whether it is Short Answer or Multiple Choice)**
       
        The questions should be appropriate for college students.

        Generate a Science Bowl question. The question must be on this {category} and specifically this {topic}.

        The toss-up should be easier than the bonus. The bonus should be more challenging and should take longer (remember 5 seconds for toss-up, 20-seconds for bonus). These time limits are for the competitors' processing time after the question is read! This doesn't include time to read the question.

        Science Bowl is an advanced high-school, challenging buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z).

        These questions are read out loud. Short Answer question answers shouldn't be more than one word or number if numerical, unless they are numbered identification. Ensure that in multiple-choice questions, there are 4 choices and each choice is designated with the letters W, X, Y, and Z.

        DON'T ASK OPEN-ENDED QUESTIONS! SHORT ANSWER QUESTION ANSWERS ARE MEANT TO BE A SINGLE WORD, TERM, OR NUMBER. No asking for explanations or long equations!!!

        Ensure that the answer to all questions is logical but still decently difficult and not just elementary school stuff. Even it's some randomly specific word, it should be clear from the context of the question. But make sure that these questions are challenging and made for advanced high-school level students.

        NEVER EVER REFER TO THE PASSAGE. The competitors answering these questions do not have access to the context you are given.

        Someone should be able to answer your queston simply by looking at the context provided. No added information other than the context. I don't care what it is, no adding information outside of your narrow context. If that happens, I will kill myself.

        The question should be properly formatted and should not contain any errors.

        The questions should be appropriate for advanced college students.

        ADDITIONAL IMPORTANT REMINDERS FOR CALCULATION QUESTIONS: competitors do not have access to a calculator, so they can't calculate really numbers with lots of decimal places or complex trig functions, also never ask for the value of any constants, and also don't ask for formulas as the answer; use lots in your questions though! avoid using too many symbols.
        the questions should still be challenging. instead of decimal numbers, use round numbers that still require some difficult formulas.

        """

        chat = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
        ],
        model="deepseek-r1-distill-llama-70b",
        )

        return chat.choices[0].message.content

def llama_generate_science_bowl_question(energy, temp_category, retrieved_text, difficulty, category, topic, question_style_tossup, question_example_tossup, question_instructions_tossup, question_style_bonus, question_example_bonus, question_instructions_bonus):
        prompt = ""
        energy_prompt = "This is an energy question. In energy questions, you will briefly mention research being done at a random lab - e.g. Sandia National Labs, Ames Laboratory, Argonne National Laboratory, Brookhaven National Laboratory, Fermi National Accelerator Laboratory, Frederick National Laboratory for Cancer Research, Idaho National Laboratory, Lawrence Berkeley National Laboratory, Lawrence Livermore National Laboratory. After that, you will ask a random {temp_category} question based on that research. Do this for both the toss-up question and the bonus question."
        physics_prompt = "Try to avoid excessively using symbols in your question."
        if(energy==True):
          prompt += energy_prompt
        elif(category=="Physics" or category=="Chemistry"):
            prompt += physics_prompt

        prompt += "The question should be difficult. The meaning of difficult is that it is intellectually challenging."
        
        prompt +=  f"""

        The question must consist of both a toss-up and a bonus.

        It must be in this format **TOSSUP** {category} **(whether it is Short Answer or Multiple Choice)**, then **BONUS** {category} **(whether it is Short Answer or Multiple Choice)**

        Use this question {question_example_tossup} as a reference while creating the style of the toss-up.

        To explain, the question presented is a {question_style_tossup} type of question: {question_instructions_tossup}.

        Only the tossup should follow this format!! It must be {question_style_tossup}.

        For the bonus, on the other hand, use this question {question_example_bonus} as a reference while creating the style of the bonus.

        To explain, the question presented is a {question_style_bonus} type of question: {question_instructions_bonus}.

        Only the bonus should follow this format!! It must be {question_style_bonus}.

        DON'T USE ANY OF THE PREVIOUS CONTEXT OF THE QUESTION PROVIDED FOR THE INFORMATION USED FOR YOUR QUESTION. THE CONTEXT YOU NEED WILL BE PRESENTED TO YOU SOON!
       
        The questions should be appropriate for college students.

        Using ONLY this context {retrieved_text}, generate a Science Bowl question.

        The question must be on this {category} and specifically this {topic}.

        The toss-up should be easier than the bonus. The bonus should be more challenging and should take longer (remember 5 seconds for toss-up, 20-seconds for bonus). These time limits are for the competitors' processing time after the question is read! This doesn't include time to read the question.

        In short answer questions, the answer should not be more than one word!!!!

        Science Bowl is an advanced high-school, challenging buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z).

        These questions are read out loud. Short Answer question answers shouldn't be more than one word or number if numerical, unless they are numbered identification. Ensure that in multiple-choice questions, there are 4 choices and each choice is designated with the letters W, X, Y, and Z.

        DON'T ASK OPEN-ENDED QUESTIONS! SHORT ANSWER QUESTION ANSWERS ARE MEANT TO BE A SINGLE WORD, TERM, OR NUMBER. No asking for explanations or long equations!!!

        Ensure that the answer to all questions is logical but still decently difficult and not just elementary school stuff. Even it's some randomly specific word, it should be clear from the context of the question. But make sure that these questions are challenging and made for advanced high-school level students.

        NEVER EVER REFER TO THE PASSAGE. The competitors answering these questions do not have access to the context you are given.

        Someone should be able to answer your queston simply by looking at the context provided. No added information other than the context. I don't care what it is, no adding information outside of your narrow context. If that happens, I will kill myself.

        The question should be properly formatted and should not contain any errors.

        The questions should be appropriate for advanced college students.

        ADDITIONAL IMPORTANT REMINDERS FOR CALCULATION QUESTIONS: competitors do not have access to a calculator, so they can't calculate really numbers with lots of decimal places or complex trig functions, also never ask for the value of any constants, and also don't ask for formulas as the answer; use lots in your questions though! avoid using too many symbols.
        the questions should still be challenging. instead of decimal numbers, use round numbers that still require some difficult formulas.

        """

        chat = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
        ],
        model="deepseek-r1-distill-llama-70b",
        )

        return chat.choices[0].message.content

def generate_science_bowl_question(temp_category, retrieved_text, difficulty, category, topic, question_style_tossup, question_example_tossup, question_instructions_tossup, question_style_bonus, question_example_bonus, question_instructions_bonus):
        prompt = ""
        energy_prompt = f"This is an energy question. In energy questions, you will briefly mention research being done at a random lab - e.g. Sandia National Labs, Ames Laboratory, Argonne National Laboratory, Brookhaven National Laboratory, Fermi National Accelerator Laboratory, Frederick National Laboratory for Cancer Research, Idaho National Laboratory, Lawrence Berkeley National Laboratory, Lawrence Livermore National Laboratory. After that, you will ask a random {temp_category} question based on that research. Do this for both the toss-up question and the bonus question."
        if(category=="Energy"):
            print("YES")
            prompt += energy_prompt
        elif(category=="Math"):
            prompt += math_prompt

        prompt += "The question should be difficult. The meaning of difficult is that it covers less-known, obscure terms."
        
        prompt +=  f"""

        The question must consist of both a toss-up and a bonus.

        The question should have both a tossup and bonus, and it should start with TOSSUP {category} short answer/multiple choice, and the bonus should start with BONUS {category} short answer/multiple choice.

        Use this question {question_example_tossup} as a reference while creating the style of the toss-up.

        To explain, the question presented is a {question_style_tossup} type of question: {question_instructions_tossup}.

        Only the tossup should follow this format!! It must be {question_style_tossup}.

        For the bonus, on the other hand, use this question {question_example_bonus} as a reference while creating the style of the bonus.

        To explain, the question presented is a {question_style_bonus} type of question: {question_instructions_bonus}.

        Only the bonus should follow this format!! It must be {question_style_bonus}.

        DON'T USE ANY OF THE CONTEXT OF THE QUESTION PROVIDED FOR THE INFORMATION USED FOR YOUR QUESTION. THE CONTEXT WILL FOLLOW!
       
        The questions should be appropriate for college students.

        The start of the question must be labeled with this category: {category}.
        
        This is the specific subtopic {topic}, which shouldn't be labeled.

        Using ONLY this context {retrieved_text}, generate a Science Bowl question.

        The question must be on this {category} and specifically this {topic}.

        In short answer questions, the answer should not be more than one word!!!!

        Science Bowl is an advanced high-school, challenging buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z).

        These questions are read out loud. Make sure that the questions are 50-50 multiple-choice and short answer, and ensure that no short answer questions ask to explain anything - short answers answers should be either a term or a number resulting from a calculation (one word max). Also ensure that in multiple-choice questions, there are 4 choices and each choice is designated with the letters W, X, Y, and Z.

        DON'T ASK OPEN-ENDED QUESTIONS! SHORT ANSWER QUESTION ANSWERS ARE MEANT TO BE A SINGLE WORD, TERM, OR NUMBER. No asking for explanations or long equations!!!

        Also ensure that the answer to all questions is logical but still decently difficult and not just elementary school stuff. Even it's some randomly specific word, it should be clear from the context of the question. But make sure that these questions are challenging and made for advanced high-school level students.

        Using ONLY this context {retrieved_text}, generate a Science Bowl question.

        Once again, this is the category: {category}.

        NEVER EVER REFER TO THE PASSAGE. The competitors answering these questions do not have access to the context you are given.

        I want to EMPHASIZE SOME REALLY IMPORTANT INFORMATION now, PROBABLY THE MOST FREAKING IMPORTANTLY IMPORTANT INFORMATION HERE that you have to ENSURE that the question CAN BE ANSWERED solely using the provided context. If the context talks about something, you must incorporate the words of the context into your question. No adding of other information!! Otherwise I will make sure you don't generate a single response ever again.

        This means that someone should be able to answer your queston simply by looking at the context provided. No added information other than the context. I don't care what it is, no adding information outside of your narrow context. If that happens, I will kill myself.

        The question should be properly formatted and should not contain any errors.

        The questions should be appropriate for college students.

        """

        completion = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::AzCT79vQ",
            messages=[
                {"role": "developer", "content": "You ask Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

def verify_science_bowl_question(temp_category, category, topic,question, difficulty, question_style_tossup, question_example_tossup, question_instructions_tossup, question_style_bonus, question_example_bonus, question_instructions_bonus):
    prompt = "The question should be difficult. The meaning of difficult is that it covers less-known, obscure terms."
    energy_prompt = f"This is an energy question. In energy questions, you will briefly mention research being done at a random lab - e.g. Sandia National Labs, Ames Laboratory, Argonne National Laboratory, Brookhaven National Laboratory, Fermi National Accelerator Laboratory, Frederick National Laboratory for Cancer Research, Idaho National Laboratory, Lawrence Berkeley National Laboratory, Lawrence Livermore National Laboratory. After that, you will ask a random {temp_category} question based on that research. Do this for both the toss-up question and the bonus question. The category should be explicitly stated as Energy."
    if(category=="Energy"):
        prompt += energy_prompt

    prompt += f"""

    The question must consist of both a toss-up and a bonus.

    The question should have both a tossup and bonus, and it should start with TOSSUP {category} short answer/multiple choice, and the bonus should start with BONUS {category} short answer/multiple choice.

    Use this question {question_example_tossup} as a reference while creating the style of the toss-up.

    To explain, the question presented is a {question_style_tossup} type of question: {question_instructions_tossup}.

    Only the tossup should follow this format!! It must be {question_style_tossup}.

    For the bonus, on the other hand, use this question {question_example_bonus} as a reference while creating the style of the bonus.

    To explain, the question presented is a {question_style_bonus} type of question: {question_instructions_bonus}.

    Only the bonus should follow this format!! It must be {question_style_bonus}.

    PRESERVE THE IDEAS OF THE QUESTION! ONLY CHANGE THE ANSWER OR SLIGHT PHRASING IF THERE ARE ERRORS!
    
    ONLY CHANGE THE ANSWER OR SLIGHT PHRASING IF THERE ARE ERRORS!

    ONLY CHANGE THE ANSWER OR SLIGHT PHRASING IF THERE ARE ERRORS!

    Even if you are changing the question, keep the same idea and topic, just modify the phrasing or answer!

    Ensure that ONLY this context {retrieved_text} is used!!

    The question should be of this {category} and this specific {topic}.

    Follow these criteria while verifying the validity and appropriateness of the question:
            - If it is short answer, does the answer require an explanation, an equation, or an open-ended, non-objective question? If so, change the question! No explanations or open-ended answers as answers! Everything in this competition is objective.
            - Does it require a calculator? If it does, make the numbers nicer or change the question entirely. The contestants solving these questions won't have access to a calculator.
            - Can the toss-up be solved in less than 5 seconds?
            - Can the bonus be solved in less than 20 seconds?
            - Does the question make the answer too obvious? (e.g. mentioning the answer in the question or hinting at it with a very obvious key word)
            - Does the question require any unnecessary assumptions? (e.g. having to guess the mass of an object if it's not given or guessing the molarity of a solution)
            - Participants will not have access to periodic tables or pages with constants, so does the question require knowledge of constants or specific values like atomic masses?
            - Is the question too easy? Make it more difficult!

    You should simply return either the same question or a modified version of it. Again, your goal is not to modify the question but to fix if there are any errors.

    """

    completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "developer", "content": "You modify Science Bowl questions. Science Bowl is a buzzer-based competition centered around speed and consisting of questions in five subjects: math, earth and space science, physics, chemistry, and biology. You write Science Bowl questions on a given topic. Each Science Bowl question consists of a toss-up, to be solved in under 5 seconds, and a bonus, to be done in under 20 seconds. Each toss-up and bonus must be either short answer (no answer choices) or multiple choice (4 choices given, designated with W, X, Y, and Z.."},
                {"role": "user", "content": prompt}
            ]
        )
    return completion.choices[0].message.content

def calculation_checker(question):

    prompt = f"""
    
    These are two Science Bowl questions: {question}. Your job is to ensure that the questions and corresponding answers provided are indeed correct.

    Also ensure that there's nothing stupid in the question (e.g. giving the answer away in the question, putting decimals that require a calculator, etc.).

    If the answer doesn't match what you get, change the answer or if it is multiple choice, change one of the choices to match your answer.

    Return the modified version of the questions. The questions you return should not only be correct but solvable.
    
    """

    chat = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": prompt,
        }
        ],
        model="deepseek-r1-distill-llama-70b",
        )

    return chat.choices[0].message.content

def similarity(question, user_answer):
    prompt = f"""

    This is the {question}.

    Assess the user's answer: {user_answer}.

    Give an explanation on how to solve the question.

    """
    completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="deepseek-r1-distill-llama-70b",
    )
    return completion.choices[0].message.content

# if "toss_up_answer" not in st.session_state:
#     st.session_state.toss_up_answer = None
# if "bonus_answer" not in st.session_state:
#     st.session_state.bonus_answer = None
# if "question_final" not in st.session_state:
#     st.session_state.question_final = None
# if "toss_up_attempt" not in st.session_state:
#     st.session_state.toss_up_attempt = ""
# if "bonus_attempt" not in st.session_state:
#     st.session_state.bonus_attempt = ""
# if "bonus_revealed" not in st.session_state:
#     st.session_state.bonus_revealed = False

topics = ["Earth Science", "Math", "Chemistry", "Physics", "Biology", "Energy"]

# selected_topic = st.selectbox("Select Topics", topics)

# if st.button("Generate Question"):
#     st.session_state.toss_up_attempt = ""
#     st.session_state.bonus_attempt = ""
#     st.session_state.bonus_revealed = False 

#     if selected_topic:
#         category, topic = select_topic(selected_topic)
#         index = 0
#         if category != "Energy":
#             for i in range(len(subtopics[category])):
#                 if subtopics[category][i] == topic:
#                     index = i
#                     break


#     ans = []
#     x = random.randint(0,2)
#     if category == "Chemistry":
#         ans = chem_text
#     elif category == "Biology":
#         ans = bio_text
#     elif category == "Physics":
#         ans = harder_phys_text
#     elif category == "Earth Science":
#         ans = ess_text
#     elif category == "Math":
#         ans.append(subtopics[category][index])
#         index = 0
#     elif category == "Energy":
#         if x == 0:
#             ans = harder_phys_text
#         elif x == 1:
#             ans = chem_text
#         else:
#             ans = bio_text

#     temp_category = category

#     if category=="Energy":
#         index = 0
#         if x == 0:
#             temp_category = "Physics"
#         elif x == 1:
#             temp_category = "Chemistry"
#         else:
#             temp_category = "Biology"
#         index = random.randint(0,len(subtopics[temp_category])-1)

#     question_style_tossup = ""
#     question_example_tossup = ""
#     question_instructions_tossup = ""
#     if temp_category=="Chemistry" or temp_category=="Biology" or temp_category=="Physics" or temp_category=="Earth Science":
#         x = random.randint(0,len(question_styles[temp_category])-1)
#         question_style_tossup = question_styles[temp_category][x]
#         question_example_tossup = question_styles_examples[temp_category][x]
#         question_instructions_tossup = question_style_explanations[question_style_tossup]

#     question_style_bonus = ""
#     question_example_bonus = ""
#     question_instructions_bonus = ""
#     if temp_category=="Chemistry" or temp_category=="Biology" or temp_category=="Physics" or temp_category=="Earth Science":
#         x = random.randint(0,len(question_styles[temp_category])-1)
#         question_style_bonus = question_styles[temp_category][x]
#         question_example_bonus = question_styles_examples[temp_category][x]
#         question_instructions_bonus= question_style_explanations[question_style_bonus]

#     difficulty = 3
#     retrieved_text = ""
#     retrieved_text = ans[8]
#     if(category=="Math"):
#         retrieved_text = "Make it difficult for college students but doable without a calculator! Remember, 5 seconds for toss-ups and 20 seconds for bonuses"
#     print("**Category**")
#     print(category)
#     print("**Topic**")
#     print(index)
#     print(topic)
#     topic = "Trigonometric equations"
#     print("**Retrieved Text**")
#     print(retrieved_text)
#     print("**Question Style Tossup")
#     print(question_style_tossup)
#     print("**Question Example Tossup")
#     print(question_example_tossup)
#     print("**Question Style Bonus")
#     print(question_style_bonus)
#     print("**Question Example Bonus")
#     print(question_example_bonus)
#     raw = llama_generate_science_bowl_question(temp_category, retrieved_text, difficulty, category, topic, question_style_tossup, question_example_tossup, question_instructions_tossup, question_style_bonus, question_example_bonus, question_instructions_bonus)
#     print("**TOSS UP style")
#     print(question_style_tossup)
#     print("**BONUS style")
#     print(question_style_bonus)
#     print("**Raw Question**")
#     print(raw)
#     st.session_state.question_final = raw
#     print("**Calculation Checked Question**")
#     print(calculation_checker(raw))
#     st.session_state.question_final = calculation_checker(raw)

# if st.session_state.question_final:
#     bonus_index = 0
#     for i in range(len(st.session_state.question_final)):
#         if st.session_state.question_final[i:i+5] == "BONUS" or st.session_state.question_final[i:i+5]=="Bonus":
#             bonus_index = i

#     tossup_ans_index = 0
#     for i in range(len(st.session_state.question_final)):
#         if st.session_state.question_final[i:i+6] == "ANSWER":
#             tossup_ans_index = i
#             break
    
#     if(tossup_ans_index==0):
#         tossup_ans_index = bonus_index

#     bonus_ans_index = 0
#     for i in range(len(st.session_state.question_final)):
#         if st.session_state.question_final[i:i+6] == "ANSWER":
#             bonus_ans_index = i
    
#     if(bonus_ans_index==0):
#         bonus_ans_index = len(st.session_state.question_final)-1
    
#     toss_up = st.session_state.question_final[0:tossup_ans_index]
#     bonus = st.session_state.question_final[bonus_index:bonus_ans_index]
    
#     st.write("### Toss-Up Question:")
#     st.write(toss_up)

#     st.session_state.toss_up_attempt = st.text_input("Your Answer for Toss-Up:", st.session_state.toss_up_attempt)
#     if st.session_state.toss_up_attempt:
#         st.session_state.toss_up_answer = similarity(toss_up, st.session_state.toss_up_attempt)
#         st.write(st.session_state.toss_up_answer)

#     if st.button("Reveal Bonus"):
#         st.session_state.bonus_revealed = True 

#     if st.session_state.bonus_revealed:
#         st.write("### Bonus Question:")
#         st.write(bonus)

#         st.session_state.bonus_attempt = st.text_input("Your Answer for Bonus:", st.session_state.bonus_attempt)
#         if st.session_state.bonus_attempt:
#             st.session_state.bonus_answer = similarity(bonus, st.session_state.bonus_attempt)
#             st.write(st.session_state.bonus_answer)

def create_question(initial):
    category, topic = select_topic(initial)
    index = 0
    if(category=="Math"):
      raw = llama_math(category, topic)
      return raw
    energy = False
    if(category=="Energy"):
      energy = True 
      x = random.randint(0,3)
      if(x==0):
        category = "Biology"
      elif(x==1):
        category = "Chemistry"
      elif(x==2):
        category = "Physics"
      elif(x==3):
        category = "Earth Science"
    for i in range(len(subtopics[category])):
      if subtopics[category][i] == topic:
          index = i
          break
    
    ans = []
    x = random.randint(0,2)
    if category == "Chemistry":
        ans = chem_text
    elif category == "Biology":
        ans = bio_text
    elif category == "Physics":
        ans = harder_phys_text
    elif category == "Earth Science":
        ans = ess_text

    question_style_tossup = ""
    question_example_tossup = ""
    question_instructions_tossup = ""
    if temp_category=="Chemistry" or temp_category=="Biology" or temp_category=="Physics" or temp_category=="Earth Science":
        x = random.randint(0,len(question_styles_tossups[temp_category])-1)
        question_style_tossup = question_styles_tossups[temp_category][x]
        question_example_tossup = question_styles_examples_tossups[temp_category][x]
        question_instructions_tossup = question_style_explanations[question_style_tossup]

    question_style_bonus = ""
    question_example_bonus = ""
    question_instructions_bonus = ""
    if temp_category=="Chemistry" or temp_category=="Biology" or temp_category=="Physics" or temp_category=="Earth Science":
        x = random.randint(0,len(question_styles_bonuses[temp_category])-1)
        question_style_bonus = question_styles_bonuses[temp_category][x]
        question_example_bonus = question_styles_examples_bonuses[temp_category][x]
        question_instructions_bonus= question_style_explanations[question_style_bonus]

    difficulty = 3
    retrieved_text = ""
    retrieved_text = ans[index]
    # print(index)
    # print(question_style_tossup)
    # print(question_style_bonus)
    # print("**Category**")
    # print(category)
    # print("**Topic**")
    # print(index)
    # print(topic)
    # print("**Retrieved Text**")
    # print(retrieved_text)
    # print("**Question Style Tossup")
    # print(question_style_tossup)
    # print("**Question Example Tossup")
    # print(question_example_tossup)
    # print("**Question Style Bonus")
    # print(question_style_bonus)
    # print("**Question Example Bonus")
    # print(question_example_bonus)
    raw = llama_generate_science_bowl_question(energy, temp_category, retrieved_text, difficulty, category, topic, question_style_tossup, question_example_tossup, question_instructions_tossup, question_style_bonus, question_example_bonus, question_instructions_bonus)
    # print("**TOSS UP style")
    # print(question_style_tossup)
    # print("**BONUS style")
    # print(question_style_bonus)
    # print("**Raw Question**")
    # print(raw)
    # print(ans)
    # ans = calculation_checker(raw)
    index = 0
    for i in range(len(raw)):
      if(raw[i:i+8]=="</think>"):
        index = i+9
    return raw[index:]

# print(create_question("Chemistry"))
  
import re
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_config import auth

# Reference to Firestore
db = firestore.client()

def find_question(category):
    doc_ref = db.collection('questions').document('sciencebowl')
    doc_snapshot = doc_ref.get()
    doc_data = doc_snapshot.to_dict()
    questions = doc_data[category]
    x = random.randint(0, len(questions) - 1)
    return questions[x]

# def find_question(category):
#   return("**TOSSUP** Who are you? ANSWER: Stavya, **BONUS** Who are you? ANSWER: Stavya")

# def upload_question(question, category):
#     doc_ref = db.collection('questions').document('sciencebowl')
#     doc_ref.update({category: firestore.ArrayUnion([question])})

# for i in range(50):
#     question = create_question("Physics")
#     upload_question(question, "Physics")

# for i in range(50):
#     question = create_question("Chemistry")
#     upload_question(question, "Chemistry")

# for i in range(50):
#     question = create_question("Biology")
#     upload_question(question, "Biology")

# doc_ref = db.collection('questions').document('sciencebowl')
# doc_snapshot = doc_ref.get()
# doc_data = doc_snapshot.to_dict()
# print("Bio")
# print(len(doc_data["Biology"]))
# print("Phys")
# print(len(doc_data["Physics"]))
# print("Chem")
# print(len(doc_data["Chemistry"]))
# print("ESS")
# print(len(doc_data["Earth Science"]))

def extract_and_upload_questions(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression to capture TOSSUP and BONUS questions with variations in formatting
    question_pair_pattern = re.compile(
        r'(\*\*(?:TOSSUP|BIOLOGY|PHYSICS|CHEMISTRY|EARTH SCIENCE|MATH).*?\bANSWER:\s*.*?(?:\n{1,2}))'
        r'(\*\*(?:BONUS|BIOLOGY|PHYSICS|CHEMISTRY|EARTH SCIENCE|MATH).*?\bANSWER:\s*.*?(?=\n\*\*|\Z))',
        re.DOTALL | re.IGNORECASE
    )

    # Find all question pairs using regex
    question_pairs = question_pair_pattern.findall(content)

    # List to hold the combined questions
    combined_questions = []
    extracted_text = []

    for tossup, bonus in question_pairs:
        combined_question = f"{tossup.strip()} {bonus.strip()}"
        
        # Ensure the combined question contains exactly two occurrences of "ANSWER:" or "Answer:"
        if combined_question.lower().count("answer:") == 2:
            combined_questions.append(combined_question)
            extracted_text.append(tossup)
            extracted_text.append(bonus)

    # Reference to Firestore
    doc_ref = db.collection('questions').document('sciencebowl')

    # Upload the valid questions to Firestore
    if combined_questions:
        doc_ref.update({'Chemistry': firestore.ArrayUnion(combined_questions)})
        print(f"Successfully added {len(combined_questions)} question pairs to Firestore.")
    else:
        print("No valid question pairs found with exactly two 'ANSWER' occurrences.")

    # Remove extracted questions from file
    if extracted_text:
        for text in extracted_text:
            content = content.replace(text, '')

        with open(file_path, 'w') as file:
            file.write(content)

        print(f"Successfully removed {len(extracted_text)//2} question pairs from file.")

# doc_ref = db.collection('questions').document('sciencebowl')
# doc = doc_ref.get()
# earth_science = doc.to_dict().get('Earth Science', [])
# earth_science = earth_science[:18]
# doc_ref.update({
#                 'Earth Science': earth_science
#             })

# extract_and_upload_questions('./chem.txt')

# while True:
#   question = create_question("Physics")
#   doc_ref = db.collection('questions').document('sciencebowl')
#   doc_ref.update({
#       'Physics': firestore.ArrayUnion([question])
#   })

# print(create_question("Math"))

# for i in range(100):
#   question = create_question("Earth Science")
#   doc_ref = db.collection('questions').document('sciencebowl')
#   doc_ref.update({
#       'Earth Science': firestore.ArrayUnion([question])
#   })

# for i in range(50):
#   question = create_question("Physics")
#   doc_ref = db.collection('questions').document('sciencebowl')
#   doc_ref.update({
#       'Physics': firestore.ArrayUnion([question])
#   })

# for i in range(50):
#   question = create_question("Chemistry")
#   doc_ref = db.collection('questions').document('sciencebowl')
#   doc_ref.update({
#       'Chemistry': firestore.ArrayUnion([question])
#   })

# for i in range(50):
#   question = create_question("Biology")
#   doc_ref = db.collection('questions').document('sciencebowl')
#   doc_ref.update({
#       'Biology': firestore.ArrayUnion([question])
#   })