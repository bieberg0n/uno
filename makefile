SRC = src/*.ts
CFLAGS = --strict
OUTPUT = build
FLAGS = 

main: ${SRC}
	tsc ${SRC} --outDir ${OUTPUT}

run: ${OUTPUT}
	node ${FLAGS} ${OUTPUT}/main.js

clean:
	rm -f ${OUTPUT}/*