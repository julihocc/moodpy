# Example course quiz brief

This is a runnable teaching example, not an educator-approved assessment.
Replace it with the actual educator's decisions when adapting the recipe.

- Audience: introductory mathematics and finance learners.
- Language: English. Adapt wording and accepted text answers when changing language.
- Objectives: add integers; solve linear equations; calculate annual compound interest;
  classify integers by sign.
- Families: addition, linear, compound, sign; 10 variants of each in the full bank.
- Bounds: addition 1–99 with distinct operands; linear a and x -10–10 excluding zero,
  b -20–20; principal $1,000–$50,000 in hundreds, annual rate 3–15% in tenths,
  term 2–20 years; integer sign -1,000–1,000.
- Answers: exact integers for arithmetic/algebra; compound amount rounded to cents
  with 0.1% relative tolerance; sign answers positive, negative, zero (case insensitive).
- Feedback: explain the calculation or classification for each sampled variant.
- Categories: Mathematics/Arithmetic, Mathematics/Algebra,
  Finance/Compound interest, Mathematics/Short answer.
- Review status: draft. Discuss representative questions before bulk generation.
- Reproduction: seed 42 initially; retain family IDs when changing counts.

Generate representative questions with `--samples 2`, revise the recipe and brief
from feedback, then generate the full bank. The exported manifest records actual
counts; `--manifest` restores them when regenerating a sample or customized bank.
Moodle quiz timing, total grade, attempts, and question selection are configured
in Moodle after importing the question bank.
