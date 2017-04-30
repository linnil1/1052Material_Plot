# A EASY Plotting for Reaction of Material

# Input

Just edit UserInput.py

## show
` show = "F,y,dy" `

means plot F(force) and Y(Y-displacement) and dy(slope of Y)

There are the list of variable name

| name | full name |
| ---  | ---- |
| F    | Force |
| V    | Shear |
| M    | Moment|
| dy   | angle(slope) of y displacement |
| y    | Deflection y displacement |
| T    | Torque |
| Fint | Internal Force |
| P    | Pressure |
| dx   | X_displacement |
| Tint | Internal Torque |
| A    | Twist Angle |

## lmax

` lmax = 3 `

Tell the length of the structure

## want

` want=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)] `

The Force (or Torque) that question give.

` (a,0,-1) ` Means $$ a \left \langle x - 0 \right \rangle _ {-1} $$

Which `a` is unknown.

` (-1,(0,1)) ` means  a continuous force `y = -1` from `0` to `1`

` (-x+3,(1,2)) ` means  a continuous force `y = -(x-1)+3` from `1` to `2`


## boundary

` boundary_condition = [("V", lmax, 0),("M", lmax, 0),("y",0,0),("y",lmax,0)] `

The boundary condition we need to solve unknowns.

` ("V", lmax, 0) ` 
means Shear Force should be `0` when `x=lmax`


If there are not exist any unknown, set `boundary_condition=[]` .

 
## weight

` weight = [(0.7,0,0.3),(0.3,0.3,1)] `

The const of each section of structure.

If no specify, weight is always = 1

` (0.7,0,0.3) ` 
means the value should **times** `0.7` at `[0,0.3]`

This cannot be applied when you want to get deflection, or deflection angle.

# Run

Recommand running it in jupyter notebook

In face, you can use command line

` python3 material_plot.py `

# Result

It will automatically calculate the variable you set

by Boundary you provided.

In this example,

We get ` {c1: 1/24, Fb: 1/2, c2: 0, Fa: 1/2} `

Also, get expression by Deflection formula ,

plot expression and show min and max for you.

![demoPNG](http://imgur.com/TrOAc9K.png)


# Author

linnil1
