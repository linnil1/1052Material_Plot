# Plot internal force diagram of Material

# Install

require Python3.5

```
git clone https://github.com/linnil1/1052Material_Plot.git
cd 1052Material_Plot
pip3 install -e .
```

# Input Usage

Just edit UserInput.py

or copy to jupyter notebook cell

## example

``` python
from material_plot import main
from sympy import symbols, Rational
a, b, c, x = symbols("Fa Fb Fc x", real=True)
show = "F,y,dy"
external=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)]
length = 3
boundary_condition = [("V", length, 0),("M", length, 0),("y",0,0),("y",length,0)]
main(show, length, external, boundary_condition, weight=[])
```

## show
` show = "F,y,dy" `

means plot diagram of F(force) and Y(Y-displacement) and dy(slope of Y)

Use comma `,` to separate each vatiable.

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

## length

` length = 3 `

Tell the length of the structure

## external

` exernal=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)] `

The External Force (or Torque or somewhat) that question given.

` (a,0,-1) ` Means $$ a \left \langle x - 0 \right \rangle _ {-1} $$

Which `a` is unknown.

` (-1,(0,1)) ` means  a continuous force `y = -1` from `0` to `1`

` (-x+3,(1,2)) ` means  a continuous force `y = -(x-1)+3` where `x` from `1` to `2`


## boundary

` boundary = [("V", length, 0),("M", length, 0),("y",0,0),("y",length,0)] `

The boundary condition we need to solve unknowns.

` ("V", length, 0) ` 
means Shear Force should be `0` when `x=length`


If there are not exist any unknown, set `boundary=[]` .

 
## weight

` weight = [(0.7,0,0.3),(0.3,0.3,1)] `

The const of each section of structure.

If no specify, weight is always = 1

` (0.7,0,0.3) ` 
means the value should **times** `0.7` at `[0,0.3]`

This cannot be applied when you want to get deflection, or deflection angle.

# Run

Recommand running it in jupyter notebook

` python3 -m notebook `

In fact, you can use it in command line.

# Result

It will automatically calculate the variable you set

by Boundary you provided.

In this example,

We get ` {c1: 1/24, Fb: 1/2, c2: 0, Fa: 1/2} `

Also, get expression by Deflection formula ,

plot expression and show min and max for you.

![demoPNG](http://imgur.com/TrOAc9K.png)

# Demo

And open `example.ipynb` for some exmaples.

Or just execute `UserInput.py`,

and you will know how to set the input.

# UnitTest

` python3 data_unit_test.py -v`

# TODO

write test for plot

# Author

linnil1
