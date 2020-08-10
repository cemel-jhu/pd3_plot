# pd3_plot
![PyPi Version](https://img.shields.io/pypi/v/pd3-plot.svg)

## Description
`pd3_plot` is a utility to help plot dislocation from `pd3` in either 2D or 3D!
It's an exceptionally useful tool for quickly analyzing a dislocation study, or
setting up the initial parameters of a study.

Here is an example of what this program can do!

![Image of 2D plot](https://raw.github.com/cemel-jhu/pd3_plot/master/images/example.png)

## Installation

`pip install pd3_plot`

## Usage

This code is generously licensed under MIT. We request that if this
visualization library is used, that the DOI for this project is properly cited.
Thanks.

```python
from pd3_plot import Plotter as pd3p

# Load up pd3 protobuf data...

plotter = pd3p(data)
plotter.plot_2D()
```

## Acknowledgements
Research was sponsored by the Army Educational Outreach Program (AEOP) and was
accomplished under AEOP Research & Engineering Apprenticeship Program FY20 Site
Agreement.  The views and conclusions contained in this document are those of
the authors and should not be interpreted as representing the official
policies, either expressed or implied, of the Army Educational Outreach Program
or the U.S. Government.  The U.S. Government is authorized to reproduce and
distribute reprints for Government purposes notwithstanding any copyright
notation herein.
