# The Agent That Marked Its Own Homework

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Veera%20S%20Gutta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veerasgutta/)

**Published:** September 2026  
**Author:** Veera S Gutta  
**Status:** Research & Thought Leadership  
**LinkedIn:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

The agent says, "Done."

The customer says, "Then why can't I log in?"

Imagine a support request like this:

> "Please stop my subscription renewing next month. I still need access until then."

The agent reads the message, calls the cancellation tool and sends a polite confirmation. The ticket closes. The dashboard records another successful resolution.

But the agent chose **cancel immediately** instead of **cancel at renewal**. The customer lost access they had already paid for.

No service crashed. No tool returned an error. The cancellation worked exactly as instructed.

The deeper failure is not that the action happened. It is that the system treated a completed tool call as proof of the right customer outcome. A self-reported success can still be wrong when reality changes underneath it.

**The system measured whether the action ran. The customer cared whether it was right.**

*This is an illustrative scenario, not a reported incident.*

## When a Mistake Becomes Its Own Proof

Now imagine the workflow asks the same agent to review what it just did.

It checks its summary: "Customer requested cancellation. Subscription cancelled. Confirmation sent."

Everything matches. It marks the task complete.

The detail it missed the first time, "I still need access until then," is missing from the review too. The original misunderstanding has become the explanation for why the work was correct.

That is what it means for an agent to mark its own homework. Not just making a mistake, but controlling the evidence used to judge it.

Adding a reviewer agent does not automatically solve it. If the reviewer receives only that summary, it may agree for exactly the same reason.

**A second opinion is useful. A second copy of the same assumption is not.**

## What a Real Check Would See

Run the same request again, this time with three distinct responsibilities.

**The agent proposes the action.** Stop renewal on the customer's account, while preserving access through the paid period.

**A separate control checks permission.** Does the proposed action match this account, this date and the company's cancellation policy? Permission to stop the next renewal does not authorize closing the account today.

**A verifier checks the result.** It reads the billing and access records. Renewal is off. Paid-through access remains on. Now the workflow has evidence that the customer got what they asked for.

For this routine request, no person needs to approve every click. Software can enforce the policy and compare the records. A person steps in when the request is ambiguous, the policy does not cover it, or the result cannot be confirmed.

The important boundary is not how many agents or people appear in the diagram. It is whether the doer can change the rules, invent an approval, or decide for itself what counts as success.

This is a familiar design rule from payments and code review: the person doing the work should not be its only source of permission and assurance. AI makes that distinction more important, not less.

**A system is only as trustworthy as the evidence it cannot control.**

## Give the Reviewer Something to Disagree With

A reviewer needs the original request, the applicable rules and the actual outcome. Not just a polished account of what the first agent says it did.

It also needs the authority to stop completion when the evidence does not agree. A logged objection that is ignored is not a control. It is theatre.

Recent work on long-running agent systems describes the same pattern: separate the agent doing the work from the agent evaluating it. The evaluator still needs calibration, because a second model can be biased in the wrong direction—especially when it is judging its own execution path instead of the actual customer outcome.

## The Question the Dice Could Not Answer

In the [dice-game episode of the Mahabharata](https://www.sacred-texts.com/hin/m02/m02058.htm), the ancient Indian epic, King Yudhishthira accepts a challenge from his cousin Duryodhana. But Duryodhana does not play himself. His uncle Shakuni, a skilled and deceitful gambler, plays on his behalf.

As the game continues, Yudhishthira loses his wealth and kingdom. He then stakes and loses his brothers, followed by himself. Even after losing his own freedom, he stakes Draupadi, the wife of the Pandava brothers.

Draupadi refuses to accept that the announced result settles the matter. Her [question to the court](https://www.sacred-texts.com/hin/m02/m02066.htm), in plain language, is this:

**If he had already lost himself, what right did he still have to stake me?**

She is challenging the authority behind the action, not merely the outcome of a throw.

The court is full of elders, advisers and relatives. Some do object. Others hesitate or defend the result. The problem is not the dice; it is the authority behind the move.

Draupadi's question cuts to the heart of it: **if the player had already lost the right to act, what authority did he still have to decide the next move?** That is the governance question for AI systems too.

The lesson is simple: **a recorded outcome is not proof of a legitimate decision.** In an agent workflow, the real question is not whether the action was logged. It is whether the actor still had authority, whether the evidence is independent, and whether a valid objection could stop execution.

Our support agent was permitted to stop the next renewal. That did not authorize removing today's access. A reviewer that only confirms "subscription cancelled" accepts the result without checking the boundary that mattered.

**Watching is not the same as checking. And a check that cannot change what happens next is not an effective safeguard.**

## The Most Useful Answer May Be "Not Yet Verified"

Suppose the access service is unavailable when the verifier checks.

The agent may have done the right thing. But we cannot confirm it yet.

Keep the task awaiting verification. Check again within a defined window, then escalate if necessary. Do not repeat the cancellation blindly, and do not tell the customer that everything has been confirmed.

That sounds like a small wording change. It is actually a change in what the system is allowed to claim.

The same discipline applies to evaluation scores. A quick, friendly reply cannot compensate for taking away paid access. A confirmed policy violation needs its own blocking verdict. An uncertain finding needs investigation, not a reassuring average.

There is a difference between a workflow that is unfinished and one that has finished incorrectly. Operators need to see both.

## Better Checks Can Mean Less Supervision

It is easy to hear "oversight" and imagine an employee watching every agent action. That would defeat much of the purpose of automation.

Useful autonomy looks different. Routine work proceeds inside clear limits. Independent checks establish the outcome. People handle the exceptions and remain accountable for the rules.

The customer in our example did not need three agents discussing cancellation. They needed one request understood, one permitted change, and one reliable check that access remained intact.

**The goal is not to make every action slower. It is to make fewer wrong actions look successful.**

## One Question for Your Next Design Review

Choose one consequential workflow: changing an account, issuing a refund or deploying a release.

Remove the agent's final "completed successfully" message from the record.

**Could you still prove that the right thing happened?**

If the answer depends on what the agent said about its own work, that is the next control to build.

The future of agentic systems will not be decided by how often they act. It will be decided by whether the system can prove those actions were valid.

*Give agents room to act. Give the system a way to prove them wrong.*

---

## ⚖️ Legal Disclaimer

**IMPORTANT NOTICE:** This document represents personal learning, research, and experimentation conducted independently. All content is created for educational purposes and knowledge sharing within the AI/ML community.

- 🎓 **Educational Content**: Based on publicly available documentation, open-source tools, and community knowledge
- 📚 **Public Research**: Insights derived from publicly available academic papers (ArXiv, Stanford HAI, MIT Technology Review, ACM, IEEE) and open-source projects
- 💡 **Illustrative Examples**: Architecture patterns and examples are created for demonstration purposes, not production specifications
- 🚫 **No Proprietary Information**: Contains no confidential information from any employer or client

---

## 🔗 Related in this series

- [Eval-Driven Development](./eval-driven-development-ai-pipeline-judges.md): how to evaluate an agent's work; this article asks what makes the check independent.
- [Capability Is Becoming a Privilege](./capability-is-becoming-a-privilege-earned-agent-access.md): what earns authority, and who can verify that it was earned.
- [Prove It Without Keeping It](./prove-it-without-keeping-it-zero-retention-audit.md): preserving evidence while limiting retained content.
- [Power You Can't Withdraw Isn't Authority](./reversibility-undo-problem-agent-autonomy.md): what happens when a verified failure needs recovery.

**Connect with me:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)
