/*
 * constants.c
 *
 *  Created on: Mar 1, 2023
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

#include <assert.h>
#include <stdlib.h>

#include "types.h"
#include "log.h"
#include "ast.h"
#include "map.h"

/* if this is included in a test binary, include the testio header to overwrite malloc and free */
#ifdef TEST
    #include "testio.h"
#endif

/**
 * Searches an expression AST for constant references and replaces them
 * with a copy of the value assigned to the constant.  Recurses over
 * a tree of expression nodes.
 * 
 * This function takes a double pointer to the expression node so that
 * it can overwrite the pointer without needing to keep track of more
 * than one thing.
 * 
 * If a reference is encountered that isn't defined in the map then it 
 * is an error.
 * 
 * This function is destructive, in that it will free any replaced 
 * constant reference nodes after copying over them in the AST.
 * 
 * @return true on no error, false on error
 */
#ifndef TEST
static 
#endif
bool propagate_to_expr(ast_node **expr_reference, data_map *constant_map) {
    bool success;
    map_key key;
    map_value constant_value;
    ast_node *expr, *constant_expr, *reference_node;

    assert(expr_reference != NULL);
    assert(constant_map != NULL);

    // get the expression node from its reference
    expr = *expr_reference;

    if (expr == NULL) {
        return true;
    }

    success = true;

    // recurse down the tree
    switch (expr->type) {
    case type_constant_reference:
        // look for the reference in the map
        key = expr->constant_reference.name;
        if (map_has_key(constant_map, key)) {
            map_get(constant_map, key, &constant_value);
            if (constant_value.type == pointer_type) {
                // get the expression
                constant_expr = (ast_node *) constant_value.value.pointer;
                // now copy the expr node pointer so we can free it later
                reference_node = expr;
                // copy the constant expression and overwrite the reference
                *expr_reference = copy_ast(constant_expr);
                // free the expr node
                free(reference_node);
                // get rid of the invalid pointer
                reference_node = NULL;
            } else {
                // something unexpected happened
                parse_error(expr, "Unexpected constant value");
                success = false;
            }
        } else {
            // the key doesn't exist, it's an error
            parse_error(expr, "Undefined constant reference");
            success = false;
        }
        break;
    case type_unary_expr:
        // recurse down the path
        success = propagate_to_expr(&expr->unary_expr.operand, constant_map);
        break;
    case type_binary_expr:
        // recurse down both sides
        success = (propagate_to_expr(&expr->binary_expr.left, constant_map) &&
                   propagate_to_expr(&expr->binary_expr.right, constant_map));
        break;
    default:
        /* nothing to do if we encounter, for example, a literal */
        break;
    }

    return success;
}

/**
 * Recurse through the contents of a module, looking for expressions
 * where constant references might appear and calling propagate_to_expr
 * for each of them, which is destructive.
 * 
 * @return true on no error, false on error
 */
#ifndef TEST
static 
#endif
bool propagate_to_rule_list(ast_node *node, data_map *constant_map) {
    bool success;

    if (node == NULL) {
        return true;
    }

    success = true;

    switch (node->type) {
    case type_map_expr_list:
        // first handle the expression
        success = propagate_to_expr(&node->map_expr_list.map_expr, constant_map);
        // then recurse down the list
        success = success && propagate_to_rule_list(node->map_expr_list.tail, constant_map);
        break;
    case type_end_points:
        // call for both end points
        success = (propagate_to_expr(&node->end_points.begin_expr, constant_map) &&
                   propagate_to_expr(&node->end_points.end_expr, constant_map));
        break;
    case type_rule:
        // first handle the where clause
        success = propagate_to_expr(&node->rule.where_expr, constant_map);
        // then recurse down the two other trees where expressions can occur
        success = success && propagate_to_rule_list(node->rule.map_expr_list, constant_map);
        success = success && propagate_to_rule_list(node->rule.end_points, constant_map);
        break;
    case type_rule_list:
        // recurse down into the rule, then continue in the list
        success = (propagate_to_rule_list(node->rule_list.head, constant_map) &&
                   propagate_to_rule_list(node->rule_list.tail, constant_map));
        break;
    
    default:
        parse_error(node, "Unexpected node type in rule list constant propogation");
        success = false;
        break;
    }
    return success;
}

/**
 * Recursively walk the list of constants and populate the map with their
 * expressions.  This is recursive so it can reverse the order, handling the
 * nodes in the order they appeared in the spec file.
 * 
 * Checks that constants referenced from other constants are defined before
 * their use.
 * Checks that constants are not defined more than once.
 * 
 * This function also populates constants to the expressions assigned to them
 * prior to assigning them to the map.  This is done with calls to 
 * propagate_to_expr which are destructive.
 * 
 * @return true if no error, false if error
 */
#ifndef TEST
static 
#endif
bool populate_constant_map(ast_node *constant, data_map *constant_map) {
    map_key key;
    map_value constant_value;
    bool success;

    if (constant == NULL) {
        return true;
    }

    assert(constant->type == type_named_constant);

    success = true;

    // recurse down the constants to handle the first ones first
    // the first in the file will be the last in the node list
    success = populate_constant_map(constant->named_constant.tail, constant_map);
    
    if (success) {
        // before setting anything on the map for this constant,
        // propagate constants to its expression
        success = propagate_to_expr(&constant->named_constant.expr, constant_map);
        // as long as it was successful, store the result in the map
        if (success) {
            // get the key
            key = constant->named_constant.name;
            // make sure the key isn't set
            if (map_has_key(constant_map, key)) {
                parse_error(constant, "Constants may only be defined once per module");
                success = false;

            } else {
                // get the value
                constant_value.type = pointer_type;
                constant_value.value.pointer = constant->named_constant.expr;

                // set the value
                map_set(constant_map, key, &constant_value);
            }
        }
    } // end if success

    return success;
}

/**
 * Propogate constants from their definitions to their references.
 * 
 * Checks that constants referenced from other constants are defined before
 * their use.
 * Checks that constants are not defined more than once.
 * Checks that constants are defined in the scope of their use (module).
 * 
 * This function works by first collecting all the values of constants
 * in a map and then using that map to copy the associated expressions
 * wherever the constant is used.  In this way, the constants disappear 
 * in the AST that is passed to the type checker.
 * 
 * This function is designed to be used after module imports are calculated
 * so that it will respect the module import flag.  This is also because
 * there is a plan to support parameterized modules and this means the
 * imports should be done first to ensure any parameter values are set.
 * 
 * Calls propagate_to_expr, which is desctructive.
 * 
 * Returns true on success, false if errors are encountered.
 */
bool propagate_constants(ast_node *root) {
    ast_node *module, *constants;
    data_map constant_map;
    bool success;

    success = true;

    // we want to iterate over the module list, visiting the imported ones
    module = root;
    while (success && module != NULL) {
        assert(module->type == type_module_list);

        // if it is imported
        if (module->module_list.imported) {
            // instantiate the map
            initialize_map(&constant_map);
            // get the constants
            constants = module->module_list.constants;

            // populate the map, also propogating constants to constant definitions
            success = populate_constant_map(constants, &constant_map);

            // at this point the constant map is populated
            // now we need to go through the rest of the module AST, looking for references
            // skip if errors have been encountered
            if (success) {
                success = propagate_to_rule_list(module->module_list.rules, &constant_map);
            }

            // destroy the map
            destroy_map(&constant_map);
        } // end if imported

        // continue to the next module
        module = module->module_list.tail;
    }

    return success;
}