def get_id(gene):
    endpoint = '/homology/symbol/human/'
    arg = f'{gene}?content-type=application/json'
    valid = True
    id = None
    status, data, contents = get_response(endpoint, arg)
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
        status, data, contents = get_response(endpoint, arg)
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
        status, data, contents = get_response(endpoint, arg)
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
        status, data, contents = get_response(endpoint, arg)
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
    status, data, contents = get_response(endpoint, arg)
    try:
        context = {"data": data}
        contents = cont("gene_list.html", context)
    except KeyError:
        status, contents = error_html()
    return status, contents
