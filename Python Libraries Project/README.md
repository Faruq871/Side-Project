# Python Library Reference

Jupyter notebooks for commonly used Python libraries and interfaces to other language runtimes.

## Notebooks

| Notebook | Topics |
|---|---|
| `numpy.ipynb` | Arrays, indexing, broadcasting, random numbers, linear algebra |
| `pandas.ipynb` | File I/O, selection, cleaning, grouping, joins, reshaping |
| `matplotlib.ipynb` | Static plots, axes, annotations, layouts, export |
| `seaborn.ipynb` | Distributions, relationships, categorical plots, facets |
| `scipy.ipynb` | Optimization, statistics, sparse matrices, interpolation, signals |
| `scikit_learn.ipynb` | Preprocessing, pipelines, validation, tuning, metrics, feature selection, unsupervised learning |
| `statsmodels.ipynb` | Regression, inference, diagnostics, time series |
| `plotly.ipynb` | Interactive charts, graph objects, subplots, export |
| `sqlalchemy.ipynb` | SQL execution, SQL expressions, ORM, sessions, relationships |
| `rpy2.ipynb` | R execution, function calls, pandas conversion |
| `pythonnet.ipynb` | .NET runtime, assemblies, classes, collections |
| `jpype.ipynb` | JVM, Java classes, arrays, collections |
| `py4j.ipynb` | Java gateway, Java objects, collection conversion |
| `ctypes.ipynb` | C shared libraries, signatures, pointers, structures, callbacks |
| `cffi.ipynb` | C declarations, shared libraries, pointers, ABI/API modes |
| `cppyy.ipynb` | C++ declarations, classes, standard library, shared libraries |

## Usage

Use Python 3.10 or later. Create a virtual environment, activate it, and install the packages you need:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install the listed Python dependencies with:

```bash
pip install -r requirements.txt
```

Some notebooks require software outside Python: `rpy2` requires R; `pythonnet` requires a compatible .NET runtime; `jpype` requires Java; `py4j` requires a running Java gateway; native interfaces may require shared libraries, headers, or compilers. Configure these dependencies for your operating system before running the relevant notebook.

Run cells in order within each notebook. Examples use small illustrative data. Paths, database URLs, runtime names, and native library names may need adjustment.

Do not load serialized Python objects or native libraries from untrusted sources. Keep test data separate from model selection when using scikit-learn.

## License

MIT. See `LICENSE`.
