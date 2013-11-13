/* mkcres example-01
 * resources in a minimal example that can list its included resources
 */
#include "cresource.h"
#include <stdio.h>

int main (int argc, char **argv) 
{
    /* List all embedded resources */
    cresource_collection_t *c = get_cresources();
    if( c ) {
        cresource_prefix_t **p = (cresource_prefix_t**)c->prefix_sections;
        for( ; p && *p; ++p) {
            printf("prefix: %s\n", (*p)->prefix);
            cresource_t **r = (cresource_t**)(*p)->resources;
            for( ; r && *r; ++r ) {
                printf(" - %s\n", (*r)->name);
            } 
        }
    }

    return 0;
}
