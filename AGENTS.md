# Google study workflow

This chat studies only `Google Questions - 2 column - 1 - Last 30 days.pdf`
(the 62-page edition containing 26 questions), in its question order.

## Three passes agreed with Emmanuel

1. Learning pass: cover the MAIN problem for all 26 questions in order.
   Explain the input/output, brute force, and optimal solution simply and slowly.
   Guide Emmanuel with one small question at a time while he writes code.
   Read the latest saved file whenever asked to review; never guess its contents.
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

- study.py: active practice file. Contains question 5's skeleton, ready for practice.
- studied.py: archive of completed MAIN solutions for questions 1, 2, 3, and 4,
  with passing user-written assertions for each. Append completed work;
  never replace earlier archived solutions.
- Pass 1 is active. Main questions 1–4 are complete.
- Next: question 5 (Longest Non-Decreasing Subarray with One Replacement), MAIN problem only.
- Question 3 used the PDF's TWO-LIST ordering variant can_merge_orders(a, b).
- Do not recreate studymain.py or the720main.py unless asked.
- Keep this progress updated when a question or pass is completed.

## Teaching preferences

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
