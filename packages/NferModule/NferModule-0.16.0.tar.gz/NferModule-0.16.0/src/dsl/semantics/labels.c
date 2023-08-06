/*
 * labels.c
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

#include <stdio.h>

#include "types.h"
#include "log.h"
#include "ast.h"
#include "memory.h"
#include "dict.h"

#include "dsl.tab.h"


/**
 * Generates a new, unique interval label for use in hidden rules.
 * This is needed for hidden rules created due to rule nesting or exclusive rules.
 * It tries to form the label using parts of the passed left/right words so as
 * to help a user understand where the intervals came from.
 * The function guarantees that the produced word does not appear in the passed 
 * dictionary and returns the resulting word_id in that dictionary.
 */
static word_id new_interval_name(dictionary *dict, word_id partial_left, word_id partial_right) {
    unsigned int counter = 0;
    char buffer[MAX_WORD_LENGTH + 1];

    // clear the whole buffer
    clear_memory(buffer, sizeof(char) * (MAX_WORD_LENGTH + 1));
    // generate the word, trying until it isn't found in the dictionary
    do {
        snprintf(buffer, MAX_WORD_LENGTH + 1, "H_%.*s%.*s-%d", MAX_WORD_LENGTH / 2 - 12, get_word(dict, partial_left), MAX_WORD_LENGTH / 2 - 12, get_word(dict, partial_right), counter++);
    } while (find_word(dict, buffer) != WORD_NOT_FOUND);

    return add_word(dict, buffer);
}

/**
 * Walk a rule AST to determine the location of labels in the tree and check that they meet certain conditions.
 * This function performs a number of label and interval name related tasks that must be done at the beginning 
 * of semantic analysis (but can be after type checking).
 * The main function is to set up data structures so that the code can find what is referred to when expressions
 * later on refer to an interval name or label.  If there's a tree of nested rules, for example, each node 
 * needs to know which side (right or left) contains that label so that expressions can be associated with the
 * correct (generated, binary) rule and values needed by their children can be passed along.
 * 
 * This function, as mentioned, also does some semantic checking for a few random things because it is walking
 * the rule trees already and is doing so early on.  This just avoids having more walks and code, but it does
 * clutter things up a bit here.
 * 
 * This is a worker function called for each top-level rule by determine_labels.
 * Returns true on success, false on failure.
 */
static bool determine_labels_per_rule(
        ast_node *node, dictionary *parser_dict, dictionary *label_dict, dictionary *name_dict,
        data_map *label_map, data_map *parent_map, word_id *result_name, ast_node *bie_ast_node) {
    bool success = true;
    word_id label_dict_name_id, label_dict_label_id, name_dict_name_id;
    map_value check, bie_value, copy_value;
    map_key copy_key;
    map_iterator mit;

    if (!node) {
        return true;
    }
    switch (node->type) {
    case type_atomic_interval_expr:
        // first set up the bie value
        // this needs to be a non-null typed value
        bie_value.type = pointer_type;
        // if bie_ast_node is null, then this is an atomic rule and we should use the atomic ie node itself
        if (bie_ast_node != NULL) {
            // check the bie node to see if it is an exclusion
            // if so, if this is the lhs, use the atomic ie node instead so we create an atomic rule
            if (bie_ast_node->binary_interval_expr.exclusion && bie_ast_node->binary_interval_expr.left == node) {
                bie_value.value.pointer = node;
                // set the flag to generate this node as a separate rule
                node->atomic_interval_expr.separate = true;
                // initialize the field map
                initialize_map(&node->atomic_interval_expr.field_map);
            } else {
                bie_value.value.pointer = bie_ast_node;
            }
        } else {
            bie_value.value.pointer = node;
        }

        // if there's no label
        if (node->atomic_interval_expr.label == WORD_NOT_FOUND) {
            // then the name should not appear in the label map
            // if it does, then there was anther one (not allowed)
            label_dict_name_id = find_word(label_dict, get_word(parser_dict, node->atomic_interval_expr.id));
            if (label_dict_name_id != WORD_NOT_FOUND) {
                map_get(label_map, label_dict_name_id, &check);
                if (check.type != null_type) {
                    // here we know the id appears more than once, but this on its own is not an error
                    // we want to throw an error if something tries to refer to one of these duplicate
                    // ids instead.  So, mark the id in the map as being present but illegal to
                    // refer to.
                    bie_value.type = SEMANTIC_ERROR_DUP_ID;
                    // this is a little cheeky - but we just designate a label map type to be the error type
                }
            }
        }
        // now add the interval name to both dictionaries
        label_dict_name_id = add_word(label_dict, get_word(parser_dict, node->atomic_interval_expr.id));
        name_dict_name_id = add_word(name_dict, get_word(parser_dict, node->atomic_interval_expr.id));
        // set it on the atomic_interval_expr, which is only really used for completely atomic rules
        // actually, it's now used in static analysis too, so don't remove this
        node->atomic_interval_expr.result_id = name_dict_name_id;
        // add the name id to the map, mapping to the binary_interval_expr_node, if it exists
        map_set(label_map, label_dict_name_id, &bie_value);
        if (parent_map != NULL) {
            map_set(parent_map, label_dict_name_id, &bie_value);
        }

        if (result_name != NULL) {
            // copy up the name
            // if we're generating a nested atomic rule, generate a new name
            if (node->atomic_interval_expr.separate) {
                *result_name = new_interval_name(name_dict, name_dict_name_id, name_dict_name_id);
            } else {
                // otherwise just copy the original
                *result_name = name_dict_name_id;
            }
        }

        if (node->atomic_interval_expr.label != WORD_NOT_FOUND) {
            // check to make sure the label isn't used twice
            label_dict_label_id = find_word(label_dict, get_word(parser_dict, node->atomic_interval_expr.label));
            if (label_dict_label_id != WORD_NOT_FOUND) {
                map_get(label_map, label_dict_label_id, &check);
                if (check.type != null_type) {
                    // here we know the label appears more than once, but this on its own is not an error
                    // we want to throw an error if something tries to refer to one of these duplicate
                    // labels instead.  So, mark the label in the map as being present but illegal to
                    // refer to.
                    bie_value.type = SEMANTIC_ERROR_DUP_LABEL;
                    // this is a little cheeky - but we just designate a label map type to be the error type
                }
            }
            // then add the label
            label_dict_label_id = add_word(label_dict, get_word(parser_dict, node->atomic_interval_expr.label));
            // add the label id to the map, mapping to the name id
            map_set(label_map, label_dict_label_id, &bie_value);
            if (parent_map != NULL) {
                map_set(parent_map, label_dict_label_id, &bie_value);
            }
        }

        break;
    case type_binary_interval_expr:
        initialize_map(&node->binary_interval_expr.left_label_map);
        initialize_map(&node->binary_interval_expr.right_label_map);
        initialize_map(&node->binary_interval_expr.left_field_map);
        initialize_map(&node->binary_interval_expr.right_field_map);

        success = success && determine_labels_per_rule(node->binary_interval_expr.left, parser_dict, label_dict, name_dict, label_map,
                &node->binary_interval_expr.left_label_map, &node->binary_interval_expr.left_name, node);
        success = success && determine_labels_per_rule(node->binary_interval_expr.right, parser_dict, label_dict, name_dict, label_map,
                &node->binary_interval_expr.right_label_map, &node->binary_interval_expr.right_name, node);

        // copy the labels to the parent maps so we can figure out where they are located
        if (parent_map != NULL) {
            get_map_iterator(&node->binary_interval_expr.left_label_map, &mit);
            while (has_next_map_key(&mit)) {
                copy_key = next_map_key(&mit);
                map_get(&node->binary_interval_expr.left_label_map, copy_key, &copy_value);
                map_set(parent_map, copy_key, &copy_value);
            }

            get_map_iterator(&node->binary_interval_expr.right_label_map, &mit);
            while (has_next_map_key(&mit)) {
                copy_key = next_map_key(&mit);
                map_get(&node->binary_interval_expr.right_label_map, copy_key, &copy_value);
                map_set(parent_map, copy_key, &copy_value);
            }
        }

        if (result_name != NULL) {
            *result_name = new_interval_name(name_dict, node->binary_interval_expr.left_name, node->binary_interval_expr.right_name);
        }

        // briefly, and this is pretty unrelated, make sure that ALSO is only allowed at the top level
        if (parent_map != NULL) {
            if (node->binary_interval_expr.interval_op == ALSO) {
                parse_error(node, "ALSO is not allowed in nested rules");
                success = false;
            }
        }
        break;
    case type_rule:
        initialize_map(&node->rule.label_map);
        success = success && determine_labels_per_rule(node->rule.interval_expr, parser_dict, label_dict, name_dict, &node->rule.label_map, NULL, NULL, NULL);

        // this is just to make sure the top level rule ids get added to the name_dict
        node->rule.result_id = add_word(name_dict, get_word(parser_dict, node->rule.id));

        // check that if the top level interval expression is ALSO, then there is both a where and end points clause
        if (node->rule.interval_expr->type == type_binary_interval_expr) {
            if (node->rule.interval_expr->binary_interval_expr.interval_op == ALSO) {
                if (!node->rule.where_expr) {
                    parse_error(node, "Where clause must be specified when ALSO is used");
                    success = false;
                }
                if (!node->rule.end_points) {
                    parse_error(node, "End points must be specified when ALSO is used");
                    success = false;
                }
            }
        }
        break;
    default:
        /* nothing */
        return success;
    }
    return success;
}

/**
 * External function to call determine_labels_per_rule on each rule in an AST.
 * This is the function that is actually called from semantic analysis so as to avoid exposing all the 
 * necessary parameters to the outside world.  This is a common pattern in the nfer AST.
 * 
 * Returns true on success, false on failure.
 */
bool determine_labels(ast_node *node, dictionary *parser_dict, dictionary *label_dict, dictionary *name_dict) {
    bool success = true;
    if (!node) {
        return true;
    }
    switch (node->type) {
    case type_rule_list:
        success = success && determine_labels_per_rule(node->rule_list.head, parser_dict, label_dict, name_dict, NULL, NULL, NULL, NULL);
        success = success && determine_labels(node->rule_list.tail, parser_dict, label_dict, name_dict);
        break;
    case type_module_list:
        // skip any modules that aren't imported
        if (node->module_list.imported) {
            success = success && determine_labels(node->module_list.rules, parser_dict, label_dict, name_dict);
        }
        success = success && determine_labels(node->module_list.tail, parser_dict, label_dict, name_dict);
        break;
    default:
        /* nothing */
        return success;
    }
    return success;
}