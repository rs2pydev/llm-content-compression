"""
Prompt compression tool using symbolic notation rules.

Reads a natural language prompt/context file and produces a token-efficient
compressed version using the symbolic notation system defined in
Symbolic_Prompting_Rules.md.

Usage:
    python compress_prompt.py <input_file> [--output <output_file>] [--dry-run]

If --output is not specified, writes to <input_file>.compressed.md
If --dry-run is specified, prints the compressed output without writing.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CompressionRule:
    """Single NLP-to-symbolic transformation rule."""

    rule_id: str
    pattern: re.Pattern[str]
    replacement: str
    description: str


@dataclass
class CompressionStats:
    """Tracks compression effectiveness."""

    original_chars: int = 0
    compressed_chars: int = 0
    original_words: int = 0
    compressed_words: int = 0
    rules_applied: dict[str, int] = field(default_factory=dict)

    @property
    def char_reduction(self) -> float:
        if self.original_chars == 0:
            return 0.0
        return (1 - self.compressed_chars / self.original_chars) * 100

    @property
    def word_reduction(self) -> float:
        if self.original_words == 0:
            return 0.0
        return (1 - self.compressed_words / self.original_words) * 100


# ---------------------------------------------------------------------------
# FILLER REMOVAL PATTERNS
# These words carry zero semantic weight and can always be removed.
# ---------------------------------------------------------------------------

FILLER_PHRASES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bplease\s+", re.IGNORECASE), ""),
    (re.compile(r"\bcould you\s+", re.IGNORECASE), ""),
    (re.compile(r"\bcan you\s+", re.IGNORECASE), ""),
    (re.compile(r"\bI would like you to\s+", re.IGNORECASE), ""),
    (re.compile(r"\bgo ahead and\s+", re.IGNORECASE), ""),
    (re.compile(r"\bbe sure to\s+", re.IGNORECASE), ""),
    (re.compile(r"\bmake sure (that |to )?\s*", re.IGNORECASE), "ensure: "),
    (re.compile(r"\bjust\s+", re.IGNORECASE), ""),
    (re.compile(r"\bsimply\s+", re.IGNORECASE), ""),
    (re.compile(r"\bbasically\s+", re.IGNORECASE), ""),
    (re.compile(r"\bactually\s+", re.IGNORECASE), ""),
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
    (re.compile(r"\bat this point in time\b", re.IGNORECASE), "now"),
    (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
    (re.compile(r"\bin the event that\b", re.IGNORECASE), "if"),
    (re.compile(r"\bwith regard to\b", re.IGNORECASE), "re:"),
    (re.compile(r"\bfor the purpose of\b", re.IGNORECASE), "to"),
    (re.compile(r"\bit is important to note that\b", re.IGNORECASE), "note:"),
    (re.compile(r"\bas a matter of fact\b", re.IGNORECASE), ""),
    (re.compile(r"\bin addition to that\b", re.IGNORECASE), "also"),
]

# ---------------------------------------------------------------------------
# STRUCTURAL TRANSFORMATION RULES
# These convert NLP patterns into symbolic equivalents.
# ---------------------------------------------------------------------------

STRUCTURAL_RULES: list[CompressionRule] = [
    CompressionRule(
        rule_id="R01",
        pattern=re.compile(
            r"(?:ensure|verify|confirm|check) that (.+)", re.IGNORECASE
        ),
        replacement=r"ensure: \1",
        description="ensure/verify X -> ensure: X",
    ),
    CompressionRule(
        rule_id="R02",
        pattern=re.compile(
            r"(?:do not|don't|never|must not|should not|shouldn't) (.+)", re.IGNORECASE
        ),
        replacement=r"x \1",
        description="do not X -> x X",
    ),
    CompressionRule(
        rule_id="R03",
        pattern=re.compile(
            r"if (.+?)(?:,\s*| then )(.+)", re.IGNORECASE
        ),
        replacement=r"\1? -> \2",
        description="if X then Y -> X? -> Y",
    ),
    CompressionRule(
        rule_id="R04",
        pattern=re.compile(
            r"for (?:each|every|all) (.+?) in (.+?)(?:,\s*| )(?:check|ensure|verify) (.+)",
            re.IGNORECASE,
        ),
        replacement=r"* \1 @ \2: \3",
        description="for each X in Y, check Z -> * X @ Y: Z",
    ),
    CompressionRule(
        rule_id="R05",
        pattern=re.compile(
            r"(.+?) (?:should be|must be) at least (.+)", re.IGNORECASE
        ),
        replacement=r"\1 >= \2",
        description="X should be at least N -> X >= N",
    ),
    CompressionRule(
        rule_id="R06",
        pattern=re.compile(
            r"(.+?) (?:should be|must be) at most (.+)", re.IGNORECASE
        ),
        replacement=r"\1 <= \2",
        description="X should be at most N -> X <= N",
    ),
    CompressionRule(
        rule_id="R07",
        pattern=re.compile(
            r"(?:set|configure) (.+?) (?:to|as) (.+)", re.IGNORECASE
        ),
        replacement=r"\1 = \2",
        description="set X to Y -> X = Y",
    ),
    CompressionRule(
        rule_id="R08",
        pattern=re.compile(
            r"(.+?) (?:reads from|gets? (?:its )?value from|sourced from) (.+)",
            re.IGNORECASE,
        ),
        replacement=r"\1 <- \2",
        description="X reads from Y -> X <- Y",
    ),
    CompressionRule(
        rule_id="R09",
        pattern=re.compile(
            r"after (.+?)(?:,\s*| )(?:then )?(.+)", re.IGNORECASE
        ),
        replacement=r"\1; \2",
        description="after X, then Y -> X; Y",
    ),
    CompressionRule(
        rule_id="R10",
        pattern=re.compile(
            r"either (.+?) or (.+)", re.IGNORECASE
        ),
        replacement=r"\1 | \2",
        description="either X or Y -> X | Y",
    ),
    CompressionRule(
        rule_id="R11",
        pattern=re.compile(
            r"both (.+?) and (.+)", re.IGNORECASE
        ),
        replacement=r"\1 + \2",
        description="both X and Y -> X + Y",
    ),
    CompressionRule(
        rule_id="R14",
        pattern=re.compile(
            r"(.+?) (?:returns?|outputs?|produces?) (.+)", re.IGNORECASE
        ),
        replacement=r"\1 -> \2",
        description="X returns Y -> X -> Y",
    ),
    CompressionRule(
        rule_id="R16",
        pattern=re.compile(
            r"(?:optional(?:ly)?|if available)[,:]?\s*(.+)", re.IGNORECASE
        ),
        replacement=r"[\1]",
        description="optionally X -> [X]",
    ),
    CompressionRule(
        rule_id="R20",
        pattern=re.compile(
            r"(.+?) (?:together with|along with|combined with) (.+)", re.IGNORECASE
        ),
        replacement=r"\1 + \2",
        description="X together with Y -> X + Y",
    ),
]

# ---------------------------------------------------------------------------
# WORD-LEVEL ABBREVIATIONS
# Replace common verbose words with their abbreviations.
# ---------------------------------------------------------------------------

ABBREVIATIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bfunction\b", re.IGNORECASE), "fn"),
    (re.compile(r"\bclass\b", re.IGNORECASE), "cls"),
    (re.compile(r"\bmodule\b", re.IGNORECASE), "mod"),
    (re.compile(r"\bpackage\b", re.IGNORECASE), "pkg"),
    (re.compile(r"\bvariable\b", re.IGNORECASE), "var"),
    (re.compile(r"\bargument\b", re.IGNORECASE), "arg"),
    (re.compile(r"\bparameter\b", re.IGNORECASE), "param"),
    (re.compile(r"\bstring\b", re.IGNORECASE), "str"),
    (re.compile(r"\binteger\b", re.IGNORECASE), "int"),
    (re.compile(r"\bboolean\b", re.IGNORECASE), "bool"),
    (re.compile(r"\bdictionary\b", re.IGNORECASE), "dict"),
    (re.compile(r"\berror\b", re.IGNORECASE), "err"),
    (re.compile(r"\bexception\b", re.IGNORECASE), "exc"),
    (re.compile(r"\bmessage\b", re.IGNORECASE), "msg"),
    (re.compile(r"\brequest\b", re.IGNORECASE), "req"),
    (re.compile(r"\bresponse\b", re.IGNORECASE), "resp"),
    (re.compile(r"\bconfiguration\b", re.IGNORECASE), "config"),
    (re.compile(r"\benvironment\b", re.IGNORECASE), "env"),
    (re.compile(r"\bdirectory\b", re.IGNORECASE), "dir"),
    (re.compile(r"\bdatabase\b", re.IGNORECASE), "db"),
    (re.compile(r"\bauthentication\b", re.IGNORECASE), "auth"),
    (re.compile(r"\bimplementation\b", re.IGNORECASE), "impl"),
    (re.compile(r"\bdependenc(?:y|ies)\b", re.IGNORECASE), "deps"),
    (re.compile(r"\bdocumentation\b", re.IGNORECASE), "docs"),
    (re.compile(r"\bspecification\b", re.IGNORECASE), "spec"),
    (re.compile(r"\bversion\b", re.IGNORECASE), "ver"),
    (re.compile(r"\bapproximately\b", re.IGNORECASE), "~"),
    (re.compile(r"\bwithout\b", re.IGNORECASE), "w/o"),
    (re.compile(r"\bwith\b", re.IGNORECASE), "w/"),
    (re.compile(r"\bmaximum\b", re.IGNORECASE), "max"),
    (re.compile(r"\bminimum\b", re.IGNORECASE), "min"),
]


def is_code_block(line: str, in_code_block: bool) -> tuple[bool, bool]:
    """Detect if we're inside a fenced code block (don't compress code)."""
    if line.strip().startswith("```"):
        return (not in_code_block, True)
    return (in_code_block, False)


def compress_line(line: str, stats: CompressionStats) -> str:
    """Apply all compression rules to a single line."""
    original = line

    # Phase 1: Remove filler phrases
    for pattern, replacement in FILLER_PHRASES:
        line = pattern.sub(replacement, line)

    # Phase 2: Apply structural rules
    for rule in STRUCTURAL_RULES:
        new_line = rule.pattern.sub(rule.replacement, line)
        if new_line != line:
            stats.rules_applied[rule.rule_id] = (
                stats.rules_applied.get(rule.rule_id, 0) + 1
            )
            line = new_line

    # Phase 3: Apply abbreviations
    for pattern, replacement in ABBREVIATIONS:
        line = pattern.sub(replacement, line)

    # Phase 4: Clean up whitespace
    line = re.sub(r"  +", " ", line)
    line = line.strip()

    return line


def compress_content(content: str) -> tuple[str, CompressionStats]:
    """Compress an entire document, preserving code blocks and structure."""
    stats = CompressionStats(
        original_chars=len(content),
        original_words=len(content.split()),
    )

    lines = content.split("\n")
    compressed_lines: list[str] = []
    in_code_block = False

    for line in lines:
        in_code_block, is_fence = is_code_block(line, in_code_block)

        if in_code_block or is_fence:
            # Never compress inside code blocks
            compressed_lines.append(line)
        elif line.strip().startswith("#"):
            # Preserve headings as-is (structural markers)
            compressed_lines.append(line)
        elif line.strip() == "":
            # Preserve blank lines (structure)
            compressed_lines.append("")
        else:
            compressed_lines.append(compress_line(line, stats))

    result = "\n".join(compressed_lines)
    stats.compressed_chars = len(result)
    stats.compressed_words = len(result.split())

    return result, stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compress natural language prompts/context into symbolic notation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python compress_prompt.py ./CLAUDE.md
  python compress_prompt.py ./skill.md --output ./skill.compressed.md
  python compress_prompt.py ./context.txt --dry-run
        """,
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the .md or .txt file to compress",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output file path (default: <input>.compressed.md)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Print compressed output without writing to file",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print compression statistics",
    )

    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    content = args.input_file.read_text(encoding="utf-8")
    compressed, stats = compress_content(content)

    if args.dry_run:
        print(compressed)
    else:
        output_path = args.output or args.input_file.with_suffix(".compressed.md")
        output_path.write_text(compressed, encoding="utf-8")
        print(f"Compressed: {args.input_file} -> {output_path}")

    if args.stats or not args.dry_run:
        print(f"\n--- Compression Stats ---")
        print(f"  Characters: {stats.original_chars} -> {stats.compressed_chars} ({stats.char_reduction:.1f}% reduction)")
        print(f"  Words:      {stats.original_words} -> {stats.compressed_words} ({stats.word_reduction:.1f}% reduction)")
        if stats.rules_applied:
            print(f"  Rules applied:")
            for rule_id, count in sorted(stats.rules_applied.items()):
                print(f"    {rule_id}: {count}x")


if __name__ == "__main__":
    main()
