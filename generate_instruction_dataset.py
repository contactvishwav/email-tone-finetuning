import json

# 45 examples across 4 categories.
# The instruction varies per example — the model must learn to follow it.
data = [

    # --- TONE: POLITE AND CONFIDENT ---
    {
        "instruction": "Rewrite this email in a polite and confident tone",
        "email": "Send me the report ASAP.",
        "output": "I'd appreciate receiving the report by end of day today. Thank you for your help.",
    },
    {
        "instruction": "Rewrite this email in a polite and confident tone",
        "email": "Where is my update? You said you'd send it by noon.",
        "output": "I wanted to follow up on the update you mentioned would be ready by noon. Could you let me know the current status?",
    },
    {
        "instruction": "Rewrite this email in a polite and confident tone",
        "email": "I still haven't gotten access to the system.",
        "output": "I wanted to follow up on my access request for the system, which is still pending. Could you let me know when that will be resolved?",
    },

    # --- TONE: ASSERTIVE ---
    {
        "instruction": "Rewrite this email to sound more assertive",
        "email": "Can you maybe look at the bug when you have time?",
        "output": "Please look into this bug today. It needs to be resolved before we can move forward.",
    },
    {
        "instruction": "Rewrite this email to sound more assertive",
        "email": "I was wondering if it would be okay to get the files?",
        "output": "Please send me the files today. I need them to proceed with the project.",
    },
    {
        "instruction": "Rewrite this email to sound more assertive",
        "email": "Do you think we could maybe discuss the timeline at some point?",
        "output": "I need to discuss the timeline with you. Please schedule a call before end of week.",
    },

    # --- TONE: FRIENDLY ---
    {
        "instruction": "Rewrite this email to sound friendlier",
        "email": "Send the presentation before the meeting.",
        "output": "Hey! Could you send over the presentation before the meeting? That would be super helpful — thanks!",
    },
    {
        "instruction": "Rewrite this email to sound friendlier",
        "email": "I need your input on this proposal.",
        "output": "Hey! I'd love to get your thoughts on this proposal when you have a moment — your input would really help!",
    },
    {
        "instruction": "Rewrite this email to sound friendlier",
        "email": "Why haven't you responded to my last two emails?",
        "output": "Hey! Just wanted to check in — I've sent a couple of emails and haven't heard back. Everything okay? Would love to connect when you get a chance!",
    },

    # --- TONE: APOLOGETIC ---
    {
        "instruction": "Rewrite this email to sound more apologetic",
        "email": "You made an error in the report.",
        "output": "I'm sorry to flag this, but I noticed there may be an error in the report. I apologize if I'm misreading it — would you be able to take a look?",
    },
    {
        "instruction": "Rewrite this email to sound more apologetic",
        "email": "I still haven't received the access I requested two weeks ago.",
        "output": "I'm so sorry to follow up on this again — I know you're busy! I just wanted to check if the access request went through. I apologize for the inconvenience.",
    },
    {
        "instruction": "Rewrite this email to sound more apologetic",
        "email": "The meeting notes were never sent out.",
        "output": "I'm sorry — I realized the meeting notes were never sent out, and I apologize for the delay. I'll make sure they go out right away.",
    },

    # --- TONE: PERSUASIVE ---
    {
        "instruction": "Rewrite this email to be more persuasive by explaining the impact",
        "email": "We need to fix this bug now.",
        "output": "Fixing this bug now would prevent it from affecting our upcoming release and save us significant debugging time later. I believe it is worth prioritizing this week.",
    },
    {
        "instruction": "Rewrite this email to be more persuasive by explaining the impact",
        "email": "Please review my code.",
        "output": "A code review on this PR would help catch any issues before they reach production. It would take about 20 minutes and could save hours of debugging later — would you be able to take a look this week?",
    },
    {
        "instruction": "Rewrite this email to be more persuasive by explaining the impact",
        "email": "We should update the documentation.",
        "output": "Updating the documentation now would save the team significant time answering repeated questions and help new members get up to speed faster. It is a small investment that pays off immediately.",
    },

    # --- TONE: PROFESSIONAL ---
    {
        "instruction": "Rewrite this email to sound more professional",
        "email": "Call me about the contract stuff.",
        "output": "Could we schedule a call to discuss the contract details? Please let me know your availability.",
    },
    {
        "instruction": "Rewrite this email to sound more professional",
        "email": "This design looks bad.",
        "output": "I have some concerns about the current design direction and would appreciate the opportunity to discuss potential improvements.",
    },
    {
        "instruction": "Rewrite this email to sound more professional",
        "email": "Hey just checking in on the thing lol, any updates?",
        "output": "I wanted to follow up on the status of this matter. Could you please provide an update at your earliest convenience?",
    },

    # --- EDITING: FIX GRAMMAR ---
    {
        "instruction": "Fix the grammar errors in this email",
        "email": "I have went to the client meeting and they was not happy with our proposal.",
        "output": "I went to the client meeting and they were not happy with our proposal.",
    },
    {
        "instruction": "Fix the grammar errors in this email",
        "email": "Between you and I, the team don't know what they doing.",
        "output": "Between you and me, the team doesn't know what they are doing.",
    },
    {
        "instruction": "Fix the grammar errors in this email",
        "email": "I have been trying to reached out to the vendor but they hasn't responded.",
        "output": "I have been trying to reach out to the vendor but they haven't responded.",
    },

    # --- EDITING: MAKE CLEARER ---
    {
        "instruction": "Rewrite this email to be clearer and easier to understand",
        "email": "I wanted to reach out at this point in time to touch base about the status of the thing we discussed last week regarding the timeline.",
        "output": "I wanted to check on the timeline we discussed last week. Could you give me a quick update?",
    },
    {
        "instruction": "Rewrite this email to be clearer and easier to understand",
        "email": "When John and Mike worked on it, he did most of the work.",
        "output": "When John and Mike worked on it, John did most of the work.",
    },
    {
        "instruction": "Rewrite this email to be clearer and easier to understand",
        "email": "Please review the attached files and the ones from last week. These will help with the audit.",
        "output": "Please review the attached files and the documents from last week. Both sets of documents will help with the audit.",
    },

    # --- EDITING: MAKE CONCISE ---
    {
        "instruction": "Make this email more concise without losing the key message",
        "email": "I hope this email finds you well. I wanted to reach out to you today because I was thinking about the project that we have been working on together and I wanted to get your thoughts on how things are going and whether there is anything I can do to help.",
        "output": "I wanted to check in on the project and see if there is anything I can help with.",
    },
    {
        "instruction": "Make this email more concise without losing the key message",
        "email": "As per my understanding of the situation, and having reviewed all of the available information that was provided to me, I believe that the conclusion that I have reached is that we need to postpone the meeting.",
        "output": "Based on my review, I believe we need to postpone the meeting.",
    },
    {
        "instruction": "Make this email more concise without losing the key message",
        "email": "I just wanted to quickly check in to see if you had a chance to look at the document I sent over to you yesterday regarding the proposed changes to the project plan.",
        "output": "Have you had a chance to review the document I sent yesterday about the proposed project plan changes?",
    },

    # --- COMBINED: POLITE BUT FIRM ---
    {
        "instruction": "Rewrite this email to be polite but firm",
        "email": "Stop changing the requirements at the last minute.",
        "output": "I'd appreciate it if requirement changes could be flagged earlier in the process. Last-minute changes are making it difficult for the team to deliver on time.",
    },
    {
        "instruction": "Rewrite this email to be polite but firm",
        "email": "You keep being late to meetings.",
        "output": "I wanted to raise a concern about meeting punctuality. It would be helpful if we could all aim to join on time, as late arrivals disrupt the flow of discussion.",
    },
    {
        "instruction": "Rewrite this email to be polite but firm",
        "email": "I need an answer on this today, not tomorrow.",
        "output": "I understand you are busy, but I do need a response on this by end of day today. Please let me know as soon as you can.",
    },

    # --- COMBINED: PROFESSIONAL AND CONCISE ---
    {
        "instruction": "Rewrite this email to be professional and concise",
        "email": "Hey so the thing with the vendor didn't work out the way we planned and we might need to find someone else to do it, just wanted to give you a heads up.",
        "output": "The vendor arrangement has not worked out as planned. We may need to find an alternative. I wanted to make you aware of this development.",
    },
    {
        "instruction": "Rewrite this email to be professional and concise",
        "email": "I just wanted to quickly check if you got my email from yesterday about the project deadline.",
        "output": "I wanted to confirm whether you received my email yesterday regarding the project deadline.",
    },
    {
        "instruction": "Rewrite this email to be professional and concise",
        "email": "I know you're busy but I need your help on a bunch of things like the report and the budget and also the client presentation.",
        "output": "I need your input on three items: the report, the budget, and the client presentation. Would you be available for a brief call this week?",
    },

    # --- COMBINED: FRIENDLY BUT DIRECT ---
    {
        "instruction": "Rewrite this email to be friendly but direct",
        "email": "I need the analysis done today, no excuses.",
        "output": "Hey! I really need the analysis done by end of day today — is that doable? Let me know if anything is blocking you!",
    },
    {
        "instruction": "Rewrite this email to be friendly but direct",
        "email": "Please do the review when you can.",
        "output": "Hey! The review is needed by end of this week to stay on schedule — could you prioritize it? Let me know if you need anything from me!",
    },

    # --- COMBINED: CONFIDENT AND CLEAR ---
    {
        "instruction": "Rewrite this email to be confident and clear",
        "email": "I think maybe the budget might be possibly off?",
        "output": "The budget figures appear to be incorrect and need to be reviewed before the next stakeholder meeting.",
    },
    {
        "instruction": "Rewrite this email to be confident and clear",
        "email": "I was sort of thinking that we could potentially consider maybe rescheduling?",
        "output": "I would like to reschedule this meeting. Please share your availability for next week.",
    },

    # --- STRUCTURAL: FOCUS ON KEY POINT ---
    {
        "instruction": "Rewrite this email to lead with the most important point",
        "email": "Hope you had a great weekend! The weather has been great lately. Anyway, the Q3 report has errors in section 2 that need to be fixed.",
        "output": "The Q3 report has errors in section 2 that need to be corrected. Please review and update it before submission.",
    },
    {
        "instruction": "Rewrite this email to lead with the most important point",
        "email": "I was going through some things and I also wanted to mention the budget is actually over by 15%.",
        "output": "The project budget is currently over by 15%. I wanted to flag this immediately so we can discuss next steps.",
    },

    # --- STRUCTURAL: SET CLEAR EXPECTATIONS ---
    {
        "instruction": "Rewrite this email to set clear expectations and next steps",
        "email": "Can you try to maybe get this done at some point?",
        "output": "Please complete this task by end of day Friday and send a confirmation once it is done.",
    },
    {
        "instruction": "Rewrite this email to set clear expectations and next steps",
        "email": "We need to do something about the onboarding process.",
        "output": "The onboarding process needs to be improved. Please prepare a proposal with suggested changes by next Thursday so we can review it as a team.",
    },

    # --- STRUCTURAL: AVOID BLAME ---
    {
        "instruction": "Rewrite this email to avoid blame and focus on the solution",
        "email": "You sent the wrong file to the client.",
        "output": "It looks like there may have been a mix-up with the file sent to the client. Could we resend the correct version as soon as possible?",
    },
    {
        "instruction": "Rewrite this email to avoid blame and focus on the solution",
        "email": "The project is behind and it's your fault.",
        "output": "The project is running behind schedule and I'd like to discuss what we can do to get back on track. Could we find time to talk through the blockers?",
    },

    # --- STRUCTURAL: OPEN A DIALOGUE ---
    {
        "instruction": "Rewrite this email to open a constructive dialogue",
        "email": "Your idea won't work.",
        "output": "I have some reservations about this approach and would like to explore some alternatives before we move forward. Could we set up time to discuss?",
    },
    {
        "instruction": "Rewrite this email to open a constructive dialogue",
        "email": "I don't agree with the timeline you set.",
        "output": "I have some concerns about the proposed timeline. Could we discuss it together to find an approach that works for everyone?",
    },
    {
        "instruction": "Rewrite this email to open a constructive dialogue",
        "email": "I don't want to work with that client anymore.",
        "output": "I have been finding the current client engagement challenging and would like to discuss how we might approach it differently going forward.",
    },
]

out_filename = "instruction_emails.jsonl"
with open(out_filename, "w") as f:
    for entry in data:
        record = {
            "instruction": f"Instruction: {entry['instruction']}\nEmail: {entry['email']}",
            "output": entry["output"],
        }
        f.write(json.dumps(record) + "\n")

print(f"Generated {len(data)} examples in {out_filename}")
