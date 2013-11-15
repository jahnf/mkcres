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

- [ ] TODO: Describe configuration file details

Usage
-----

### Command line

- [ ] TODO: Describe command line usage and arguments

### CMake

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

Using the `mkcres_add_library` function will automatically add additional make targets 
to your project:
* *mkcres-update*: will update the C resource files form all targets added with `mkcres_add_library`
* *mkcres-force-rewrite*: will rewrite all the C resource files completely from all targets added with `mkcres_add_library`

For a full example have a look at example-01 in the examples directory of mkcres.

##### Drawbacks with CMake

- [ ] TODO: Describe the minor drawbacks when detecting changes to the resources.

Dependencies
------------
mkcres needs Python 2 version 2.7 or higher since it currently uses the argparse library.

License
-------
See [LICENSE](https://github.com/jahnf/mkcres/blob/master/LICENSE).
