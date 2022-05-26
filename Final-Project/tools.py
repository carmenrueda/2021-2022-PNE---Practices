import http.client
import json
import jinja2 as j
from pathlib import Path


SERVER = "rest.ensembl.org"
HTML = "./html/"
OK = 200
ERROR = 400
HUMAN_GENES = {"SRCAP": "ENSG00000080603",
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


def error_html():
    status = ERROR
    contents = Path(HTML + "error.html").read_text()
    return status, contents


def get_contents(file, context):
    file_contents = Path(HTML + file).read_text()
    contents = j.Template(file_contents).render(context=context) #haces una plantilla html y con render le metes tus variables
    return contents


def get_response(endpoint, arg):
    url = endpoint + arg
    connection = http.client.HTTPConnection(SERVER)
    connection.request("GET", url)
    response = connection.getresponse()
    status = OK #estas tres lineas son para inicializar las variables
    contents = ""
    data = {}
    if response.status == OK: #si to bien cogemos data y luego trabajamos con ella pa sacar cositas dependiendo d la funcion
        data = json.loads(response.read().decode("utf8")) #convert from json to python and get a dict
        print(data)
    else:
        status, contents = error_html()
    return status, data, contents


def list_species(limit=None):
    endpoint = '/info/species'
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        species = data['species']
        my_species = []
        if limit == 0:
            my_species == []
        else:
            for dicts in species:
                if 'display_name' in dicts:
                    specie = dicts['display_name']
                    my_species.append(specie)
                if len(my_species) == limit:
                    break
        context = {"total": len(species), "species": my_species, "limit": limit}
        contents = get_contents("myspecies.html", context)
    except (KeyError, IndexError):
        status, data = error_html()
    return status, contents


def karyotype(specie):
    endpoint = '/info/assembly/'
    arg = f'{specie}?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        karyotype = data['karyotype']
        context = {"karyotype": karyotype}
        contents = get_contents("karyotype.html", context)
    except KeyError:
      status, contents = error_html()
    return status, contents


def chromosome_length(species, chromosome=int):
    endpoint = '/info/assembly/'
    arg = f'{species}?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        list_chromo = []
        top_level_region = data["top_level_region"]
        for d in top_level_region:
            if d['length'] > chromosome:
                list_chromo.append(d['name'])
        context = {"specie": species, "chromosome": chromosome, "list_chromo": list_chromo}
        contents = get_contents("chromo_length.html", context)
    except (KeyError, ValueError, IndexError):
        status, contents = error_html()
    return status, contents


def gene_seq(gene):
    endpoint = f"/sequence/id/{HUMAN_GENES[gene]}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        bases = data['seq']
        context = {"gene": gene, "bases": bases}
        contents = get_contents("gene_seq.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents


def gene_info(gene):
    endpoint = f"/sequence/id/{HUMAN_GENES[gene]}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        id = data['id']
        seq = data['seq']
        desc = data['desc'].split(':')
        chrom_name = desc[1]
        start = int(desc[3])
        end = int(desc[4])
        context = {"gene": gene, "start": start, "end": end, "id": id, "length": len(seq), "chromosome_name": chrom_name}
        contents = get_contents("gene_info.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents


def gene_calc(gene):
    endpoint = f"/sequence/id/{HUMAN_GENES[gene]}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        seq = data['seq']
        length = len(seq)
        bases_percent = {"A": 0, "T": 0, "C": 0, "G": 0}
        for base in bases_percent.keys():
            bases_percent[base] = round(seq.count(base) * 100 / len(seq), 2)
        context = {"gene": gene, "length": length, "bases_percent": bases_percent}
        contents = get_contents("gene_calc.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents


def gene_list(chromosome, start, end):
    endpoint = f"/phenotype/region/homo_sapiens/{chromosome}:{start}-{end}"
    arg = '?content-type=application/json'
    status, data, contents = get_response(endpoint, arg)
    try:
        associated_genes = []
        for d in data:
            if "phenotype_associations" in d:
                pheno = d["phenotype_associations"]
                for p in pheno:
                    if "attributes" in p:
                        attributes = p["attributes"]
                        for a in attributes.keys():
                            if a == "associated_gene":
                                a = attributes["associated_gene"]
                                associated_genes.append(a)
        empty_list_error = associated_genes[0]
        context = {"chromo": chromosome, "associated_genes": associated_genes}
        contents = get_contents("gene_list.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents
