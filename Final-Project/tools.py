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


def ok_response(response):
    status = OK
    data = json.loads(response.read().decode("utf8"))
    return status, data


def cont(file, context):
    contents = read_html_file(file).render(context=context)
    return contents


def get_response(endpoint, arg):
    url = endpoint + arg
    conn = http.client.HTTPConnection(SERVER)
    conn.request("GET", url)
    response = conn.getresponse()
    status = OK
    contents = ""
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
        print(data)
        status = OK
    elif response.status == ERROR:
        status, contents = error_html()
        data = 0
    return status, data, contents


def list_species(limit=None):
    endpoint = '/info/species'
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        species = data['species']
        file = "species.html"
        context = {"total": len(species), "species": species, "limit": limit}
        contents = cont(file, context)
    except KeyError:
        status, data = error_html()
    return status, contents


def karyotype(specie):
    endpoint = '/info/assembly/'
    arg = f'{specie}?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        karyotype = data['karyotype']
        context = {"karyotype": karyotype}
        contents = cont("karyotype.html", context)
    except KeyError:
      status, contents = error_html()
    return status, contents


def chromosome_length(species, chromosome):

    '''En arg hay dos diccionarios: uno con la key specie y value human,
    y otro con keys como assembly_name, karyotype, top_level_region...
    Accedemos a la key top_level_region.
    El valor de la key es una lista de diccionarios de los distintos cromosomas.
    Cada diccionario contiene keys como name, length...
    Accedemos a nuestro cromosoma por su nombre y llamamos a la key length de ese cromosoma.'''

    endpoint = '/info/assembly/'
    arg = f'{species}?content-type=application/json'
    status, data = get_response(endpoint, arg)
    try:
        top_level_region = data["top_level_region"]
        length = 0
        for chromosome_interest in top_level_region:
            if chromosome_interest['name'] == chromosome:
                length = chromosome_interest['length']
        context = {"chromosome": chromosome, "specie": species, "length": length}
        contents = cont("chromo_length.html", context)
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
            context = {"gene": gene, "bases": bases}
            contents = cont("gene_seq.html", context)
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
            context = {"gene": gene, "start": start, "end": end, "id": id, "length": length,"chromosome_name": chrom_name}
            contents = cont("gene_info.html", context)
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
            context = {"gene": gene, "seq": seq}
            contents = cont("gene_calc.html", context)
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
        context = {"data": data}
        contents = cont("gene_list.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents

