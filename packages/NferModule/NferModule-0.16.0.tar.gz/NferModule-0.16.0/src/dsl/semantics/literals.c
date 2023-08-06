/*
 * literals.c
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
#include "dict.h"

/**
 * Populate the string literals in the value dictionary.  Since the dictionary is separate it is nicer to
 * have a separate function to do just this, since all the prior analysis didn't need the value dict.
 */
void populate_string_literals(ast_node *node, dictionary *parser_dict, dictionary *val_dict) {
    if (!node) {
        return;
    }
    switch (node->type) {
    case type_int_literal:
        break;
    case type_float_literal:
        break;
    case type_string_literal:
        node->string_literal.val_dict_id = add_word(val_dict, get_word(parser_dict, node->string_literal.id));
        break;
    case type_boolean_literal:
        break;
    case type_unary_expr:
        populate_string_literals(node->unary_expr.operand, parser_dict, val_dict);
        break;
    case type_binary_expr:
        populate_string_literals(node->binary_expr.left, parser_dict, val_dict);
        populate_string_literals(node->binary_expr.right, parser_dict, val_dict);
        break;
    case type_map_field:
        break;
    case type_time_field:
        break;
    case type_atomic_interval_expr:
        break;
    case type_binary_interval_expr:
        populate_string_literals(node->binary_interval_expr.left, parser_dict, val_dict);
        populate_string_literals(node->binary_interval_expr.right, parser_dict, val_dict);
        break;
    case type_map_expr_list:
        populate_string_literals(node->map_expr_list.map_expr, parser_dict, val_dict);
        populate_string_literals(node->map_expr_list.tail, parser_dict, val_dict);
        break;
    case type_end_points:
        populate_string_literals(node->end_points.begin_expr, parser_dict, val_dict);
        populate_string_literals(node->end_points.end_expr, parser_dict, val_dict);
        break;
    case type_rule:
        populate_string_literals(node->rule.interval_expr, parser_dict, val_dict);
        populate_string_literals(node->rule.where_expr, parser_dict, val_dict);
        populate_string_literals(node->rule.map_expr_list, parser_dict, val_dict);
        populate_string_literals(node->rule.end_points, parser_dict, val_dict);

        break;
    case type_rule_list:
        populate_string_literals(node->rule_list.head, parser_dict, val_dict);
        populate_string_literals(node->rule_list.tail, parser_dict, val_dict);
        break;
    case type_module_list:
        // skip any modules that aren't imported
        if (node->module_list.imported) {
            populate_string_literals(node->module_list.rules, parser_dict, val_dict);
        }
        populate_string_literals(node->module_list.tail, parser_dict, val_dict);
        break;
    default:
        /* do nothing */
        break;
    }
}