# Lab 5: Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest fixes were the style issues reported by Flake8 and Pylint, such as the unused math import, the == None comparison, the missing final newline, and the camelCase function names. Each of these was a small change in one place and did not affect how the program behaved. The hardest fixes were removing eval and the global statement. Removing eval meant changing the function signature from an expression string to a numeric surcharge rate, and removing global meant restructuring how total revenue is stored. Both of these required changing the program's design rather than a single line.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Yes. Pylint (W0612) and Flake8 (F841) both reported that base_fare in calculateBaggageFee was an unused variable. The variable was actually used, because the expression string passed to eval was "base_fare * 0.15", which reads base_fare at runtime. The tools cannot look inside a string to see that a variable is used there. Bandit's hardcoded password warning was also only medium confidence, since the tool flags any long uppercase string that resembles a token.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint automatically through the editor while writing code, and add all three tools as pre-commit hooks so that problems are caught before a commit is made. I would also run them in a CI pipeline, such as GitHub Actions, on every push and pull request, and fail the build on any high or medium severity Bandit issue or a Pylint score below a set threshold. A shared configuration file would keep the rules the same for every team member.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score rose from 4.00/10 to 10.00/10, and both Flake8 and Bandit went from 10 and 6 issues to none. The code is safer because it no longer runs arbitrary strings with eval, no longer builds shell commands, uses SHA-256 instead of MD5, and keeps the API token out of the source code and the output. It is more readable because of snake_case names, docstrings, and f-strings. It is more robust because errors are caught specifically instead of silently ignored, files are always closed properly, and the cancellation logic no longer reopens full flights or leaves revenue incorrect.
