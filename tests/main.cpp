/* mkcres example-01
 * resources in a minimal example that can list its included resources
 * Visit https://github.com/jahnf/mkcres for more details
 */
#include "cresource.h"
#include <stdlib.h>
#include <iostream>
#include <fstream>

static int save_resource_to_file(const char *res_name, const char *filename) 
{
    cresource_t *res = get_cresource(res_name);
    if(res == NULL) {
        std::cerr << "Resource '" << res_name << "' not found." << std::endl;
        return EXIT_FAILURE;
    }
    
    std::cout << "Resource '" << res_name << "' found (" << res->size << " bytes)" << std::endl;

    std::ofstream outfile(filename, std::ofstream::binary);
    if(!outfile) {
        std::cerr << "Cannot write to file '" << filename << "" << std::endl;
        return EXIT_FAILURE;
    }
    
    outfile.write(reinterpret_cast<const char*>(res->data),res->size);
    outfile.close();

    std::cout << "Saved to '" << filename << "'" << std::endl;
    return EXIT_SUCCESS;
}

int main (int argc, char **argv) 
{
    /* usage: executable resource output_file */
    if(argc == 3) exit(save_resource_to_file(argv[1],argv[2]));


    /* Check all files from test_resources1.json */
    const char* filenames[] = { "images/linux_logo.jpg",
                                "images/tux.jpg", "images/penguin.jpg",
                                "source-main.cpp", "source-main.c",
                                "data-files/FILE01",
                                "data-files/FILE02",
                                "data-files/FILE03", NULL };
                                
    int i =0;                            
    for( ; filenames[i] != NULL; ++i) {
        const char filename[] = "data-files/FILE01";
        cresource_t *res = get_cresource(filenames[i]);
        if(res) {
            std::cout << filenames[i] << " found (" << res->size << " bytes)" << std::endl;
        } else {
            std::cerr << filenames[i] << " not found." << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    
    std::cout << std::endl << "=== List all resources:" << std::endl;
    
    /* List all embedded resources */
    cresource_collection_t *c = get_cresources();
    if( c ) {
        cresource_prefix_t **p = (cresource_prefix_t**)c->prefix_sections;
        for( ; p && *p; ++p) {
            cresource_t **r = (cresource_t**)(*p)->resources;
            for( ; r && *r; ++r ) {
                std::cout << (*p)->prefix << (*r)->name << " (" 
                          << (*r)->size << " bytes)" << std::endl;
            } 
        } 
    } 

    return 0;
}
