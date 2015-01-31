# mkcres CMake functions
#
# see README.md and LICENSE for more details
#
#
# USAGE: 1) include this file 
#        2) use mkcres_add_library function
#        3) link any of your executable targets to your mkcres library target
#
# EXAMPLE (mkcres files are residing in a subdir 'mkcres'):      
# -------------------------------------------------------------
#   include(mkcres/mkcres.cmake)
#   mkcres_add_library(myresources resources.json "./mkcres")
#    
#   add_executable(example main.c) 
#   target_link_libraries(example myresources)
#

function(mkcres_add_library name configfiles mkcres_dir) 
    # currently we need at least python 2.7 because of the usage argparse
    find_package(PythonInterp 2.7 REQUIRED) 
    set(mkcres_script ${mkcres_dir}/mkcres.py)
    set(mkcres_res_target "${name}-cres-update")
    set(mkcres_res_force_target "${name}-cres-force-rewrite")
    set(mkcres_outdir ${CMAKE_CURRENT_BINARY_DIR}/${name}_cresources)
    set(mkcres_outfile ${mkcres_outdir}/cres_files.cmake)

	# mkcres update command arguments
	set(mkcres_update_args create --list-outfile "${mkcres_outfile}" --list-cmake-prefix=${name}
                                  --outdir "${mkcres_outdir}" ${configfiles})
	
    add_custom_target(${mkcres_res_target} "${PYTHON_EXECUTABLE}" "${mkcres_script}" 
						${mkcres_update_args} --quiet
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

    add_custom_target(${mkcres_res_force_target} "${PYTHON_EXECUTABLE}" "${mkcres_script}" 
						${mkcres_update_args} --force --quiet
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

    if(NOT EXISTS "${mkcres_outfile}")
        execute_process(COMMAND "${PYTHON_EXECUTABLE}" "${mkcres_script}" 
						${mkcres_update_args} --force --quiet
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
	endif()
	
	include("${mkcres_outfile}")
    include_directories(${mkcres_dir})
    add_library(${name} STATIC EXCLUDE_FROM_ALL ${${name}_CRES_SOURCE_FILES} ${mkcres_dir}/cresource.c)
    add_dependencies(${name} ${mkcres_res_target})

    if(NOT TARGET mkcres-update)
        add_custom_target(mkcres-update)
    endif()
    add_dependencies(mkcres-update ${mkcres_res_target})
    
    if(NOT TARGET mkcres-force-rewrite)
        add_custom_target(mkcres-force-rewrite)
    endif()
    add_dependencies(mkcres-force-rewrite ${mkcres_res_force_target})
endfunction()
