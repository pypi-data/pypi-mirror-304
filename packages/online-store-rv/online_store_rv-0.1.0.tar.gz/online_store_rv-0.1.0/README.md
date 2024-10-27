The project is designed for convenient store management.
It offers two algorithms to manage orders, as well as keep a report on customers.

Package Assembly Steps:

Make sure everything is set up: You must have a pyproject.toml file in the root directory of the project, which contains all the necessary dependencies and build settings.

Install the build tool: If you don't have the build tool installed yet, install it using pip:

pip install build
Assemble the package: Run the command to build the package:

python -m build
This command will create two types of packages in the dist directory:

Source Distribution (sdist) is an archive with the source files of the project (for example .tar.gz ).
Wheel Distribution (wheel) is an assembled and ready—to-install package (.whl).
Check: In the dist directory you will see the files that have been created. Example of output files:

dist/
 my_package-0.1.0-py3-none-any.whl

 my_package-0.1.0.tar.gz