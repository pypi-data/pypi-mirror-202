/*
 * ast.c
 *
 *  Created on: Apr 23, 2017
 *      Author: skauffma
 *
 *    nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2017  Sean Kauffman
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
#include <stdlib.h>
#include <assert.h>
#include "types.h"
#include "dict.h"
#include "map.h"
#include "log.h"
#include "ast.h"

/* if this is included in a test binary, include the testio header to overwrite malloc and free */
#ifdef TEST
    #include "testio.h"
#endif

#define ALLOCATE_AST_NODE_TO_P \
    if ((p = malloc(sizeof(ast_node))) == NULL) { \
        filter_log_msg(LOG_LEVEL_ERROR, "Out of memory in AST construction"); \
        return NULL; \
    }\


ast_node *new_int_literal(long int value, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = loc->last_line;
    p->location.last_column = loc->last_column;

    /* copy information */
    p->type = type_int_literal;
    p->int_literal.value = value;

    return p;
}

ast_node *new_float_literal(double value, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = loc->last_line;
    p->location.last_column = loc->last_column;

    /* copy information */
    p->type = type_float_literal;
    p->float_literal.value = value;

    return p;
}

ast_node *new_string_literal(word_id id, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = loc->last_line;
    p->location.last_column = loc->last_column;

    /* copy information */
    p->type = type_string_literal;
    p->string_literal.id = id;

    return p;
}

ast_node *new_constant_reference(word_id name, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = loc->last_line;
    p->location.last_column = loc->last_column;

    /* copy information */
    p->type = type_constant_reference;
    p->constant_reference.name = name;

    return p;
}

ast_node *new_boolean_literal(bool value, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = loc->last_line;
    p->location.last_column = loc->last_column;

    /* copy information */
    p->type = type_boolean_literal;
    p->boolean_literal.value = value;

    return p;
}

ast_node *new_unary_expr(int op, ast_node *operand, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = operand->location.last_line;
    p->location.last_column = operand->location.last_column;

    /* copy information */
    p->type = type_unary_expr;
    p->unary_expr.operator = op;
    p->unary_expr.operand = operand;

    /* initialize data structures for later analysis */

    return p;
}

ast_node *new_binary_expr(int op, ast_node *left, ast_node *right) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = left->location.first_line;
    p->location.first_column = left->location.first_column;
    p->location.last_line = right->location.last_line;
    p->location.last_column = right->location.last_column;

    /* copy information */
    p->type = type_binary_expr;
    p->binary_expr.operator = op;
    p->binary_expr.left = left;
    p->binary_expr.right = right;

    /* initialize data structures for later analysis */
    p->binary_expr.belongs_in = NULL;

    return p;
}

ast_node *new_map_field(word_id label, word_id map_key, location_type *loc1, location_type *loc2) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc1->first_line;
    p->location.first_column = loc1->first_column;
    p->location.last_line = loc2->last_line;
    p->location.last_column = loc2->last_column;

    /* copy information */
    p->type = type_map_field;
    p->map_field.label = label;
    p->map_field.map_key = map_key;

    /* initialize data structures for later analysis */
    p->map_field.resulting_map_key = MAP_MISSING_KEY;
    p->map_field.side = left_side;
    p->map_field.interval_expression = NULL;
    p->map_field.resulting_label_id = MAP_MISSING_KEY;
    p->map_field.is_non_boolean = true;

    return p;
}
ast_node *new_time_field(int time_field, word_id label, location_type *loc1, location_type *loc2) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc1->first_line;
    p->location.first_column = loc1->first_column;
    p->location.last_line = loc2->last_line;
    p->location.last_column = loc2->last_column;

    /* copy information */
    p->type = type_time_field;
    p->time_field.time_field = time_field;
    p->time_field.label = label;

    /* initialize data structures for later analysis */
    p->time_field.resulting_map_key = MAP_MISSING_KEY;
    p->time_field.side = left_side;
    p->time_field.interval_expression = NULL;
    p->time_field.is_time = true;
    p->time_field.resulting_label_id = MAP_MISSING_KEY;

    return p;
}
ast_node *new_atomic_interval_expr(word_id label, word_id id, location_type *loc1, location_type *loc2) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc1->first_line;
    p->location.first_column = loc1->first_column;
    if (loc2) {
        p->location.last_line = loc2->last_line;
        p->location.last_column = loc2->last_column;
    } else {
        p->location.last_line = loc1->last_line;
        p->location.last_column = loc1->last_column;
    }

    /* copy information */
    p->type = type_atomic_interval_expr;
    p->atomic_interval_expr.label = label;
    p->atomic_interval_expr.id = id;

    /* initialize data structures for later analysis */
    p->atomic_interval_expr.result_id = WORD_NOT_FOUND;
    p->atomic_interval_expr.separate = false;

    p->atomic_interval_expr.field_map = EMPTY_MAP;
    p->atomic_interval_expr.begin_map = WORD_NOT_FOUND;
    p->atomic_interval_expr.end_map = WORD_NOT_FOUND;

    return p;
}
ast_node *new_binary_interval_expr(int op, bool exclusion, ast_node *left, ast_node *right) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = left->location.first_line;
    p->location.first_column = left->location.first_column;
    p->location.last_line = right->location.last_line;
    p->location.last_column = right->location.last_column;

    /* copy information */
    p->type = type_binary_interval_expr;
    p->binary_interval_expr.interval_op = op;
    p->binary_interval_expr.exclusion = exclusion;
    p->binary_interval_expr.left = left;
    p->binary_interval_expr.right = right;

    /* initialize data structures for later analysis */
    p->binary_interval_expr.left_label_map = EMPTY_MAP;
    p->binary_interval_expr.right_label_map = EMPTY_MAP;
    p->binary_interval_expr.left_field_map = EMPTY_MAP;
    p->binary_interval_expr.right_field_map = EMPTY_MAP;

    p->binary_interval_expr.left_begin_map = WORD_NOT_FOUND;
    p->binary_interval_expr.right_begin_map = WORD_NOT_FOUND;
    p->binary_interval_expr.left_end_map = WORD_NOT_FOUND;
    p->binary_interval_expr.right_end_map = WORD_NOT_FOUND;

    return p;
}
ast_node *new_map_expr_list(word_id map_key, ast_node *map_expr, ast_node *tail, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    if (tail) {
        p->location.last_line = tail->location.last_line;
        p->location.last_column = tail->location.last_column;
    } else {
        p->location.last_line = map_expr->location.last_line;
        p->location.last_column = map_expr->location.last_column;
    }

    /* copy information */
    p->type = type_map_expr_list;
    p->map_expr_list.map_key = map_key;
    p->map_expr_list.map_expr = map_expr;
    p->map_expr_list.tail = tail;

    return p;
}
ast_node *new_end_points(ast_node *begin_expr, ast_node *end_expr, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    p->location.last_line = end_expr->location.last_line;
    p->location.last_column = end_expr->location.last_column;

    /* copy information */
    p->type = type_end_points;
    p->end_points.begin_expr = begin_expr;
    p->end_points.end_expr = end_expr;

    return p;
}
ast_node *new_rule(word_id id, ast_node *interval_expr, ast_node *where_expr, ast_node *map_expr_list, ast_node *end_points, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    if (end_points) {
        p->location.last_line = end_points->location.last_line;
        p->location.last_column = end_points->location.last_column;
    } else if (map_expr_list) {
        p->location.last_line = map_expr_list->location.last_line;
        p->location.last_column = map_expr_list->location.last_column;
    } else if (where_expr) {
        p->location.last_line = where_expr->location.last_line;
        p->location.last_column = where_expr->location.last_column;
    } else {
        p->location.last_line = interval_expr->location.last_line;
        p->location.last_column = interval_expr->location.last_column;
    }

    /* copy information */
    p->type = type_rule;
    p->rule.id = id;
    p->rule.interval_expr = interval_expr;
    p->rule.where_expr = where_expr;
    p->rule.map_expr_list = map_expr_list;
    p->rule.end_points = end_points;
    /* initialize data structures for later analysis */
    p->rule.label_map = EMPTY_MAP;
    p->rule.result_id = WORD_NOT_FOUND;
    p->rule.disabled = false;

    return p;
}
ast_node *new_rule_list(ast_node *head, ast_node *tail) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = head->location.first_line;
    p->location.first_column = head->location.first_column;
    if (tail) {
        p->location.last_line = tail->location.last_line;
        p->location.last_column = tail->location.last_column;
    } else {
        p->location.last_line = head->location.last_line;
        p->location.last_column = head->location.last_column;
    }

    /* copy information */
    p->type = type_rule_list;
    p->rule_list.head = head;
    p->rule_list.tail = tail;

    return p;
}
ast_node *new_module_list(word_id id, 
                          ast_node *imports, 
                          ast_node *constants, 
                          ast_node *rules, 
                          ast_node *tail, 
                          location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    if (tail) {
        p->location.last_line = tail->location.last_line;
        p->location.last_column = tail->location.last_column;
    } else if (rules) {
        // it may be that rules is null during, for example, testing or static analysis
        p->location.last_line = rules->location.last_line;
        p->location.last_column = rules->location.last_column;
    } else {
        p->location.last_line = loc->last_line;
        p->location.last_column = loc->last_column;
    }

    /* copy information */
    p->type = type_module_list;
    p->module_list.id = id;
    p->module_list.imports = imports;
    p->module_list.constants = constants;
    p->module_list.rules = rules;
    p->module_list.tail = tail;

    /* initialize data structures for later analysis */
    p->module_list.imported = false;
    p->module_list.silent = false;

    return p;
}
ast_node *new_import_list(word_id import, ast_node *tail, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.last_line = loc->last_line;
    p->location.last_column = loc->last_column;
    if (tail) {
        p->location.first_line = tail->location.first_line;
        p->location.first_column = tail->location.first_column;
    } else {
        p->location.first_line = loc->first_line;
        p->location.first_column = loc->first_column;
    }

    /* copy information */
    p->type = type_import_list;
    p->import_list.import = import;
    p->import_list.tail = tail;

    /* initialize data structures for later analysis */
    p->import_list.silent = false;

    return p;
}
/* this is to stick two import lists together.
   head should never be null */
ast_node * append_import_list(ast_node *head, ast_node *tail) {
    ast_node *node, *last_node;
    assert(node != NULL);

    node = head;
    last_node = NULL;
    // walk the list to the end
    while (node != NULL) {
        last_node = node;
        if (last_node->type == type_import_list) {
            node = last_node->import_list.tail;
        } else if (node->type == type_option_flag) {
            node = last_node->option_flag.child;
        }
    }
    assert(last_node != NULL);
    if (last_node->type == type_import_list) {
        last_node->import_list.tail = tail;
    } else if (node->type == type_option_flag) {
        last_node->option_flag.child = tail;
    }

    return head;
}
/* in practice this is currently only used to specify the silent flag for imports */
ast_node *new_option_flag(int flag, ast_node *child, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    if (child) {
        p->location.last_line = child->location.last_line;
        p->location.last_column = child->location.last_column;
    } else {
        p->location.last_line = loc->last_line;
        p->location.last_column = loc->last_column;
    }

    /* copy information */
    p->type = type_option_flag;
    p->option_flag.flag = flag;
    p->option_flag.child = child;

    return p;
}
/* named constants */
ast_node *new_named_constant(word_id name, ast_node *expr, ast_node *tail, location_type *loc) {
    ast_node *p;

    /* allocate node */
    ALLOCATE_AST_NODE_TO_P

    p->location.first_line = loc->first_line;
    p->location.first_column = loc->first_column;
    if (expr) {
        p->location.last_line = expr->location.last_line;
        p->location.last_column = expr->location.last_column;
    } else {
        p->location.last_line = loc->last_line;
        p->location.last_column = loc->last_column;
    }

    /* copy information */
    p->type = type_named_constant;
    p->named_constant.name = name;
    p->named_constant.expr = expr;
    p->named_constant.tail = tail;

    return p;
}

void parse_error(ast_node *node, const char *message) {
    filter_log_msg(LOG_LEVEL_ERROR, "%s on Lines %d:%d - %d:%d\n", message,
            node->location.first_line, node->location.first_column, node->location.last_line, node->location.last_column);
}

void free_node(ast_node *p) {
    if (!p) return;
    /* free any children first */
    switch(p->type) {
    case type_unary_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free unary_expr %x\n", p);
        free_node(p->unary_expr.operand);
        break;
    case type_binary_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free binary_expr %x\n", p);
        free_node(p->binary_expr.left);
        free_node(p->binary_expr.right);
        break;
    case type_atomic_interval_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free atomic_interval_expr %x\n", p);
        destroy_map(&p->atomic_interval_expr.field_map);
        break;
    case type_binary_interval_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free binary_interval_expr %x\n", p);
        free_node(p->binary_interval_expr.left);
        free_node(p->binary_interval_expr.right);
        destroy_map(&p->binary_interval_expr.left_label_map);
        destroy_map(&p->binary_interval_expr.right_label_map);
        destroy_map(&p->binary_interval_expr.left_field_map);
        destroy_map(&p->binary_interval_expr.right_field_map);
        break;
    case type_map_expr_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free map_expr_list %x\n", p);
        free_node(p->map_expr_list.map_expr);
        free_node(p->map_expr_list.tail);
        break;
    case type_end_points:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free end_points %x\n", p);
        free_node(p->end_points.begin_expr);
        free_node(p->end_points.end_expr);
        break;
    case type_rule:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free rule %x\n", p);
        free_node(p->rule.interval_expr);
        free_node(p->rule.where_expr);
        free_node(p->rule.map_expr_list);
        free_node(p->rule.end_points);
        destroy_map(&p->rule.label_map);
        break;
    case type_rule_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free rule_list %x\n", p);
        free_node(p->rule_list.head);
        free_node(p->rule_list.tail);
        break;
    case type_module_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free module_list %x\n", p);
        free_node(p->module_list.imports);
        free_node(p->module_list.constants);
        free_node(p->module_list.rules);
        free_node(p->module_list.tail);
        break;
    case type_import_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free import_list %x\n", p);
        free_node(p->import_list.tail);
        break;
    case type_option_flag:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free option_flag %x\n", p);
        free_node(p->option_flag.child);
        break;
    case type_named_constant:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Free named_constant %x\n", p);
        free_node(p->named_constant.expr);
        free_node(p->named_constant.tail);
    default:
        break;
    }
    free (p);
}

/**
 * Recursively copy an AST without preserving any extra data structures
 * that are populated during semantic analysis.  This permits using the 
 * worker functions above.
 * 
 * This function is needed for both constant propagation and (once it is
 * implemented) parameterized modules.
 * 
 * @return a pointer to the copy of the node
 */
ast_node * copy_ast(ast_node *p) {
    ast_node *result;

    // copy null :)
    if (p == NULL) {
        return NULL;
    }

    /* depth first recurse */
    switch(p->type) {
    /* unlike with free_node we need to handle the leaves */
    case type_int_literal:
        result = new_int_literal(p->int_literal.value, &p->location);
        break;
    case type_float_literal:
        result = new_float_literal(p->float_literal.value, &p->location);
        break;
    case type_string_literal:
        result = new_string_literal(p->string_literal.id, &p->location);
        break;
    case type_constant_reference:
        result = new_constant_reference(p->constant_reference.name, &p->location);
        break;
    case type_boolean_literal:
        result = new_boolean_literal(p->boolean_literal.value, &p->location);
        break;
    case type_map_field:
        result = new_map_field(p->map_field.label,
                               p->map_field.map_key,
                               &p->location,
                               &p->location);
        break;
    case type_time_field:
        result = new_time_field(p->time_field.time_field,
                                p->time_field.label,
                                &p->location,
                                &p->location);
        break;
    case type_unary_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy unary_expr %x\n", p);
        result = new_unary_expr(p->unary_expr.operator, 
                                copy_ast(p->unary_expr.operand),
                                &p->location
                                );
        break;
    case type_binary_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy binary_expr %x\n", p);
        result = new_binary_expr(p->binary_expr.operator,
                                 copy_ast(p->binary_expr.left),
                                 copy_ast(p->binary_expr.right)
                                 );
        break;
    case type_atomic_interval_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy atomic_interval_expr %x\n", p);
        result = new_atomic_interval_expr(p->atomic_interval_expr.label, 
                                          p->atomic_interval_expr.id, 
                                          &p->location, &p->location
                                          );
        break;
    case type_binary_interval_expr:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy binary_interval_expr %x\n", p);
        result = new_binary_interval_expr(p->binary_interval_expr.interval_op,
                                          p->binary_interval_expr.exclusion,
                                          copy_ast(p->binary_interval_expr.left),
                                          copy_ast(p->binary_interval_expr.right)
                                          );
        break;
    case type_map_expr_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy map_expr_list %x\n", p);
        result = new_map_expr_list(p->map_expr_list.map_key,
                                   copy_ast(p->map_expr_list.map_expr),
                                   copy_ast(p->map_expr_list.tail),
                                   &p->location);
        break;
    case type_end_points:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy end_points %x\n", p);
        result = new_end_points(copy_ast(p->end_points.begin_expr),
                                copy_ast(p->end_points.end_expr),
                                &p->location);
        break;
    case type_rule:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy rule %x\n", p);
        result = new_rule(p->rule.id,
                          copy_ast(p->rule.interval_expr),
                          copy_ast(p->rule.where_expr),
                          copy_ast(p->rule.map_expr_list),
                          copy_ast(p->rule.end_points),
                          &p->location);
        break;
    case type_rule_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy rule_list %x\n", p);
        result = new_rule_list(copy_ast(p->rule_list.head),
                               copy_ast(p->rule_list.tail));
        break;
    case type_module_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy module_list %x\n", p);
        result = new_module_list(p->module_list.id,
                                 copy_ast(p->module_list.imports),
                                 copy_ast(p->module_list.constants),
                                 copy_ast(p->module_list.rules),
                                 copy_ast(p->module_list.tail),
                                 &p->location);
        break;
    case type_import_list:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy import_list %x\n", p);
        result = new_import_list(p->import_list.import,
                                 copy_ast(p->import_list.tail),
                                 &p->location);
        break;
    case type_option_flag:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy option_flag %x\n", p);
        result = new_option_flag(p->option_flag.flag,
                                 copy_ast(p->option_flag.child),
                                 &p->location);
        break;
    case type_named_constant:
        filter_log_msg(LOG_LEVEL_SUPERDEBUG, "-- Copy named_constant %x\n", p);
        result = new_named_constant(p->named_constant.name,
                                    copy_ast(p->named_constant.expr),
                                    copy_ast(p->named_constant.tail),
                                    &p->location);
    }

    return result;
}
