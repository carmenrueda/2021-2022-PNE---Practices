import http.client
import json
import jinja2
from pathlib import Path


SERVER = "http://rest.ensembl.org"
HTML_FOLDER = "./html/"
valid = 200
error = 400

def read_html_file(filename):
    contents = Path(HTML_FOLDER + filename).read_text()
    contents = jinja2.Template(contents)
    return contents

def list_species(limit=None):
    endpoint = '/info/species'
    params = '?content-type=application/json'
    url = endpoint + params

    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()
    status = valid

    if response.status == valid:
        data = json.loads(response.read().decode("utf8"))
        try:
            species = data["species"]
            contents = read_html_file(HTML_FOLDER + "species.html")\
                .render(context={
                "total": len(species),
                "species": species,
                "limit": limit
            })
        except KeyError:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()
    else:
        status = error
        contents = Path(HTML_FOLDER + "error.html").read_text()

def karyotype(species):
    endpoint = '/info/assembly/'
    params = f'{species}?content-type=application/json'
    url = endpoint + params

    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()
    status = valid

    if response.status == valid:
        data = json.loads(response.read().decode("utf8"))
        try:
            karyotype = data["karyotype"]
            contents = read_html_file(HTML_FOLDER + "karyotype.html")\
                .render(context={
                "karyotype": karyotype
            })
        except KeyError:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()
    else:
        status = error
        contents = Path(HTML_FOLDER + "error.html").read_text()


def chrom_length(species, chromosomes):
    endpoint = '/info/assembly/'
    params = f'{species}?content-type=application/json'
    url = endpoint + params

    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()
    status = valid

    if response.status == valid:
        data = json.loads(response.read().decode("utf8"))
        try:
            top_level_region = data["top_level_region"]
            lenght = 0
            for chromosome in top_level_region:
                if chromosome['name'] == chromosomes:
                    lenght = chromosomes['length']
                    break
            contents = read_html_file(HTML_FOLDER + "species.html")\
                .render(context={
                "length": length,
            })
        except KeyError:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()
    else:
        status = error
        contents = Path(HTML_FOLDER + "error.html").read_text()


