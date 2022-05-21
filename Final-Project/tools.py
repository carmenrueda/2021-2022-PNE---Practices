import http.client
import json
import jinja2 as j
from pathlib import Path
from Seq1 import Seq


SERVER = "rest.ensembl.org"
HTML = "./html/"
OK = 200
ERROR = 400


def read_html_file(filename):
    contents = Path(HTML + filename).read_text()
    contents = j.Template(contents)
    return contents


def error_html():
    status = ERROR
    contents = Path(HTML + "error.html").read_text()
    return status, contents


def get_response(endpoint, params):
    url = endpoint + params
    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()
    status = OK
    return response, status


def list_species(limit=None):
    endpoint = '/info/species'
    arg = '?content-type=application/json'
    response, status = get_response(endpoint, arg)
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
        try:
            species = data['species']
            contents = read_html_file("species.html").render(context={"total": len(species), "species": species, "limit": limit})
        except KeyError:
            status, contents = error_html()
    elif response.status == ERROR:
            status, contents = error_html()
    return status, contents


def karyotype(species):
    endpoint = '/info/assembly/'
    arg = f'{species}?content-type=application/json'
    response, status = get_response(endpoint, arg)
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
        try:
            karyotype = data["karyotype"]
            contents = read_html_file(HTML + "karyotype.html").render(context={"karyotype": karyotype})
        except KeyError:
            status, contents = error_html()
    elif response.status == ERROR:
        status, contents = error_html()
    return status, contents


def chrom_length(species, chromosome):
    endpoint = '/info/assembly/'
    arg = f'{species}?content-type=application/json'
    response = get_response(endpoint, arg)
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
        try:
            chromo_dict = data["top_level_region"]
            length = 0
            for c in chromo_dict:
                if c['name'] == chromosome:
                    length = chromosome['length']
                    break #???????????????????????????????????????????????
            contents = read_html_file(HTML + "species.html").render(context={"length": length})
        except KeyError:
            status, contents = error_html()
    elif response.status == ERROR:
        status, contents = error_html()
    return status, contents


def get_id(gene):
    endpoint = '/homology/symbol/human/'
    arg = f'{gene}?content-type=application/json'
    response = get_response(endpoint, arg)
    valid = True
    id = None
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
        try:
            id = data['data'][0]['id']
        except(KeyError, IndexError):
            valid = False
    else:
        valid = False
    return valid, id


def gene_seq(gene):
    valid, id = get_id(gene)
    if valid:
        endpoint = '/sequence/id'
        params = f'{id}?content-type=application/json'
        response = get_response(endpoint, params)
        status = None
        contents = ""

        if response.status == valid:
            data = json.loads(response.read().decode("utf8"))
            try:
                bases = data['seq']
                contents = read_html_file(HTML + "gene_seq.html").render(context={"gene": gene, "bases": bases})
            except KeyError:
                status, contents = error_html()
        elif response.status == 400:
            status, contents = error_html()
    return status, contents


def gene_info(gene):
    ok, id = get_id(gene)
    if ok:
        endpoint = '/overlap/id'
        params = f'{id}?feature=gene;content-type=application/json'
        response = get_response(endpoint, params)
        status = None
        contents = ""

        if response.status == valid:
            data = json.loads(response.read().decode("utf8"))
            try:
                start = data[0]['start']
                end = data[0]['end']
                length = end - start
                chrom_name = data[0]['assembly_name']
                contents = read_html_file(HTML + "gene_info.html").render(context={"gene": gene, "start": start, "end": end, "id": id, "lenght": length, "chrom_name": chrom_name})
            except KeyError:
                status, contents = error_html()
        elif response.status == 400:
            status, contents = error_html()
    return status, contents


def gene_calc(gene, seq):
    endpoint = '/info/assembly/'
    params = f'{gene}?content-type=application/json'
    response = get_response(endpoint, params)
    status = None
    contents = ""

    if response.status == valid:
        data = json.loads(response.read().decode("utf8"))
        try:
            bases = data['seq']
            seq = Seq(bases)
            contents = read_html_file(HTML + "gene_calc.html").render(context={"gene": gene, "seq": seq})
        except KeyError:
            status, contents = error_html()
    elif response.status == 400:
        status, contents = error_html()
    return status, contents



