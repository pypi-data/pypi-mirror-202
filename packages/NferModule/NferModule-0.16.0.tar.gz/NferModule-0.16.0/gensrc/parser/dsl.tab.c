/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 2

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1





# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "dsl.tab.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_INTLITERAL = 3,                 /* INTLITERAL  */
  YYSYMBOL_FLOATLITERAL = 4,               /* FLOATLITERAL  */
  YYSYMBOL_IDENTIFIER = 5,                 /* IDENTIFIER  */
  YYSYMBOL_STRINGLITERAL = 6,              /* STRINGLITERAL  */
  YYSYMBOL_CONSTANT = 7,                   /* CONSTANT  */
  YYSYMBOL_LPAREN = 8,                     /* LPAREN  */
  YYSYMBOL_RPAREN = 9,                     /* RPAREN  */
  YYSYMBOL_LBRACE = 10,                    /* LBRACE  */
  YYSYMBOL_RBRACE = 11,                    /* RBRACE  */
  YYSYMBOL_LISTSEP = 12,                   /* LISTSEP  */
  YYSYMBOL_MAPSTO = 13,                    /* MAPSTO  */
  YYSYMBOL_LABELS = 14,                    /* LABELS  */
  YYSYMBOL_MODULE = 15,                    /* MODULE  */
  YYSYMBOL_SILENT = 16,                    /* SILENT  */
  YYSYMBOL_LOUD = 17,                      /* LOUD  */
  YYSYMBOL_IMPORT = 18,                    /* IMPORT  */
  YYSYMBOL_WHERE = 19,                     /* WHERE  */
  YYSYMBOL_MAP = 20,                       /* MAP  */
  YYSYMBOL_BEGINTOKEN = 21,                /* BEGINTOKEN  */
  YYSYMBOL_ENDTOKEN = 22,                  /* ENDTOKEN  */
  YYSYMBOL_FIELD = 23,                     /* FIELD  */
  YYSYMBOL_YIELDS = 24,                    /* YIELDS  */
  YYSYMBOL_TRUE = 25,                      /* TRUE  */
  YYSYMBOL_FALSE = 26,                     /* FALSE  */
  YYSYMBOL_EOL = 27,                       /* EOL  */
  YYSYMBOL_UNLESS = 28,                    /* UNLESS  */
  YYSYMBOL_ALSO = 29,                      /* ALSO  */
  YYSYMBOL_BEFORE = 30,                    /* BEFORE  */
  YYSYMBOL_MEET = 31,                      /* MEET  */
  YYSYMBOL_DURING = 32,                    /* DURING  */
  YYSYMBOL_START = 33,                     /* START  */
  YYSYMBOL_FINISH = 34,                    /* FINISH  */
  YYSYMBOL_OVERLAP = 35,                   /* OVERLAP  */
  YYSYMBOL_SLICE = 36,                     /* SLICE  */
  YYSYMBOL_COINCIDE = 37,                  /* COINCIDE  */
  YYSYMBOL_AFTER = 38,                     /* AFTER  */
  YYSYMBOL_FOLLOW = 39,                    /* FOLLOW  */
  YYSYMBOL_CONTAIN = 40,                   /* CONTAIN  */
  YYSYMBOL_AND = 41,                       /* AND  */
  YYSYMBOL_OR = 42,                        /* OR  */
  YYSYMBOL_GE = 43,                        /* GE  */
  YYSYMBOL_LE = 44,                        /* LE  */
  YYSYMBOL_EQ = 45,                        /* EQ  */
  YYSYMBOL_NE = 46,                        /* NE  */
  YYSYMBOL_GT = 47,                        /* GT  */
  YYSYMBOL_LT = 48,                        /* LT  */
  YYSYMBOL_PLUS = 49,                      /* PLUS  */
  YYSYMBOL_MINUS = 50,                     /* MINUS  */
  YYSYMBOL_MUL = 51,                       /* MUL  */
  YYSYMBOL_DIV = 52,                       /* DIV  */
  YYSYMBOL_MOD = 53,                       /* MOD  */
  YYSYMBOL_UMINUS = 54,                    /* UMINUS  */
  YYSYMBOL_BANG = 55,                      /* BANG  */
  YYSYMBOL_YYACCEPT = 56,                  /* $accept  */
  YYSYMBOL_specification = 57,             /* specification  */
  YYSYMBOL_module_list = 58,               /* module_list  */
  YYSYMBOL_imports = 59,                   /* imports  */
  YYSYMBOL_import = 60,                    /* import  */
  YYSYMBOL_identifier_list = 61,           /* identifier_list  */
  YYSYMBOL_constant = 62,                  /* constant  */
  YYSYMBOL_rule_list = 63,                 /* rule_list  */
  YYSYMBOL_rule = 64,                      /* rule  */
  YYSYMBOL_where_expr = 65,                /* where_expr  */
  YYSYMBOL_map_expr = 66,                  /* map_expr  */
  YYSYMBOL_map_expr_list = 67,             /* map_expr_list  */
  YYSYMBOL_end_points = 68,                /* end_points  */
  YYSYMBOL_interval_expr = 69,             /* interval_expr  */
  YYSYMBOL_const_expr = 70,                /* const_expr  */
  YYSYMBOL_expr = 71                       /* expr  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;




#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_uint8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if 1

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* 1 */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL \
             && defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
  YYLTYPE yyls_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE) \
             + YYSIZEOF (YYLTYPE)) \
      + 2 * YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  11
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   272

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  56
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  16
/* YYNRULES -- Number of rules.  */
#define YYNRULES  89
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  180

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   310


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint8 yyrline[] =
{
       0,    76,    76,    77,    78,    83,    84,    85,    86,    90,
      91,    95,    96,   100,   101,   105,   106,   110,   111,   115,
     119,   120,   124,   125,   129,   130,   134,   135,   139,   140,
     141,   142,   143,   144,   145,   146,   147,   148,   149,   150,
     151,   152,   153,   157,   158,   159,   160,   161,   162,   163,
     164,   165,   166,   167,   168,   169,   170,   171,   172,   173,
     174,   175,   176,   177,   178,   182,   183,   184,   185,   186,
     187,   188,   189,   190,   191,   192,   193,   194,   195,   196,
     197,   198,   199,   200,   201,   202,   203,   204,   205,   206
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if 1
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "INTLITERAL",
  "FLOATLITERAL", "IDENTIFIER", "STRINGLITERAL", "CONSTANT", "LPAREN",
  "RPAREN", "LBRACE", "RBRACE", "LISTSEP", "MAPSTO", "LABELS", "MODULE",
  "SILENT", "LOUD", "IMPORT", "WHERE", "MAP", "BEGINTOKEN", "ENDTOKEN",
  "FIELD", "YIELDS", "TRUE", "FALSE", "EOL", "UNLESS", "ALSO", "BEFORE",
  "MEET", "DURING", "START", "FINISH", "OVERLAP", "SLICE", "COINCIDE",
  "AFTER", "FOLLOW", "CONTAIN", "AND", "OR", "GE", "LE", "EQ", "NE", "GT",
  "LT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "UMINUS", "BANG", "$accept",
  "specification", "module_list", "imports", "import", "identifier_list",
  "constant", "rule_list", "rule", "where_expr", "map_expr",
  "map_expr_list", "end_points", "interval_expr", "const_expr", "expr", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-71)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  ((Yyn) == YYTABLE_NINF)

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int16 yypact[] =
{
      28,   -13,     5,    21,    -1,    35,    56,   -71,    36,    12,
      86,   -71,    92,   -11,    56,    76,   -71,    89,    36,   133,
     -71,   -71,   -71,   -71,    12,   -71,   -71,    12,    12,   162,
     -71,    99,    12,   106,    93,    65,    78,    36,    36,    36,
      36,    36,    36,    36,    36,    36,   111,    33,   -71,   -71,
      12,    12,    12,    12,    12,    12,    12,    12,    12,    12,
      12,    12,    12,    94,   -71,   162,   -71,   -71,   -71,   -71,
      90,   -71,    65,   -71,   -71,    65,    65,   175,    36,    36,
      36,   222,   222,   222,   222,   222,   222,   222,   222,   222,
     104,    98,   -71,   186,   186,   123,   123,   123,   123,   123,
     123,   105,   105,   -71,   -71,   -71,   115,   129,   -71,    35,
      -2,    94,    14,    97,   -71,   -71,    65,    65,    65,    65,
      65,    65,    65,    65,    65,    65,    65,    65,    65,   222,
     222,   222,   132,    65,   -71,   129,   -71,    -5,    34,   -71,
      35,    83,   -71,   -71,   -71,   -71,   197,   197,   211,   211,
     211,   211,   211,   211,   214,   214,   -71,   -71,   -71,   140,
      81,   149,    60,   263,   -71,   -71,    84,   -71,    65,   -71,
     264,    65,   -71,   -71,   -71,   175,   257,   175,    65,   175
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       0,     0,     0,     0,     4,     0,     3,    17,     0,     0,
       0,     1,     0,     0,     2,     0,    18,    29,     0,    21,
      43,    44,    46,    45,     0,    47,    48,     0,     0,    15,
      10,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,    23,     0,    49,    50,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,    10,    16,    28,    42,    65,    66,
      68,    67,     0,    69,    70,     0,     0,    20,     0,     0,
       0,    30,    31,    32,    33,    34,    35,    36,    37,    38,
       0,    27,    64,    62,    63,    58,    59,    61,    60,    57,
      56,    54,    55,    51,    52,    53,     0,     0,     9,     0,
       0,     0,     0,     0,    71,    72,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,    39,
      40,    41,     0,     0,    19,     0,    13,     0,     0,     6,
       0,     0,    86,    87,    88,    89,    84,    85,    80,    81,
      83,    82,    79,    78,    76,    77,    73,    74,    75,     0,
       0,     0,     0,     0,    11,     5,     0,     8,     0,    22,
       0,     0,    12,    14,     7,    24,     0,    26,     0,    25
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
     -71,   -71,   -71,   207,   -71,   137,   -51,    -4,    -6,   -71,
     -71,   -71,   -71,   -14,   127,   -70
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_uint8 yydefgoto[] =
{
       0,     3,     4,    63,   108,   137,     5,     6,     7,    46,
      91,   160,   134,    19,    29,    77
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
      16,    14,   113,    15,    34,   114,   115,   163,    16,   139,
      10,     8,   109,     8,    12,    20,    21,    22,    23,   142,
      24,    11,   164,    81,    82,    83,    84,    85,    86,    87,
      88,    89,     9,     1,    32,   143,   144,    25,    26,    15,
      13,    17,    92,     2,    18,   165,   146,   147,   148,   149,
     150,   151,   152,   153,   154,   155,   156,   157,   158,   110,
     140,    15,    27,   161,   129,   130,   131,    28,    68,    69,
      70,    71,   163,    72,    50,    51,    52,    53,    54,    55,
      56,    57,    58,    59,    60,    61,    62,   172,    15,    15,
      73,    74,   169,   170,   167,   174,    30,    31,   175,     1,
       8,   177,    67,    33,    16,   138,   145,   141,   179,    64,
     106,    66,   107,   112,   132,    75,    78,    79,    80,   133,
      76,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    90,    16,   135,   136,    16,   166,   159,   116,   117,
     118,   119,   120,   121,   122,   123,   124,   125,   126,   127,
     128,    47,    35,   168,    48,    49,    60,    61,    62,    65,
      16,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,   171,    58,    59,    60,    61,    62,    93,    94,    95,
      96,    97,    98,    99,   100,   101,   102,   103,   104,   105,
     116,   117,   118,   119,   120,   121,   122,   123,   124,   125,
     126,   127,   128,    50,    51,    52,    53,    54,    55,    56,
      57,    58,    59,    60,    61,    62,   116,   117,   118,   119,
     120,   121,   122,   123,   124,   125,   126,   127,   128,    52,
      53,    54,    55,    56,    57,    58,    59,    60,    61,    62,
     118,   119,   120,   121,   122,   123,   124,   125,   126,   127,
     128,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
     124,   125,   126,   127,   128,   126,   127,   128,   173,   176,
     178,   111,   162
};

static const yytype_uint8 yycheck[] =
{
       6,     5,    72,     5,    18,    75,    76,    12,    14,    11,
       5,    24,    63,    24,    15,     3,     4,     5,     6,     5,
       8,     0,    27,    37,    38,    39,    40,    41,    42,    43,
      44,    45,    45,     5,    45,    21,    22,    25,    26,     5,
       5,     5,     9,    15,     8,    11,   116,   117,   118,   119,
     120,   121,   122,   123,   124,   125,   126,   127,   128,    63,
     111,     5,    50,   133,    78,    79,    80,    55,     3,     4,
       5,     6,    12,     8,    41,    42,    43,    44,    45,    46,
      47,    48,    49,    50,    51,    52,    53,    27,     5,     5,
      25,    26,    11,    12,    11,    11,    10,     5,   168,     5,
      24,   171,     9,    14,   110,   109,     9,   111,   178,    10,
      16,     5,    18,    23,    10,    50,    38,    39,    40,    21,
      55,    28,    29,    30,    31,    32,    33,    34,    35,    36,
      37,    20,   138,    18,     5,   141,   140,     5,    41,    42,
      43,    44,    45,    46,    47,    48,    49,    50,    51,    52,
      53,    24,    19,    13,    27,    28,    51,    52,    53,    32,
     166,    28,    29,    30,    31,    32,    33,    34,    35,    36,
      37,    22,    49,    50,    51,    52,    53,    50,    51,    52,
      53,    54,    55,    56,    57,    58,    59,    60,    61,    62,
      41,    42,    43,    44,    45,    46,    47,    48,    49,    50,
      51,    52,    53,    41,    42,    43,    44,    45,    46,    47,
      48,    49,    50,    51,    52,    53,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    43,
      44,    45,    46,    47,    48,    49,    50,    51,    52,    53,
      43,    44,    45,    46,    47,    48,    49,    50,    51,    52,
      53,    29,    30,    31,    32,    33,    34,    35,    36,    37,
      49,    50,    51,    52,    53,    51,    52,    53,     5,     5,
      13,    64,   135
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,     5,    15,    57,    58,    62,    63,    64,    24,    45,
       5,     0,    15,     5,    63,     5,    64,     5,     8,    69,
       3,     4,     5,     6,     8,    25,    26,    50,    55,    70,
      10,     5,    45,    14,    69,    19,    28,    29,    30,    31,
      32,    33,    34,    35,    36,    37,    65,    70,    70,    70,
      41,    42,    43,    44,    45,    46,    47,    48,    49,    50,
      51,    52,    53,    59,    10,    70,     5,     9,     3,     4,
       5,     6,     8,    25,    26,    50,    55,    71,    38,    39,
      40,    69,    69,    69,    69,    69,    69,    69,    69,    69,
      20,    66,     9,    70,    70,    70,    70,    70,    70,    70,
      70,    70,    70,    70,    70,    70,    16,    18,    60,    62,
      63,    59,    23,    71,    71,    71,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    69,
      69,    69,    10,    21,    68,    18,     5,    61,    63,    11,
      62,    63,     5,    21,    22,     9,    71,    71,    71,    71,
      71,    71,    71,    71,    71,    71,    71,    71,    71,     5,
      67,    71,    61,    12,    27,    11,    63,    11,    13,    11,
      12,    22,    27,     5,    11,    71,     5,    71,    13,    71
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    56,    57,    57,    57,    58,    58,    58,    58,    59,
      59,    60,    60,    61,    61,    62,    62,    63,    63,    64,
      65,    65,    66,    66,    67,    67,    68,    68,    69,    69,
      69,    69,    69,    69,    69,    69,    69,    69,    69,    69,
      69,    69,    69,    70,    70,    70,    70,    70,    70,    70,
      70,    70,    70,    70,    70,    70,    70,    70,    70,    70,
      70,    70,    70,    70,    70,    71,    71,    71,    71,    71,
      71,    71,    71,    71,    71,    71,    71,    71,    71,    71,
      71,    71,    71,    71,    71,    71,    71,    71,    71,    71
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     2,     1,     1,     7,     6,     8,     7,     2,
       0,     3,     4,     1,     3,     3,     4,     1,     2,     6,
       2,     0,     4,     0,     3,     5,     4,     0,     3,     1,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     4,
       4,     4,     3,     1,     1,     1,     1,     1,     1,     2,
       2,     3,     3,     3,     3,     3,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     1,     1,     1,     1,     1,
       1,     2,     2,     3,     3,     3,     3,     3,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     3
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (&yylloc, scanner, parser_dict, ast_root, YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF

/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)                                \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;        \
          (Current).first_column = YYRHSLOC (Rhs, 1).first_column;      \
          (Current).last_line    = YYRHSLOC (Rhs, N).last_line;         \
          (Current).last_column  = YYRHSLOC (Rhs, N).last_column;       \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).first_line   = (Current).last_line   =              \
            YYRHSLOC (Rhs, 0).last_line;                                \
          (Current).first_column = (Current).last_column =              \
            YYRHSLOC (Rhs, 0).last_column;                              \
        }                                                               \
    while (0)
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K])


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)


/* YYLOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

# ifndef YYLOCATION_PRINT

#  if defined YY_LOCATION_PRINT

   /* Temporary convenience wrapper in case some people defined the
      undocumented and private YY_LOCATION_PRINT macros.  */
#   define YYLOCATION_PRINT(File, Loc)  YY_LOCATION_PRINT(File, *(Loc))

#  elif defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL

/* Print *YYLOCP on YYO.  Private, do not rely on its existence. */

YY_ATTRIBUTE_UNUSED
static int
yy_location_print_ (FILE *yyo, YYLTYPE const * const yylocp)
{
  int res = 0;
  int end_col = 0 != yylocp->last_column ? yylocp->last_column - 1 : 0;
  if (0 <= yylocp->first_line)
    {
      res += YYFPRINTF (yyo, "%d", yylocp->first_line);
      if (0 <= yylocp->first_column)
        res += YYFPRINTF (yyo, ".%d", yylocp->first_column);
    }
  if (0 <= yylocp->last_line)
    {
      if (yylocp->first_line < yylocp->last_line)
        {
          res += YYFPRINTF (yyo, "-%d", yylocp->last_line);
          if (0 <= end_col)
            res += YYFPRINTF (yyo, ".%d", end_col);
        }
      else if (0 <= end_col && yylocp->first_column < end_col)
        res += YYFPRINTF (yyo, "-%d", end_col);
    }
  return res;
}

#   define YYLOCATION_PRINT  yy_location_print_

    /* Temporary convenience wrapper in case some people defined the
       undocumented and private YY_LOCATION_PRINT macros.  */
#   define YY_LOCATION_PRINT(File, Loc)  YYLOCATION_PRINT(File, &(Loc))

#  else

#   define YYLOCATION_PRINT(File, Loc) ((void) 0)
    /* Temporary convenience wrapper in case some people defined the
       undocumented and private YY_LOCATION_PRINT macros.  */
#   define YY_LOCATION_PRINT  YYLOCATION_PRINT

#  endif
# endif /* !defined YYLOCATION_PRINT */


# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value, Location, scanner, parser_dict, ast_root); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, void * scanner, dictionary *parser_dict, ast_node **ast_root)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  YY_USE (yylocationp);
  YY_USE (scanner);
  YY_USE (parser_dict);
  YY_USE (ast_root);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, void * scanner, dictionary *parser_dict, ast_node **ast_root)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  YYLOCATION_PRINT (yyo, yylocationp);
  YYFPRINTF (yyo, ": ");
  yy_symbol_value_print (yyo, yykind, yyvaluep, yylocationp, scanner, parser_dict, ast_root);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp, YYLTYPE *yylsp,
                 int yyrule, void * scanner, dictionary *parser_dict, ast_node **ast_root)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)],
                       &(yylsp[(yyi + 1) - (yynrhs)]), scanner, parser_dict, ast_root);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, yylsp, Rule, scanner, parser_dict, ast_root); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


/* Context of a parse error.  */
typedef struct
{
  yy_state_t *yyssp;
  yysymbol_kind_t yytoken;
  YYLTYPE *yylloc;
} yypcontext_t;

/* Put in YYARG at most YYARGN of the expected tokens given the
   current YYCTX, and return the number of tokens stored in YYARG.  If
   YYARG is null, return the number of expected tokens (guaranteed to
   be less than YYNTOKENS).  Return YYENOMEM on memory exhaustion.
   Return 0 if there are more than YYARGN expected tokens, yet fill
   YYARG up to YYARGN. */
static int
yypcontext_expected_tokens (const yypcontext_t *yyctx,
                            yysymbol_kind_t yyarg[], int yyargn)
{
  /* Actual size of YYARG. */
  int yycount = 0;
  int yyn = yypact[+*yyctx->yyssp];
  if (!yypact_value_is_default (yyn))
    {
      /* Start YYX at -YYN if negative to avoid negative indexes in
         YYCHECK.  In other words, skip the first -YYN actions for
         this state because they are default actions.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;
      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yyx;
      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
        if (yycheck[yyx + yyn] == yyx && yyx != YYSYMBOL_YYerror
            && !yytable_value_is_error (yytable[yyx + yyn]))
          {
            if (!yyarg)
              ++yycount;
            else if (yycount == yyargn)
              return 0;
            else
              yyarg[yycount++] = YY_CAST (yysymbol_kind_t, yyx);
          }
    }
  if (yyarg && yycount == 0 && 0 < yyargn)
    yyarg[0] = YYSYMBOL_YYEMPTY;
  return yycount;
}




#ifndef yystrlen
# if defined __GLIBC__ && defined _STRING_H
#  define yystrlen(S) (YY_CAST (YYPTRDIFF_T, strlen (S)))
# else
/* Return the length of YYSTR.  */
static YYPTRDIFF_T
yystrlen (const char *yystr)
{
  YYPTRDIFF_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
# endif
#endif

#ifndef yystpcpy
# if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#  define yystpcpy stpcpy
# else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
# endif
#endif

#ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYPTRDIFF_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYPTRDIFF_T yyn = 0;
      char const *yyp = yystr;
      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            else
              goto append;

          append:
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (yyres)
    return yystpcpy (yyres, yystr) - yyres;
  else
    return yystrlen (yystr);
}
#endif


static int
yy_syntax_error_arguments (const yypcontext_t *yyctx,
                           yysymbol_kind_t yyarg[], int yyargn)
{
  /* Actual size of YYARG. */
  int yycount = 0;
  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yyctx->yytoken != YYSYMBOL_YYEMPTY)
    {
      int yyn;
      if (yyarg)
        yyarg[yycount] = yyctx->yytoken;
      ++yycount;
      yyn = yypcontext_expected_tokens (yyctx,
                                        yyarg ? yyarg + 1 : yyarg, yyargn - 1);
      if (yyn == YYENOMEM)
        return YYENOMEM;
      else
        yycount += yyn;
    }
  return yycount;
}

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return -1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return YYENOMEM if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYPTRDIFF_T *yymsg_alloc, char **yymsg,
                const yypcontext_t *yyctx)
{
  enum { YYARGS_MAX = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat: reported tokens (one for the "unexpected",
     one per "expected"). */
  yysymbol_kind_t yyarg[YYARGS_MAX];
  /* Cumulated lengths of YYARG.  */
  YYPTRDIFF_T yysize = 0;

  /* Actual size of YYARG. */
  int yycount = yy_syntax_error_arguments (yyctx, yyarg, YYARGS_MAX);
  if (yycount == YYENOMEM)
    return YYENOMEM;

  switch (yycount)
    {
#define YYCASE_(N, S)                       \
      case N:                               \
        yyformat = S;                       \
        break
    default: /* Avoid compiler warnings. */
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
    }

  /* Compute error message size.  Don't count the "%s"s, but reserve
     room for the terminator.  */
  yysize = yystrlen (yyformat) - 2 * yycount + 1;
  {
    int yyi;
    for (yyi = 0; yyi < yycount; ++yyi)
      {
        YYPTRDIFF_T yysize1
          = yysize + yytnamerr (YY_NULLPTR, yytname[yyarg[yyi]]);
        if (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM)
          yysize = yysize1;
        else
          return YYENOMEM;
      }
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return -1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yytname[yyarg[yyi++]]);
          yyformat += 2;
        }
      else
        {
          ++yyp;
          ++yyformat;
        }
  }
  return 0;
}


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep, YYLTYPE *yylocationp, void * scanner, dictionary *parser_dict, ast_node **ast_root)
{
  YY_USE (yyvaluep);
  YY_USE (yylocationp);
  YY_USE (scanner);
  YY_USE (parser_dict);
  YY_USE (ast_root);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}






/*----------.
| yyparse.  |
`----------*/

int
yyparse (void * scanner, dictionary *parser_dict, ast_node **ast_root)
{
/* Lookahead token kind.  */
int yychar;


/* The semantic value of the lookahead symbol.  */
/* Default value used for initialization, for pacifying older GCCs
   or non-GCC compilers.  */
YY_INITIAL_VALUE (static YYSTYPE yyval_default;)
YYSTYPE yylval YY_INITIAL_VALUE (= yyval_default);

/* Location data for the lookahead symbol.  */
static YYLTYPE yyloc_default
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
  = { 1, 1, 1, 1 }
# endif
;
YYLTYPE yylloc = yyloc_default;

    /* Number of syntax errors so far.  */
    int yynerrs = 0;

    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

    /* The location stack: array, bottom, top.  */
    YYLTYPE yylsa[YYINITDEPTH];
    YYLTYPE *yyls = yylsa;
    YYLTYPE *yylsp = yyls;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;
  YYLTYPE yyloc;

  /* The locations where the error started and ended.  */
  YYLTYPE yyerror_range[3];

  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYPTRDIFF_T yymsg_alloc = sizeof yymsgbuf;

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N), yylsp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  yylsp[0] = yylloc;
  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;
        YYLTYPE *yyls1 = yyls;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yyls1, yysize * YYSIZEOF (*yylsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
        yyls = yyls1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
        YYSTACK_RELOCATE (yyls_alloc, yyls);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;
      yylsp = yyls + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex (&yylval, &yylloc, scanner, parser_dict);
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      yyerror_range[1] = yylloc;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END
  *++yylsp = yylloc;

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];

  /* Default location. */
  YYLLOC_DEFAULT (yyloc, (yylsp - yylen), yylen);
  yyerror_range[1] = yyloc;
  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2: /* specification: constant rule_list  */
#line 76 "src/dsl/dsl.y"
                                 { *ast_root = new_module_list(WORD_NOT_FOUND, NULL, (yyvsp[-1].node), (yyvsp[0].node), NULL, &(yylsp[0])); }
#line 1660 "gensrc/parser/dsl.tab.c"
    break;

  case 3: /* specification: rule_list  */
#line 77 "src/dsl/dsl.y"
                                 { *ast_root = new_module_list(WORD_NOT_FOUND, NULL, NULL, (yyvsp[0].node), NULL, &(yylsp[0])); }
#line 1666 "gensrc/parser/dsl.tab.c"
    break;

  case 4: /* specification: module_list  */
#line 78 "src/dsl/dsl.y"
                                 { *ast_root = (yyvsp[0].node); }
#line 1672 "gensrc/parser/dsl.tab.c"
    break;

  case 5: /* module_list: MODULE IDENTIFIER LBRACE imports constant rule_list RBRACE  */
#line 83 "src/dsl/dsl.y"
                                                                         { (yyval.node) = new_module_list((yyvsp[-5].string_value), (yyvsp[-3].node), (yyvsp[-2].node), (yyvsp[-1].node), NULL, &(yylsp[-6])); }
#line 1678 "gensrc/parser/dsl.tab.c"
    break;

  case 6: /* module_list: MODULE IDENTIFIER LBRACE imports rule_list RBRACE  */
#line 84 "src/dsl/dsl.y"
                                                                         { (yyval.node) = new_module_list((yyvsp[-4].string_value), (yyvsp[-2].node), NULL, (yyvsp[-1].node), NULL, &(yylsp[-5])); }
#line 1684 "gensrc/parser/dsl.tab.c"
    break;

  case 7: /* module_list: module_list MODULE IDENTIFIER LBRACE imports constant rule_list RBRACE  */
#line 85 "src/dsl/dsl.y"
                                                                                  { (yyval.node) = new_module_list((yyvsp[-5].string_value), (yyvsp[-3].node), (yyvsp[-2].node), (yyvsp[-1].node), (yyvsp[-7].node), &(yylsp[-6])); }
#line 1690 "gensrc/parser/dsl.tab.c"
    break;

  case 8: /* module_list: module_list MODULE IDENTIFIER LBRACE imports rule_list RBRACE  */
#line 86 "src/dsl/dsl.y"
                                                                         { (yyval.node) = new_module_list((yyvsp[-4].string_value), (yyvsp[-2].node), NULL, (yyvsp[-1].node), (yyvsp[-6].node), &(yylsp[-5])); }
#line 1696 "gensrc/parser/dsl.tab.c"
    break;

  case 9: /* imports: imports import  */
#line 90 "src/dsl/dsl.y"
                                                { (yyval.node) = (yyvsp[0].node); append_import_list((yyval.node), (yyvsp[-1].node)); }
#line 1702 "gensrc/parser/dsl.tab.c"
    break;

  case 10: /* imports: %empty  */
#line 91 "src/dsl/dsl.y"
                                                { (yyval.node) = NULL; }
#line 1708 "gensrc/parser/dsl.tab.c"
    break;

  case 11: /* import: IMPORT identifier_list EOL  */
#line 95 "src/dsl/dsl.y"
                                                { (yyval.node) = new_option_flag(LOUD, (yyvsp[-1].node), &(yylsp[-2])); }
#line 1714 "gensrc/parser/dsl.tab.c"
    break;

  case 12: /* import: SILENT IMPORT identifier_list EOL  */
#line 96 "src/dsl/dsl.y"
                                                { (yyval.node) = new_option_flag(SILENT, (yyvsp[-1].node), &(yylsp[-3])); }
#line 1720 "gensrc/parser/dsl.tab.c"
    break;

  case 13: /* identifier_list: IDENTIFIER  */
#line 100 "src/dsl/dsl.y"
                                                { (yyval.node) = new_import_list((yyvsp[0].string_value), NULL, &(yylsp[0])); }
#line 1726 "gensrc/parser/dsl.tab.c"
    break;

  case 14: /* identifier_list: identifier_list LISTSEP IDENTIFIER  */
#line 101 "src/dsl/dsl.y"
                                                { (yyval.node) = new_import_list((yyvsp[0].string_value), (yyvsp[-2].node), &(yylsp[0])); }
#line 1732 "gensrc/parser/dsl.tab.c"
    break;

  case 15: /* constant: IDENTIFIER EQ const_expr  */
#line 105 "src/dsl/dsl.y"
                                                { (yyval.node) = new_named_constant((yyvsp[-2].string_value), (yyvsp[0].node), NULL, &(yylsp[-2])); }
#line 1738 "gensrc/parser/dsl.tab.c"
    break;

  case 16: /* constant: constant IDENTIFIER EQ const_expr  */
#line 106 "src/dsl/dsl.y"
                                                { (yyval.node) = new_named_constant((yyvsp[-2].string_value), (yyvsp[0].node), (yyvsp[-3].node), &(yylsp[-2])); }
#line 1744 "gensrc/parser/dsl.tab.c"
    break;

  case 17: /* rule_list: rule  */
#line 110 "src/dsl/dsl.y"
                                                { (yyval.node) = new_rule_list((yyvsp[0].node), NULL); }
#line 1750 "gensrc/parser/dsl.tab.c"
    break;

  case 18: /* rule_list: rule_list rule  */
#line 111 "src/dsl/dsl.y"
                                                { (yyval.node) = new_rule_list((yyvsp[0].node), (yyvsp[-1].node)); }
#line 1756 "gensrc/parser/dsl.tab.c"
    break;

  case 19: /* rule: IDENTIFIER YIELDS interval_expr where_expr map_expr end_points  */
#line 115 "src/dsl/dsl.y"
                                                                         { (yyval.node) = new_rule((yyvsp[-5].string_value), (yyvsp[-3].node), (yyvsp[-2].node), (yyvsp[-1].node), (yyvsp[0].node), &(yylsp[-5])); }
#line 1762 "gensrc/parser/dsl.tab.c"
    break;

  case 20: /* where_expr: WHERE expr  */
#line 119 "src/dsl/dsl.y"
                                                { (yyval.node) = (yyvsp[0].node); }
#line 1768 "gensrc/parser/dsl.tab.c"
    break;

  case 21: /* where_expr: %empty  */
#line 120 "src/dsl/dsl.y"
                                                { (yyval.node) = NULL; }
#line 1774 "gensrc/parser/dsl.tab.c"
    break;

  case 22: /* map_expr: MAP LBRACE map_expr_list RBRACE  */
#line 124 "src/dsl/dsl.y"
                                                { (yyval.node) = (yyvsp[-1].node); }
#line 1780 "gensrc/parser/dsl.tab.c"
    break;

  case 23: /* map_expr: %empty  */
#line 125 "src/dsl/dsl.y"
                                                { (yyval.node) = NULL; }
#line 1786 "gensrc/parser/dsl.tab.c"
    break;

  case 24: /* map_expr_list: IDENTIFIER MAPSTO expr  */
#line 129 "src/dsl/dsl.y"
                                                        { (yyval.node) = new_map_expr_list((yyvsp[-2].string_value), (yyvsp[0].node), NULL, &(yylsp[-2])); }
#line 1792 "gensrc/parser/dsl.tab.c"
    break;

  case 25: /* map_expr_list: map_expr_list LISTSEP IDENTIFIER MAPSTO expr  */
#line 130 "src/dsl/dsl.y"
                                                        { (yyval.node) = new_map_expr_list((yyvsp[-2].string_value), (yyvsp[0].node), (yyvsp[-4].node), &(yylsp[-2])); }
#line 1798 "gensrc/parser/dsl.tab.c"
    break;

  case 26: /* end_points: BEGINTOKEN expr ENDTOKEN expr  */
#line 134 "src/dsl/dsl.y"
                                                { (yyval.node) = new_end_points((yyvsp[-2].node), (yyvsp[0].node), &(yylsp[-3])); }
#line 1804 "gensrc/parser/dsl.tab.c"
    break;

  case 27: /* end_points: %empty  */
#line 135 "src/dsl/dsl.y"
                                                { (yyval.node) = NULL; }
#line 1810 "gensrc/parser/dsl.tab.c"
    break;

  case 28: /* interval_expr: IDENTIFIER LABELS IDENTIFIER  */
#line 139 "src/dsl/dsl.y"
                                                { (yyval.node) = new_atomic_interval_expr((yyvsp[-2].string_value), (yyvsp[0].string_value), &(yylsp[-2]), &(yylsp[0])); }
#line 1816 "gensrc/parser/dsl.tab.c"
    break;

  case 29: /* interval_expr: IDENTIFIER  */
#line 140 "src/dsl/dsl.y"
                                                { (yyval.node) = new_atomic_interval_expr(WORD_NOT_FOUND, (yyvsp[0].string_value), &(yylsp[0]), NULL); }
#line 1822 "gensrc/parser/dsl.tab.c"
    break;

  case 30: /* interval_expr: interval_expr ALSO interval_expr  */
#line 141 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(ALSO, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1828 "gensrc/parser/dsl.tab.c"
    break;

  case 31: /* interval_expr: interval_expr BEFORE interval_expr  */
#line 142 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(BEFORE, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1834 "gensrc/parser/dsl.tab.c"
    break;

  case 32: /* interval_expr: interval_expr MEET interval_expr  */
#line 143 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(MEET, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1840 "gensrc/parser/dsl.tab.c"
    break;

  case 33: /* interval_expr: interval_expr DURING interval_expr  */
#line 144 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(DURING, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1846 "gensrc/parser/dsl.tab.c"
    break;

  case 34: /* interval_expr: interval_expr START interval_expr  */
#line 145 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(START, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1852 "gensrc/parser/dsl.tab.c"
    break;

  case 35: /* interval_expr: interval_expr FINISH interval_expr  */
#line 146 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(FINISH, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1858 "gensrc/parser/dsl.tab.c"
    break;

  case 36: /* interval_expr: interval_expr OVERLAP interval_expr  */
#line 147 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(OVERLAP, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1864 "gensrc/parser/dsl.tab.c"
    break;

  case 37: /* interval_expr: interval_expr SLICE interval_expr  */
#line 148 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(SLICE, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1870 "gensrc/parser/dsl.tab.c"
    break;

  case 38: /* interval_expr: interval_expr COINCIDE interval_expr  */
#line 149 "src/dsl/dsl.y"
                                                { (yyval.node) = new_binary_interval_expr(COINCIDE, false, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1876 "gensrc/parser/dsl.tab.c"
    break;

  case 39: /* interval_expr: interval_expr UNLESS AFTER interval_expr  */
#line 150 "src/dsl/dsl.y"
                                                     { (yyval.node) = new_binary_interval_expr(AFTER, true, (yyvsp[-3].node), (yyvsp[0].node)); }
#line 1882 "gensrc/parser/dsl.tab.c"
    break;

  case 40: /* interval_expr: interval_expr UNLESS FOLLOW interval_expr  */
#line 151 "src/dsl/dsl.y"
                                                     { (yyval.node) = new_binary_interval_expr(FOLLOW, true, (yyvsp[-3].node), (yyvsp[0].node));}
#line 1888 "gensrc/parser/dsl.tab.c"
    break;

  case 41: /* interval_expr: interval_expr UNLESS CONTAIN interval_expr  */
#line 152 "src/dsl/dsl.y"
                                                     { (yyval.node) = new_binary_interval_expr(CONTAIN, true, (yyvsp[-3].node), (yyvsp[0].node));}
#line 1894 "gensrc/parser/dsl.tab.c"
    break;

  case 42: /* interval_expr: LPAREN interval_expr RPAREN  */
#line 153 "src/dsl/dsl.y"
                                                { (yyval.node) = (yyvsp[-1].node); }
#line 1900 "gensrc/parser/dsl.tab.c"
    break;

  case 43: /* const_expr: INTLITERAL  */
#line 157 "src/dsl/dsl.y"
                                        { (yyval.node) = new_int_literal((yyvsp[0].int_value), &(yylsp[0])); }
#line 1906 "gensrc/parser/dsl.tab.c"
    break;

  case 44: /* const_expr: FLOATLITERAL  */
#line 158 "src/dsl/dsl.y"
                                        { (yyval.node) = new_float_literal((yyvsp[0].float_value), &(yylsp[0])); }
#line 1912 "gensrc/parser/dsl.tab.c"
    break;

  case 45: /* const_expr: STRINGLITERAL  */
#line 159 "src/dsl/dsl.y"
                                        { (yyval.node) = new_string_literal((yyvsp[0].string_value), &(yylsp[0])); }
#line 1918 "gensrc/parser/dsl.tab.c"
    break;

  case 46: /* const_expr: IDENTIFIER  */
#line 160 "src/dsl/dsl.y"
                                        { (yyval.node) = new_constant_reference((yyvsp[0].string_value), &(yylsp[0])); }
#line 1924 "gensrc/parser/dsl.tab.c"
    break;

  case 47: /* const_expr: TRUE  */
#line 161 "src/dsl/dsl.y"
                                        { (yyval.node) = new_boolean_literal(true, &(yylsp[0])); }
#line 1930 "gensrc/parser/dsl.tab.c"
    break;

  case 48: /* const_expr: FALSE  */
#line 162 "src/dsl/dsl.y"
                                        { (yyval.node) = new_boolean_literal(false, &(yylsp[0])); }
#line 1936 "gensrc/parser/dsl.tab.c"
    break;

  case 49: /* const_expr: MINUS const_expr  */
#line 163 "src/dsl/dsl.y"
                                        { (yyval.node) = new_unary_expr(UMINUS, (yyvsp[0].node), &(yylsp[-1])); }
#line 1942 "gensrc/parser/dsl.tab.c"
    break;

  case 50: /* const_expr: BANG const_expr  */
#line 164 "src/dsl/dsl.y"
                                        { (yyval.node) = new_unary_expr(BANG, (yyvsp[0].node), &(yylsp[-1])); }
#line 1948 "gensrc/parser/dsl.tab.c"
    break;

  case 51: /* const_expr: const_expr MUL const_expr  */
#line 165 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(MUL, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1954 "gensrc/parser/dsl.tab.c"
    break;

  case 52: /* const_expr: const_expr DIV const_expr  */
#line 166 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(DIV, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1960 "gensrc/parser/dsl.tab.c"
    break;

  case 53: /* const_expr: const_expr MOD const_expr  */
#line 167 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(MOD, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1966 "gensrc/parser/dsl.tab.c"
    break;

  case 54: /* const_expr: const_expr PLUS const_expr  */
#line 168 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(PLUS, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1972 "gensrc/parser/dsl.tab.c"
    break;

  case 55: /* const_expr: const_expr MINUS const_expr  */
#line 169 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(MINUS, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1978 "gensrc/parser/dsl.tab.c"
    break;

  case 56: /* const_expr: const_expr LT const_expr  */
#line 170 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(LT, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1984 "gensrc/parser/dsl.tab.c"
    break;

  case 57: /* const_expr: const_expr GT const_expr  */
#line 171 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(GT, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1990 "gensrc/parser/dsl.tab.c"
    break;

  case 58: /* const_expr: const_expr GE const_expr  */
#line 172 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(GE, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 1996 "gensrc/parser/dsl.tab.c"
    break;

  case 59: /* const_expr: const_expr LE const_expr  */
#line 173 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(LE, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2002 "gensrc/parser/dsl.tab.c"
    break;

  case 60: /* const_expr: const_expr NE const_expr  */
#line 174 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(NE, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2008 "gensrc/parser/dsl.tab.c"
    break;

  case 61: /* const_expr: const_expr EQ const_expr  */
#line 175 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(EQ, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2014 "gensrc/parser/dsl.tab.c"
    break;

  case 62: /* const_expr: const_expr AND const_expr  */
#line 176 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(AND, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2020 "gensrc/parser/dsl.tab.c"
    break;

  case 63: /* const_expr: const_expr OR const_expr  */
#line 177 "src/dsl/dsl.y"
                                        { (yyval.node) = new_binary_expr(OR, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2026 "gensrc/parser/dsl.tab.c"
    break;

  case 64: /* const_expr: LPAREN const_expr RPAREN  */
#line 178 "src/dsl/dsl.y"
                                        { (yyval.node) = (yyvsp[-1].node); }
#line 2032 "gensrc/parser/dsl.tab.c"
    break;

  case 65: /* expr: INTLITERAL  */
#line 182 "src/dsl/dsl.y"
                                { (yyval.node) = new_int_literal((yyvsp[0].int_value), &(yylsp[0])); }
#line 2038 "gensrc/parser/dsl.tab.c"
    break;

  case 66: /* expr: FLOATLITERAL  */
#line 183 "src/dsl/dsl.y"
                                { (yyval.node) = new_float_literal((yyvsp[0].float_value), &(yylsp[0])); }
#line 2044 "gensrc/parser/dsl.tab.c"
    break;

  case 67: /* expr: STRINGLITERAL  */
#line 184 "src/dsl/dsl.y"
                                { (yyval.node) = new_string_literal((yyvsp[0].string_value), &(yylsp[0])); }
#line 2050 "gensrc/parser/dsl.tab.c"
    break;

  case 68: /* expr: IDENTIFIER  */
#line 185 "src/dsl/dsl.y"
                                { (yyval.node) = new_constant_reference((yyvsp[0].string_value), &(yylsp[0])); }
#line 2056 "gensrc/parser/dsl.tab.c"
    break;

  case 69: /* expr: TRUE  */
#line 186 "src/dsl/dsl.y"
                                { (yyval.node) = new_boolean_literal(true, &(yylsp[0])); }
#line 2062 "gensrc/parser/dsl.tab.c"
    break;

  case 70: /* expr: FALSE  */
#line 187 "src/dsl/dsl.y"
                                { (yyval.node) = new_boolean_literal(false, &(yylsp[0])); }
#line 2068 "gensrc/parser/dsl.tab.c"
    break;

  case 71: /* expr: MINUS expr  */
#line 188 "src/dsl/dsl.y"
                                  { (yyval.node) = new_unary_expr(UMINUS, (yyvsp[0].node), &(yylsp[-1])); }
#line 2074 "gensrc/parser/dsl.tab.c"
    break;

  case 72: /* expr: BANG expr  */
#line 189 "src/dsl/dsl.y"
                                { (yyval.node) = new_unary_expr(BANG, (yyvsp[0].node), &(yylsp[-1])); }
#line 2080 "gensrc/parser/dsl.tab.c"
    break;

  case 73: /* expr: expr MUL expr  */
#line 190 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(MUL, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2086 "gensrc/parser/dsl.tab.c"
    break;

  case 74: /* expr: expr DIV expr  */
#line 191 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(DIV, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2092 "gensrc/parser/dsl.tab.c"
    break;

  case 75: /* expr: expr MOD expr  */
#line 192 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(MOD, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2098 "gensrc/parser/dsl.tab.c"
    break;

  case 76: /* expr: expr PLUS expr  */
#line 193 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(PLUS, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2104 "gensrc/parser/dsl.tab.c"
    break;

  case 77: /* expr: expr MINUS expr  */
#line 194 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(MINUS, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2110 "gensrc/parser/dsl.tab.c"
    break;

  case 78: /* expr: expr LT expr  */
#line 195 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(LT, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2116 "gensrc/parser/dsl.tab.c"
    break;

  case 79: /* expr: expr GT expr  */
#line 196 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(GT, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2122 "gensrc/parser/dsl.tab.c"
    break;

  case 80: /* expr: expr GE expr  */
#line 197 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(GE, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2128 "gensrc/parser/dsl.tab.c"
    break;

  case 81: /* expr: expr LE expr  */
#line 198 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(LE, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2134 "gensrc/parser/dsl.tab.c"
    break;

  case 82: /* expr: expr NE expr  */
#line 199 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(NE, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2140 "gensrc/parser/dsl.tab.c"
    break;

  case 83: /* expr: expr EQ expr  */
#line 200 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(EQ, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2146 "gensrc/parser/dsl.tab.c"
    break;

  case 84: /* expr: expr AND expr  */
#line 201 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(AND, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2152 "gensrc/parser/dsl.tab.c"
    break;

  case 85: /* expr: expr OR expr  */
#line 202 "src/dsl/dsl.y"
                                { (yyval.node) = new_binary_expr(OR, (yyvsp[-2].node), (yyvsp[0].node)); }
#line 2158 "gensrc/parser/dsl.tab.c"
    break;

  case 86: /* expr: IDENTIFIER FIELD IDENTIFIER  */
#line 203 "src/dsl/dsl.y"
                                       { (yyval.node) = new_map_field((yyvsp[-2].string_value), (yyvsp[0].string_value), &(yylsp[-2]), &(yylsp[0])); }
#line 2164 "gensrc/parser/dsl.tab.c"
    break;

  case 87: /* expr: IDENTIFIER FIELD BEGINTOKEN  */
#line 204 "src/dsl/dsl.y"
                                       { (yyval.node) = new_time_field(BEGINTOKEN, (yyvsp[-2].string_value), &(yylsp[-2]), &(yylsp[0])); }
#line 2170 "gensrc/parser/dsl.tab.c"
    break;

  case 88: /* expr: IDENTIFIER FIELD ENDTOKEN  */
#line 205 "src/dsl/dsl.y"
                                       { (yyval.node) = new_time_field(ENDTOKEN, (yyvsp[-2].string_value), &(yylsp[-2]), &(yylsp[0])); }
#line 2176 "gensrc/parser/dsl.tab.c"
    break;

  case 89: /* expr: LPAREN expr RPAREN  */
#line 206 "src/dsl/dsl.y"
                                       { (yyval.node) = (yyvsp[-1].node); }
#line 2182 "gensrc/parser/dsl.tab.c"
    break;


#line 2186 "gensrc/parser/dsl.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;
  *++yylsp = yyloc;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      {
        yypcontext_t yyctx
          = {yyssp, yytoken, &yylloc};
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = yysyntax_error (&yymsg_alloc, &yymsg, &yyctx);
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == -1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = YY_CAST (char *,
                             YYSTACK_ALLOC (YY_CAST (YYSIZE_T, yymsg_alloc)));
            if (yymsg)
              {
                yysyntax_error_status
                  = yysyntax_error (&yymsg_alloc, &yymsg, &yyctx);
                yymsgp = yymsg;
              }
            else
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = YYENOMEM;
              }
          }
        yyerror (&yylloc, scanner, parser_dict, ast_root, yymsgp);
        if (yysyntax_error_status == YYENOMEM)
          YYNOMEM;
      }
    }

  yyerror_range[1] = yylloc;
  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval, &yylloc, scanner, parser_dict, ast_root);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;

      yyerror_range[1] = *yylsp;
      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp, yylsp, scanner, parser_dict, ast_root);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  yyerror_range[2] = yylloc;
  ++yylsp;
  YYLLOC_DEFAULT (*yylsp, yyerror_range, 2);

  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (&yylloc, scanner, parser_dict, ast_root, YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, &yylloc, scanner, parser_dict, ast_root);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp, yylsp, scanner, parser_dict, ast_root);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
  return yyresult;
}

#line 210 "src/dsl/dsl.y"


void yyerror(YYLTYPE * yylloc, void * UNUSED(scanner), dictionary *UNUSED(parser_dict), ast_node **UNUSED(ast_root), const char *msg) {
    filter_log_msg(LOG_LEVEL_ERROR, "Parse error on lines %d:%d to %d:%d: %s\n", 
                   yylloc->first_line, yylloc->first_column, yylloc->last_line, yylloc->last_column, msg);
}


