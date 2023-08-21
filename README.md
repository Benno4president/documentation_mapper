# Documentation Mapper
This repo contains:
- A documentation scraper app.
- A data analysis 'lib' containing a set of text sentiment methods.
- A set of tools to pull and transform stored data.

## Installation
```bash
# get repository.
git clone git@github.com:Benno4president/documentation_mapper.git
# create a virtual environment (optional).
python3 -m venv venv
# install the required libs.
pip3 install -r requirements.txt
# install the driver needed by selenium.
sudo apt install chromium-chromedriver
```

## Usage
```bash
# scraper usage.
python3 app/main.py --help 
# to build a .gexf file.
python3 tools/build_doc_link_graph.py [path-to-file]
```


## dev notes
use lib:
- https://github.com/dbader/schedule
- https://github.com/Delgan/loguru