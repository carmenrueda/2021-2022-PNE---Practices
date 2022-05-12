import http.client
import json
import jinja2
from pathlib import Path
from Seq1 import Seq


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
            len = 0
            for chromosome in top_level_region:
                if chromosome['name'] == chromosomes:
                    lenght = chromosomes['length']
                    break
            contents = read_html_file(HTML_FOLDER + "species.html")\
                .render(context={
                "length": len,
            })
        except KeyError:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()
    else:
        status = error
        contents = Path(HTML_FOLDER + "error.html").read_text()

def get_id(gene):
    endpoint = '/homology/symbol/human/'
    params = f'{gene}?content-type=application/json'
    url = endpoint + params

    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()

    ok = True
    id = None

    if response.status == valid:
        data = json.loads(response.read().decode("utf8"))
        try:
            bases = data['data'][0]['id']
        except(KeyError, IndexError):
            ok = False
    else:
        ok = False


def gene_seq(gene):
    ok, id = get_id(gene)
    if ok:
        endpoint = '/sequence/id'
        params = f'{id}?content-type=application/json'
        url = endpoint + params

        conn = http.client.HTTPConnection(SERVER)
        conn.request("GET", url)
        response = conn.getresponse()
        status = valid

        if response.status == valid:
            data = json.loads(response.read().decode("utf8"))
            try:
                bases = data['seq']
                contents = read_html_file(HTML_FOLDER + "gene_seq.html") \
                    .render(context={
                    "gene": gene,
                    "bases": bases
                })
            except KeyError:
                status = error
                contents = Path(HTML_FOLDER + "error.html").read_text()
        else:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()

        return status, contents


def gene_info(gene):
    ok, id = get_id(gene)
    if ok:
        endpoint = '/overlap/id'
        params = f'{id}?feature=gene;content-type=application/json'
        url = endpoint + params

        conn = http.client.HTTPConnection(SERVER)
        conn.request("GET", url)
        response = conn.getresponse()
        status = valid

        if response.status == valid:
            data = json.loads(response.read().decode("utf8"))
            try:
                start = data[0]['start']
                end = data[0]['end']
                length = end - start
                chrom_name = data[0]['assembly_name']
                contents = read_html_file(HTML_FOLDER + "gene_info.html") \
                    .render(context={
                    "gene": gene,
                    "start": start,
                    "end": end,
                    "id": id,
                    "lenght": length,
                    "chrom_name": chrom_name
                })
            except KeyError:
                status = error
                contents = Path(HTML_FOLDER + "error.html").read_text()
        else:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()

        return status, contents


def gene_calc(gene, seq):
    endpoint = '/info/assembly/'
    params = f'{gene}?content-type=application/json'
    url = endpoint + params

    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()
    status = valid

    if response.status == valid:
        data = json.loads(response.read().decode("utf8"))
        try:
            bases = data['seq']
            seq = Seq(bases)
            contents = read_html_file(HTML_FOLDER + "gene_calc.html") \
                .render(context={
                "gene": gene,
                "seq": seq,
            })
        except KeyError:
            status = error
            contents = Path(HTML_FOLDER + "error.html").read_text()
    else:
        status = error
        contents = Path(HTML_FOLDER + "error.html").read_text()



