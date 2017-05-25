# autospecs

autospecs scrapes car specifications from "Car & Driver"


# Installation

Simply run:

    $ pip install .


# Usage

    $ autospecs --help

At the minimum, you need a make and a model.

    $ autospecs toyota camry
    - Camry-Sedan
    - Camry-Sedan-Hybrid

You need to specify the style to get a list of trims.

    $ autospecs toyota camry Camry-Sedan
    2016 Camry 4dr Sdn I4 Auto LE (Natl): '377158'
    2016 Camry 4dr Sdn I4 Auto SE (Natl): '377153'

Add the trim to get the list of specs.

    $ autospecs toyota camry Camry-Sedan 377158

You can specify a list of which specs you want output, since the full list is quite long.
To get a list of all the available specs, use the --listfields option

    $ autospecs --listfields toyota camry Camry-Sedan 377158 > myfields.json

After paring down and sorting your fields, you can pass in the filename as an option.

    $ autospecs --usefields myfields.json toyota camry Camry-Sedan 377158 > myfields.json
