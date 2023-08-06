/*
 * file.h
 *
 *  Created on: Feb 3, 2017
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

#ifndef FILE_H_
#define FILE_H_

#include "types.h"
#include "pool.h"
#include "dict.h"

typedef enum {
  PARSE_SUCCESS,
  PARSE_LABEL_FILTERED,
  PARSE_FILE_ERROR,
  PARSE_UNEXPECTED_LINE,
  PARSE_UNEXPECTED_NULL,
  PARSE_INVALID_CHAR,
  PARSE_TOO_MUCH_DATA,
  PARSE_LINE_TOO_LONG
} event_parse_result;

#define MAX_MAP_PAIRS 32
#define MAX_LINE_LENGTH 4096

#define FILTER_NAMES_AND_KEYS  1
#define DO_NOT_FILTER 0

#define IS_WHITESPACE(_c_) ((_c_) == ' ' || (_c_) == '\t')
#define IS_DELIMETER(_c_) ((_c_) == '|' || (_c_) == ',')
#define IS_NEWLINE(_c_) ((_c_) == '\n')

event_parse_result read_event_file(char *, pool *, dictionary *, dictionary *, dictionary *, bool);
event_parse_result read_event_from_csv(pool *, char *, int, dictionary *, dictionary *, dictionary *, bool);

#endif /* FILE_H_ */
