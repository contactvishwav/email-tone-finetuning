import json

# Three categories: grammar only, clarity only, both.
# Outputs fix errors and improve clarity WITHOUT changing tone or meaning.
data = [
    # --- GRAMMAR ONLY ---
    {
        "input":  "The team are struggling to meet the deadline and we needs your help.",
        "output": "The team is struggling to meet the deadline and we need your help.",
    },
    {
        "input":  "I have went to the meeting yesterday and took notes for everyone.",
        "output": "I went to the meeting yesterday and took notes for everyone.",
    },
    {
        "input":  "Between you and I, the project is already two weeks behind schedule.",
        "output": "Between you and me, the project is already two weeks behind schedule.",
    },
    {
        "input":  "He don't have access to the shared drive and cannot view the files.",
        "output": "He doesn't have access to the shared drive and cannot view the files.",
    },
    {
        "input":  "You should of flagged this issue before it reached the client.",
        "output": "You should have flagged this issue before it reached the client.",
    },
    {
        "input":  "We didn't receive no response from the vendor after three follow-ups.",
        "output": "We didn't receive any response from the vendor after three follow-ups.",
    },
    {
        "input":  "I reviewed the proposal yesterday and I will find two sections that need revision.",
        "output": "I reviewed the proposal yesterday and found two sections that need revision.",
    },
    {
        "input":  "The informations in the report are outdated and need to be updated.",
        "output": "The information in the report is outdated and needs to be updated.",
    },
    {
        "input":  "After reviewing the code, the bug was obvious and needed to be fixed.",
        "output": "After reviewing the code, I found an obvious bug that needed to be fixed.",
    },
    {
        "input":  "Each of the team members have submitted their timesheets on time this week.",
        "output": "Each of the team members has submitted their timesheet on time this week.",
    },

    # --- CLARITY ONLY ---
    {
        "input":  "When Anna and Claire submitted the report, she received all the credit.",
        "output": "When Anna and Claire submitted the report, Anna received all the credit.",
    },
    {
        "input":  "I wanted to let you know that we have completed phase one and are moving to phase two which will take three weeks and we need your sign-off before we can start so please let me know your availability.",
        "output": "We have completed phase one and are moving into phase two. This phase will take three weeks, and we need your sign-off before we can start. Please let me know your availability.",
    },
    {
        "input":  "Due to the fact that the meeting was cancelled, we are in a situation where all attendees need to be notified of the reschedule.",
        "output": "Because the meeting was cancelled, all attendees need to be notified of the reschedule.",
    },
    {
        "input":  "Mistakes were made in the budget projections and corrections will be submitted before Friday.",
        "output": "I made mistakes in the budget projections and will submit corrections before Friday.",
    },
    {
        "input":  "I just wanted to quickly reach out and touch base with you regarding the current status of the onboarding process at this point in time.",
        "output": "I wanted to check on the current status of the onboarding process.",
    },
    {
        "input":  "Hope you had a great weekend! I also wanted to mention that the quarterly results are ready, and I was also thinking about the team lunch, but the main thing is that the client approval is needed by tomorrow.",
        "output": "The client approval is needed by tomorrow. The quarterly results are also ready for your review.",
    },
    {
        "input":  "We need to make a decision about whether to make a recommendation to the board regarding the implementation of the new system.",
        "output": "We need to decide whether to recommend implementing the new system to the board.",
    },
    {
        "input":  "Please review the attached files and the documents from last week. These will help with the audit.",
        "output": "Please review the attached files and the documents from last week. Both sets of documents will help with the audit.",
    },
    {
        "input":  "The reason why the deadline was missed is because the vendor failed to deliver the components that we needed, which were supposed to arrive last Monday.",
        "output": "The vendor failed to deliver the components we needed, which were due last Monday. This caused us to miss the deadline.",
    },
    {
        "input":  "Please revert back to me with your final decision at your earliest possible convenience.",
        "output": "Please get back to me with your final decision at your earliest convenience.",
    },

    # --- BOTH GRAMMAR AND CLARITY ---
    {
        "input":  "I has reviewed the contract and there is several issues I want to discuss and also we need to schedule a meeting as soon as possible because the deadline is approaching fast.",
        "output": "I reviewed the contract and found several issues I want to discuss. We need to schedule a meeting soon, as the deadline is approaching.",
    },
    {
        "input":  "The project was completed yesterday and all deliverables have been submitted and the client was informed and they was happy with the results.",
        "output": "The project was completed yesterday. All deliverables were submitted and the client was informed. They were happy with the results.",
    },
    {
        "input":  "John and Mike both worked on the proposal but he done most of the writing.",
        "output": "John and Mike both worked on the proposal, but John did most of the writing.",
    },
    {
        "input":  "You should of included the budget breakdown due to the fact that the stakeholders would of wanted to see it.",
        "output": "You should have included the budget breakdown because the stakeholders would have wanted to see it.",
    },
    {
        "input":  "The data are showing a downward trend and we needs to address this in the next meeting which is scheduled for Thursday at 2pm and everyone should be prepared to discuss solutions.",
        "output": "The data shows a downward trend. We need to address this in Thursday's 2pm meeting, and everyone should come prepared to discuss solutions.",
    },
    {
        "input":  "Between you and I, the same identical issue has occurred before in the past and nothing was done about it.",
        "output": "Between you and me, this issue has occurred before and nothing was done about it.",
    },
    {
        "input":  "We didn't receive no feedback on the design and a decision hasn't been made by the team yet.",
        "output": "We haven't received any feedback on the design, and the team hasn't made a decision yet.",
    },
    {
        "input":  "Hope all is well! Wanted to touch base about couple of things, first I like to say the documentation is great, but main issue is that the API endpoint is returning incorrect data.",
        "output": "The API endpoint is returning incorrect data — this needs to be resolved. Also, the documentation looks great.",
    },
    {
        "input":  "I just wanted to quickly let you know that I have reviewed the code and I will find two bugs which I am fixing now and will submit a PR by end of day.",
        "output": "I reviewed the code and found two bugs. I am fixing them now and will submit a PR by end of day.",
    },
    {
        "input":  "Before Sarah and Tom presented, she had a discussion with the client to get an understanding of their requirements and to make an evaluation of their current system.",
        "output": "Before Sarah and Tom presented, Sarah discussed the client's requirements and evaluated their current system.",
    },
    {
        "input":  "I have spoke with the vendor this morning and they have said that they can have the fix ready by Wednesday which is earlier than we expected and we should let the client know about this update as soon as possible.",
        "output": "I spoke with the vendor this morning. They confirmed the fix will be ready by Wednesday, which is earlier than expected. We should update the client as soon as possible.",
    },
    {
        "input":  "The reports has been reviewed by the team and due to the fact that there is errors found in section three, a revision needs to be made before submission.",
        "output": "The team reviewed the reports and found errors in section three. These need to be corrected before submission.",
    },
    {
        "input":  "You must need to resubmit your application again since the previous one was incomplete and missing required information.",
        "output": "You need to resubmit your application since the previous one was incomplete.",
    },
    {
        "input":  "When the manager and the intern worked on the presentation, she learned a lot and he was providing guidance throughout the whole entire process.",
        "output": "When the manager and the intern worked on the presentation, the intern learned a lot and the manager provided guidance throughout.",
    },
    {
        "input":  "Each of the reports were reviewed individually and the findings is summarized in the attached document which you should read before our Thursday meeting.",
        "output": "Each report was reviewed individually, and the findings are summarized in the attached document. Please read it before our Thursday meeting.",
    },
]

out_filename = "email_improver.jsonl"
with open(out_filename, "w") as f:
    for entry in data:
        record = {
            "instruction": f"Fix the grammar and improve clarity: {entry['input']}",
            "output": entry["output"],
        }
        f.write(json.dumps(record) + "\n")

print(f"Generated {len(data)} examples in {out_filename}")
