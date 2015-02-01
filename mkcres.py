#!/usr/bin/python2

# mkcres.py - mkcres is a Python tool for generating and maintaining C/C++ 
# resource files that can be embedded in a program. mkcres comes with a python 
# comand line tool and also a header and source for easy access to the embedded 
# resources within the program.
# ------------------------------------------------------------------------------ 
# The MIT License (MIT)
#
# Copyright (c) 2013 Jahn Fuchs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------

# Example JSON configuration file:
##################################
# { 
#   "CRES": [
#     {
#       "prefix": "icons/",
#       "files": [
#         { "name": "img/app32x32.png" },
#         { "name": "x.png", "alias": "img/exit.png" }
#      ]
#     }, 
#     {
#       "prefix": "other_stuff/",
#       "files": [
#         { "name": "encryption_key_v1.pub", "alias": "key.pub" },
#         { "name": "lookup.sqlite" }
#       ]
#     
#     }
#   ]
# }

import sys, os, textwrap, json
import filecmp
import argparse  # needs Python version 2.7 or higher
import hashlib
import binascii

SCRIPT_VERSION = "0.2"
OUT_FILENAME = "CRES.out"
OUT_SOURCENAME = 'cres.c'
CRES_KEY = 'CRES'
CRES_CRESOURCE_TYPE = 'cresource_t'
CRES_CPREFIX_TYPE = 'cresource_prefix_t'
CRES_CCOLL_TYPE = 'cresource_collection_t'
CRES_CRESOURCE_VAR = '___cres_resources'

def bytes_from_file(infile, chunksize=8192):
    while True:
        chunk = infile.read(chunksize)
        if len(chunk):
            yield chunk
        else:
            break

def error_and_exit(reason):
    sys.stderr.write(reason + '\n')
    exit(1)

def write_c_source(infile, outfile_config, out_basedir):
    global CRES_CRESOURCE_TYPE
    
    if not 'c_src' in outfile_config or outfile_config['c_src'] == "":
        hashname = hashlib.sha1()
        hashname.update(outfile_config['abspath'].encode('utf-8'))
        outfile_config['c_src'] = '__' + hashname.hexdigest() + '.c'    
    
    if not 'c_data_var' in outfile_config or outfile_config['c_data_var'] == "":
        outfile_config['c_data_var'] = "___cres_data" + os.path.splitext(os.path.basename(outfile_config['c_src']))[0];
    
    try:
        outfile = open(os.path.join(out_basedir, outfile_config['c_src']), 'w+')
    except:
        error_and_exit("Could not write c resource file.")
        
    outfile.write("/* auto generated CRES source */\n")
    outfile.write("/* {} */\n".format(outfile_config['abspath']))
    outfile.write("const unsigned char const {}[] = {{\n".format(outfile_config['c_data_var']))
    
    read_len = 0
    if outfile_config['size'] == 0:
        outfile.write("\t\"\"\n")
    else:
        for bindata in bytes_from_file(infile,20):
            read_len += len(bindata)
            s=binascii.b2a_hex(bindata).upper().decode('utf-8')
#            print(s)
#            print("".join(["\\x"+x+y for (x,y) in zip(s[0::2], s[1::2])]))
            outfile.write("\t\"" + "".join(["\\x"+x+y for (x,y) in zip(s[0::2], s[1::2])]) + "\"\n")
    
    outfile.write("};")
    outfile.truncate()
    outfile.close()

def write_c_main_source(config):
    global OUT_SOURCENAME
    temp_varlist = []
    for p in config[CRES_KEY]:
        for f in p['files']:
            if not f['c_data_var'] in temp_varlist:
                temp_varlist.append(f['c_data_var'])
                
    try:
        outfile = open(os.path.join(config['outdir'], OUT_SOURCENAME), 'w+')
    except:
        error_and_exit("Could not write c resource file.")
    
    outfile.write("/* auto generated CRES source */\n")
    outfile.write("#include \"cresource.h\"\n\n")
    for var in temp_varlist:
        outfile.write("extern const unsigned char {}[];\n".format(var))

    file_count = 0
    for p in config[CRES_KEY]:
        for f in p['files']:
            c_resource_name = f['name_out'].replace('"', '\\"')
            f['c_var'] = "___cres_resfile_n{}".format(file_count)
            outfile.write("\nstatic {} {} = {{\n".format(CRES_CRESOURCE_TYPE, f['c_var']))
            outfile.write("\t\"{}\", /* filename */\n".format(c_resource_name))
            outfile.write("\t{}, /* filesize */\n".format(f['size']))
            outfile.write("\t{} /* data */\n".format(f['c_data_var']))
            outfile.write("};\n")
            file_count = file_count +1

    prefix_count = 0
    prefix_varlist = []
    for p in config[CRES_KEY]:
        if len(p['files']) == 0:
            continue  
        escaped = p['prefix'].replace('"', '\\"')
        prefix_var = "___cres_prefix_n{}".format(prefix_count)
        outfile.write("\nstatic {0} {1} = {{\n".format(CRES_CPREFIX_TYPE, prefix_var))
        outfile.write("\t\"{0}\", /* prefix */\n".format(escaped))
        outfile.write("\t{0}, /* prefix len */\n".format(len(escaped)))
        outfile.write("\t{0}, /* number of resources */\n\t{{ /* file list */\n".format(len(p['files'])))
        for f in p['files']:
            outfile.write("\t\t&{0},\n".format(f['c_var']))
        outfile.write("\t\t0\n\t}\n};\n")
        prefix_varlist.append(prefix_var)
        prefix_count = prefix_count + 1
    
    outfile.write("\nstatic {0} {1} = {{\n".format(CRES_CCOLL_TYPE, CRES_CRESOURCE_VAR))
    outfile.write("\t{0}, /* number of prefix sections */\n\t{{ /* prefix sections */\n".format(len(prefix_varlist)))
    for p in prefix_varlist:
        outfile.write("\t\t&{0},\n".format(p))
    outfile.write("\t\t0\n\t}\n};\n")
    outfile.write("\n{0}* get_cresources() {{ return &{1}; }}".format(CRES_CCOLL_TYPE, CRES_CRESOURCE_VAR))
    
    outfile.truncate()
    outfile.close()
    return

def add_resource(args, prefix, fileconf, origin_in, outconf):
    if not 'name' in fileconf: return 0
    abspath = os.path.join(os.path.abspath(os.path.dirname(origin_in)), fileconf['name'])
    try:
        infile_mtime = os.path.getmtime(abspath)
        infile_size = os.path.getsize(abspath)
        infile = open(abspath, 'rb')
    except:
        error_and_exit("prefix: " + prefix + "\nCould not open: " + abspath);

    found_prefix = False
    for out_pre in outconf[CRES_KEY]:
        if 'prefix' in out_pre:
            if out_pre['prefix'] == prefix:
                if not 'files' in out_pre:
                    out_pre['files'] = []
                found_prefix = True
                break

    if not found_prefix:
        out_pre = {'prefix': prefix, 'files': []}
        outconf[CRES_KEY].append(out_pre)

    if 'alias' in fileconf:
        name_out = fileconf['alias']
    else:
        name_out = fileconf['name']

    found_file = False
    found_data_file = False
    df = {'abspath': abspath, 'mtime': 0.0, 'size': 0}
    of = {'abspath': abspath, 'mtime': 0.0, 'size': 0}
    for p in outconf[CRES_KEY]:
        for f in p['files']:
            if 'abspath' in f:
                if f['abspath'] == abspath:
                    if not 'mtime' in f: f['mtime'] = 0.0
                    if not 'size' in f: f['size'] = 0
                    found_data_file = True
                    df = f
                    if (found_prefix and 'prefix' in p and p['prefix'] == prefix  
                        and 'name_out' in f and f['name_out'] == name_out):
                        found_file = True
                        of = f
                    
    if not found_file:
        if found_data_file and of != df:
            of['c_data_var'] = df['c_data_var']
            of['c_src'] = df['c_src']
            of['mtime'] = df['mtime']
            of['size'] = df['size']
        out_pre['files'].append(of)
    
    if (not found_data_file or not found_file or not 'name_out' in of or
        ('name_out' in of and of['name_out'] != name_out)):
        changes = True
    else: 
        changes = False

    of['name_out'] = name_out
    of['origin_config'] = origin_in
    csrc_missing = False
    if ('c_src' in of and not
        os.path.exists(os.path.join(outconf['outdir'], of['c_src']))):
        csrc_missing = True
    
    if of['mtime'] != infile_mtime or of['size'] != infile_size or csrc_missing:
        changes = True
        if not args.quiet: print("Updating/Creating sources for file: " + abspath)
        of['mtime'] = infile_mtime
        of['size'] = infile_size
        write_c_source(infile, of, outconf['outdir'])
        # update all other resources that use the same binary data
        for p in outconf[CRES_KEY]:
            for f in p['files']:
                if f != of and of['c_src'] == f['c_src']:
                    f['mtime'] = of['mtime']
                    f['size'] = of['size']
    
    infile.close()
    return 1 if changes else 0

def is_src_in_config(src_filename, config):
    for p in config[CRES_KEY]:
        for f in p['files']:
            if 'c_src' in f and f['c_src'] == src_filename:
                return True
    return False

def create(args):
    if args.outdir:
        res_outdir = args.outdir
    else:
        res_outdir = os.getcwd()

    # make sure the output directory exists, if not create it
    if not os.path.exists(res_outdir):
        try:
            os.makedirs(res_outdir)
        except:
            error_and_exit("Could not create output directory '{0}'.".format(res_outdir))

    # Open or create CRES intermediate output file
    # The CRES output file keeps track of timestamps and mappings of resource files
    # to C source files. This enables incremental updates for changed files only. 
    if not os.path.exists(os.path.join(res_outdir, OUT_FILENAME)) or args.force:
        outfile = open(os.path.join(res_outdir, OUT_FILENAME),"w+")
        cres_outconfig = { CRES_KEY : [] }
    else:
        outfile = open(os.path.join(res_outdir, OUT_FILENAME),"r+")
        try:
            cres_outconfig = json.loads(outfile.read())
        except:
            cres_outconfig = { CRES_KEY : [] }
            
        if not CRES_KEY in cres_outconfig: cres_outconfig[CRES_KEY] = []
        outfile.seek(0,0)
    
    cres_outconfig['outdir'] = os.path.abspath(res_outdir)

    of_remove_list = []
    new_entries = 0

    # for every resource configuration file, do...
    for infile in args.resfile:
        try:
            resfile_inconfig = json.loads(infile.read())
        except:
            error_and_exit("Could not parse resource file '{0}'.".format(infile.name))
            
        if not CRES_KEY in resfile_inconfig:
            error_and_exit("Not a cresource config file. Missing {0} key.".format(CRES_KEY))

        res_infile_dir = os.path.dirname(infile.name)
        res_infile_abspath = os.path.abspath(infile.name)
        res_infile_absdir = os.path.abspath(res_infile_dir)

        for p in resfile_inconfig[CRES_KEY]:
            # for every prefix section
            if not 'prefix' in p:
                p['prefix'] = ""
            if not 'files' in p:
                p['files'] = []

        # for every file in cres_outconfig check if in infile -> if not remove
        if not args.keep_missing:
            inconfig_absdir = os.path.abspath(os.path.dirname(res_infile_abspath))
            for op in cres_outconfig[CRES_KEY]:
                if not 'prefix' in op: op['prefix'] = ""
                if 'files' in op:
                    for of in op['files']:
                        if not 'abspath' in of: continue
                        if not 'origin_config' in of: continue
                        if not of['origin_config'] == res_infile_abspath: continue
                        found = False
                        for ip in resfile_inconfig[CRES_KEY]:
                           for f in ip['files']:
                                if not 'name' in f: continue
                                abspath = os.path.join(inconfig_absdir, f['name'])
                                if (of['abspath'] == abspath and op['prefix'] == ip['prefix']):
                                    if 'alias' in f: 
                                        if f['alias'] == of['name_out']: found = True
                                    elif 'name' in f and f['name'] == of['name_out']:
                                        found = True
                                    if found: break
                        
                        if not found:
                            of_remove_list.append(of)
                            op['files'].remove(of)
        
        # add resources loop
        for p in resfile_inconfig[CRES_KEY]:
            for f in p['files']:
                new_entries += add_resource(args, p['prefix'], f, res_infile_abspath, cres_outconfig)
        
    # delete orphaned source files
    for f in of_remove_list:
        if 'c_src' in f and not is_src_in_config(f['c_src'], cres_outconfig):
            abs_delpath = os.path.join(cres_outconfig['outdir'],f['c_src'])
            if os.path.exists(abs_delpath):
                if not args.quiet: print("deleting: " + f['c_src'])
                os.remove(abs_delpath)
    
    # write main source file for config
    if new_entries > 0 or len(of_remove_list) > 0:
        write_c_main_source(cres_outconfig) 
        if args.list_outfile:
            listfile_temp = args.list_outfile + ".tmp~"
            try: slfile = open(listfile_temp,'w+')
            except: error_and_exit("Cannot open:" + listfile_temp)
            write_sources_list(cres_outconfig, cres_outconfig['outdir'], slfile, cmake=args.list_cmake_prefix, absolute=True)
            slfile.truncate()
            slfile.close()

            # If list file exists, only update if it would change or --force is set
            if os.path.exists(args.list_outfile):
                if not filecmp.cmp(args.list_outfile, listfile_temp) or args.force:
                    os.remove(args.list_outfile) # otherwise os.rename will fail on Windows
                    os.rename(listfile_temp,args.list_outfile)
                else:
                    os.remove(listfile_temp)
            else:
                os.rename(listfile_temp,args.list_outfile)

    outfile.write(json.dumps(cres_outconfig, indent=2))
    outfile.truncate()
    outfile.close()
    if not args.quiet: print("OK")
    return

def listfiles(args):
    try:
        infile = open(os.path.join(args.dir, OUT_FILENAME),"r")
    except:
        error_and_exit("Cannot open: " + os.path.join(args.dir, OUT_FILENAME))
    
    try:
        config = json.loads(infile.read())
    except:
        error_and_exit("Parser error")

    infile.close()
    write_sources_list(config, args.dir, args.outfile,cmake=args.cmake_prefix,relative=args.relative,absolute=args.absolute)
    
def write_sources_list(config, outdir, outfile, cmake, relative=False, absolute=False):
    """Write a list of source files for a given configuration."""

    if not CRES_KEY in config: config[CRES_KEY] = []
    source_files = [OUT_SOURCENAME]
    for p in config[CRES_KEY]:
        if not 'prefix' in p: p['prefix'] = ""
        if not 'files' in p: p['files'] = []
        for f in p['files']:
            if 'c_src' in f and f['c_src'] not in source_files:
                source_files.append(f['c_src'])
            
    if cmake: 
        outfile.write("set(" + cmake + "_CRES_SOURCE_FILES" + '\n')
        
    for s in source_files:
        if cmake: outfile.write('\t"')
        if relative:
            outfile.write(os.path.join(os.path.relpath(os.path.abspath(outdir),os.getcwd()), s).replace('\\', '/'))
        elif absolute:
            outfile.write(os.path.join(os.path.abspath(outdir), s).replace('\\', '/'))
        else:
            outfile.write(s).replace('\\', '/')
        if cmake: outfile.write('"')
        outfile.write('\n')
        
    if cmake: outfile.write(')\n')

def main():
    global SCRIPT_VERSION
    global OUT_FILENAME
    global CRES_KEY
    parser = argparse.ArgumentParser(description='C Resource generator.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + SCRIPT_VERSION)
    subparsers = parser.add_subparsers(help='options')
    parser_a = subparsers.add_parser('create', help='Generate resource files')
    parser_a.add_argument('--outdir', help='output directory')
    parser_a.add_argument('--force', help='force rewrite, default is update mode', action='store_const', const=True)
    parser_a.add_argument('--keep-missing', help='keep missing entries in output', action='store_const', const=True)
    parser_a.add_argument('--quiet', help='no outputs', action='store_const', const=True)
    parser_a.add_argument('--list-outfile', help='', required=False)
    parser_a.add_argument('--list-cmake-prefix', help='cmake format', required=False)
    parser_a.add_argument('resfile', help='resource definition file', nargs='+', type=argparse.FileType('r'))
    parser_a.set_defaults(func=create)
    
    parser_b = subparsers.add_parser('list', help='List generated files')
    parser_b.add_argument('dir', help='output directory to scan for ' + OUT_FILENAME)
    group = parser_b.add_mutually_exclusive_group(required=True) 
    group.add_argument('--absolute', action='store_const', const=True, help='list source files with absolute path')
    group.add_argument('--relative', action='store_const', const=True, help='list source files with relative path from current working directory')
    parser_b.add_argument('--cmake-prefix', help='output for cmake', required=False)
    parser_b.add_argument('outfile',nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser_b.set_defaults(func=listfiles)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
