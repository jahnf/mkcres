/* mkcres example-02
 * resources in a minimal example that can list its included resources
 * Visit https://github.com/jahnf/mkcres for more details
 */
#include "cresource.h"
#include <stdio.h>

int main (int argc, char **argv) 
{
    /* Get a single resource file by name */
    {
        const char filename[] = "images/tux.jpg";
        cresource_t *res = get_cresource(filename);
        if(res) {
            printf("%s found (%lu bytes)\n", filename, res->size);
        } else {
            printf("%s not found.\n", filename);
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
