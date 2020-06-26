# Notes (6/22-26/2020)

### Materials Science Notes 
- rb.gy/qgrau1 (the text in red are the scources I got the information from)
    - A crystal is a solid made of atoms, ions, or molecules in a repetitive pattern
    - Each crystal structure in a specific crystal system is defined by a unit cell
    - Unit cell = the smallest repeatable subsection of the crystal 
- http://aflowlib.org/CrystalDatabase/cubic_lattice.html
- https://www.slideshare.net/omaratefradwan/mse501-ch5-radwan
    - Types of cubic crystals: Simple, Face-centered, and Body-centered
        - face- centered: the atoms are at each of the cornoers and the centers of all the cube faces
        - Simple:
        - Body-Centered: 
- https://www.youtube.com/watch?v=cpvTwYAUeA8 
- https://www.slideshare.net/omaratefradwan/mse501-ch5-radwan
- https://study.com/academy/answer/1-what-are-the-slip-planes-burgers-vector-and-tangent-vector-for-the-locking-dislocation.html
- https://www.doitpoms.ac.uk/tlplib/dislocations/burgers.php
- https://www.nde-ed.org/EducationResources/CommunityCollege/Materials/Structure/linear_defects.htm#:~:text=There%20are%20two%20basic%20types,dislocation%20structures%20that%20can%20occur.
- https://www.sciencedirect.com/topics/physics-and-astronomy/screw-dislocations
    - Slip = plastic deformation produced by dislocation motion
    - Slip plane = the horizontal plane separating the stationary lower block of atoms from the displaced top block.
    - ffc = face centered cubic structure
    - slip planes of ffc = __________________
        - thompson tetrahedran notation______________
    - A dislocation is a defect in the lattice (a missing atom)
    - dislocation density = the total dislocation length per unit volume
    - A sessile dislocation = when the the burgers vector? isn't contained in one of the planes and it can't glide and mvove under applied stress. It CAN move by climb (climb = when the dislocation gets excoted eough to move up rows of atoms).
    - A glissile dislocation = The dislocation can move in its own plane
    - a dislocation can belong to multiple planes, when it moves on one plane and then another plane, its called "cross slip"
    - Types of dislocations:
        - screw dislocation
            - the dislocation moves perpendicular to the direction of stress
            - The lattice plane shifts like a spiral staircase 
        - edge dislocation
            - The dislocation moves parallel to the direction of stress
    - The burgers vector measures the difference between the distorted lattice at the dislocation and the perfect lattice. It also is the direction and magnitude of the atomic displacement that happens when a dislocation happens.
        - the space between the gap in the loop around the atoms.
           
### Math Notes
- https://www.youtube.com/watch?v=DgXR2OWQnLc&list=PLDV1Zeh2NRsDGO4--qE8yH72HFL1Km93P
- https://realpython.com/linked-lists-python/
- https://mathworld.wolfram.com/DotProduct.html
- https://www.math.ucdavis.edu/~hunter/intro_analysis_pdf/ch1.pdf
- https://www.mathsisfun.com/algebra/vectors-dot-product.html
- https://www.mathsisfun.com/algebra/vectors-cross-product.html
-https://www.youtube.com/watch?v=BaM7OCEm3G0&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&index=11
    - Graph theory = the mathematical theory of the properties and applications of graphs
    - Types of graphs (ask what cycles mean)
        - undirected graph - edges have no orientation
        - directed graph (Digraphs) - the edges are directed ( you can only go from point a to point b and not the other way around)
        - weighted graphs - edges can have weights to represent an arbitrary value
        - Trees- an undirected graph with no cycles
        - rooted tree- a tree with a deisgnated root node, every edge points away or towrards the root node. 
           - arborescence (out-tree) = when edges point away from the root
           - anti arborescence (in -tree) = when edges point toward the root
       - Directed acyclic graphs = graph with directed edges and no cycles
       - Complete graph - there is a unique edge between every pair of nodes
    - Linked list - an ordered collection of objects,
        - each element of a linked list is called a node and every node has two different feilds:
            - Data contains the value that is stored in the node
            - Next contains a reference to the next node on the list
        - The first node in a linked list is called the head and is the starting point of all iterations through the list
        - The last node must have its next reference pointing to None to make it the end of the list
    - graph
        - can be used to show relationships between objects or to represent different types of networks
        - The most common way to implent graphs is by using an adjacency list 
            - Adjacency list = a list of linked lists where each vertex of the graph is stored alongside a collection of connected verticies
    - a cross product (set theory)
        - cartesian product = the product of two sets: the product of set X and set Y is the set that contains all ordered pairs ( x, y ) for which x belongs to X and y belongs to Y.
        - X×Y={(x,y):x∈X and y∈Y} <---- cartesian product
            - Example: If X = {1, 2, 3} and Y = {4, 5} then X × Y = {(1, 4),(1, 5),(2, 4),(2, 5),(3, 4),(3, 5)} 
        - ask if the cross product is the same as the cartesian product
    - Cross product (vector)
        - a × b = | a | * | b | * sin(θ) * n
            - a is the length of the first vector and b is the length of the second
            - θ is the angle between the vectors
            - n is the unit vector at the right angle of both vectors
        - Right hand rule = you point your pointer finger in the direction of the first vector, and your middle finger in the direction of the second. The way your thumb points is the direction of the cross product
    - Cross product (Geometric interpretation)
        - Results in another vector that's at the right angles of the first two vectors
        - a × b = | a | * | b | * sin(θ) * n
            - a is the length of the first vector and b is the length of the second
            - θ is the angle between the vectors
            - n is the unit vector at the right angle of both vectors
        - Right hand rule = you point your pointer finger in the direction of the first vector, and your middle finger in the direction of the second. The way your thumb points is the direction of the cross product
        - Geometrically, it gives you the area of a parallelogram that is defined by the two vectors
    - a dot product = can be defined for two vectors X and Y by X * Y = |X| * |Y| * cosθ
       - θ is the angle between the vectors
       - X * Y = 0 if X is perpendicular to Y
       - "The dot product therefore has the geometric interpretation as the length of the projection of X onto the unit vector Y^^ when the two vectors are placed so that their tails coincide."

### Python
1)
class Multiples: #unlike java, you don't use public____
    x = 0
    for i in range (1000): #colon instead of {}
      if(i%3==0 or i%5==00 ): #instead of using || and && you just type out "or" "and"
        x +=i #no semi colon at the end
    print (x)
5)

12)

13)