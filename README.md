# Documentation Mapper
![Final network abstract](planday.png)
This repo contains:
- A documentation scraper app.
- A data analysis 'lib' containing a set of text sentiment methods.
- A set of tools to pull and transform stored data.

![Final network](planday_text.png)

## Installation
```bash
# get repository.
git clone git@github.com:Benno4president/documentation_mapper.git
# create a virtual environment (optional).
python3 -m venv venv
# install the required libs.
pip3 install -r requirements.txt
```

## Usage
```bash
# scraper usage.
python3 app/main.py --help 
# to build a .gexf file.
python3 tools/build_doc_link_graph.py [path-to-file]
```
