/*
 * typecheck.c
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

#include "types.h"
#include "log.h"
#include "ast.h"

#include "dsl.tab.h"

/**
 * Check the types of an AST for sanity.
 * This function walks an AST and checks that the types make sense.
 * That means it checks all the expressions and ensures the types
 * are compatible and tries to guess at what numeric expressions
 * will produce.
 * If there is a problem with types, say from a string being used
 * in a Boolean expression, then it will call parse_error and return
 * an error type.
 * If there is no error, then it will return the type of the root
 * node of the tree or null if the root isn't part of a checkable
 * expression.
 */
ast_value_type check_types(ast_node *node) {
    ast_value_type value_type, child_type_1, child_type_2;

    if (!node) {
        return null;
    }
    // if it isn't reset later on, then it's an error
    value_type = error;

    switch (node->type) {
    case type_int_literal:
        value_type = integer;
        break;
    case type_float_literal:
        value_type = real;
        break;
    case type_string_literal:
        value_type = string;
        break;
    case type_boolean_literal:
        value_type = boolean;
        break;
    case type_unary_expr:
        child_type_1 = check_types(node->unary_expr.operand);

        switch (node->unary_expr.operator) {
        case UMINUS:
            if (child_type_1 == integer || child_type_1 == real || child_type_1 == duck) {
                value_type = child_type_1;
            }
            break;
        case BANG:
            if (child_type_1 == boolean || child_type_1 == duck) {
                value_type = child_type_1;
            }
            break;
        }
        break;
    case type_binary_expr:
        child_type_1 = check_types(node->binary_expr.left);
        child_type_2 = check_types(node->binary_expr.right);

        switch (node->binary_expr.operator) {
        case PLUS:
        case MINUS:
        case MUL:
        case DIV:
            if (child_type_1 == integer) {
                if (child_type_2 == integer || child_type_2 == duck) {
                    value_type = integer;
                } else if (child_type_2 == real) {
                    value_type = real;
                }
            } else if (child_type_1 == real) {
                if (child_type_2 == integer || child_type_2 == real || child_type_2 == duck) {
                    value_type = real;
                }
            } else if (child_type_1 == duck) {
                if (child_type_2 == integer || child_type_2 == duck) {
                    value_type = integer;
                } else if (child_type_2 == real) {
                    value_type = real;
                }
            }
            break;
        case MOD:
            if (child_type_1 == integer) {
                if (child_type_2 == integer || child_type_2 == duck) {
                    value_type = integer;
                }
            } else if (child_type_1 == duck) {
                if (child_type_2 == integer || child_type_2 == duck) {
                    value_type = integer;
                }
            }
            break;

        case GT:
        case LT:
        case GE:
        case LE:
            if ((child_type_1 == integer || child_type_1 == real || child_type_1 == duck) &&
                    (child_type_2 == integer || child_type_2 == real || child_type_2 == duck)) {
                value_type = boolean;
            }
            break;
        case EQ:
        case NE:
            if (
                    (
                        (child_type_1 == integer || child_type_1 == real || child_type_1 == duck) &&
                        (child_type_2 == integer || child_type_2 == real || child_type_2 == duck)
                    ) ||
                    (
                        (child_type_1 == string || child_type_1 == duck) &&
                        (child_type_2 == string || child_type_2 == duck)
                    )
            ) {
                value_type = boolean;
            }
            break;
        case AND:
        case OR:
            if ((child_type_1 == boolean || child_type_1 == duck) &&
                    (child_type_2 == boolean || child_type_2 == duck)) {
                value_type = boolean;
            }
            break;
        }
        break;
    case type_map_field:
        value_type = duck;
        break;
    case type_time_field:
        value_type = integer;
        break;
    case type_map_expr_list:
        child_type_1 = check_types(node->map_expr_list.map_expr);
        child_type_2 = check_types(node->map_expr_list.tail);
        if (child_type_1 != error && child_type_2 == null) {
            value_type = null;
        }
        break;
    case type_end_points:
        child_type_1 = check_types(node->end_points.begin_expr);
        child_type_2 = check_types(node->end_points.end_expr);
        if ((child_type_1 == integer || child_type_1 == duck) &&
                (child_type_2 == integer || child_type_2 == duck)) {
            value_type = integer;
        }
        break;
    case type_rule:
        if (node->rule.where_expr) {
            child_type_1 = check_types(node->rule.where_expr);
        } else {
            child_type_1 = duck;
        }

        if (child_type_1 == boolean || child_type_1 == duck) {
            if (check_types(node->rule.map_expr_list) != error) {
                if (check_types(node->rule.end_points) != error) {
                    value_type = null;
                }
            }
        }

        break;
    case type_rule_list:
        if (check_types(node->rule_list.head) != error &&
            check_types(node->rule_list.tail) != error) {
            value_type = null;
        }
        break;
    case type_module_list:
        // skip modules that aren't imported
        if (node->module_list.imported) {
            if(check_types(node->module_list.rules) != error &&
                check_types(node->module_list.tail) != error) {
                value_type = null;
            }
        } else {
            if(check_types(node->module_list.tail) != error) {
                value_type = null;
            }
        }
        break;
    default:
        return null;
    }

    if (value_type == error) {
        parse_error(node, "Type checking error");
    }
    return value_type;
}