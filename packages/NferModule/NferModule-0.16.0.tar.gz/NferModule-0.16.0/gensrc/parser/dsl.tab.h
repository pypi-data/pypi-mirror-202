/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_GENSRC_PARSER_DSL_TAB_H_INCLUDED
# define YY_YY_GENSRC_PARSER_DSL_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 1 "src/dsl/dsl.y"

/*
 * dsl.y
 *
 *  Created on: Apr 20, 2017
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

#include "types.h"
#include "dict.h"
#include "log.h"
#include "ast.h"
#include "semantic.h"
#line 46 "src/dsl/dsl.y"

    #define YYLTYPE YYLTYPE
    typedef location_type YYLTYPE;

#line 85 "gensrc/parser/dsl.tab.h"

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    INTLITERAL = 258,              /* INTLITERAL  */
    FLOATLITERAL = 259,            /* FLOATLITERAL  */
    IDENTIFIER = 260,              /* IDENTIFIER  */
    STRINGLITERAL = 261,           /* STRINGLITERAL  */
    CONSTANT = 262,                /* CONSTANT  */
    LPAREN = 263,                  /* LPAREN  */
    RPAREN = 264,                  /* RPAREN  */
    LBRACE = 265,                  /* LBRACE  */
    RBRACE = 266,                  /* RBRACE  */
    LISTSEP = 267,                 /* LISTSEP  */
    MAPSTO = 268,                  /* MAPSTO  */
    LABELS = 269,                  /* LABELS  */
    MODULE = 270,                  /* MODULE  */
    SILENT = 271,                  /* SILENT  */
    LOUD = 272,                    /* LOUD  */
    IMPORT = 273,                  /* IMPORT  */
    WHERE = 274,                   /* WHERE  */
    MAP = 275,                     /* MAP  */
    BEGINTOKEN = 276,              /* BEGINTOKEN  */
    ENDTOKEN = 277,                /* ENDTOKEN  */
    FIELD = 278,                   /* FIELD  */
    YIELDS = 279,                  /* YIELDS  */
    TRUE = 280,                    /* TRUE  */
    FALSE = 281,                   /* FALSE  */
    EOL = 282,                     /* EOL  */
    UNLESS = 283,                  /* UNLESS  */
    ALSO = 284,                    /* ALSO  */
    BEFORE = 285,                  /* BEFORE  */
    MEET = 286,                    /* MEET  */
    DURING = 287,                  /* DURING  */
    START = 288,                   /* START  */
    FINISH = 289,                  /* FINISH  */
    OVERLAP = 290,                 /* OVERLAP  */
    SLICE = 291,                   /* SLICE  */
    COINCIDE = 292,                /* COINCIDE  */
    AFTER = 293,                   /* AFTER  */
    FOLLOW = 294,                  /* FOLLOW  */
    CONTAIN = 295,                 /* CONTAIN  */
    AND = 296,                     /* AND  */
    OR = 297,                      /* OR  */
    GE = 298,                      /* GE  */
    LE = 299,                      /* LE  */
    EQ = 300,                      /* EQ  */
    NE = 301,                      /* NE  */
    GT = 302,                      /* GT  */
    LT = 303,                      /* LT  */
    PLUS = 304,                    /* PLUS  */
    MINUS = 305,                   /* MINUS  */
    MUL = 306,                     /* MUL  */
    DIV = 307,                     /* DIV  */
    MOD = 308,                     /* MOD  */
    UMINUS = 309,                  /* UMINUS  */
    BANG = 310                     /* BANG  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 39 "src/dsl/dsl.y"

    int64_t int_value;
    double float_value;
    word_id string_value;
    ast_node *node;

#line 164 "gensrc/parser/dsl.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif




int yyparse (void * scanner, dictionary *parser_dict, ast_node **ast_root);

/* "%code provides" blocks.  */
#line 51 "src/dsl/dsl.y"

int yylex(YYSTYPE * yylval_param, YYLTYPE * llocp, void * yyscanner, dictionary *parser_dict);
void yyerror(YYLTYPE * yylloc, void * scanner, dictionary *parser_dict, ast_node **ast_root, const char* message);

#line 197 "gensrc/parser/dsl.tab.h"

#endif /* !YY_YY_GENSRC_PARSER_DSL_TAB_H_INCLUDED  */
