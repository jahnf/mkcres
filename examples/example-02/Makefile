# An example how you could use mkcres in a Makefile
#
# NOTE: THIS IS NOT a good example for a Makefile in general,
#       I am not a Makefile expert and it just happens to work ;)
#
#		Improvements and additions are welcome!
#       Drop me a message at https://github.com/jahnf/mkcres       

mkcres_DIR := ../..
mkcres_SCRIPT := $(mkcres_DIR)/mkcres.py
mkcres_OUTDIR := ./cresources
mkcres_CONFIG := resources.json
mkcres_CFILE := $(mkcres_DIR)/cresource.c

$(shell python2 $(mkcres_SCRIPT) create --quiet --outdir $(mkcres_OUTDIR) $(mkcres_CONFIG))
mkcres_FILES := $(shell python2 $(mkcres_SCRIPT) list --absolute $(mkcres_OUTDIR))

EXECUTABLE := example-02
SOURCES := main.c $(mkcres_CFILE) $(mkcres_FILES)

OBJECTS := $(addprefix obj/, $(notdir $(SOURCES:.c=.o)))
program_INCLUDE_DIRS := "../.."
CFLAGS += $(foreach includedir,$(program_INCLUDE_DIRS),-I$(includedir))

.PHONY: all clean clean-mkcres distclean

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $^

obj/%.o: %.c
	@mkdir -p $(dir $@)                                                        
	$(CC) $(CFLAGS) -c $< -o $@	

obj/%.o: $(mkcres_OUTDIR)/%.c
	@mkdir -p $(dir $@)                                                        
	$(CC) $(CFLAGS) -c $< -o $@	

obj/%.o: $(mkcres_DIR)/%.c
	@mkdir -p $(dir $@)                                                        
	$(CC) $(CFLAGS) -c $< -o $@	

clean-mkcres:
	@rm $(mkcres_OUTDIR)/*
	@rmdir $(mkcres_OUTDIR)
	
clean: clean-mkcres
	@rm $(OBJECTS) $(EXECUTABLE) 
	@rmdir obj

distclean: clean
