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
date of a file changes.

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

- [ ] TODO: Describe how to use within CMake with mkcres.cmake

Dependencies
------------
mkcres needs Python 2 version 2.7 or higher since it currently uses the argparse library.

License
-------
See [LICENSE](https://github.com/jahnf/mkcres/blob/master/LICENSE).
