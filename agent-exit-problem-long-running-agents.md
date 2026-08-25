# Getting In Is the Easy Part

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Veera%20S%20Gutta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veerasgutta/)

**Published:** August 2026  
**Author:** Veera S Gutta  
**Status:** Research & Thought Leadership  
**LinkedIn:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

## ⚖️ Legal Disclaimer

**IMPORTANT NOTICE:** This document represents personal learning, research, and experimentation conducted independently. All content is created for educational purposes and knowledge sharing within the AI/ML community.

- 🎓 **Educational Content**: Based on publicly available documentation, open-source tools, and community knowledge
- 📚 **Public Research**: Insights derived from publicly available academic papers (ArXiv, Stanford HAI, MIT Technology Review, ACM, IEEE) and open-source projects
- 💡 **Illustrative Examples**: Architecture patterns and examples are created for demonstration purposes, not production specifications
- 🚫 **No Proprietary Information**: Contains no confidential information from any employer or client

---

## 📋 Executive Summary

Every agent demo shows the same thing: something impressive **starting**. A task kicks off, steps execute, progress streams by.

Nobody demos an agent stopping halfway through and leaving things clean.

We have spent three years making agents better at going forward. We have done almost nothing about coming back. That was survivable when a run lasted thirty seconds. It is not survivable now that runs last days.

**Key Insights:**
- 🚪 **Every agent plan is a plan for going forward.** Almost none include a plan for coming back, and nobody notices until the moment it matters.
- ⏳ **Duration changed the stakes.** A thirty-second failure is a retry. A three-day failure is a half-finished state that nobody in the building can describe.
- 🧗 **Register the undo before the step, not after.** Climbers plan the descent before the ascent. Every anchor placed going up is one you use coming down.
- 📞 **Most agent runs are letters, not phone calls.** If it goes wrong at minute two of a four-hour run, you find out at hour four.
- ❓ **When an agent is unsure, the output should be a question, not a guess.** Confident guessing is where invented data comes from.
- 🛠️ **The design rule:** an agent that cannot exit cleanly and cannot call for help should not be sent in alone — regardless of how capable it is going forward.

---

There is a question we ask about every agent we deploy, and a question we almost never ask.

The asked question is: **can it do the task?** We benchmark it, we eval it, we watch it plan and execute and hand back a result. This is the entire visible surface of agent engineering, and we have gotten genuinely good at it.

The unasked question is: **what happens if it stops in the middle?**

Not fails. Not errors out. *Stops.* Four steps into a six-step job, with three of those steps having already changed something real.

Most deployments have no answer. For a long time that was fine, because runs were short enough that the answer was "just run it again." That era ended this year.

---

## The Year Runs Got Long

Something shifted in 2026 and it shifted fast.

The frontier models are now explicitly positioned for **long-running agents** — designed to hold a single task for hours or days rather than a handful of turns. Enterprise messaging moved from *the AI helped someone do the work* to *the AI did the work*. Agents drive real browsers and real desktops. And inference keeps getting dramatically faster, which means the number of consequential actions inside a single run keeps climbing.

A 2024 agent did six things in forty seconds. If it broke, you shrugged and re-ran it.

A 2026 agent does four thousand things over two days, across a dozen systems, most of them while you are asleep. If it breaks at hour nineteen, "just run it again" is not a recovery strategy. It might not even be a safe thing to do.

We scaled the run. We did not scale the recovery.

---

## The Half-Finished Problem

Here is the scenario that keeps showing up, stripped of any particular domain.

An agent has a six-step job. It provisions a resource. It updates a record. It notifies a downstream system. It writes a file somewhere. Then step five hits something unexpected — a permission it does not have, a response shape it did not anticipate, a rate limit, a genuine ambiguity — and it stops.

The job is not done. That much is obvious.

But the job is also not *undone*. Four real things happened to real systems. There is no error state that captures this, because it is not an error. There is no success state, because it did not succeed. There is a third thing, and most platforms have no word for it.

Call it **stranded**.

Stranded state is expensive in a way that failure is not. Failure is legible — you see it, you retry, you move on. Stranded state is illegible. Someone has to go find out what actually happened, in what order, to which systems, and decide what to do about each one. That someone is a human, usually on a weekend, usually without a map.

And the longer the run, the bigger the map they do not have.

---

## Forward Planning and Return Planning

The root cause is that we only ever design one direction of travel.

| | Planning the way in | Planning the way out |
|---|---|---|
| **What it answers** | What steps get me to the goal? | How do I leave cleanly from any step? |
| **When it's designed** | Always — it *is* the task | Almost never |
| **What it costs** | Nothing extra | One additional decision per step |
| **Who notices it's missing** | Nobody | One person, at the worst possible moment |

Look at that last row. Forward planning is self-enforcing — an agent without a plan to move forward simply does not work, so the gap announces itself immediately. Return planning is the opposite. Its absence is completely invisible during every successful run, and completely decisive during the one that is not.

That asymmetry is why this gap survives in production systems built by careful people. Nothing in normal operation surfaces it.

---

## The Descent Is Planned First

Climbers have a rule that translates almost perfectly.

You do not summit and then work out how to get down. The descent is planned before the ascent begins, because most accidents happen on the way back — when you are tired, the weather has turned, and the decisions are worse. So every anchor you place going up is an anchor you have already decided you will use coming down. The route out is built *while* you build the route in, using the same effort, at the same time.

Apply that to an agent and the rule becomes concrete and unglamorous:

> **Before an agent takes a step that changes something real, the undo for that step should already be written down.**

Not discoverable. Not inferrable. Written down, at the moment the step is taken, so that unwinding is a matter of reading a list backward rather than a matter of investigation.

When step five fails, you do not launch a forensic exercise. You pop step four, then three, then two, then one, in reverse, executing the undo that was registered alongside each. You end where you started. Nothing is stranded, because nothing was ever taken without its return ticket.

And when a step has no possible undo — some genuinely do not — that is not a detail to note in a runbook. That is a hard stop. A step with no way back is a step an agent should not take on its own, no matter how well it has performed up to that point.

---

There is a version of this idea in the Indian epics that is worth borrowing, because it is unusually precise about the failure.

A young warrior learned how to break into an impenetrable battle formation, but never learned how to get out of it. He went in anyway. He fought brilliantly — by every account the best fighting of the day — and he was surrounded, while his own army was blocked at the entrance and could not reach him. He did not lose because he was outmatched going in. He lost because there was no way back and no way to call for help.

Skill at entry was never the constraint. It just looked like the only one.

---

## The Other Half: You Cannot Help What You Cannot Hear From

An exit path solves one half of the problem. The other half is that most agent runs are structurally unreachable while they are happening.

The dominant interaction shape is still request and response. You send the task, the agent disappears into it, and you learn the outcome when it is over. This was a perfectly reasonable design when "when it is over" meant thirty seconds from now.

At four hours, it means something different. If the run went sideways at minute two, you spent the next two hundred and thirty-eight minutes watching a progress indicator that told you nothing, on a job that was already lost.

Long runs need a line that stays open, and it has to carry traffic in both directions.

**Outbound**, the agent needs to be able to say more than "working." It needs to say *where it is*, what it just changed, and — most importantly — when it is not sure. Something closer to: *"I found twelve records that do not match the expected shape. I can skip them, process them with a guess, or stop and wait. I would recommend skipping."*

**Inbound**, you need to be able to answer without restarting anything. *Skip them.* *Stop.* *Do not touch that system.* *Yes, continue.* Steering a run in flight is a fundamentally different capability from approving one before it starts, and almost no platform has it.

That outbound half matters more than it first appears. An agent that is unsure has exactly two options: **ask** or **guess**. Today, the overwhelming default is guess — confidently, in the correct format, with the correct tone, which is precisely why invented table names and fabricated figures are so hard to catch. A confidence floor that converts uncertainty into a question is one of the cheapest quality controls available, and one of the least used.

The safe default matters too. If nobody answers the question in time, the agent should take the *most conservative* branch, not the most ambitious one. Silence is not consent.

---

## What This Looks Like In Practice

Four changes. None of them exotic, none of them research.

**1. Write the undo at the same moment as the action.**
Keep the undos in order, and unwind in reverse on failure. If a step has no registered undo, it does not run autonomously — it queues for a human to execute. Not approve. Execute.

**2. Make long runs suspendable, and make resume honest.**
A run that lasts days must be able to pause and continue. Capture where it was, what it had learned, and — this is the part people miss — **what it was permitted to do at the time it stopped**. A run that suspends on Monday and resumes on Thursday should not quietly resume on Monday's permissions.

**3. Keep the line open in both directions for the life of the run.**
Progress out, steering in. And keep it on a channel separate from the work itself, so that a stuck task does not also mean a silent one. The most useless failure mode is an agent that is both broken and unreachable.

**4. Set a confidence floor, and give the timeout a safe answer.**
Below the floor, the agent asks instead of proceeding. If nobody responds, it takes the conservative branch and records that it did.

---

## The Part Nobody Wants to Hear

This makes agents look slower and considerably less magical.

The impressive demo is impressive partly *because* nothing stands between intent and consequence. The agent decides, and the thing happens. Add return planning and a confidence floor, and some of that fluency turns into pauses, questions, and steps that stop and wait for a person.

That is the trade, and it is the same trade in a different costume. The previous version of this argument was about what happens *after* an action you cannot take back. This one is about what happens *during* a run you cannot get out of. Both come down to the same uncomfortable principle: capability going forward was never the binding constraint. Recoverability was.

Teams will make this trade either deliberately or by accident. The ones who make it deliberately will ship less impressive demos this year and will not spend a weekend reconstructing what an agent did to four systems before it stopped.

---

## What To Do Next

One exercise, worth more than any framework.

**Take your longest-running agent job and write down what happens if it dies at step four.**

Who finds out. How they discover which steps completed. Where the undo for each one lives. How long the cleanup takes. Whether anyone has ever actually done it.

You will find three groups. Some jobs unwind cleanly — those are safe to run longer and more autonomously. Some have a cleanup story that exists only in one person's head — those need writing down before that person takes a holiday. And some have nothing at all, where the honest answer is "we would figure it out."

That third list is your real risk register. It is usually shorter than people fear and considerably more alarming than they expect.

Most teams have never made this list. It takes an afternoon.

---

## One Last Thought

We taught agents to go further. We did not teach them to come back.

For a while those were the same skill, because the distance was short enough that the return trip was trivial. That is no longer true, and the gap will not announce itself. It will sit quietly through every successful run and present its bill exactly once.

Going in is a capability question.
Coming out is a survival question.

Only one of them gets harder as agents run longer. And it is not the first one.

---

---

**Related Articles:**
- [Power You Can't Withdraw Isn't Authority](./reversibility-undo-problem-agent-autonomy.md)
- [The Agent That Remembers: Why Persistent Memory Is the Next Trust Boundary](./agent-memory-persistent-state-trust-boundary.md)
- [Agent Identity: OAuth Was Built for Humans — What Works for Machines?](./agent-identity-oauth-built-for-humans.md)
- [Autonomous, Deterministic & Self-Healing Systems](./autonomous-deterministic-systems-architecture.md)
- [Digital Colleagues: Accountability, Ownership & Judgment](./digital-colleagues-accountability-ownership-judgment.md)
- [AI Trust Boundaries: Protecting Platforms in the Age of Agentic AI](./ai-trust-boundaries-protecting-platforms.md)
- [Eval-Driven Development: Building AI Pipelines That Judge Themselves](./eval-driven-development-ai-pipeline-judges.md)
- [The Invisible Fortress: Why Every Enterprise Needs an Agentic Operating System](./agentic-os-invisible-fortress-enterprise.md)
- [The Dharma Machine: Ancient Indian Wisdom & Governing AI](./the-dharma-machine-ancient-indian-wisdom-governing-ai.md)

---

**Connect with me:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

## 🔗 Related in this series

- [Power You Can't Withdraw Isn't Authority](./reversibility-undo-problem-agent-autonomy.md) — the undo *after* an action; this article covers the exit *during* a run
- [Prove It Without Keeping It](./prove-it-without-keeping-it-zero-retention-audit.md) — unwinding a stranded run is much harder when you are not permitted to keep the record of what it did
- [The Agent That Remembers](./agent-memory-persistent-state-trust-boundary.md) — why a suspended run has to capture what the agent learned, not just where it stopped
- [Autonomous, Deterministic & Self-Healing Systems](./autonomous-deterministic-systems-architecture.md) — the recovery patterns this argument depends on
- [Digital Colleagues: Accountability, Ownership & Judgment](./digital-colleagues-accountability-ownership-judgment.md) — who owns the cleanup when a run strands

---

*Going in is a capability question. Coming out is a survival question.*
