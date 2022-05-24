import http.client
import json
import jinja2 as j
from pathlib import Path
from Seq1 import Seq


SERVER = "rest.ensembl.org"
HTML = "./html/"
OK = 200
ERROR = 400
genes_dict = {"SRCAP": "ENSG00000080603",
              "FRAT1": "ENSG00000165879",
              "ADA": "ENSG00000196839",
              "FXN": "ENSG00000165060",
              "RNU6_269P": "ENSG00000212379",
              "MIR633": "ENSG00000207552",
              "TTTY4C": "ENSG00000228296",
              "RBMY2YP": "ENSG00000227633",
              "FGFR3": "ENSG00000068078",
              "KDR": "ENSG00000128052",
              "ANK2": "ENSG00000145362"}


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
    data = {}
    if response.status == OK:
        data = json.loads(response.read().decode("utf8"))
        print("Data:", data)
    else:
        status, contents = error_html()
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
    status, data, contents = get_response(endpoint, arg)
    try:
        top_level_region = data["top_level_region"]
        length = 0
        for dicts_chrom in top_level_region:
            try:
                if dicts_chrom['name'] == chromosome:
                    length = dicts_chrom['length']
                    break
                context = {"specie": species, "chromosome": chromosome, "length": length}
                contents = cont("chromo_length.html", context)
            except (KeyError, ValueError, IndexError):
                status, contents = error_html()
    except KeyError:
        status, contents = error_html()
    return status, contents


def gene_seq(gene):
    endpoint = f"/sequence/id/{genes_dict[gene]}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        bases = data['seq']
        context = {"gene": gene, "bases": bases}
        contents = cont("gene_seq.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents

def gene_info(gene):
    endpoint = f"/sequence/id/{genes_dict[gene]}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        id = data['id']
        desc = data['desc']
        desc = desc.split(':')
        chrom_name = desc[1]
        start = int(desc[3])
        end = int(desc[4])
        length = end - start
        context = {"gene": gene, "start": start, "end": end, "id": id, "length": length, "chromosome_name": chrom_name}
        contents = cont("gene_info.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents

def gene_calc(gene):
    endpoint = f"/sequence/id/{genes_dict[gene]}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    BASES = {"A":0, "C":0, "G":0, "T":0}
    try:
        seq = data['seq']
        base_percent = 0
        for base, percent in BASES.items():
            base_percent = round((seq.count(base) * 100) / len(seq), 2)
            BASES[base] = base_percent
        context = {"gene": gene, "length": len(seq), "base_percent": base_percent}
        contents = cont("gene_calc.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents

    '''try:
        seq = data['seq']
        length = len(seq)
        A = round((seq.count("A") * 100) / len(seq), 2)
        C = round((seq.count("C") * 100) / len(seq), 2)
        T = round((seq.count("T") * 100) / len(seq), 2)
        G = round((seq.count("G") * 100) / len(seq), 2)
        context = {"gene": gene, "length": length, "A": A, "C": C, "G": G, "T": T}
        contents = cont("gene_calc.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents'''

