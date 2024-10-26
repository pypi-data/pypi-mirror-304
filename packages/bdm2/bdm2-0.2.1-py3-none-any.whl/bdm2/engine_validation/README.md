engine_validation
Version: 0.1.1

##Description
engine_validation is a package for the release of Birdoo engines. In release 0.1.1, there are two types of releases:

aws_cloud (on EC2)
split (in the split repository)

####Package Structure

````
engine_validation
├── __init__.py
├── entities
│   ├── db_component.py
│   ├── device_engine.py
│   ├── ec2_engine.py
│   ├── engine_component.py
│   ├── git_comon_component.py
│   ├── split_engine.py
├── poetry.lock
├── README.md
├── release_engine.py
└── release_engine_config.yaml
````

Installation
To install the package, use the following command:

bash

````
pip install path_to_your_package/engine_validation
````

####Usage
Release Types

- AWS Cloud Release
  This release type is for deploying Birdoo engines on EC2 instances.
- Split Release
  This release type is for deploying Birdoo engines in the split repository.

####Modules and Components

 ````
db_component.py 
````

1) Handles database-related operations for the engine validation.

 ````
device_engine.py
 ````

2) Manages device-specific engine validation logic.

 ````
ec2_engine.py
 ````

3) Manages EC2-specific engine validation and deployment logic.

 ```` 
engine_component.py
 ````

4) Core engine components for validation and deployment.

 ````
git_comon_component.py
 ````

5) Common Git operations and handling for engine validation.

 ````
split_engine.py
 ````

6) Manages split repository-specific engine validation and deployment logic.

####Configuration
The package uses a configuration file release_engine_config.yaml for various settings and parameters required during the
release process.

Examples
Here is a basic example of how to use the release_engine.py script:

from engine_validation.release_engine import release_engine

### Initialize the release process

release_engine(config_path='path_to_config/release_engine_config.yaml')
setup config:

````
local_release_paths:
    - \\PawlinServer\Projects\prj\MHDR\BIRDOO\Releases\v4.0.0.00\jetson_split_v4.10.0.00_0101

# aws, split
this_is_release_for: split

# can not to be empty
commit_message: 'some message'

# for split does not set as actual
set_actual: False
combination:
    client: DEFAULT
    breed_type: DEFAULT
    gender: DEFAULT
````


