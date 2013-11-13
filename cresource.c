/* mkcres 
 * https://github.com/jahnf/mkcres
 * For licensing and details see LICENSE and README.md
 */

#include "cresource.h"

#include <string.h>

cresource_t* get_cresource(const char* filename) 
{
    cresource_collection_t *c = get_cresources();
    if( c ) {
        cresource_prefix_t **p = (cresource_prefix_t**)c->prefix_sections;
        for( ; p && *p; ++p) {
            if( strncmp((*p)->prefix, filename, (*p)->prefix_len) == 0 ) {
                cresource_t **r = (cresource_t**)(*p)->resources;
                for( ; r && *r; ++r ) {
                    if( strcmp((*r)->name, &filename[(*p)->prefix_len]) == 0 )
                        return *r;
                } 
            }
        }
    }
    return 0;
}
