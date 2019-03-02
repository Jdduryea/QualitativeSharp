import sys


# Syntax

# Big numbers
BIG = "big"
MASSIVE = "massive"

# small numbers
SMALL = "small"
TINY = "tiny"

# Operators
PLUS = "+"
MINUS = "-"


# qualifiers
REALLY = "really"
FUCKING = "fucking"
KINDA = "kinda"


EQUALS = "="
say = "say"

values = {}
# TODO: random values?
values[BIG] = 69
values[MASSIVE] = 14001

values[SMALL] = -17
values[TINY] = -100000


values[REALLY] = 6
values[FUCKING] = 19
values[KINDA] = 3


BIG_QUALIFIERS = [BIG, MASSIVE]
SMALL_QUALIFIERS = [SMALL, TINY]
INCREASERS = [REALLY, FUCKING]

TOKEN_MAP = {}
TOKEN_MAP["big"] = BIG
TOKEN_MAP["massive"] = MASSIVE
TOKEN_MAP["small"] = SMALL
TOKEN_MAP["tiny"] = TINY
TOKEN_MAP["big"] = BIG
TOKEN_MAP["really"] = REALLY
TOKEN_MAP["fucking"] = FUCKING
TOKEN_MAP["kinda"] = KINDA

TOKEN_MAP["+"] = PLUS
TOKEN_MAP["-"] = MINUS


OPS = ["+","-"]


# Grammar
#VAR = EXPR


# maps from variable names to their values
SYM_TABLE = {}


def run():
	file = sys.argv
	file = "test.q"
	line_no = 0
	with open(file) as f:

		for line in f:
			parse_line(line,line_no)
			line_no+=1



def parse_line(line, line_number):
	tokens = line.split()

	# case 0: comment:
	if tokens[0] == "/" and tokens[1] == "/":
		return

	# case 1: VAR = EXPR
	if isVar(tokens[0]):
		var = tokens[0]
		SYM_TABLE[var] = eval_expr(tokens[2:]) # tokens[1] is an equals sign

	# case 2: say VAR
	else:
		if "say" == tokens[0]:
			var = tokens[1]
			print(str(var)+" = " + str(SYM_TABLE[var]))
		


def isVar(token):
	return "var" in token

def toParseToken(literal_token):
	if "\n" in literal_token:
		literal_token = literal_token[:-1]
	return TOKEN_MAP[literal_token]


def getValue(token):
	return values[token]

def eval_op(expr1, op, expr2):
	if op == PLUS:
		return expr1 + expr2
	if op == MINUS:
		return expr1 - expr2


def eval_expr(remaining_tokens):


	val_accumulator = 1
	
	# Case 0: var = var op EXPR
	if isVar(remaining_tokens[0]) and not isVar(remaining_tokens[-1]) and toParseToken(remaining_tokens[1]) in OPS:
		op = toParseToken(remaining_tokens[1])
		var = remaining_tokens[0]
		val_accumulator = eval_op(SYM_TABLE[var], op, eval_expr(remaining_tokens[2:]))
		
	# Case 1: var = EXPR op var
	elif not isVar(remaining_tokens[0]) and isVar(remaining_tokens[-1]):
		var = remaining_tokens[-1]
		op = toParseToken(remaining_tokens[-2])
		expr = eval_expr(remaining_tokens[:-2])

		val_accumulator = eval_op(SYM_TABLE[var], op, expr)

	# Case 2: var = var op var
	elif isVar(remaining_tokens[0]) and isVar(remaining_tokens[-1]):

		var1 = remaining_tokens[0]
		op = toParseToken(remaining_tokens[1])
		var2 = remaining_tokens[2]
		val_accumulator = eval_op(SYM_TABLE[var1], op, SYM_TABLE[var2])

	# Case 3:  var = EXPR
	else:
		for token in remaining_tokens:
			if token != "\n":
				parseToken = toParseToken(token)
				val_accumulator *= getValue(parseToken)


	return val_accumulator










run()


