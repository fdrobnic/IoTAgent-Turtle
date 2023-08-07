<div id="top"></div>

# SDMX to JSON-LD Parser

<!-- PROJECT SHIELDS -->
[![Stable Version][version-shield]][version-url]
[![Issues][issues-shield]][issues-url]
[![Apache2.0 License][license-shield]][license-url]
[![Python Versions][python-shield]][python-url]
[![Package Status][package-shield]][package-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/flopezag/IoTAgent-Turtle">
    <img src="https://raw.githubusercontent.com/flopezag/IoTAgent-Turtle/master/images/logo.png" 
alt="Logo" width="280" height="160">
  </a>

<h3 align="center">SDMX (Turtle) to NGSI-LD (JSON-LD) converter</h3>

  <p align="center">
    A SDMX to JSON-LD parser to communicate with FIWARE Context Brokers using ETSI NGSI-LD.
    <br />
    <a href="https://github.com/flopezag/IoTAgent-Turtle"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/flopezag/IoTAgent-Turtle">View Demo</a>
    ·
    <a href="https://github.com/flopezag/IoTAgent-Turtle/issues">Report Bug</a>
    ·
    <a href="https://github.com/flopezag/IoTAgent-Turtle/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

A SDMX in RDF Turtle 1.1 format parser to generate valid JSON-LD and send to FIWARE Context Brokers using ETSI NGSI-LD.

It is based on a 
[EBNF LALR(1) grammar](https://github.com/flopezag/IoTAgent-Turtle/blob/master/sdmx2jsonld/grammar/grammar.lark).

This project is part of INTERSTAT. For more information about the INTERSTAT Project, please check the url 
https://cef-interstat.eu.


<p align="right">(<a href="#top">back to top</a>)</p>


### Dependencies

The dependencies of the sdmx2jsonld python package are the following:

* [Lark - a modern general-purpose parsing library for Python](https://lark-parser.readthedocs.io/en/latest).
* [hi-dateinfer - a python library to infer date format from examples](https://github.com/hi-primus/hi-dateinfer).
* [Loguru - a library which aims to bring enjoyable logging in Python](https://loguru.readthedocs.io/en/stable/index.html).
* [Requests - an elegant and simple HTTP library for Python, built for human beings](https://requests.readthedocs.io).
* [RDFLib - a pure Python package for working with RDF](https://rdflib.readthedocs.io).

For more details about the versions of each library, please refer to 
[requirements.txt](https://github.com/flopezag/IoTAgent-Turtle/blob/master/requirements.txt).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Installing SDMX2JSON-LD and Supported Versions
SDMX2JSON-LD is available on PyPI:

```bash
$ python -m pip install sdmx2jsonld
```

SDMX2JSON-LD officially supports Python 3.10+.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To execute the python module you can follow the following code to parse the RDF Turtle file to generate the JSON-LD 
content to be sent to the FIWARE Context Broker:

```python
from sdmx2jsonld.transform.parser import Parser
from sdmx2jsonld.exceptions import UnexpectedEOF, UnexpectedInput, UnexpectedToken

file_in = open("structures-accounts.ttl")
generate_files = True

# Start parsing the file
my_parser = Parser()

try:
    my_parser.parsing(content=file_in, out=generate_files)
except UnexpectedToken as e:
    print(e)
except UnexpectedInput as e:
    print(e)
except UnexpectedEOF as e:
    print(e)
```

Where:
* `file_in` is the RDF Turtle content that can be a string in StringIO class or a read file in TextIOWrapper class.
* `file_out` is a boolean variable to indicate if we want to save the JSON-LD parser content into files (True) or we 
want to show the content in the screen (False).

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. 
Any contributions you make are **greatly appreciated**. If you have a suggestion that would make this better, 
please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Fernando López - [@flopezaguilar](https://twitter.com/flopezaguilar) - fernando.lopez@fiware.org

Project Link: [https://github.com/flopezag/IoTAgent-Turtle](https://github.com/flopezag/IoTAgent-Turtle)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the Apache2.0 License. See [LICENSE](https://github.com/flopezag/IoTAgent-Turtle/blob/master/LICENSE) 
for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/flopezag/IoTAgent-Turtle.svg?style=flat
[issues-url]: https://github.com/flopezag/IoTAgent-Turtle/issues

[license-shield]: https://img.shields.io/github/license/flopezag/IoTAgent-Turtle
[license-url]: https://github.com/flopezag/IoTAgent-Turtle/blob/master/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/fernandolopezaguilar

[python-shield]: https://img.shields.io/pypi/pyversions/sdmx2json-ld
[python-url]: https://pypi.org/project/sdmx2json-ld

[version-shield]: https://img.shields.io/pypi/v/sdmx2json-ld
[version-url]: https://pypi.org/project/sdmx2json-ld/#history

[package-shield]: https://img.shields.io/pypi/status/sdmx2json-ld
[package-url]: https://pypi.org/project/sdmx2json-ld
