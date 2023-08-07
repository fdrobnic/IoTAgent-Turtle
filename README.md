<div id="top"></div>

# IoTAgent-Turtle

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
    <img src="images/logo.png" alt="Logo" width="280" height="160">
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



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

A SDMX in RDF Turtle 1.1 format parser to generate valid JSON-LD and send to FIWARE Context Brokers using ETSI NGSI-LD.

It is based on a [EBNF LALR(1) grammar](./grammar/grammar.lark).

This project is part of INTERSTAT. For more information about the INTERSTAT Project, please check the url 
https://cef-interstat.eu.


<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

This project has been built using the following python libraries:

* Lark, a parsing library for python
* docopt, command-line interface description language
* FastAPI, is high-performance web framework for building APIs with Python 3.6+ based on standard Python type hints.
* Secure, a lightweight package that adds optional security headers for Python web frameworks.
* Schema, a python library for validating Python data structures.
* Uvicorn, an Asynchronous Server Gateway Interface (ASGI) web server implementation for Python.
* Requests, an HTTP library for Python.
* Python-Multipart, a streaming multipart parser for Python.
* loguru, a library which aims to bring detailed logging in Python.

For more details about the versions of each library, please refer to [requirements.txt](requirements.txt).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This section explains the different steps that we need to do in order to start using this agent.

### Prerequisites

The following software must be installed:

- Python 3.10
- pip 22.3 (python 3.10)
- virtualenv 20.13.1

This is an example of how to list things you need to use the software and how to install them.

* python, follow the recommendations for your own OS in [Python/Downloads](https://www.python.org/downloads)
* pip, usually, it is automatically installed if you installed python in the previous steps. If you had already 
  installed a python version, but you have no pip follow the instructions for your own OS in 
  [installation pip](https://pip.pypa.io/en/stable/installation).
* virtualenv, is a tool to create isolated Python environments, you can use other available options, but it is 
  recommended to use one. You can follow the instructions to install it in your OS in 
  [Installation virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

### Installation

The recommended installation method is using a virtualenv. Actually, the installation 
process is only about the python dependencies. By default, the service configuration
follow the description of the [local configuration file](./common/config.json). You 
have to modify the `broker` attribute to specify any other location of the FIWARE Context
Broker LD.

1. Clone the repo
   ```bash
   git clone https://github.com/flopezag/IoTAgent-Turtle.git
   ```
2. Define the configuration file: `./common/config.json`
3. Create the virtualenv
   ```bash
   virtualenv -ppython3.9 .env
   ```
4. Activate the python environment
   ```bash
   source .env/bin/activate
   ```
5. Install the requirements 
   ```bash
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos 
work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Increase Unit Tests of the code
- [ ] Cover several examples of use of the component
- [ ] Testing deployment in Kubernetes Clusters
- [ ] Improve Error Messages

See the [open issues](https://github.com/flopezag/IoTAgent-Turtle/issues) for a full list of proposed features 
(and known issues).

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

Distributed under the Apache2.0 License. See `LICENSE` for more information.

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
