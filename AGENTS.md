# Google study workflow

For the original Google study workflow, use `Google Questions - 2 column - 1 - Last 30 days.pdf`
(the 62-page edition containing 26 questions), in its question order.
The separate full-book study workflow is specified below.

## Three passes agreed with Emmanuel

1. Learning pass: cover the MAIN problem for all 26 questions in order.
   Explain the input/output, brute force, and optimal solution simply and slowly.
   Guide Emmanuel with one small question at a time while he writes code.
   Read the latest saved file whenever asked to review; never guess its contents. Before preparing the next question, verify its exact title, wording, and examples directly in the PDF.
   Review the implementation and guide him to write his own direct assert tests.
2. Independent assessment pass: after learning all 26 mains, return to question 1
   and cover all 26 mains again in order. Emmanuel codes each solution from scratch
   in study.py, explains it, and writes his own test cases. Assess the complete
   implementation, explanation, and user-written tests together. Guide corrections
   and verify meaningful tests before moving to the next question.
   Finish this pass successfully for every main question before starting follow-ups.
3. Follow-up pass: only then revisit each question's follow-ups in order. Extend
   that question's existing solution, reuse helpers where appropriate, and present
   one complete organized program. Mark NEW/CHANGED/REMOVED regions and explain
   why changes are needed. Distinguish simple baselines from advanced optimizations.

## Files and current progress

- study.py: active practice file. Contains question 8's skeleton, ready for practice.
- studied.py: archive of completed MAIN solutions for questions 1 through 7,
  with passing user-written assertions for each. Append completed work;
  never replace earlier archived solutions.
- Pass 1 is active. Main questions 1–7 are complete.
- Next: question 8 (Shortest Path Nodes and Escaping a Pursuer), MAIN problem only.
- Question 3 used the PDF's TWO-LIST ordering variant can_merge_orders(a, b).
- Do not recreate studymain.py or the720main.py unless asked.
- Keep this progress updated when a question or pass is completed.

## Teaching preferences

Before every next coding step, read the latest saved code when needed and
name the exact insertion point: after which existing line, inside or outside
which block, and the required indentation. Show a small excerpt with the new
location marked. Give one change or one guiding question at a time; do not jump
to the next phase without making placement explicit.

When a technical term comes up during guided practice, let Emmanuel explain
it in his own words FIRST. Do not immediately define it or reveal the answer.
Listen to his interpretation, then correct only errors or fill missing details.

Use plain explanations, name the exact line being discussed, and pause for
understanding before moving on. Keep examples consistent and define every number.
Do not give a finished answer during guided practice unless requested; use hints.
When a user says to inspect, read saved code before judging. Explain each important
line's purpose. Preserve their code and completed solutions. Never claim a test,
save, commit, or push occurred unless verified. Commit/push when requested.

Provide only skeletons in study.py until Emmanuel codes the solution.
When giving example/test inputs, place them in study.py if requested and always
state their location explicitly. Show comparison solutions only in the chat when
requested that way; do not replace his implementation.


## Full-book daily study workflow (agreed October 16, 2026)

This separate workflow uses `All Questions - 2 column (Medium, Hard, Easy).pdf`
and the dated study tracker. Its practice file is `the720study.py`.
Keep the original Google workflow and its practice/archive files separate.

- Follow the chosen day's questions in tracker order: Mediums first, then Hards,
  then Easies. The plan starts October 16, 2026, with four Mediums per day,
  then three Hards per day, then five Easies per day. Exclude the completed
  Trees & BST section (45 Medium, 5 Hard, 18 Easy).
- When Emmanuel requests a day or a set of problems, first read the exact
  questions, signatures, and examples from the source PDF. Put skeletons for
  every question in that requested set into `the720study.py`, without solution
  code. Include only necessary signatures, data structures, problem references,
  and empty bodies; do not reveal algorithms in implementation comments.
- Work on one problem at a time. Explain its input/output and one or two
  concrete examples in plain language, then ask whether he understands.
  Wait for understanding before beginning guided coding.
- Guide him with one small question at a time, starting with the base case
  when relevant and continuing through each remaining part of his solution.
  Let him write the code himself. Offer incremental hints without giving the
  finished answer unless he explicitly asks for it.
- After he implements a problem, ask him to write two or three meaningful
  tests, including a suitable edge case. Read his latest saved code and tests
  before reviewing, and guide corrections. Run tests only when appropriate;
  never claim they passed without running them.
- When adding test scaffolds, provide the call/input and leave the expected
  result after `==` blank for Emmanuel to write. Do not supply the answer
  unless he asks. A requested blank assertion is intentionally incomplete;
  wait for him to fill it before running the file.
- Only after he has completed and tested that problem, append a clearly
  labeled comparison solution in the SAME `the720study.py` file, using the PDF
  or a verified primary online source. Do not overwrite his implementation or
  earlier work. Use distinct function names or classes so both remain usable.
- Explain how his solution differs from the comparison: reasoning, correctness,
  readability, time/space complexity, and any useful improvement. If his approach
  is already equivalent, say so. Verify online sources when using them.
- After each problem is completed and its user-written tests have been checked,
  append that problem's completed work to `the720.py`, the revision archive.
  Archive his implementation, his tests, and the labeled comparison solution
  after discussing the comparison. Preserve all earlier archive entries; never
  replace or truncate them. Keep question references and distinct names so
  archived implementations and tests remain understandable and usable.
- `the720study.py` is the active guided-practice file; `the720.py` is the permanent
  revision archive. After archiving a completed question, verify that the archive
  contains its implementation, tests, and comparison, then REMOVE that completed
  question block from the practice file, as Emmanuel requested. This brings the
  next question to the top. Preserve shared node definitions, pending skeletons,
  and all unfinished user work. Keep using the same practice file; do not create
  a new file for each question.
- Day 1 Q46 Simplify Path, Q47 Flatten Binary Tree, Q48 Reorder List, and Q49
  Evaluate Reverse Polish Notation are complete for guided learning. All four
  user implementations, their tests, and their labeled comparisons are archived
  in `the720.py`; completed blocks are removed from `the720study.py`.
- All archive assertions passed before and after commenting. Clear explanatory
  comments cover every meaningful executable line in all eight solution versions
  and both shared node classes (111 added comment lines). An AST comparison
  verified executable code and test expectations were unchanged.
- Q49 tests cover a zero answer, mixed operations, and negative division toward
  zero. All three and the comparison's matching checks passed.
- Guided completion is not independent mastery. No Day 1 revision attempt has
  started. Emmanuel explicitly deferred revision and requested TODAY'S four new
  question skeletons; follow that change rather than starting revision now.
- Current active set: Day 2, October 17, 2026, four Medium Stack questions:
  Q50 Min Stack (LC 155), Q51 Binary Search Tree Iterator (LC 173), Q52 Basic
  Calculator II (LC 227), Q53 Verify Preorder Sequence in Binary Search Tree
  (LC 255). These match the dated tracker and current source PDF pages
  119, 121, 123, and 125. All four skeletons are saved in `the720study.py`,
  with signatures, problem notes, empty bodies, and test areas only.
- Next learning question when Emmanuel is ready: Q50 Min Stack. Explain the
  problem and examples first, check understanding, then guide one coding step
  at a time. Let him interpret technical terms before providing definitions.

## Full-book independent revision routine (requested October 17, 2026)

Required before the FIRST Day 1 revision: after Q49 is completed, tested,
compared, and archived, go through `the720.py` and add clear line-by-line comments
inside all four completed user solutions and their labeled comparison versions.
Explain each meaningful line's purpose, how state/pointers change, and why the
order of operations matters, in plain language suitable for later revision.
Explain base cases, loop bounds, saved references, end markers, stack order, and
operator/operand order where relevant. Preserve the executable code, user
implementations, test expectations, and archive history; this is documentation,
not an algorithm rewrite. Run the archive assertions before and after commenting.
This Day 1 annotation step is COMPLETED: comments are saved, the executable
AST is unchanged, and archive assertions passed. Day 1 revision remains deferred
at Emmanuel's explicit request to prepare the Day 2 questions instead.

Finish ALL questions in the requested day/set before starting revision.
For Day 1, finish all FOUR questions (Q46-49), including tests, comparisons,
and archiving, then begin revision from Q46 and continue through Q49 in order.
Do not offer revision between individual questions in this learning set.
Repeat revision rounds over the whole set as needed until Emmanuel can explain
and solve them independently. He may stop whenever he wants; follow any later
explicit change to this plan.

- Prepare each question again with its statement and a fresh skeleton in the
  SAME `the720study.py`. Keep archive solutions out of the revision prompt.
  Preserve unfinished work and pending questions when preparing a revision.
- Let Emmanuel talk through the approach, interpret technical terms, and code
  independently before evaluating. Do not supply the explanation or solution
  in advance. Follow his request if he needs a small hint.
- Read the latest saved file. Judge the whole implementation, his explanation,
  correctness, edge cases, complexity, and two or three meaningful tests.
- When there is a mistake, ask one targeted question at a time to help him find
  and fix it. Give incremental hints rather than the correction outright.
- Track revision attempts separately from guided learning. Repeat the same
  questions across rounds until he can explain and solve them independently;
  do not infer mastery from one assisted completion. Record concrete evidence
  of strengths, errors, and remaining practice needs after each attempt.
- Preserve earlier archive entries. An additional independently completed
  attempt may be appended with a clear revision label; never overwrite the
  learning solution or claim a revision occurred before it has happened.
