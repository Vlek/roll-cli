# Roll

Dice roller CLI Script

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

    Usage:

        roll <nothing>      - Rolls 1d20

        roll <expression>   - Rolls all dice + does math

    Expressions:

        1d20                - Rolls one 20-sided die

        d20                 - Does not require a '1' in front of 'd'

        d%                  - Rolls 1d100

        d8 + 3d6 + 5        - Rolls 1d8, 3d6, and adds everything together

        (1d4)d6             - Rolls 1d4 d6 die
