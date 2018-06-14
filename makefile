SRC = src/*.ts
CFLAGS = --strict -t "ESNext" -m "CommonJS"
OUTPUT = build
FLAGS =

main: ${SRC}
	tsc ${CFLAGS} ${SRC} --outDir ${OUTPUT}

run: ${OUTPUT}
	node ${FLAGS} ${OUTPUT}/main.js

clean:
	rm -f ${OUTPUT}/*
