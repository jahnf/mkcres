/* mkcres example-01%
 * resources in a minimal example that can list its included resources
 * Visit https://github.com/jahnf/mkcres for more details
 */
#include "cresource.h"
#include <stdio.h>
#include <stdlib.h>

static int save_resource_to_file(const char *res_name, const char *filename) 
{
    FILE *fp;
    cresource_t *res = get_cresource(res_name);
    if(res == NULL) {
        printf("Resource '%s' not found.\n", res_name);
        return EXIT_FAILURE;
    }
    
    printf("Resource '%s' found (%lu bytes)\n", res_name, res->size);

    fp=fopen(filename, "wb");
    if(fp == NULL) {
        printf("Cannot write to file '%s'\n", filename);
        return EXIT_FAILURE;
    }
    
    size_t written = fwrite(res->data, sizeof(unsigned char), res->size, fp);
    if(written != res->size) {
        printf("Error writing to file. Could only write %lu bytes.\n", written);
        return EXIT_FAILURE;
    }
    fclose(fp);
    printf("Saved to '%s' (%lu bytes)\n", filename, written);
    return EXIT_SUCCESS;
}


int main (int argc, char **argv) 
{
    /* usage: executable resource output_file */
    if(argc == 3) exit(save_resource_to_file(argv[1],argv[2]));

    /* Check all files from test_resources1.json */
    const char* filenames[] = { "images/linux_logo.jpg",
                                "images/tux.jpg",
                                "data-files/FILE01",
                                "data-files/FILE02",
                                "data-files/FILE03", NULL };
                                
    int i =0;                            
    for( ; filenames[i] != NULL; ++i) {
        const char filename[] = "data-files/FILE01";
        cresource_t *res = get_cresource(filenames[i]);
        if(res) {
            printf("%s found (%lu bytes)\n", filenames[i], res->size);
        } else {
            printf("%s not found.\n", filenames[i]);
            exit(EXIT_FAILURE);
        }
    }
    
    printf("\n=== List all resources:\n");
    
    /* List all embedded resources */
    cresource_collection_t *c = get_cresources();
    if( c ) {
        cresource_prefix_t **p = (cresource_prefix_t**)c->prefix_sections;
        for( ; p && *p; ++p) {
            cresource_t **r = (cresource_t**)(*p)->resources;
            for( ; r && *r; ++r ) {
                printf("%s%s (%lu bytes)\n", (*p)->prefix, (*r)->name, (*r)->size);
            } 
        } 
    } 

    return 0;
}
