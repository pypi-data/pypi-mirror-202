/*
 * imports.c
 *
 *  Created on: Mar 1, 2023 (copied from semantic.c)
 *      Author: skauffma
 *
 *    nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2023  Sean Kauffman
 *
 *   This file is part of nfer.
 *   nfer is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <stdlib.h>
#include <assert.h>

#include "types.h"
#include "log.h"
#include "ast.h"

#include "dsl.tab.h"

/* if this is included in a test binary, include the testio header to overwrite malloc and free */
#ifdef TEST
    #include "testio.h"
#endif

/**
 * Walks the list of modules looking for the passed import name.
 * Returns it if it's found, or null if not.
 */
static ast_node * find_module(ast_node *module, word_id name) {
    assert(module->type == type_module_list);

    while (module != NULL) {
        // check the name
        if (module->module_list.id == name) {
            return module;
        }
        // otherwise walk
        module = module->module_list.tail;
    }
    return NULL;
}

/**
 * Append any imports attached to the passed module to the list of
 * imports.  Return the front of the list.  Sets silent flags on 
 * the imports if necessary.  If no imports are passed, returns
 * the list of imports from this module.  Does not touch the
 * module flags.
 * The silent_parent flag says if the import list is from a module
 * that was silently imported, make all sub-imports silent too.
 * This function is destructive - it will modify the AST to remove
 * option_flag nodes and it will alter the structure to put the
 * imports into one list.
 */
static ast_node * insert_imports(ast_node *module, ast_node *imports, bool silent_parent) {
    ast_node *first_child, *child, *last_child, *option_child;
    bool silent;

    assert(module->type == type_module_list);
    assert(imports == NULL || imports->type == type_import_list);

    silent = silent_parent;

    first_child = module->module_list.imports;
    // if there's no imports, just return the passed import list
    if (first_child == NULL) {
        filter_log_msg(LOG_LEVEL_DEBUG, "    There are no imports: returning NULL\n");
        return imports;
    }

    // walk over the list of imports, setting the silent flag
    // this has to look for interstitial option nodes because more
    // than one import statement will be appended into one list
    child = first_child;
    last_child = NULL;
    while (child != NULL) {
        // check if this is an option node
        if (child->type == type_option_flag) {
            filter_log_msg(LOG_LEVEL_DEBUG, "    Found option: silent? %d\n", child->option_flag.flag == SILENT);
            // there is a silent option, copy it to the variable
            silent = silent_parent || (child->option_flag.flag == SILENT);
            // overwrite the var to point to the imports
            // store the pointer to the children of this node
            option_child = child->option_flag.child;
            if (last_child != NULL) {
                // if there was already an import list, override its tail
                assert(last_child->type == type_import_list);
                last_child->import_list.tail = option_child;
                
            } else {
                // there was no import list, override the module_list imports
                module->module_list.imports = option_child;
            }
            // check if first_child needs overwritten
            if (child == first_child) {
                first_child = option_child;
            }
            // now remove the option flag node from memory
            free(child);
            // last_child stays the same, update child
            child = option_child;

        } else {
            filter_log_msg(LOG_LEVEL_DEBUG, "    Found import: %d\n", child->import_list.import);
            // if it's not an option flag it's an import node
            // set the silent flag
            child->import_list.silent = silent;
            // record the last child for linking the list
            last_child = child;
            // walk the list
            child = child->import_list.tail;
        }
    }

    // now link the list
    if (imports != NULL) {
        // if there is something to link
        if (last_child != NULL) {
            // record the next thing from the import list
            child = imports->import_list.tail;
            // overwrite it with the first thing from this list
            imports->import_list.tail = first_child;
            // set the tail
            last_child->import_list.tail = child;
            // now modify the module it came from so there's no double free
            // if there was an option flag it's already removed
            module->module_list.imports = NULL;
        }
        // return the import list
        return imports;
    }

    // if imports is null, return whatever we found
    return first_child;
}

/**
 * Function to set the imported flag on modules.
 * This flag is then used throughout analysis and generation to ignore modules
 * that aren't imported.  This saves work and memory, and is important in 
 * static analysis where we don't want to worry about unused modules.
 * This also sets the silent flag on modules for when they are imported with
 * that flag set.  It will be read in code generation to set the included rules
 * to hidden.
 * 
 * Returns true on success, false otherwise.
 **/
bool set_imported(ast_node *node) {
    ast_node *imports, *module;
    // the trick is that this needs to be a fixed point computation
    // since we can only figure out what import lists to include
    // when we know if the module they're in is included
    // we will basically use a worklist
    assert(node != NULL);

    // if this node isn't a module, then we're done
    if (node->type != type_module_list) {
        return true;
    }

    // otherwise...
    // step 1. get the first module import list and set the flags
    // we are using left recursion in the grammar now, so we have to
    // go get the last module to find the first one in the file
    module = node;
    while (module->module_list.tail != NULL) {
        module = module->module_list.tail;
    }
    imports = insert_imports(module, NULL, false);
    module->module_list.imported = true;
    module->module_list.silent = false;
    filter_log_msg(LOG_LEVEL_DEBUG, "    (main) module imported at 0x%p\n", module);

    // if there's anything in there
    while (imports != NULL) {
        // get the first import name and go find it
        module = find_module(node, imports->import_list.import);
        filter_log_msg(LOG_LEVEL_DEBUG, "    Found module for import: %d\n", imports->import_list.import);
        if (module == NULL) {
            // if none was found, it's an error
            parse_error(imports, "Missing imported module");
            return false;
        } else if (module->module_list.imported) {
            // if it was already imported, it's an error
            parse_error(imports, "Module imported more than once");
            return false;
        }
        // otherwise, set its flags
        module->module_list.imported = true;
        module->module_list.silent = imports->import_list.silent;
        // now, get its imports if it has any
        // make sure to pass the silent flag
        // we don't need its return value - we can continue using import
        insert_imports(module, imports, imports->import_list.silent);
        
        // get the next import
        imports = imports->import_list.tail;
    }
    // if we reach the end then we've imported everything 
    return true;
}