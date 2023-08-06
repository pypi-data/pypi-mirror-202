/*
 * static.c
 *
 *  Created on: Dec 10, 2021
 *      Author: skauffma
 *
 *   nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2021  Sean Kauffman
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
#include "ast.h"
#include "dsl.tab.h"
#include "dict.h"
#include "static.h"
#include "nfer.h"
#include "log.h"


/**
 * Determine if any rule defines custom begin or end timestamps that refer to anything
 * apart from the four input begin and end timestamps.  This is strictly not permitted
 * if one relies on the known complexity classes.
 **/
bool check_computes_ts(ast_node *node) {
    bool does_compute_ts;

    // if we hit a null pointer (end of a list), return
    if (node == NULL) {
        return false;
    }

    /* no preconditions - there are too many node types to make it worth checking */

    // doesn't do it unless we find otherwise
    does_compute_ts = false;

    switch (node->type) {
    case type_time_field:
        // users are allowed to specify end points are just a timestamp from the input
        does_compute_ts = false;
        break;
    case type_end_points:
        does_compute_ts = check_computes_ts(node->end_points.begin_expr) ||
                          check_computes_ts(node->end_points.end_expr);
        break;
    case type_rule:
        does_compute_ts = check_computes_ts(node->rule.end_points);

        break;
    case type_rule_list:
        does_compute_ts = check_computes_ts(node->rule_list.head) ||
                          check_computes_ts(node->rule_list.tail);
        break;
    case type_module_list:
        /* skip any non-imported modules */
        if (node->module_list.imported) {
            does_compute_ts = check_computes_ts(node->module_list.rules);
        }
        does_compute_ts = does_compute_ts || check_computes_ts(node->module_list.tail);
        break;
    default:
        // if we get here, it's because we hit some arithmetic expression in the end points
        // therefore, we got some computation
        does_compute_ts = true;
        filter_log_msg(LOG_LEVEL_DEBUG, "    Found possible arithmetic in end point expression: %d\n", (int)node->type);
        break;
    }
    return does_compute_ts;
}

/**
 * Fold constants in the AST into single nodes instead of trees.
 * The result parameter is populated with the constant value
 * of the node on return, or null if it isn't constant.
 */
void fold_constants(ast_node *node, typed_value *result) {
    typed_value child_value_1, child_value_2;

    // default to the node not being constant
    result->type = null_type;

    if (!node) {
        return;
    }
    switch (node->type) {
    case type_int_literal:
        // set up the result
        result->type = integer_type;
        result->value.integer = node->int_literal.value;
        break;
    case type_float_literal:
        // set up the result
        result->type = real_type;
        result->value.real = node->float_literal.value;
        break;
    case type_boolean_literal:
        // set up the result
        result->type = boolean_type;
        result->value.boolean = node->boolean_literal.value;
        break;
    case type_unary_expr:
        fold_constants(node->unary_expr.operand, &child_value_1);

        if (child_value_1.type != null_type) {
            // it is safe to remove the child, since we have its value
            free_node(node->unary_expr.operand);
            // the result will always be the same as the child node
            result->type = child_value_1.type;

            switch (node->unary_expr.operator) {
            case UMINUS:
                if (child_value_1.type == integer_type) {
                    // change this node's type and value - careful!
                    node->type = type_int_literal;
                    node->int_literal.value = -(child_value_1.value.integer);
                    // set the result
                    result->value.integer = -(child_value_1.value.integer);

                } else if (child_value_1.type == real_type) {
                    // change this node's type and value - careful!
                    node->type = type_float_literal;
                    node->float_literal.value = -(child_value_1.value.real);
                    // set the result
                    result->value.real = -(child_value_1.value.real);
                    
                }
                break;
            case BANG:
                if (child_value_1.type == boolean_type) {
                    // change this node's type and value - careful!
                    node->type = type_boolean_literal;
                    node->boolean_literal.value = !(child_value_1.value.boolean);
                    // set the result
                    result->value.boolean = !(child_value_1.value.boolean);
                    
                }
                break;
            }
        }
        break;
    case type_binary_expr:
        fold_constants(node->binary_expr.left, &child_value_1);
        fold_constants(node->binary_expr.right, &child_value_2);

        // only fold if both are constant
        if (child_value_1.type != null_type && child_value_2.type != null_type) {
            // it is safe to remove the children, since we have their values
            free_node(node->binary_expr.left);
            free_node(node->binary_expr.right);

            // handle each operator separately - it saves small amounts of code
            switch (node->binary_expr.operator) {
            case PLUS:
                if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                    // result is an integer
                    node->type = type_int_literal;
                    node->int_literal.value = child_value_1.value.integer + child_value_2.value.integer;
                    result->type = integer_type;
                    result->value.integer = node->int_literal.value;
                } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                    // result is a real
                    node->type = type_float_literal;
                    node->float_literal.value = child_value_1.value.real + child_value_2.value.real;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                } else {
                    // it's one of each, then
                    // check which is which
                    if (child_value_1.type == real_type) {
                        // left is real
                        node->float_literal.value = child_value_1.value.real + child_value_2.value.integer;
                    } else {
                        // right is real
                        node->float_literal.value = child_value_1.value.integer + child_value_2.value.real;
                    }
                    // result is a real
                    node->type = type_float_literal;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                }
                break;
            case MINUS:
                if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                    // result is an integer
                    node->type = type_int_literal;
                    node->int_literal.value = child_value_1.value.integer - child_value_2.value.integer;
                    result->type = integer_type;
                    result->value.integer = node->int_literal.value;
                } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                    // result is a real
                    node->type = type_float_literal;
                    node->float_literal.value = child_value_1.value.real - child_value_2.value.real;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                } else {
                    // it's one of each, then
                    // check which is which
                    if (child_value_1.type == real_type) {
                        // left is real
                        node->float_literal.value = child_value_1.value.real - child_value_2.value.integer;
                    } else {
                        // right is real
                        node->float_literal.value = child_value_1.value.integer - child_value_2.value.real;
                    }
                    // result is a real
                    node->type = type_float_literal;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                }
                break;
            case MUL:
                if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                    // result is an integer
                    node->type = type_int_literal;
                    node->int_literal.value = child_value_1.value.integer * child_value_2.value.integer;
                    result->type = integer_type;
                    result->value.integer = node->int_literal.value;
                } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                    // result is a real
                    node->type = type_float_literal;
                    node->float_literal.value = child_value_1.value.real * child_value_2.value.real;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                } else {
                    // it's one of each, then
                    // check which is which
                    if (child_value_1.type == real_type) {
                        // left is real
                        node->float_literal.value = child_value_1.value.real * child_value_2.value.integer;
                    } else {
                        // right is real
                        node->float_literal.value = child_value_1.value.integer * child_value_2.value.real;
                    }
                    // result is a real
                    node->type = type_float_literal;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                }
                break;
            case DIV:
                if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                    // result is an integer
                    node->type = type_int_literal;
                    node->int_literal.value = child_value_1.value.integer / child_value_2.value.integer;
                    result->type = integer_type;
                    result->value.integer = node->int_literal.value;
                } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                    // result is a real
                    node->type = type_float_literal;
                    node->float_literal.value = child_value_1.value.real / child_value_2.value.real;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                } else {
                    // it's one of each, then
                    // check which is which
                    if (child_value_1.type == real_type) {
                        // left is real
                        node->float_literal.value = child_value_1.value.real / child_value_2.value.integer;
                    } else {
                        // right is real
                        node->float_literal.value = child_value_1.value.integer / child_value_2.value.real;
                    }
                    // result is a real
                    node->type = type_float_literal;
                    result->type = real_type;
                    result->value.real = node->float_literal.value;
                }
                break;
            case MOD:
                // can't do mod with floats...
                if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                    // result is an integer
                    node->type = type_int_literal;
                    node->int_literal.value = child_value_1.value.integer % child_value_2.value.integer;
                    result->type = integer_type;
                    result->value.integer = node->int_literal.value;
                } 
                break;
            default:
                // we split this into another case so we can share some code since every one of these
                // results in a Boolean value
                node->type = type_boolean_literal;
                result->type = boolean_type;

                switch (node->binary_expr.operator) {
                case GT:
                    if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                        node->boolean_literal.value = child_value_1.value.integer > child_value_2.value.integer;
                    } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                        node->boolean_literal.value = child_value_1.value.real > child_value_2.value.real;
                    } else {
                        // it's one of each, then
                        // check which is which
                        if (child_value_1.type == real_type) {
                            // left is real
                            node->float_literal.value = child_value_1.value.real > child_value_2.value.integer;
                        } else {
                            // right is real
                            node->float_literal.value = child_value_1.value.integer > child_value_2.value.real;
                        }
                    }
                    break;
                case LT:
                    if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                        node->boolean_literal.value = child_value_1.value.integer < child_value_2.value.integer;
                    } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                        node->boolean_literal.value = child_value_1.value.real < child_value_2.value.real;
                    } else {
                        // it's one of each, then
                        // check which is which
                        if (child_value_1.type == real_type) {
                            // left is real
                            node->float_literal.value = child_value_1.value.real < child_value_2.value.integer;
                        } else {
                            // right is real
                            node->float_literal.value = child_value_1.value.integer < child_value_2.value.real;
                        }
                    }
                    break;
                case GE:
                    if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                        node->boolean_literal.value = child_value_1.value.integer >= child_value_2.value.integer;
                    } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                        node->boolean_literal.value = child_value_1.value.real >= child_value_2.value.real;
                    } else {
                        // it's one of each, then
                        // check which is which
                        if (child_value_1.type == real_type) {
                            // left is real
                            node->float_literal.value = child_value_1.value.real >= child_value_2.value.integer;
                        } else {
                            // right is real
                            node->float_literal.value = child_value_1.value.integer >= child_value_2.value.real;
                        }
                    }
                    break;
                case LE:
                    if (child_value_1.type == integer_type && child_value_2.type == integer_type) {
                        node->boolean_literal.value = child_value_1.value.integer <= child_value_2.value.integer;
                    } else if (child_value_1.type == real_type && child_value_2.type == real_type) {
                        node->boolean_literal.value = child_value_1.value.real <= child_value_2.value.real;
                    } else {
                        // it's one of each, then
                        // check which is which
                        if (child_value_1.type == real_type) {
                            // left is real
                            node->float_literal.value = child_value_1.value.real <= child_value_2.value.integer;
                        } else {
                            // right is real
                            node->float_literal.value = child_value_1.value.integer <= child_value_2.value.real;
                        }
                    }
                    break;
                case EQ:
                    // we have logic to handle equals already, so just use that
                    node->boolean_literal.value = equals(&child_value_1, &child_value_2);

                    break;
                case NE:
                    // we have logic to handle equals already, so just use that
                    node->boolean_literal.value = !(equals(&child_value_1, &child_value_2));
                    break;
                
                case AND:
                    // we know the type for logical operators at least
                    node->boolean_literal.value = child_value_1.value.boolean && child_value_2.value.boolean;
                    break;
                case OR:
                    // we know the type for logical operators at least
                    node->boolean_literal.value = child_value_1.value.boolean || child_value_2.value.boolean;
                    break;
                default:
                    /* do nothing */
                    break;
                }
                // copy the value to the result
                result->value.boolean = node->boolean_literal.value;
                break;
            } // switch
        } // if the children are both non-null
        break;
    case type_map_expr_list:
        fold_constants(node->map_expr_list.map_expr, &child_value_1);
        fold_constants(node->map_expr_list.tail, &child_value_2);
        break;
    case type_end_points:
        fold_constants(node->end_points.begin_expr, &child_value_1);
        fold_constants(node->end_points.end_expr, &child_value_2);
        break;
    case type_rule:
        // if a where expression results in a boolean literal, then we can either
        // discard it (if true) or actually discard the whole rule (if false).
        fold_constants(node->rule.where_expr, &child_value_1);

        if (child_value_1.type == boolean_type) {
            // check the value
            if (child_value_1.value.boolean) {
                // we can remove the where expr
                free_node(node->rule.where_expr);
                // set it to null so we don't try to follow a freed pointer
                node->rule.where_expr = NULL;
            } else {
                // the rule will never match, so we can disable it
                // set the flag to ignore the rule
                node->rule.disabled = true;
            }
        }

        // note that, since we don't use the results we can just pass the same pointer
        // we can't pass null, though, since it can be written to if the value is,
        // in fact, constant.
        fold_constants(node->rule.map_expr_list, &child_value_2);
        fold_constants(node->rule.end_points, &child_value_2);

        break;
    case type_rule_list:
        fold_constants(node->rule_list.head, &child_value_1);
        fold_constants(node->rule_list.tail, &child_value_2);
        break;
    case type_module_list:
        // skip any modules that aren't imported
        if (node->module_list.imported) {
            fold_constants(node->module_list.rules, &child_value_1);
        }
        fold_constants(node->module_list.tail, &child_value_2);
        break;
    default:
        /* do nothing */
        break;
    }
}
