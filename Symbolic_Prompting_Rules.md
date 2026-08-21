# Symbolic Prompting Rules

Complete mapping of symbolic notation to natural language equivalents. This file serves as the authoritative legend for all compressed content.

## Notation Categories

---

### 1. Flow and Sequence Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `->` | "leads to", "then", "results in", "produces" | Sequential causation or transformation. Left side causes/produces right side. | `parse -> validate -> store` means "parse, then validate, then store" |
| `=>` | "implies", "therefore", "because of this" | Logical implication. Left side being true means right side follows. | `null input => raise ValueError` means "if input is null, that implies we raise ValueError" |
| `>>` | "pipe to", "pass output to", "feed into" | Data flow. Output of left becomes input of right. | `fetch >> transform >> render` means "fetch data, pipe its output to transform, pipe that to render" |
| `;` | "then", "followed by", "next" | Sequential execution without causal link. Steps happen in order. | `lint; test; build` means "run lint, then test, then build" |
| `\|` | "or", "alternatively", "in parallel" | Alternatives or parallel options. | `redis \| memcached` means "use redis or memcached" |
| `+` | "and", "also", "together with" | Conjunction. Both things happen/apply. | `log(err) + retry` means "log the error and retry" |
| `>` | "before", "has precedence over", "higher priority" | Ordering or priority. | `lint > test` means "lint runs before test" |
| `<` | "after", "lower priority than" | Reverse ordering. | `deploy < test` means "deploy happens after test" |

---

### 2. Conditional and Logic Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `?` | "if", "when", "in case of", "check whether" | Conditional trigger. Preceding expression is the condition. | `err? -> retry` means "if there's an error, retry" |
| `!` | "not", "never", "don't", "prevent", "forbid" | Negation. The thing must not happen/exist. | `!mutate args` means "do not mutate arguments" |
| `&&` | "and" (both required) | Logical AND. Both conditions must be true. | `valid && auth -> allow` means "if valid AND authenticated, allow" |
| `\|\|` | "or" (either sufficient) | Logical OR. At least one condition must be true. | `cache \|\| fetch` means "use cache, or if unavailable, fetch" |
| `?:` | "if-else", "when-otherwise" | Ternary conditional. condition ? true-branch : false-branch | `prod? https : http` means "if production use https, else http" |
| `??` | "if null/missing, use", "fallback to" | Null coalescing. Use right side when left is absent. | `config.port ?? 8080` means "use config.port, or 8080 if not set" |

---

### 3. Quantifiers and Scope Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `*` | "all", "every", "each" | Universal quantifier. Applies to every item in scope. | `* fn: typed` means "every function must be typed" |
| `@` | "at", "in", "within", "located at" | Scope/location marker. Specifies where a rule applies. | `@ src/` means "within the src directory" |
| `#N` | "N times", "count of N", "up to N" | Numeric quantifier. Specifies a count. | `retry #3` means "retry up to 3 times" |
| `..` | "through", "to", "range" | Range operator. Inclusive range between values. | `lines 10..50` means "lines 10 through 50" |
| `~` | "approximately", "about", "roughly" | Approximation. Value is not exact. | `~100ms` means "approximately 100 milliseconds" |
| `N+` | "N or more", "at least N" | Minimum bound. | `3+ tests` means "at least 3 tests" |
| `N-` | "N or fewer", "at most N" | Maximum bound. | `30- LOC` means "at most 30 lines of code" |

---

### 4. Assignment and State Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `=` | "is", "equals", "set to", "configured as" | Direct assignment or equality. | `timeout = 30s` means "timeout is set to 30 seconds" |
| `:=` | "defined as", "initialized as", "create as" | Definition/initialization. Stronger than `=`, implies creation. | `logger := getLogger(__name__)` means "define logger as getLogger call" |
| `+=` | "add", "append", "include", "also has" | Additive modification. Adds to existing value. | `deps += pytest` means "add pytest to dependencies" |
| `-=` | "remove", "exclude", "drop" | Subtractive modification. Removes from existing value. | `deps -= unused` means "remove unused from dependencies" |
| `<-` | "receives from", "sourced from", "read from" | Data source. Right side provides data to left side. | `config <- env` means "config is read from environment variables" |
| `->` (assign) | "outputs to", "writes to", "produces" | Data sink. Left side produces data stored in right side. | `query -> results` means "query outputs to results variable" |

---

### 5. Validation and Assertion Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `[checkmark]` | "required", "must have", "ensure exists" | Positive assertion. Thing must be present/true. | `[checkmark] docstring` means "docstring is required" |
| `[x]` | "forbidden", "must not have", "never" | Negative assertion. Thing must not be present. | `[x] bare except` means "bare except is forbidden" |
| `!=` | "must not equal", "different from" | Inequality assertion. Values must differ. | `new != old` means "new must not equal old" |
| `>=` | "at least", "minimum of" | Minimum threshold. | `coverage >= 80%` means "coverage must be at least 80%" |
| `<=` | "at most", "maximum of", "no more than" | Maximum threshold. | `fn LOC <= 30` means "function must be at most 30 lines" |
| `==` | "exactly", "must equal" | Exact match assertion. | `indent == 4 spaces` means "indentation must be exactly 4 spaces" |

---

### 6. Grouping and Structure Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `()` | "group", "together", "as a unit" | Groups expressions for precedence or clarity. | `(fetch + parse) -> store` means "fetch and parse together, then store" |
| `[]` | "optional", "may include", "list of" | Optional elements or array/list types. | `fn(x, [y])` means "function takes x, and optionally y" |
| `{}` | "one of", "set of", "enum", "choices" | Enumeration of valid values. | `status: {ok, err, pending}` means "status is one of: ok, err, pending" |
| `<>` | "of type", "generic", "parameterized by" | Type parameters or generics. | `list<str>` means "list of strings" |
| `/` | "or", "per", "divided by" | Context-dependent separator. | `req/sec` means "requests per second"; `pass/fail` means "pass or fail" |
| `:` | "has property", "specifically", "detail" | Property access or specification. | `fn: typed` means "function has property: typed" |

---

### 7. Reference and Annotation Operators

| Symbol | NLP Equivalent | Expanded Meaning | Usage Context |
|--------|---------------|------------------|---------------|
| `#` | "number", "issue", "count", "tag" | Numeric reference or tag. Context determines meaning. | `#123` = issue 123; `#3` = three times |
| `$` | "variable", "environment value", "dynamic" | Dynamic value resolved at runtime. | `$PORT` means "the value of PORT variable" |
| `&` | "reference to", "address of", "link to" | Reference or pointer to another entity. | `& config.yaml` means "reference the config.yaml file" |
| `^` | "parent", "above", "inherits from" | Inheritance or parent scope. | `^ BaseAgent` means "inherits from BaseAgent" |
| `_` | "private", "internal", "hidden" | Internal/private scope marker. | `_helper()` means "private helper function" |
| `...` | "et cetera", "and so on", "continues" | Continuation/ellipsis. Pattern continues in obvious way. | `a, b, c, ...` means "a, b, c, and more following the same pattern" |

---

### 8. Action Verbs (Compressed)

| Compressed | NLP Equivalent | Usage |
|-----------|---------------|-------|
| `rm` | "remove", "delete" | `rm unused imports` |
| `mv` | "move", "rename", "relocate" | `mv old_name -> new_name` |
| `cp` | "copy", "duplicate" | `cp template -> new_file` |
| `chk` | "check", "verify", "validate" | `chk all types` |
| `gen` | "generate", "create", "produce" | `gen docstrings` |
| `fix` | "fix", "repair", "correct" | `fix lint errors` |
| `add` | "add", "insert", "include" | `add type hints` |
| `del` | "delete", "remove", "drop" | `del dead code` |
| `upd` | "update", "modify", "change" | `upd config` |
| `run` | "execute", "invoke", "start" | `run tests` |
| `ret` | "return", "output", "yield" | `ret list<str>` |
| `log` | "log", "record", "emit" | `log(err)` |
| `fmt` | "format", "style", "prettify" | `fmt code` |

---

### 9. Domain Abbreviations

| Abbreviation | Full Form |
|-------------|-----------|
| `fn` | function |
| `cls` | class |
| `mod` | module |
| `pkg` | package |
| `var` | variable |
| `arg` | argument |
| `param` | parameter |
| `ret` | return |
| `str` | string |
| `int` | integer |
| `bool` | boolean |
| `dict` | dictionary |
| `arr` / `lst` | array / list |
| `err` | error |
| `exc` | exception |
| `msg` | message |
| `req` | request |
| `resp` | response |
| `cfg` / `config` | configuration |
| `env` | environment |
| `dir` | directory |
| `src` | source |
| `dst` | destination |
| `tmp` | temporary |
| `db` | database |
| `auth` | authentication |
| `impl` | implementation |
| `dep` / `deps` | dependency / dependencies |
| `doc` / `docs` | documentation |
| `spec` | specification |
| `ver` | version |
| `prev` | previous |
| `curr` | current |
| `max` | maximum |
| `min` | minimum |
| `avg` | average |
| `approx` | approximately |
| `incl` | including |
| `excl` | excluding |
| `w/` | with |
| `w/o` | without |

---

### 10. Structural Patterns

#### Key-Value Pattern
```
key: value
```
Replaces: "The key is set to value" or "Key should be configured as value"

#### Scoped Block Pattern
```
@ scope:
  rule1
  rule2
```
Replaces: "Within scope, the following rules apply: rule1 and rule2"

#### Conditional Block Pattern
```
condition?
  true-branch
  !condition?
  false-branch
```
Replaces: "If condition is true, do true-branch. Otherwise, do false-branch"

#### List Pattern
```
items:
  - item1
  - item2
  - item3
```
Replaces: "The items include item1, item2, and item3"

#### Pipeline Pattern
```
input >> step1 >> step2 >> output
```
Replaces: "Take the input, pass it through step1, then step2, and produce output"

#### Assertion Block Pattern
```
gates:
  [checkmark] condition1
  [checkmark] condition2
  [x] anti-condition
```
Replaces: "Ensure condition1 and condition2 are met. Prevent anti-condition."

---

### 11. Composition Rules

1. **Left-to-right reading**: `A -> B -> C` reads as "A then B then C"
2. **Indentation = scope**: Indented lines belong to the parent above them
3. **Comma = list separator**: `a, b, c` is a list of items at the same level
4. **Newline = separate rule**: Each line is an independent statement unless indented
5. **Parentheses = grouping**: `(A + B) -> C` means "A and B together produce C"
6. **Colon = specification**: `X: Y` means "X has the property/value Y"
7. **Semicolon = sequence**: `A; B; C` means "do A, then B, then C" (no causal link)
8. **Pipe = alternative**: `A | B` means "A or B" (choose one)

---

### 12. Precedence (highest to lowest)

1. `()` - Explicit grouping
2. `!` - Negation
3. `*`, `@`, `#N` - Quantifiers and scope
4. `:`, `.` - Property access
5. `->`, `>>` - Flow/pipe
6. `&&` - Logical AND
7. `||` - Logical OR
8. `?`, `?:` - Conditionals
9. `=`, `:=`, `+=`, `-=` - Assignment
10. `;` - Statement separator

---

### 13. Escape Rules

When symbols conflict with literal content:

- Backtick-wrap literals: `` `->` `` means the literal string "->"
- Quote file paths: `"src/main.py"` keeps the path literal
- Code blocks remain uncompressed: triple-backtick blocks are never symbolically rewritten

---

### 14. Transformation Rules (NLP to Symbolic)

These rules define how to convert natural language into symbolic notation:

| NLP Pattern | Symbolic Replacement | Rule ID |
|-------------|---------------------|---------|
| "make sure that X" / "ensure that X" / "verify X" | `ensure: X` or `[checkmark] X` | R01 |
| "do not X" / "never X" / "X is not allowed" | `[x] X` or `!X` | R02 |
| "if X then Y" / "when X, do Y" | `X? -> Y` or `X -> Y` | R03 |
| "for each X in Y" / "every X in Y" | `* X @ Y:` or `for X in Y:` | R04 |
| "X should be at least N" / "minimum N for X" | `X >= N` | R05 |
| "X should be at most N" / "maximum N for X" | `X <= N` | R06 |
| "X is set to Y" / "configure X as Y" | `X = Y` | R07 |
| "X reads from Y" / "X gets its value from Y" | `X <- Y` | R08 |
| "after X, do Y" / "X followed by Y" | `X; Y` or `X -> Y` | R09 |
| "X or Y" / "either X or Y" | `X \| Y` | R10 |
| "X and Y" / "both X and Y" | `X + Y` or `X && Y` | R11 |
| "repeat X N times" / "do X up to N times" | `X #N` or `loop(X, N)` | R12 |
| "X within Y" / "X inside Y" / "X located at Y" | `X @ Y` | R13 |
| "X produces Y" / "X outputs Y" / "X returns Y" | `X -> Y` | R14 |
| "X of type Y" / "X is a Y" | `X: Y` or `X<Y>` | R15 |
| "optional X" / "X if available" | `[X]` | R16 |
| "one of X, Y, Z" / "X can be X, Y, or Z" | `{X, Y, Z}` | R17 |
| "first X, then Y, finally Z" | `X; Y; Z` or `X -> Y -> Z` | R18 |
| "X unless Y" / "X except when Y" | `!Y? -> X` | R19 |
| "X with Y" / "X together with Y" | `X + Y` or `X w/ Y` | R20 |
