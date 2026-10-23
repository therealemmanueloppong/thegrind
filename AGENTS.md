## Current study source (October 23, 2026)

Use `00 STUDY PATH CLEAN FULL CODE - MEDIUM - Google (197).pdf` as the
current source, superseding earlier source selections below. Preserve the
helper/main/tests/follow-up teaching structure in pointacresworkflow.txt.

## Current study source (October 22, 2026)

Use `00 STUDY PATH - Google (288).pdf` in this repository root as the current
question source. This supersedes older references to the 167-question edition.
Keep the guided structure in pointacresworkflow.txt for every question.

## Current Google Study Path reset (October 21, 2026)

This user instruction supersedes the older practice-file workflows below.
Use pointacres.py and pointacresarchived.py exclusively for active study and
archives. Read pointacresworkflow.txt for the current teaching sequence and
program structure. Verify the current Google Study Path PDF before each step.
Older Python files and recovered Sublime copies are backed up under
recovery-backups; do not recreate old practice files unless requested.

## Current full-book archive policy (October 19, 2026)

This explicit user update supersedes older full-book instructions below that
include tests or PDF/book solutions in the archive. The original Google workflow
and its files are unchanged.

- `the720.py` is the clean revision archive: ONLY Emmanuel's completed user
  implementations, necessary shared node classes, question references with their scheduled calendar dates, and
  clear beginner-friendly comments. Do NOT put tests, test helpers, comparison
  classes, book/reference solutions, or a startup print in this file.
- Before archiving, add comments explaining every meaningful line that lacks
  them: variables vs indexes/values, state changes, bounds, stack/pointer order,
  base cases, and why return statements are inside/outside loops. Preserve his
  executable implementation; comments are documentation, not a rewrite.
- Keep tests and any requested comparisons separately in `the720_checks.py`.
  It imports the actual user classes from `the720.py`; avoid duplicate copies
  of user implementations so tests exercise the clean archive.
- Run `python3 -B the720_checks.py` when checking archived work. Running the
  archive alone no longer runs tests. Verify tests before removing a completed
  practice block and preserve unfinished work and shared definitions.
- The October 19 cleanup annotated missing Day 2 comments and retained existing
  Day 1 comments. All 8 solutions and 2 shared node classes have unchanged ASTs.
  All previous test/comparison executable code was moved unchanged to the checks
  file and passed after the move. Tests include all 12 Q53 cases for both versions.
- All Day 1 and Day 2 guided mains (Q46-53) are complete. Day 3-4 Q54-61
  skeletons are now prepared at Emmanuel's request; Q54 is next. No independent
  revision or follow-up has started.

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
- After each problem is completed and its tests have been checked, append ONLY
  Emmanuel's commented implementation to `the720.py`, the clean revision archive.
  Keep tests and requested book comparisons in `the720_checks.py` instead.
  Preserve earlier user implementations and question references.
- `the720study.py` is the active guided-practice file; `the720.py` is the permanent
  revision archive. After archiving a completed question, verify that the archive
  contains its commented user implementation and that separate checks pass,
  then REMOVE that completed
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
  119, 121, 123, and 125. All four Day 2 mains (Q50-53) are complete in `the720.py`; their tests are in `the720_checks.py`.
  `the720study.py` retains shared definitions and no unfinished question.
- Day 2 guided learning is complete. Independent revision of Day 2 has not begun.
  Do not begin follow-ups or a new day without following Emmanuel's next instruction.

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

## Phone practice update (October 17, 2026)

- During phone practice, review code pasted in chat as the active draft. Give one
  small instruction/question at a time as comments inside a code block in chat.
- When a solution is complete, save the user's code in `the720study.py`, write
  and run meaningful tests yourself (explicit phone-mode exception to user-written
  tests), explain expected results, then archive completed work in `the720.py`.
- Q50 Min Stack: user completed the parallel-list implementation in chat and
  explained that storing minimums avoids rescanning the value stack. Assistant
  tests cover minimum restoration, duplicate minimums, and empty/reuse. All three
  passed before archiving. The PDF comparison uses the same algorithm; this
  equivalence was explained. No independent revision or follow-up has started.
- Day 2 Q50-53 are archived; no active skeleton remains. Do not commit/push to GitHub unless
  requested; saving on the Mac and archiving are the authorized phone workflow.

## Q51 completion (October 18, 2026)

- User completed BSTIterator on Mac and explained why next moves right then
  walks left. Guided corrections covered tree .left vs linked-list .next,
  self.stack naming, leftward movement, and accessing .left on None.
- User explicitly requested the assistant finish tests to move to the next main.
  Four assistant-written scenarios passed on both implementations: singleton,
  branching tree, left-only tree, and right-only tree. Each checks repeated
  hasNext calls and exhaustion. Entire archive ran successfully after appending.
- User implementation, tests, and PDF helper-method comparison are archived in
  the720.py; earlier archive content is unchanged. Q51 is removed from active
  practice. Q52 Basic Calculator II is next; Q53 remains an untouched skeleton.
- No independent revision or follow-up has been completed. Return to user-written
  tests on Mac for later questions unless Emmanuel requests otherwise.

## Q52 completion (October 18, 2026)

- Emmanuel dictated the stack calculator line by line; assistant saved only the
  agreed steps. The completed implementation is archived unchanged in `the720.py`.
- At his request, 15 assistant-written tests with expected-result explanations
  were saved and run. All passed, covering precedence, zero, multi-digit numbers,
  spaces, signed truncation, left-to-right division/multiplication, and max integer.
- Matching PDF stack comparison and its 15 checks are also archived. Full archive
  assertions and practice assertions passed before removal of the completed block.
- Discussed that an O(1)-space alternative exists; user explicitly did not request
  its code. Keep that alternative uncoded. No independent revision or follow-up.
- Q52 removed from active practice after verifying the archive. Q53 Verify Preorder
  Sequence in Binary Search Tree is the sole pending skeleton. Explain the problem
  and examples, then check understanding before any coding.

## Q53 completion (October 19, 2026)

- Emmanuel completed the main preorder verification using a stack and lower bound.
  His implementation was preserved without algorithm changes. At his explicit
  request, 12 assistant-written test cases with expected-result explanations
  were added, run, and archived. Coverage includes both PDF examples, valid
  [8,4,2,6,10], invalid [8,4,10,2], a single node, left/right chains, nested
  ancestor violations, nested valid subtrees, and ascending/descending inputs
  of 10,000 unique values. All passed; input-preservation checks also passed.
- Matching PDF comparison is algorithmically equivalent, O(n) time/O(n) space.
  Its same 12 tests passed. Full archive assertions passed after appending;
  existing archive prefix was verified unchanged before practice cleanup.
- All Day 2 mains Q50-53 are complete for guided learning and archived in
  `the720.py`. Completed Q53 removed from `the720study.py` after verification;
  shared definitions preserved. No new question or follow-up prepared.
- Independent understanding still needs revision: user initially thought 8->4
  violated preorder; clarified that descending left is valid and a cutoff
  applies only after entering an ancestor's right subtree. Also corrected
  maximum-so-far vs lower-bound reasoning, if vs while, and storing the popped
  cutoff in lower_bound. Do not infer independent mastery from passing tests.
- Emmanuel requests full current question code shown in chat at each coding
  step, with the next instruction as comments and explicit placement.

## October 18-19 scheduled set prepared (October 19, 2026)

- User requested all eight scheduled question skeletons in `the720study.py`.
  October 18: Q54 Remove Duplicate Letters, Q55 Decode String, Q56 Remove K
  Digits, Q57 Convert BST to Sorted Doubly Linked List. October 19: Q58 Ternary
  Expression Parser, Q59 Add Two Numbers II, Q60 132 Pattern, Q61 Find Permutation.
- Verified dated rows in the saved tracker schedule.json under Documents/Codex/
  2026-10-16/https-chatgpt-com-share-6ad1bad4-60f4/work/. Verified signatures,
  wording and examples against source PDF pages 127,129,131,133-134,135,137,139,141.
- All eight skeletons include names, type signatures, question notes and examples,
  with pass bodies only. No algorithms, implementations or tests supplied. Shared
  TreeNode/ListNode preserved; Node interface added for LC426 left/right links.
- Next learning question: Q54 Remove Duplicate Letters. Explain input/output and
  examples, check understanding, then guide one small coding step at a time.
- Continue the clean archive policy: only commented user solutions in the720.py;
  tests and book comparisons stay separate in the720_checks.py.

## Study chat consolidation (October 19, 2026)

- Emmanuel noticed the accidental separate chat "Find the 720 Grind (3)" and
  asked to merge its progress into the original study chat. Its recent turns
  were read and checked against the shared saved `the720study.py`. Message
  histories cannot be literally merged with the available tools. Continue here
  using the existing files; no source edits or duplicate work are necessary.
- Active question is Q54 Remove Duplicate Letters, still unfinished. Saved code:
  Counter import; stack=[]; seen=set(); counts=Counter(s); for c in s; decrement
  counts[c]; if c in seen: continue. No tests or archiving for Q54 yet.
- Reviewed pitfalls in the other chat: Python compares letters directly, so an
  alphabet helper array is unnecessary; Counter(s) initially counts all
  occurrences and decrementing makes it count occurrences still ahead; mark
  a letter seen only when it is actually kept in stack.
- Exact pending teaching example: s="bab", stack=['b'], current c='a', and
  counts['b']=1. Ask whether to keep the first b before a or remove it and use
  the later b, and ask why. Wait for his reasoning before introducing the
  stack-removal condition. No full solution or future steps revealed.
- Q55-61 remain untouched skeletons. All clean-archive and slow teaching
  preferences remain in effect. No other chat was messaged, archived or deleted.

## Q54 completion and dated archive headings (October 19, 2026)

- Q54 Remove Duplicate Letters: completed user code archived with a purpose
  comment on every meaningful line. AST verified unchanged. Eight fixed tests
  passed before archiving, then all existing checks passed against the archive.
  Tests and expected-result explanations are only in the720_checks.py. No book
  solution was added to the clean archive.
- Removed Q54 from practice only after archive verification. Q55 Decode String
  is now first; Q55-61 skeletons and helpers were preserved. Explain Q55 and
  examples, check understanding, then begin one coding step at a time.
- At Emmanuel's request, every archive question heading now includes its
  SCHEDULED date, day number, PDF question, LC number, and title. Dates were
  checked against saved schedule.json: Day 1 Oct 16, Day 2 Oct 17, Day 3 Oct 18.
  These labels are scheduled study dates, not claims of actual completion dates.
  Use this heading format for every future archived question too.
