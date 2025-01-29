---
title: Writing a C compiler
subtitle: chapter 1
author: Nirv
author-url: "https://github.com/AnarchistHoneybun"
date: 2024-09-14
lang: en
toc-title: Contents
version: v0.1.1
---

## Introduction

This blog (series of blogs, hopefully) will follow me writing a C compiler in C++, following 
[Nora Sandler's](https://norasandler.com/about/) book "[Writing a C Compiler](https://nostarch.com/writing-c-compiler)".
I intend to write a short intro to what each chapter covers, show some of the code written to implement the concepts, and 
write about anything interesting that comes up.

## Chapter details

The first chapter is mostly about setting up the essentials. The project is modelled with the following elements: a lexer,
a parser, a code generator, and a code emission module. Note that for now the book only wants us to write the "compiler" only, 
so preprocessing and assembling are delegated to the gcc toolchain.

## Program flow

Here's essentially how the program ends up working after implementing all details from chapter 1:
- The compiler takes in an input file as argument, with an optional stage flag (--lex, --parse, --codegen)
- the preprocess function runs gcc on the input file, and writes the output to a `.i` file
- the lexer reads the `.i` file and tokenizes the input. This is stored as a vector
- the parser goes through the tokens and builds an abstract syntax tree (AST)
- the code generator takes the above AST and generates an assembly AST from it
- the code emission step writes the assembly AST to a `.s` file
- the assemble function runs gcc on the `.s` file, and creates an executable

## Program output

Sample C source code:
```
╭─────────────────╮
│  int main() {   │
│      return 0;  │
│  }              │
╰─────────────────╯
```

Lexer output:
```
╭─────────────────────────────────╮
│Token: Type = 2, Value = "int"   │
│Token: Type = 0, Value = "main"  │
│Token: Type = 5, Value = "("     │
│Token: Type = 3, Value = "void"  │
│Token: Type = 6, Value = ")"     │
│Token: Type = 7, Value = "{"     │
│Token: Type = 4, Value = "return"│
│Token: Type = 1, Value = "0"     │
│Token: Type = 9, Value = ";"     │
│Token: Type = 8, Value = "}"     │
╰─────────────────────────────────╯

```

Parser output:
```
╭──────────────────────────╮
│   Program(               │
│     Function(            │
│       name="main",       │
│       body=              │
│         Return(          │
│           Constant(0)    │
│         )                │
│     )                    │
│   )                      │
╰──────────────────────────╯
```

Code generator output:
```
╭───────────────────────────╮
│   Program(                │
│     Function(             │
│       name="main",        │
│       instructions=[      │
│         Mov(              │
│           Imm(0),         │
│           Register("eax") │
│         ),                │
│         Ret(),            │
│       ]                   │
│     )                     │
│   )                       │
╰───────────────────────────╯
```

Code emission output:
```
╭────────────────────────────────────────────╮
│.globl main                                 │
│main:                                       │
│ movl $0, %eax                              │
│ ret                                        │
│.section .note.GNU-stack,"",@progbits       │
╰────────────────────────────────────────────╯
```