# pip freeze for pyproject.toml

# Usage

```
pyenv local 3.12.6
python -m venv venv_3126
source venv_3126/bin/activate
pip install tomlkit

# now we "freeze" into a pyproject.toml
python freeze.py 

Enter the path for pyproject.toml (default: pyproject.toml): 
Choose package manager (p)ip, (po)etry, (u)v, or (r)ye (default: p): p
Enter project name (default: your-project-name): pyproject-freeze
Enter project version (default: 0.1.0): 
Enter project description (default: Your project description): pip freeze for pyproject.toml
Enter author name and email (format: Name <email@example.com>) (default: ): James Munsch <james.a.munsch@gmail.com>
<enter> if there are no more authors
Enter author name and email (format: Name <email@example.com>) (default: ): 
<enter> if there are no more authors
Enter readme file name (default: README.md): 
Enter required Python version (default: >=3.12): 
Include all installed packages as dependencies? (y/n) (default: y): y
Updated pyproject.toml with user-provided information and selected packages.
```

# Output


```
11:21:03 (venv_3126) jm@pop-os pyproject-freeze ±|main ✗|→ cat pyproject.toml 
[project]
name = "pyproject-freeze"
version = "0.1.0"
description = "pip freeze for pyproject.toml"
authors = [
    {name = "James Munsch", email = "james.a.munsch@gmail.com"},
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pip==24.2",
    "tomlkit==0.13.2",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```


### Related info

- https://peps.python.org/pep-0621/
