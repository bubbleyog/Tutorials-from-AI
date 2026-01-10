# 最小Makefile：用于演示 make 与脚本集成

CXX ?= g++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra

SRC := sample.cpp
BIN := sample_app

.PHONY: all clean run

all: $(BIN)

$(BIN): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $<

run: $(BIN)
	./$(BIN) --name MakeUser --seed 42

clean:
	rm -f $(BIN)
