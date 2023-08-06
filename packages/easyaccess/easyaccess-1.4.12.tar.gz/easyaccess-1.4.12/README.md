# easyaccess 

**easyaccess**: an enhanced command line SQL interpreter client for astronomical surveys.

**Jump to:**

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [FAQ](#faq)
       
<img src="data/help.gif" alt="help_screen" style="width: 70%; margin: auto;">

## Description

`easyaccess` is an enhanced command line interpreter and Python package created to facilitate access to astronomical catalogs stored in SQL Databases. It provides a custom interface with custom commands and was specifically designed to access data from the Dark Energy Survey Oracle database, including autocompletion of tables, columns, users and commands, simple ways to upload and download tables using csv, fits and HDF5 formats, iterators, search and description of tables among others. It can easily be extended to another surveys or SQL databases. The package was completely written in Python and support customized addition of commands and functionalities.

For a short tutorial check [here](https://des.ncsa.illinois.edu/desaccess/docs/easyaccess).

## DES DR1/DR2 access quickstart

To access the DES public data releases, you first need an account, which you can register yourself [here](https://des.ncsa.illinois.edu/desaccess). Once you have login credentials for the public DES data server, you can start `easyaccess` with:

```bash
easyaccess -s desdr
```

## Features

- Nice output format (using pandas)
- Very flexible configuration
- Smart tab autocompletion for commands, table names, column names, and file paths
- Write output results to CSV, TAB, FITS, or HDF5 files
- Load tables from CSV, FITS or HDF5 files directly into DB (memory friendly by using number of rows or memory limit)
- Intrinsic DB commands to describe tables, schema, quota, and more
- easyaccess can be imported as module from Python with a complete Python API
- Run commands directly from command line
- Load SQL queries from a file and/or from the editor
- Show the execution plan of a query if needed
- Python functions can be run in a inline query

## FAQ

We have a running list of [FAQ](FAQ.md) which we will constantly update, please check [here](FAQ.md).

## Contributing

Please take a look at our [Code of Conduct](CODE_OF_CONDUCT.md) and our [contribution guide](CONTRIBUTING.md).

## Citation

If you use `easyaccess` in your research, we encourage you to use this reference [https://arxiv.org/abs/1810.02721](https://arxiv.org/abs/1810.02721) or copy/paste this BibTeX:

```bibtex
@ARTICLE{2018arXiv181002721C,
       author = {{Carrasco Kind}, M. and {Drlica-Wagner}, A. and {Koziol}, A.~M.~G. and
        {Petravick}, D.},
        title = "{easyaccess: Enhanced SQL command line interpreter for astronomical surveys}",
      journal = {arXiv e-prints},
     keywords = {Astrophysics - Instrumentation and Methods for Astrophysics},
         year = 2018,
        month = Oct,
          eid = {arXiv:1810.02721},
        pages = {arXiv:1810.02721},
archivePrefix = {arXiv},
       eprint = {1810.02721},
 primaryClass = {astro-ph.IM},
       adsurl = {https://ui.adsabs.harvard.edu/\#abs/2018arXiv181002721C},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

See also: Carrasco Kind et al., (2019). *easyaccess: Enhanced SQL command line interpreter for astronomical surveys*. **Journal of Open Source Software**, 4(33), 1022, https://doi.org/10.21105/joss.01022

## Installation

Installing `easyaccess` can be a little bit tricky given the external libraries required, in particular the Oracle libraries which are free to use. If you are primarily interested in *using* the `easyaccess` client, we recommend running the Docker image as described below.

### Docker

Running `easyaccess` in Docker is easy. Execute the command below to download and run our published image.

```bash
$ docker run -it --rm \
    registry.gitlab.com/des-labs/kubernetes/easyaccess:latest \
    easyaccess -s desdr

Enter username : 
Enter password : 
Connecting to DB ** desdr ** ...
Loading metadata into cache...
     _______      
     \      \      
  // / .    .\    
 // /   .    _\   
// /  .     / // 
\\ \     . / //  
 \\ \_____/ //   
  \\_______//    DARK ENERGY SURVEY
   `-------`     DATA MANAGEMENT

easyaccess 1.4.12. The DESDM Database shell.
_________
DESDR ~> SELECT RA, DEC, MAG_AUTO_G, TILENAME FROM DR2_MAIN sample(0.001) FETCH FIRST 5 ROWS ONLY ;

         RA        DEC  MAG_AUTO_G      TILENAME
1  8.236249 -24.021460   24.450422  DES0032-2415
2  8.084798 -25.715401   26.279263  DES0033-2541
3  8.142266 -35.854926   26.509785  DES0032-3540
4  8.197418 -48.274010   25.243387  DES0030-4831
5  8.107404 -26.313876   24.758778  DES0032-2623
```

Alternatively, you may build and run the image yourself using the included Dockerfile with the commands:

```bash
docker build -t des-easyaccess .
docker run -it --rm des-easyaccess easyaccess -s desdr
```

### Source Installation

`easyaccess` is based heavily on the Oracle python client `cx_Oracle`, you can follow the installation instructions from [here](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#quick-start-cx-oracle-installation). For `cx_Oracle` to work, you will need the Oracle Instant Client packages which can be obtained from [here](https://www.oracle.com/technetwork/database/database-technologies/instant-client/overview/index.html).

Make sure you have these libraries installed before proceeding to the installation of easyaccess, you can try by opening a Python interpreter and type:

```python
import cx_Oracle
```

If you have issues, please check the [Troubleshooting page](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#troubleshooting) or our [FAQ page](FAQ.md).

You can clone this repository and install `easyaccess` with:

```bash
python setup.py install
```

#### Requirements

- [Oracle Client](https://www.oracle.com/technetwork/database/database-technologies/instant-client/overview/index.html) > 11g.2 (External library, no python)
  Check [here](https://www.oracle.com/technetwork/database/database-technologies/instant-client/overview/index.html) for instructions on how to install these libraries
- [cx_Oracle](https://cx-oracle.readthedocs.io/en/latest/index.html)
  - Note that cx_Oracle needs libaio on some Linux systems
  - Note that cx_Oracle needs libbz2 on some Linux systems
- See the `setup.py` file for additional requirements.

## Usage

For a short tutorial and documentation see [here](https://des.ncsa.illinois.edu/desaccess/docs/easyaccess). Note that not all the features are available for public database use.

### Interactive interpreter

Assuming that ```easyaccess``` is in your path, you can enter the interactive interpreter by calling ```easyaccess``` without any command line arguments:

```bash
easyaccess
```

### Command line usage

Much of the functionality provided through the interpreter is also available directly from the command line. To see a list of command-line options, use the ```--help``` option

```bash
easyaccess --help
```

### Running SQL commands

Once inside the interpreter run SQL queries by adding a ";" at the end::

```bash
DESDB ~> select ... from ... where ... ;
```

To save the results into a table add ">" after the end of the query (after ";") and namefile at the end of line

```bash
DESDB ~> select ... from ... where ... ; > test.fits
```

The file types supported so far are: .csv, .tab, .fits, and .h5. Any other extension is ignored.

### Load tables

To load a table it needs to be in a csv format with columns names in the first row
the name of the table is taken from filename or with optional argument --tablename

```bash
DESDB ~> load_table <filename> --tablename <mytable> --chunksize <number of rows to read/upload> --memsize <memory in MB to read at a time>
```

The `--chunsize` and `--memsize` are optional arguments to facilitate uploading big files.

### Load SQL queries

To load SQL queries just run:

```bash
DESDB ~> loadsql <filename.sql>
```
or

```bash
DESDB ~> @filename.sql
```

The query format is the same as the interpreter, SQL statement must end with `;` and to write output files the query must be followed by a standard output redirect `command > outfile`

## Configuration

The configuration file is located at ```$HOME/.easyaccess/config.ini``` but everything can be configured from inside easyaccess type:

```bash
DESDB ~> help config
```

to see the meanings of all the options, and:

```bash
DESDB ~> config all show
```

to see the current values, to modify one value, e.g., the prefetch value

```bash
DESDB ~> config prefetch set 50000
```

and to see any particular option (e.g., timeout):

```bash
DESDB ~> config timeout show
```

## Architecture

We have included a simplified UML diagram describing the architecture and dependencies of `easyaccess` which shows only the different methods for a given class and the name of the file hosting a given class. The main class, `easy_or()`, inherits all methods from all different subclasses, making this model flexible and extendable to other surveys or databases. These methods are then converted to command line commands and functions that can be called inside `easyaccess`. Given that there are some DES specific functions, we have moved DES methods into a separate class `DesActions()`.

![`easyaccess` architecture diagram](paper/classes_simple.png)
