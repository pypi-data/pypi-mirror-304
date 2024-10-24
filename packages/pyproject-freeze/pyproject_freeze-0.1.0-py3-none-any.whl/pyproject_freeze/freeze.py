import importlib.metadata
import sys
from pathlib import Path
from tomlkit import document, table, array, inline_table, dumps

def get_installed_packages():
    return {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions()}

def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default: {default}): ").strip()
    return user_input if user_input else default

def parse_author(author_string):
    name, email = author_string.split('<')
    return {"name": name.strip(), "email": email.strip()[:-1]}

def generate_pyproject_toml():
    doc = document()
    
    # Choose package manager
    package_manager = get_user_input("Choose package manager (p)ip, (po)etry, (u)v, or (r)ye", "p").lower()
    
    # Project section
    project = table()
    project.add("name", get_user_input("Enter project name", "your-project-name"))
    project.add("version", get_user_input("Enter project version", "0.1.0"))
    project.add("description", get_user_input("Enter project description", "Your project description"))
    
    # Authors as an array of inline tables
    authors = array().multiline(True)
    while True:
        author = get_user_input("Enter author name and email (format: Name <email@example.com>)", "")
        print('<enter> if there are no more authors')
        if not author:
            break
        authors.append(inline_table())
        authors[-1].update(parse_author(author))
    project.add("authors", authors)    
    project.add("readme", get_user_input("Enter readme file name", "README.md"))
    project.add("requires-python", get_user_input("Enter required Python version", f">={get_python_version()}"))
    
    # Dependencies as an array or table, depending on the package manager
    installed_packages = get_installed_packages()
    include_all = get_user_input("Include all installed packages as dependencies? (y/n)", "y").lower() == 'y'
    
    dependency_strings = []
    if package_manager in ['p', 'po']:  # pip or poetry
        dependencies = array().multiline(True)
        if include_all:
            for package, version in installed_packages.items():
                dependency_strings.append(f"{package}=={version}")
        else:
            for package, version in installed_packages.items():
                if get_user_input(f"Include {package} ({version}) as a dependency? (y/n)", "n").lower() == 'y':
                    dependency_strings.append(f"{package}=={version}")
    else:  # uv or rye
        dependencies = table()
        if include_all:
            for package, version in installed_packages.items():
                dependency_strings.add(package, version)
        else:
            for package, version in installed_packages.items():
                if get_user_input(f"Include {package} ({version}) as a dependency? (y/n)", "n").lower() == 'y':
                    dependency_strings.add(package, version)
    for dep in sorted(dependency_strings, key=str.casefold):
        dependencies.append(dep)
    project.add("dependencies", dependencies)
    doc.add("project", project)
    
    # Build system section
    build_system = table()
    if package_manager == 'po':
        build_system.add("requires", ["poetry-core"])
        build_system.add("build-backend", "poetry.core.masonry.api")
    elif package_manager == 'r':
        build_system.add("requires", ["hatchling"])
        build_system.add("build-backend", "hatchling.build")
    else:  # pip or uv
        build_system.add("requires", ["setuptools>=61.0"])
        build_system.add("build-backend", "setuptools.build_meta")
    
    doc.add("build-system", build_system)
    
    # Add tool-specific configurations
    if package_manager == 'po':
        tool_poetry = table()
        tool_poetry.add("version", project["version"])
        tool_poetry.add("description", project["description"])
        tool_poetry.add("authors", project["authors"])
        tool_poetry.add("readme", project["readme"])
        tool_poetry.add("dependencies", project["dependencies"])
        doc.add("tool", {"poetry": tool_poetry})
    elif package_manager == 'r':
        tool_rye = table()
        tool_rye.add("managed", True)
        doc.add("tool", {"rye": tool_rye})
    
    return dumps(doc, sort_keys=True)

def update_pyproject_toml(file_path):
    pyproject_content = generate_pyproject_toml()
    
    with open(file_path, "w") as f:
        f.write(pyproject_content)
    
    print(f"Updated {file_path} with user-provided information and selected packages.")

def run():
    file_path = Path(get_user_input("Enter the path for pyproject.toml", "pyproject.toml"))
    update_pyproject_toml(file_path)


if __name__ == "__main__":
    run()
