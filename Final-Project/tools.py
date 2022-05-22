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
    connection = http.client.HTTPConnection(SERVER)
    connection.request("GET", url)
    response = connection.getresponse()
    status = OK
    data = None
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
    elif response.status == ERROR:
        status, contents = error_html()
    return status, data


def list_species(limit=None):
    endpoint = '/info/species'
    arg = '?content-type=application/json'
    status, data = get_response(endpoint, arg)
    try:
        species = data['species']
        contents = read_html_file("species.html").render(context={"total": len(species), "species": species, "limit": limit})
    except KeyError:
        status, contents = error_html()
    return status, contents


def karyotype(specie):
    endpoint = '/info/assembly/'
    arg = f'{specie}?content-type=application/json'
    status, data = get_response(endpoint, arg)
    try:
        karyotype = data['karyotype']
        contents = read_html_file("karyotype.html").render(context={"karyotype": karyotype})
    except KeyError:
        status, contents = error_html()
    return status, contents


def chromosome_length(specie, chromo):
    endpoint = '/info/assembly/'
    arg = f'{specie}?content-type=application/json'
    status, data = get_response(endpoint, arg)
    try:
        chromosome_dict = data["top_level_region"]
        length = 0
        for c in chromosome_dict:
            if c['name'] == chromo:
                length = c['length']
                break
        contents = read_html_file("chromo_length.html").render(context={"chromosome": chromo, "specie": specie, "length": length})
    except KeyError:
        status, contents = error_html()
    return status, contents


def get_id(gene):
    endpoint = '/homology/symbol/human/'
    arg = f'{gene}?content-type=application/json'
    valid = True
    id = None
    status, data = get_response(endpoint, arg)
    try:
        id = data['data'][0]['id']
    except (KeyError, IndexError):
        valid = False
    return valid, id


def gene_seq(gene):
    valid, id = get_id(gene)
    if valid:
        endpoint = '/sequence/id/'
        arg = f'{id}?content-type=application/json'
        status, data = get_response(endpoint, arg)
        try:
            bases = data['seq']
            contents = read_html_file("gene_seq.html").render(context={"gene": gene, "bases": bases})
        except KeyError:
            status, contents = error_html()
    else:
        status, contents = error_html()
    return status, contents


def gene_info(gene):
    valid, id = get_id(gene)
    if valid:
        endpoint = '/overlap/id/'
        arg = f'{id}?feature=gene;content-type=application/json'
        status, data = get_response(endpoint, arg)
        try:
            start = data[0]['start']
            end = data[0]['end']
            length = end - start
            chrom_name = data[0]['assembly_name']
            contents = read_html_file("gene_info.html").render(context={"gene": gene, "start": start, "end": end, "id": id, "length": length, "chromosome_name": chrom_name})
        except KeyError:
            status, contents = error_html()
    else:
        status, contents = error_html()
    return status, contents


def gene_calc(gene):
    valid, id = get_id(gene)
    if valid:
        endpoint = '/sequence/id/'
        arg = f'{id}?content-type=application/json'
        status, data = get_response(endpoint, arg)
        try:
            bases = data['seq']
            seq = Seq(bases)
            contents = read_html_file("gene_calc.html").render(context={"gene": gene, "seq": seq})
        except KeyError:
            status, contents = error_html()
    else:
        status, contents = error_html()
    return status, contents


def gene_list(chromo, start, end):
    endpoint = '/overlap/region/human/'
    arg = f'{chromo}:{start}-{end}?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon'
    status, data = get_response(endpoint, arg)
    try:
        contents = read_html_file("gene_list.html").render(context={"data": data})
    except KeyError:
        status, contents = error_html()
    return status, contents
