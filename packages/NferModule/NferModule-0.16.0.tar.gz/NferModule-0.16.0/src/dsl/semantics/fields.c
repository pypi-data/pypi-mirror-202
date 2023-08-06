/*
 * fields.c
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
 * Generate a new, unique map key name for data maps created by the analysis code.
 * This is needed because, in the mapping from nested rules to binary rules, sometimes
 * data must be passed along from a lower level (nested) rule to its parent.  That means
 * setting data, and so we need unique map keys to use for storing said data.
 * This function tries to use part of a passed string from the original data key in 
 * the field name to make it easier for a user to understand where it came from.
 * Gurantees the returned name did not appear in the passed dictionary.
 * Returns the word_id of the string in that dictionary.
 */
static word_id new_field_name(dictionary *dict, const char *partial) {
    unsigned int counter = 0;
    char buffer[MAX_WORD_LENGTH + 1];

    // clear the whole buffer
    clear_memory(buffer, sizeof(char) * (MAX_WORD_LENGTH + 1));
    // generate the word, trying until it isn't found in the dictionary
    do {
        snprintf(buffer, MAX_WORD_LENGTH + 1, "F_%.*s-%d", MAX_WORD_LENGTH / 2 - 12, partial, counter++);
    } while (find_word(dict, buffer) != WORD_NOT_FOUND);

    return add_word(dict, buffer);
}

/**
 * This gets the side of an interval expression referenced by a label.
 * For BIE this does what you expect and for AIE it just returns left.
 */
static bool get_label_side_from_ie(side_enum *side, ast_node *interval_expr, word_id label) {
    map_value check_left, check_right;
    bool success = true;

    switch(interval_expr->type) {
    case type_atomic_interval_expr:
        // it's always left for atomic interval expressions
        *side = left_side;
        break;
    case type_binary_interval_expr:
        // find the key in the label maps
        map_get(&interval_expr->binary_interval_expr.left_label_map, label, &check_left);
        map_get(&interval_expr->binary_interval_expr.right_label_map, label, &check_right);

        // we are not allowed to find the label in both sides
        if (check_left.type != null_type && check_right.type == null_type) {
            *side = left_side;
        } else if (check_right.type != null_type && check_left.type == null_type) {
            *side = right_side;

        } else {
            if (check_right.type == null_type && check_left.type == null_type) {
                parse_error(interval_expr, "Label or interval reference not found");
            } else {
                parse_error(interval_expr, "Ambiguous label or interval reference");
            }
            success = false;
        }
        break;
    default:
        /* do nothing */
        success = false;
    }

    return success;
}

/**
 * Takes an interval expression, where there is a map_field node that references either that BIE
 * or one of its children.  The function looks for the BIE that is referenced and then creates
 * mappings for the field up the tree until the rule for the top level BIE can access it.
 * There are also some incidental checks for referencing excluded intervals.
 */
#ifndef TEST
static
#endif
bool set_field_mapping_per_rule(
        ast_node *interval_expr,
        dictionary *key_dict,
        word_id label,
        map_key key,
        map_key *result,
        side_enum *side,
        bool exclusion_ok,
        bool nested
        ) {
    map_value set_value;
    map_key intermediate_key = MAP_MISSING_KEY, search_key;
    bool success = true;
    binary_interval_expr_node *bie_node = &interval_expr->binary_interval_expr;
    side_enum label_side;

    if (!interval_expr) {
        return false;
    }

    switch(interval_expr->type) {
    case type_atomic_interval_expr:
        if (interval_expr->atomic_interval_expr.separate) {
            // we know this is nested - just go ahead and remap
            set_value.type = string_type;
            set_value.value.string = key;
            *result = new_field_name(key_dict, get_word(key_dict, key));
            map_set(&interval_expr->atomic_interval_expr.field_map, *result, &set_value);

            filter_log_msg(LOG_LEVEL_DEBUG, "      Mapping field %d to %d for nested AIE\n", key, *result);
        } else {
            *result = key;
        }
        break;

    case type_binary_interval_expr:
        // find the key in the label maps
        success = get_label_side_from_ie(&label_side, interval_expr, label);

        if (success && label_side == left_side) {
            // we don't want to remap the field if this BIE is not nested
            if (!nested) {
                success = success && set_field_mapping_per_rule(bie_node->left, key_dict, label, key, result, side, exclusion_ok, NESTED_IE);
                // record which side its on at the map_field level
                *side = left_side;

            } else {
                // only do this work if we've succeeded so far
                if (success) {
                    // if this is a nested rule, then we want to add a remapping
                    // since there could be several levels of remapping, each one needs to know what it will get from the rule below it
                    success = set_field_mapping_per_rule(bie_node->left, key_dict, label, key, &intermediate_key, side, exclusion_ok, NESTED_IE);
                    // first search for the key, and use it if is already present in the field map
                    set_value.type = string_type;
                    set_value.value.string = intermediate_key;
                    search_key = map_find(&bie_node->left_field_map, &set_value);
                    if (search_key != MAP_MISSING_KEY) {
                        *result = search_key;
                    } else {
                        // add a field name to map to
                        *result = new_field_name(key_dict, get_word(key_dict, intermediate_key));

                        map_set(&bie_node->left_field_map, *result, &set_value);
                    }
                }
            }
        } else if (success && label_side == right_side) {
            // if this is an exclusion and exclusions are prohibited, we need to throw an error
            if (exclusion_ok || !bie_node->exclusion) {
                // we don't want to remap the field if this BIE is not nested
                if (!nested) {
                    success = success && set_field_mapping_per_rule(bie_node->right, key_dict, label, key, result, side, exclusion_ok, NESTED_IE);
                    // record which side its on at the map_field level
                    *side = right_side;

                } else {
                    // only do this work if success is true so far
                    if (success) {
                        // if this is a nested rule, then we want to add a remapping
                        // since there could be several levels of remapping, each one needs to know what it will get from the rule below it
                        success = set_field_mapping_per_rule(bie_node->right, key_dict, label, key, &intermediate_key, side, exclusion_ok, NESTED_IE);
                        // first search for the key, and use it if is already present in the field map
                        set_value.type = string_type;
                        set_value.value.string = intermediate_key;
                        search_key = map_find(&bie_node->right_field_map, &set_value);
                        if (search_key != MAP_MISSING_KEY) {
                            *result = search_key;
                        } else {
                            // add a field name to map to
                            *result = new_field_name(key_dict, get_word(key_dict, intermediate_key));

                            map_set(&bie_node->right_field_map, *result, &set_value);
                        }
                    }
                }
            } else {
                // if this is an exclusion and exclusions are prohibited, we need to throw an error
                parse_error(bie_node->right, "Referenced a parameter of an excluded interval");
                success = false;
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
 * Takes an interval expression, where there is a time_field node that references either that BIE
 * or one of its children.  The function looks for the BIE that is referenced and then creates
 * mappings for the time field up the tree until the rule for the top level BIE can access it.
 * After the first mapping the time field ceases to be a time field per se as it will be stored in
 * map fields, so that must be reflected in the generated expression actions that reference it.
 * There are also some incidental checks for referencing excluded intervals.
 */
#ifndef TEST
static
#endif
bool set_time_mapping_per_rule(
        ast_node *interval_expr,
        dictionary *key_dict,
        word_id label,
        map_key *result,
        side_enum *side,
        bool *is_time,
        int time_field,
        bool exclusion_ok,
        bool nested
        ) {
    map_value set_value;
    map_key intermediate_key = MAP_MISSING_KEY;
    bool success = true, intermediate_time = false;
    const char *begin_string = "BEGIN", *end_string = "END";
    binary_interval_expr_node *bie_node = &interval_expr->binary_interval_expr;
    side_enum label_side;

    if (!interval_expr) {
        return false;
    }

    switch(interval_expr->type) {
    case type_atomic_interval_expr:
        if (interval_expr->atomic_interval_expr.separate) {
            // this must be generated as a separate rule, so remap the time field at this level
            // we know it's nested, so don't worry about that.
            switch(time_field) {
            case BEGINTOKEN:
                // check to see if it's already set
                if (interval_expr->atomic_interval_expr.begin_map != WORD_NOT_FOUND) {
                    *result = interval_expr->atomic_interval_expr.begin_map;
                } else {
                    // otherwise generate one
                    *result = new_field_name(key_dict, begin_string);
                    interval_expr->atomic_interval_expr.begin_map = *result;
                }
                filter_log_msg(LOG_LEVEL_DEBUG, "      Mapping begin time field to %d for nested AIE\n", *result);

                break;
            case ENDTOKEN:
                // check to see if it's already set
                if (interval_expr->atomic_interval_expr.end_map != WORD_NOT_FOUND) {
                    *result = interval_expr->atomic_interval_expr.end_map;
                } else {
                    // otherwise generate one
                    *result = new_field_name(key_dict, begin_string);
                    interval_expr->atomic_interval_expr.end_map = *result;
                }
                filter_log_msg(LOG_LEVEL_DEBUG, "      Mapping end time field to %d for nested AIE\n", *result);

                break;
            }
            // the time field is nested, so the result will be a map-field, not a time-field
            *is_time = false;

        } else {
            *result = MAP_MISSING_KEY;
            *is_time = true;
        }
        break;

    case type_binary_interval_expr:
        // find the key in the label maps
        success = get_label_side_from_ie(&label_side, interval_expr, label);

        if (success && label_side == left_side) {
            // we don't want to remap the field if this BIE is not nested
            if (!nested) {
                success = success && set_time_mapping_per_rule(bie_node->left, key_dict, label, result, side, is_time, time_field, exclusion_ok, NESTED_IE);
                // record which side its on at the map_field level
                *side = left_side;

            } else {
                // skip all of this if success is false
                if (success) {
                    // if this is a nested rule, then we want to add a remapping
                    // since there could be several levels of remapping, each one needs to know what it will get from the rule below it
                    success = set_time_mapping_per_rule(bie_node->left, key_dict, label, &intermediate_key, side,
                            &intermediate_time, time_field, exclusion_ok, NESTED_IE);
                    // whatever is below this is atomic (and not separate), then this is the level at which we will map the time field to a map field
                    if (intermediate_time) {
                        // add a field to map to and use the dedicated binary_interval_expr fields to store them
                        switch(time_field) {
                        case BEGINTOKEN:
                            // first check to see if one is already set
                            if (bie_node->left_begin_map != WORD_NOT_FOUND) {
                                // if one has been set, use it
                                *result = bie_node->left_begin_map;
                            } else {
                                // otherwise generate one
                                *result = new_field_name(key_dict, begin_string);
                                bie_node->left_begin_map = *result;
                            }
                            break;
                        case ENDTOKEN:
                            // first check to see if one is already set
                            if (bie_node->left_end_map != WORD_NOT_FOUND) {
                                // if one has been set, use it
                                *result = bie_node->left_end_map;
                            } else {
                                // otherwise generate one
                                *result = new_field_name(key_dict, end_string);
                                bie_node->left_end_map = *result;
                            }
                            break;
                        }
                    } else {
                        // now we have to map the intermediate key to another key instead of mapping the time field
                        // this works just like if it were a regular map field
                        // add a field name to map to
                        *result = new_field_name(key_dict, get_word(key_dict, intermediate_key));
                        set_value.type = string_type;
                        set_value.value.string = intermediate_key;
                        map_set(&bie_node->left_field_map, *result, &set_value);
                    }
                }

                // we are at a nested rule, so the final field will not be a time field, it will be copied to a map field
                *is_time = false;
            }
        } else if (success && label_side == right_side) {
            // if this is an exclusion and exclusions are prohibited, we need to throw an error
            if (exclusion_ok || !bie_node->exclusion) {
                // we don't want to remap the field if this BIE is not nested
                if (!nested) {
                    success = success && set_time_mapping_per_rule(bie_node->right, key_dict, label, result, side, is_time, time_field, exclusion_ok, NESTED_IE);
                    // record which side its on at the map_field level
                    *side = right_side;

                } else {
                    // skip this whole section if success is false
                    if (success) {
                        // if this is a nested rule, then we want to add a remapping
                        // since there could be several levels of remapping, each one needs to know what it will get from the rule below it
                        success = set_time_mapping_per_rule(bie_node->right, key_dict, label, &intermediate_key, side,
                                &intermediate_time, time_field, exclusion_ok, NESTED_IE);
                        // whatever is below this is atomic, then this is the level at which we will map the time field to a map field
                        if (intermediate_time) {
                            // add a field to map to and use the dedicated binary_interval_expr fields to store them
                            switch(time_field) {
                            case BEGINTOKEN:
                                // first check to see if one is already set
                                if (bie_node->right_begin_map != WORD_NOT_FOUND) {
                                    // if one has been set, use it
                                    *result = bie_node->right_begin_map;
                                } else {
                                    // otherwise generate one
                                    *result = new_field_name(key_dict, begin_string);
                                    bie_node->right_begin_map = *result;
                                }
                                break;
                            case ENDTOKEN:
                                // first check to see if one is already set
                                if (bie_node->right_end_map != WORD_NOT_FOUND) {
                                    // if one has been set, use it
                                    *result = bie_node->right_end_map;
                                } else {
                                    // otherwise generate one
                                    *result = new_field_name(key_dict, end_string);
                                    bie_node->right_end_map = *result;
                                }
                                break;
                            }
                        } else {
                            // now we have to map the intermediate key to another key instead of mapping the time field
                            // this works just like if it were a regular map field
                            // add a field name to map to
                            *result = new_field_name(key_dict, get_word(key_dict, intermediate_key));
                            set_value.type = string_type;
                            set_value.value.string = intermediate_key;
                            map_set(&bie_node->right_field_map, *result, &set_value);
                        }
                    }

                    // we are at a nested rule, so the final field will not be a time field, it will be copied to a map field
                    *is_time = false;
                }
            } else {
                // if this is an exclusion and exclusions are prohibited, we need to throw an error
                parse_error(bie_node->right, "Referenced a parameter of an excluded interval");
                success = false;
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
 * Parent function to call the remap functions for either time or field mappings.
 * This keeps some of the incidental AST walking from needing to be duplicated in
 * those functions and keeps the argument list sane at this level.
 * Returns true on success and false on failure.
 */
#ifndef TEST
static
#endif
bool remap_field_or_time_mappings(
        ast_node *ie_node,
        ast_node *expr_node,
        dictionary *key_dict,
        bool is_where_expr
        ) {
    bool success = true;

    if (!expr_node) {
        return true;
    }
    switch (expr_node->type) {
    case type_unary_expr:
        // recurse down the hole
        success = success && remap_field_or_time_mappings(ie_node, expr_node->unary_expr.operand, key_dict, is_where_expr);
        break;
    case type_binary_expr:
        if (expr_node->binary_expr.belongs_in == NULL) {
            success = success && remap_field_or_time_mappings(ie_node, expr_node->binary_expr.left, key_dict, is_where_expr);
            success = success && remap_field_or_time_mappings(ie_node, expr_node->binary_expr.right, key_dict, is_where_expr);
        }
        break;
    case type_map_field:
        //        ast_node *interval_expr,
        //        dictionary *key_dict,
        //        word_id label,
        //        map_key key,
        //        map_key *result,
        //        side_enum *side,
        //        bool exclusion_ok,
        //        bool nested
        // skip this field if it is a subfield of a Boolean expression
        // this is to avoid remapping fields that really just shouldn't ever be remapped
        if (expr_node->map_field.is_non_boolean) {
            success = success && set_field_mapping_per_rule(
                    ie_node,
                    key_dict,
                    expr_node->map_field.resulting_label_id,
                    expr_node->map_field.resulting_map_key,
                    &expr_node->map_field.resulting_map_key,
                    &expr_node->map_field.side,
                    is_where_expr,
                    NOT_NESTED_IE);
        }
        break;
    case type_time_field:
        //        ast_node *interval_expr,
        //        dictionary *key_dict,
        //        word_id label,
        //        map_key *result,
        //        side_enum *side,
        //        bool *is_time,
        //        int time_field,
        //        bool exclusion_ok,
        //        bool nested
        // figure out 1) if it will still be a time field when it gets up to the top level
        //            2) if not, what the map field will be called where it is copied
        success = success && set_time_mapping_per_rule(
                ie_node,
                key_dict,
                expr_node->time_field.resulting_label_id,
                &expr_node->time_field.resulting_map_key,
                &expr_node->time_field.side,
                &expr_node->time_field.is_time,
                expr_node->time_field.time_field,
                is_where_expr,
                NOT_NESTED_IE);
        break;
    default:
        return false;
    }
    return success;
}

/**
 * Determine if the passed AST of expression nodes references a specific Interval Expression.
 * This is called from the version that tests a whole IE tree.
 *
 * Recursive: true
 * Side-effects: none
 */
static bool expr_references_exact_ie(
        ast_node *ie_node,      /* The binary interval expression to search for */
        ast_node *node          /* The expression AST node in which to search for the IE */
        ) {

    if (!node || !ie_node) {
        return true;
    }
    switch (node->type) {
    case type_int_literal:
    case type_float_literal:
    case type_string_literal:
    case type_boolean_literal:
        return true;
        break;
    case type_unary_expr:
        return expr_references_exact_ie(ie_node, node->unary_expr.operand);
        break;
    case type_binary_expr:
        return expr_references_exact_ie(ie_node, node->binary_expr.left)
                && expr_references_exact_ie(ie_node, node->binary_expr.right);
        break;
    case type_map_field:
        // the interval expression was stored by determine_fields_per_rule
        // just check to see if it is the same as the ie_node
        return node->map_field.interval_expression == ie_node;
        break;
    case type_time_field:
        // the interval expression was stored by determine_fields_per_rule
        // just check to see if it is the same as the ie_node
        return node->time_field.interval_expression == ie_node;
        break;
    default:
        /* nothing */
        return true;
    }
    /* shouldn't be possible to reach this, but it is here to avoid warnings from dumber compilers */
    return true;
}

/**
 * Determine if the passed AST of expression nodes references a tree of Interval Expressions.
 * This is called from expression generation during rule generation to determine if subexpressions should
 * be replaced by Booleans.
 *
 * Recursive: true
 * Side-effects: none
 */
#ifndef TEST
static
#endif
bool expr_references_ie(
        ast_node *ie_node,      /* The binary interval expression to search for */
        ast_node *node           /* The expression AST node in which to search for the BIE */
        ) {

    if (!node || !ie_node) {
        return true;
    }
    switch (ie_node->type) {
    case type_atomic_interval_expr:
        /* expr_nodes should only reference atomic interval expression nodes in the case of atomic rules. 
           OR, when it is the left side of an exclusive rule with restrictions. */
        return expr_references_exact_ie(ie_node, node);
        break;
    case type_binary_interval_expr:
        return expr_references_exact_ie(ie_node, node) ||
                expr_references_ie(ie_node->binary_interval_expr.left, node) ||
                expr_references_ie(ie_node->binary_interval_expr.right, node);
        break;
    default:
        return true;
    }
    return true;
}

/**
 * Given an interval expression and an AST of expression nodes, update the expressions to point to
 * this IE if they refer exclusively to this IE or its children.
 *
 * The basic algorithm is approximately:
 *
 * for each ie, bottom up
 * for each expr node
 *   for each side of a boolean binary expr node
 *     skip any side which is already assigned
 *     if both sides refer to this bie or its children
 *       then use the side/field of the bie for ones referring to this ie
 *            but use the remapped version for others, and set the remapping on that rule
 *     if one side does not refer to this side or its children
 *       then skip it and replace with Boolean in the code generator
 */
static bool determine_fields_per_ie(
        ast_node *ie_node,
        ast_node *expr_node,
        dictionary *parser_dict,
        dictionary *label_dict,
        dictionary *key_dict,
        data_map *label_map,
        bool is_where_expr
        ) {
    bool success = true, left_refers, right_refers;
    map_key label_id;
    map_value label_value;

    if (!expr_node) {
        return true;
    }
    switch (expr_node->type) {
    case type_unary_expr:
        success = success && determine_fields_per_ie(ie_node, expr_node->unary_expr.operand, parser_dict, label_dict, key_dict, label_map, is_where_expr);

        break;
    case type_binary_expr:
        // recurse down the binary expression unless the side is already assigned to an IE
        if (expr_node->binary_expr.belongs_in == NULL) {
            /* Check if each side refers to this IE or its children.
             * We do this by first recursing down the tree until we find map or time fields, then updating their interval_expression pointers.
             * Once that is done, we can call expr_references_bie on the tree.
             */
            filter_log_msg(LOG_LEVEL_DEBUG, "    IE %p : Recursing left from %p\n", ie_node, expr_node);
            success = success && determine_fields_per_ie(ie_node, expr_node->binary_expr.left, parser_dict, label_dict, key_dict, label_map, is_where_expr);
            filter_log_msg(LOG_LEVEL_DEBUG, "    IE %p : Recursing right from %p\n", ie_node, expr_node);
            success = success && determine_fields_per_ie(ie_node, expr_node->binary_expr.right, parser_dict, label_dict, key_dict, label_map, is_where_expr);

            left_refers = expr_references_ie(ie_node, expr_node->binary_expr.left);
            right_refers = expr_references_ie(ie_node, expr_node->binary_expr.right);

            // if both sides refer to this bie or its children
            if (left_refers && right_refers) {
                filter_log_msg(LOG_LEVEL_DEBUG, "    IE %p : Both sides reference from %p!\n", ie_node, expr_node);
                // then update their interval_expression pointer to this
                expr_node->binary_expr.belongs_in = ie_node;

                // if either side refers not exactly to this, then we must create a remapping to access it
                if (!expr_references_exact_ie(ie_node, expr_node->binary_expr.left)) {
                    filter_log_msg(LOG_LEVEL_DEBUG, "      Not exact reference on left!\n");
                    success = success && remap_field_or_time_mappings(ie_node, expr_node->binary_expr.left, key_dict, is_where_expr);
                }

                if (!expr_references_exact_ie(ie_node, expr_node->binary_expr.right)) {
                    filter_log_msg(LOG_LEVEL_DEBUG, "      Not exact reference on right!\n");
                    success = success && remap_field_or_time_mappings(ie_node, expr_node->binary_expr.right, key_dict, is_where_expr);
                }
            }
        } else {
            filter_log_msg(LOG_LEVEL_DEBUG, "    IE %p : Skipping recursion, interval_expression already set for %p\n", ie_node, expr_node);
        }
        break;
    case type_map_field:
        // first find the label
        label_id = find_word(label_dict, get_word(parser_dict, expr_node->map_field.label));
        if (label_id == WORD_NOT_FOUND) {
            parse_error(expr_node, "Label or interval reference not found");
            success = false;

        } else {
            map_get(label_map, label_id, &label_value);
            if (label_value.type == null_type) {
                parse_error(expr_node, "Label or interval reference not found");
                success = false;

            } else {
                if (label_value.type == SEMANTIC_ERROR_DUP_ID) {
                    parse_error(expr_node, "Duplicate interval identifier referred to in expression.  Add a unique label to fix this (label:id).\n");
                    success = false;
                } else if (label_value.type == SEMANTIC_ERROR_DUP_LABEL) {
                    parse_error(expr_node, "Duplicate interval label referred to in expression.  Labels must be unique if referenced.\n");
                    success = false;
                } else {
                    // set the interval expression referenced by this map label for later ease of access
                    // the binary_interval_expr_node is the value stored in the label_map
                    expr_node->map_field.interval_expression = (ast_node *)label_value.value.pointer;

                    // add the key to the key dictionary
                    expr_node->map_field.resulting_map_key = add_word(key_dict, get_word(parser_dict, expr_node->map_field.map_key));

                    // store the label_id too
                    expr_node->map_field.resulting_label_id = label_id;

                    // get the side of the label to default to
                    success = get_label_side_from_ie(&expr_node->map_field.side, expr_node->map_field.interval_expression, label_id);
                    
                    // We have to try to remap here as well because of the possibility that map expressions 
                    // refer to nested interval expressions.
                    if (!is_where_expr && !expr_references_exact_ie(ie_node, expr_node)) {
                        filter_log_msg(LOG_LEVEL_DEBUG, "      Remapping map key from %u . %u\n", label_id, expr_node->map_field.resulting_map_key);
                        success = success && remap_field_or_time_mappings(ie_node, expr_node, key_dict, is_where_expr);
                    }
                }
            }
        }

        break;
    case type_time_field:
        // first find the label
        label_id = find_word(label_dict, get_word(parser_dict, expr_node->time_field.label));
        if (label_id == WORD_NOT_FOUND) {
            parse_error(expr_node, "Label or interval reference not found");
            success = false;

        } else {
            map_get(label_map, label_id, &label_value);
            if (label_value.type == null_type) {
                parse_error(expr_node, "Label or interval reference not found");
                success = false;

            } else {
                if (label_value.type == SEMANTIC_ERROR_DUP_ID) {
                    parse_error(expr_node, "Duplicate interval identifier referred to in expression.  Add a unique label to fix this (label:id).\n");
                    success = false;
                } else if (label_value.type == SEMANTIC_ERROR_DUP_LABEL) {
                    parse_error(expr_node, "Duplicate interval label referred to in expression.  Labels must be unique if referenced.\n");
                    success = false;
                } else {
                    // set the interval expression referenced by this time field label for later ease of access
                    // the binary_interval_expr_node is the value stored in the label_map
                    expr_node->time_field.interval_expression = (ast_node *)label_value.value.pointer;

                    expr_node->time_field.resulting_label_id = label_id;

                    // get the side of the label to default to
                    success = get_label_side_from_ie(&expr_node->time_field.side, expr_node->time_field.interval_expression, label_id);

                    // We have to try to remap here as well because of the possibility that time expressions 
                    // refer to nested interval expressions.
                    if (!is_where_expr && !expr_references_exact_ie(ie_node, expr_node)) {
                        filter_log_msg(LOG_LEVEL_DEBUG, "      Remapping time field from %u\n", label_id);
                        success = success && remap_field_or_time_mappings(ie_node, expr_node, key_dict, is_where_expr);
                    }
                }
            }
        }


        break;
    case type_map_expr_list:
        success = success && determine_fields_per_ie(ie_node, expr_node->map_expr_list.map_expr, parser_dict, label_dict, key_dict, label_map, is_where_expr);
        success = success && determine_fields_per_ie(ie_node, expr_node->map_expr_list.tail, parser_dict, label_dict, key_dict, label_map, is_where_expr);
        // add map key to the key_dict
        // this map_key is what the "map" keys are being set to
        expr_node->map_expr_list.resulting_map_key = add_word(key_dict, get_word(parser_dict, expr_node->map_expr_list.map_key));
        filter_log_msg(LOG_LEVEL_DEBUG, "      Results go in key %u\n", expr_node->map_expr_list.resulting_map_key);
        break;
    case type_end_points:
        success = success && determine_fields_per_ie(ie_node, expr_node->end_points.begin_expr, parser_dict, label_dict, key_dict, label_map, is_where_expr);
        success = success && determine_fields_per_ie(ie_node, expr_node->end_points.end_expr, parser_dict, label_dict, key_dict, label_map, is_where_expr);
        break;
    default:
        // do nothing
        return success;
    }
    return success;
}

/**
 * Given an AST of BIEs, and an AST of expression nodes, recurse over the BIE nodes
 * calling determine_fields_per_bie for each BIE, bottom-up.
 */
static bool determine_fields_per_rule(
        rule_node  *rule,         /* a reference to the top level rule node */
        ast_node   *interval_expr,/* a reference to the interval expression for which to determine fields, along with its children */
        ast_node   *expr_node,    /* a reference to the expression for which to determine fields */
        dictionary *parser_dict,  /* the parser dictionary */
        dictionary *label_dict,   /* the labels dictionary */
        dictionary *key_dict,     /* the map key dictionary */
        bool       is_where_expr, /* we need to know this so we don't recurse on non-where and because exclusion is only for where */
        bool       is_nested      /* we need to know if an atomic ie is nested because for atomic rules we must still determine fields */
        ) {

    bool success = true;
    /* the map from labels to pointers for the interval expression nodes */
    data_map *label_map;

    /* get the label map from the rule */
    label_map = &rule->label_map;

    if (!interval_expr) {
        return true;
    }

    switch(interval_expr->type) {
    case type_atomic_interval_expr:
        /* do nothing if nested and not separate */
        if (is_nested && !interval_expr->atomic_interval_expr.separate) {
            return true;
        }

        /* otherwise this is an atomic rule and we need to determine fields */
        filter_log_msg(LOG_LEVEL_DEBUG, "  DFPR %p is (%u) where %u, nested %u\n", interval_expr, interval_expr->atomic_interval_expr.label, is_where_expr, is_nested);
        success = determine_fields_per_ie(interval_expr, expr_node, parser_dict, label_dict, key_dict, label_map, is_where_expr);

        break;
    case type_binary_interval_expr:
        /* only recurse down the BIE tree if this is a where expression */
        if (is_where_expr) {
            success = success && determine_fields_per_rule(
                    rule,
                    interval_expr->binary_interval_expr.left,
                    expr_node,
                    parser_dict,
                    label_dict,
                    key_dict,
                    is_where_expr,
                    NESTED_IE);
            success = success && determine_fields_per_rule(
                    rule,
                    interval_expr->binary_interval_expr.right,
                    expr_node,
                    parser_dict,
                    label_dict,
                    key_dict,
                    is_where_expr,
                    NESTED_IE);
        }
        filter_log_msg(LOG_LEVEL_DEBUG, "  DFPR %p is (%u - %u) where %u, nested %u\n", interval_expr, interval_expr->binary_interval_expr.left_name, interval_expr->binary_interval_expr.right_name, is_where_expr, is_nested);
        success = success && determine_fields_per_ie(interval_expr, expr_node, parser_dict, label_dict, key_dict, label_map, is_where_expr);
        break;
    default:
        return false;
    }

    return success;
}

/**
 * Recurse through an expression tree and set the is_non_boolean value for map_fields.
 * is_non_boolean is set when a map field is a child of a non-Boolean expression and cleared when it is a child of a Boolean expression.
 */
#ifndef TEST
static
#endif
void set_map_boolean_type(ast_node *node, bool subfield) {
    bool is_boolean_type;

    if (!node) {
        return;
    }
    switch (node->type) {
    case type_unary_expr:
        // recurse down the hole
        set_map_boolean_type(node->unary_expr.operand, subfield);
        break;
    case type_binary_expr:
        is_boolean_type = node->binary_expr.operator == AND || node->binary_expr.operator == OR;

        set_map_boolean_type(node->binary_expr.left, !is_boolean_type);
        set_map_boolean_type(node->binary_expr.right, !is_boolean_type);
        break;
    case type_map_field:
        node->map_field.is_non_boolean = subfield;
        break;
    default:
        /* nothing */
        return;
    }
}

/**
 * Given a root node, recurse and call determine_fields_per_rule for each rule.
 */
bool determine_fields(
        ast_node *node,
        dictionary *parser_dict,
        dictionary *label_dict,
        dictionary *key_dict
        ) {
    bool success = true;
    if (!node) {
        return true;
    }
    switch (node->type) {
    case type_rule:
        if (node->rule.where_expr) {
            // first set the subfields flag on map_fields
            set_map_boolean_type(node->rule.where_expr, false);
            // exclusions are okay for where clauses, but not for map expressions or end points
            success = success && determine_fields_per_rule(
                    &node->rule,
                    node->rule.interval_expr,
                    node->rule.where_expr,
                    parser_dict,
                    label_dict,
                    key_dict,
                    WHERE_EXPR,
                    NOT_NESTED_IE);
        }
        if (node->rule.map_expr_list) {
            success = success && determine_fields_per_rule(
                    &node->rule,
                    node->rule.interval_expr,
                    node->rule.map_expr_list,
                    parser_dict,
                    label_dict,
                    key_dict,
                    NOT_WHERE_EXPR,
                    NOT_NESTED_IE);
        }
        if (node->rule.end_points) {
            success = success && determine_fields_per_rule(
                    &node->rule,
                    node->rule.interval_expr,
                    node->rule.end_points,
                    parser_dict,
                    label_dict,
                    key_dict,
                    NOT_WHERE_EXPR,
                    NOT_NESTED_IE);
        }
        break;
    case type_rule_list:
        success = success && determine_fields(node->rule_list.head, parser_dict, label_dict, key_dict);
        success = success && determine_fields(node->rule_list.tail, parser_dict, label_dict, key_dict);
        break;
    case type_module_list:
        // skip any modules that aren't imported
        if (node->module_list.imported) {
            success = success && determine_fields(node->module_list.rules, parser_dict, label_dict, key_dict);
        }
        success = success && determine_fields(node->module_list.tail, parser_dict, label_dict, key_dict);
        break;
    default:
        /* nothing */
        return success;
    }
    return success;
}
