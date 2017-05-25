import click
import json
import yaml
from bs4 import BeautifulSoup
import urllib


def get_specs(make, model, style, trim):
    url = 'http://www.caranddriver.com/{make}/{model}/specs/2018/{style}/{trim}'.format(
        **{'make': make, 'model': model, 'style': style, 'trim': trim})

    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    specs = soup.find_all("cd-specs")

    top_divs = specs[0].section.find_all("div", recursive=False)[1].div.find_all("div", recursive=False)
    selects = top_divs[0].find_all("select")

    style_value = selects[0].attrs['value']
    style = selects[0].find("option", value=style_value).string.strip()

    trim_value = selects[1].attrs['value']
    trim = selects[1].find("option", value=trim_value).string.strip()

    details = {
        "make": make,
        "model": model,
        "style": style,
        "trim":  trim,
        "price": top_divs[1].div.p.string
    }

    specifications_table = specs[0].section.find(id="specifications").find_parents("table")[0]

    def filter_spec_rows(tag):
        return ((tag.name == 'tr') and len(tag.find_all('td', recursive=False)) == 2)

    spec_rows = specifications_table.find_all(filter_spec_rows)

    for row in spec_rows:
        children = row.findChildren("td")
        details[children[0].string] = children[1].string
    return details


def get_styles(make, model):
    url = 'http://www.caranddriver.com/{make}/{model}/specs/'.format(
        **{'make': make, 'model': model})

    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    options = soup.find(id="selectStyle").find_all("option")
    styles = []
    for o in options:
        styles.append(o.attrs["value"])
    return styles


def get_trims(make, model, style):
    url = 'http://www.caranddriver.com/{make}/{model}/specs/2018/{style}/'.format(
        **{'make': make, 'model': model, 'style': style})

    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "html.parser")
    options = soup.find(id="selectTrim").find_all("option")
    trims = {}
    for o in options:
        trims[o.string.strip()] = o.attrs["value"]
    return trims


@click.command()
@click.argument('make', required=True)
@click.argument('model', required=True)
@click.argument('style', required=False)
@click.argument('trim', required=False)
@click.option('--listfields', is_flag=True, help='Show a list of all fields instead of the full specs')
@click.option('--usefields', help='Use only the fields listed in the provide file which contains a JSON list')
def main(make, model, style, trim, listfields, usefields):

    if(make and model and style and trim):
        specs = get_specs(make, model, style, trim)
        if(usefields):
            data = open(usefields).read()
            fields = json.loads(data)
            newspecs = {}
            for field in fields:
                try:
                    newspecs[field] = specs[field]
                except KeyError:
                    newspecs[field] = None
            specs = newspecs
        if(listfields):
            print json.dumps(sorted(specs.keys()), indent=4)
        else:
            print json.dumps(specs, sort_keys=True, indent=2)
    elif(make and model and style):
        trims = get_trims(make, model, style)
        print yaml.safe_dump(trims, default_flow_style=False)
    elif(make and model):
        styles = get_styles(make, model)
        print yaml.safe_dump(styles, default_flow_style=False)
    else:
        print "missing params"
        return -1
