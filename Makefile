
docs := *.md
examples := examples/*

all: test

%.md: ${examples}
	./process_md "$@"

compile: ${docs}

test: compile
	./run_all_tests

cellincell:
	./cell incell/cell.cell

