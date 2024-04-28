# CroissantCompiler

A verrrry French Compiler (with the associated accent)

# How to use

First, you need to install the dependencies:

```bash
pip install -r requirements.txt
```

Then, you can run the compiler with the following command:

```bash
python spf.py
```

This will take you to the interactive shell, where you can write your code. The
compiler will then parse and execute it line by line, updating the global
context every time.

> [!NOTE] If you want to exit the shell, you can type `sortir;` (don't forget
> the semicolon at the end).

> [!NOTE] If you want to see the list of available commands, you can type run
> the `python spf.py --help` command.

## Virtual environment

If you want to use a virtual environment, you can create one with the following
commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then, you can run the compiler as usual.

![](https://github.com/kazawai/CroissantCompiler/blob/master/gif.gif)

# File structure

The project is structured as follows:

- `spf.py`: the main file of the compiler, which contains the interactive shell
  and the main loop of the program.
- `spf.lark`: the grammar of the language, written in Lark (EBNF).
- `sample/`: a directory containing sample programs written in the language.
- `modules/`: a directory containing the necessary modules for the compiler.

## Modules

The `modules/` directory contains the following modules:

- `exceptions/`: a module containing the exceptions raised by the compiler.
- `types/`: a directory containing the classes representing the different types
  of the language (e.g., `Entier`, `Booleen`, `Texte`, etc.).
- `utils/`: a directory containing utility functions used by the compiler.
  - `global_vars.py`: a module containing the global variables of the compiler
    (e.g., the global context, the nested counter, etc.).
  - `interpreter.py`: a module containing the interpreter of the language.
  - `variables.py`: a module containing the classes representing the variables
    of the language (relies on the `types` module).
  - `wrapper.py`: a module containing the wrapper class of the language. The
    wrapper is used to execute the code in a safe environment (e.g., to catch
    exceptions and display them in a user-friendly way).

# Language features

The language has the following features:

- Variables: you can declare and assign variables of different types (e.g.,
  `entier`, `booleen`, `texte`, etc.).
- Expressions: you can use arithmetic, logical, and comparison expressions in
  your code. You can also use parentheses to group expressions. Every expression
  has its own precedence level.
- Conditions: you can use `si` and `sinon` statements to execute code based on
  conditions.
- Boucles: you can use `tant que ... faire {...}` and
  `pour chaque ... dans ... faire {...}` statements to execute code in a loop.
- Nested blocks: you can nest blocks of code (e.g., inside conditions or loops).
  Each block has its own context.

# Grammar

The grammar of the language is defined in the `spf.lark` file. It is written in
Lark, a parsing library for Python that uses EBNF notation.

The grammar is structured as follows:

- `start`: the starting rule of the grammar, which defines the structure of the
  program.
- `statement`: the rule that defines the structure of a statement in the
  program. It can be an assignment, a condition, a loop, an expression or an
  instruction.
- `assignment`: the rule that defines the structure of an assignment statement.
  This also includes the declaration of a variable.
- `condition`: the rule that defines the structure of a condition statement.
- `loop`: the rule that defines the structure of a loop statement.
- `expression`: the rule that defines the structure of an expression in the
  program. It can be a comparison, an arithmetic operation, a string operation,
  a list operation, a logical operation or simply an identifier call.
- `instruction`: the rule that defines the structure of an instruction in the
  program. It can be a function call, a print statement, a
  `ajouter ... dans ...` statement or the exit call.

All the tokens used in the grammar can be found at the end of the file.

# Examples

Here are some examples of programs written in the language:

## Monotonic sequence

```
liste nombres = [3, 3, 6, 7, 8];
booléen monotone = vrai;
pour chaque entier position dans [1:taille nombres - 1] faire {
    si nombres[position] > nombres[position + 1] alors {
        monotone = faux;
    }
}
si monotone alors {
    afficher "La liste", nombres, "est monotone";
} sinon {
    afficher "La liste", nombres, "n'est pas monotone";
}
```

> Output

```
La liste [3, 3, 6, 7, 8] est monotone
```

## Words in a sentence

```
texte phrase = "Bonjour à tout le monde";
texte mot = "";
liste mots = [];
pour chaque texte caractère dans phrase faire {
    si caractère vaut " " alors {
        si taille mot > 0 alors {
            ajouter mot dans mots;
            mot = "";
        }
    } sinon {
        mot = mot + caractère;
    }
}
# Potentiel dernier mot
si taille mot > 0 alors {
    ajouter mot dans mots;
}
afficher mots;
```

> Output

```
["Bonjour", "à", "tout", "le", "monde"]
```

> [!NOTE] You can find more examples in the `sample/` directory.

# Acknowledgements

This project was made for the course "Compilation" at the University of Mons. It
was developed by:

- [Julien Ladeuze](https://github.com/EliotBD03)
- [Maxime (KazaWai)](https://github.com/kazawai)
