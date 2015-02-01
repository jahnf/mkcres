mkcres
======

mkcres is a Python tool for generating and maintaining C/C++ resource 
files that can be embedded in a program. mkcres comes with a python comand 
line tool and also a header and source for easy access to the embedded 
resources within the program.

Basically mkcres takes a JSON configuration file and turns it into a bunch 
of C source files that can be compiled together with your project and 
included in your build process. It also supports partial updates of the 
generated C files since mkcres only updates files if the modification 
date of a file changes. A single file can appear in the resources multiple
times under a different name but will be compiled in only once.

**Table of Contents** 

- [Usage](#usage)
  - [Configuration](#configuration)
  - [Command line options](#command-line-options)
  - [Usage in your C code](#usage-in-your-c-code)
    - [Get a resource](#get-a-resource)
    - [Loop throuh all resources]("#loop-throuh-all-resources)
  - [Integrate with CMake](#integrate-with-cmake)
    - [Drawbacks with CMake](#drawbacks-with-cmake)
  - [Integrate within a Makefile](#integrate-within-a-makefile)
- [Dependencies](#dependencies)
- [License](#license)

Usage
-----
mkcres should work with Python versions 2 and 3, but will require at least 
version 2.7 since the `argparse` is used.

### Configuration

The configuration is done in a JSON file. The file has to contain the 
`CRES` value, which is an array of prefix conigurations. A prefix
configuration can contain the `prefix` and an array of `files`.
A resource can be later found and referenced via *prefix + filename* or
*prefix + alias* if the alias for a resource file is set.
If *prefix* is not set, it will be automatically an empty string.


Here is an example JSON configuration file:

``` json
{ 
  "CRES": [
    {
      "prefix": "icons/",
      "files": [
        { "name": "img/app32x32.png" },
        { "name": "x.png", "alias": "img/exit.png" }
      ]
    }, 
    {
      "prefix": "other_stuff/",
      "files": [
        { "name": "encryption_key_v1.pub", "alias": "key.pub" },
        { "name": "lookup.sqlite" }
      ]
    }
  ]
}
```

### Command line options

- [ ] *TODO*: Describe command line usage and arguments

### Usage in your C code

To use the resources compiled with your executable code include the 
mkcres C-header [cresource.h](cresource.h).
```c
#include "cresource.h"
```
Also have a look at the [examples](examples) in the example directory.

##### Get a resource

Use the function `get_cresource` to get a resource file:
```c
/** Get a resource with the given filename. Returns a null ptr if the resource
* was not found. */
cresource_t* get_cresource(const char* filename);
```
If the resource exists, the function will return a pointer to a `cresource_t`
struct, `null` otherwise. This is how `cresource_t` is defined:
```c
typedef const struct {
const char *name;
const unsigned long size;
const unsigned char *data;
} cresource_t;
```

##### Loop throuh all resources

*TODO*

### Integrate with CMake

For easy use within CMake files the function `mkcres_add_library(name config_file mkcres_dir)` 
of the helper script `mkcres.cmake` can be used.  Lets have a look at a simple example:

```CMake
# Assuming you have all the mkcres files in a subdirectory called 'mkcres'
# (mkcres.cmake mkcres.py cresource.c cresource.h)

include(mkcres/mkcres.cmake)
mkcres_add_library(myresources resources.json "./mkcres")

add_executable(example main.c)
target_link_libraries(example myresources)
```

Using the `mkcres_add_library` function will automatically add additional 
make targets to your project:
* *mkcres-update*: will update the C resource files form all 
  targets added with `mkcres_add_library`
* *mkcres-force-rewrite*: will rewrite all the C resource files 
  completely from all targets added with `mkcres_add_library`

For a full example have a look at the [CMake example](examples/example-cmake) 
in the examples directory.

##### Drawbacks with CMake

**run `make mkcres-update` before running `make`** when changing the 
JSON resource configuration so that resources files are added or 
removed - otherwise the first `make` call will result in an error.
*Here is why:*

Once a CMake build is configured and if the JSON configuration is changed, 
so that resources files are added or removed the first `make` call will 
result in either a linker or a CMake error. This is because CMake needs 
the full list of source files for a target (executable or library)
at configuration time. In the background mkcres.py creates another 
CMake file that will be included from mkcres.cmake. This file contains the
list of C-resource files to be compiled.

A `make` step will update the generated include file for CMake but this 
is at a point where CMake already has included the file to change and 
will only be detected from CMake with the next `make` run. Unfortunately
there is no way around this.

### Integrate within a Makefile

mkcres can be integrated with basically everywhere where Python is available.
For an integration into your Makefiles have a look at the 
[Makefile example](examples/example-make) in the examples directory.

Dependencies
------------
mkcres needs Python version 2.7 or higher since it uses the argparse library.

License
-------
See [LICENSE](https://github.com/jahnf/mkcres/blob/master/LICENSE).
