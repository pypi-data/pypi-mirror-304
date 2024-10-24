# SlurmiPy

Run python functions on a SLURM cluster as easy as:
```
@slurm_cluster.execute
def hello_world():
    print("YAY, I am running via SLURM!")
```

SlurmiPy provides a factory class for managing Dask clusters on SLURM-based systems and provides very easy exectution of python code on a SLURM cluster.

## Installation

```bash
pip install slurmipy
```

## Usage

Here iss a basic example of how to use `SlurmiPy` on NERSCs' Perlmutter Supercomputer:

```python
from slurmipy import SlurmiPy, configs

# Create a SLURM cluster with 4 jobs
slurm_cluster = SlurmiPy(jobs=4, **configs["perlmutter_shared_interactive"])

@slurm_cluster.execute
def process_data(data):
    return [x**2 for x in data]

# Execute the function using the SLURM cluster
result = process_data([1, 2, 3, 4])

print(result)  # Output: [1, 4, 9, 16]
```
