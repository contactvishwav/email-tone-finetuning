import json

# Each entry has one blunt email and four genuinely distinct rewrites.
# The tone word in the instruction is what the model learns to condition on.
data = [
    {
        "blunt": "You missed the deadline again. This is unacceptable.",
        "friendly":    "Hey! I noticed the deadline passed and we haven't received your submission yet. No worries — these things happen! Could you let me know when you think you'll be able to get it over to us? Happy to help if anything is blocking you.",
        "assertive":   "The deadline passed without your submission. I need this delivered by end of day today. Please confirm you can meet this revised deadline.",
        "apologetic":  "I'm sorry to bother you about this, but I noticed the deadline may have passed. I completely understand if you've been swamped — I apologize if my original timeline wasn't communicated clearly. Whenever you get a chance, could you share an update?",
        "persuasive":  "I wanted to flag that the deadline has passed on this deliverable. Meeting these timelines matters because it affects the whole team's planning — if we can get this wrapped up today, we stay on track for the next milestone and avoid a cascade of delays.",
    },
    {
        "blunt": "This code is garbage and broke the build.",
        "friendly":    "Hey! Just a heads-up — it looks like the recent commit may have introduced a build issue. These things happen to all of us! Could you take a quick look when you get a chance? Happy to help debug together if that would be useful.",
        "assertive":   "The recent commit broke the build and is blocking the entire team. Fix or revert it immediately — this is your top priority until resolved.",
        "apologetic":  "I'm so sorry to flag this urgently — I know this isn't what you want to hear. It looks like the build may be failing after the recent commit. I apologize if the testing requirements weren't clear on our end. Would you be able to look into it when you have a moment?",
        "persuasive":  "I wanted to bring to your attention that the recent commit appears to have broken the build. Fixing this quickly would unblock the entire team and protect our release timeline — I know you're busy, but this one has a wide impact and is worth prioritizing now.",
    },
    {
        "blunt": "You didn't show up to the meeting. Again.",
        "friendly":    "Hey, we missed you at today's meeting! No worries — these things happen. Would you be able to catch up on the notes? And if you know you'll need to miss future meetings, just give us a heads-up so we can plan around it. Thanks!",
        "assertive":   "You were absent from today's meeting without notice. This is a recurring pattern. Going forward, if you cannot attend you must notify the team at least one hour in advance. Your attendance is expected.",
        "apologetic":  "I'm sorry to mention this, but I noticed you weren't able to make it to today's meeting. I completely understand that schedules get complicated. I apologize if the meeting time doesn't work well for you — please let me know and we can try to find a better slot.",
        "persuasive":  "I wanted to reach out about today's missed meeting. Your input in these discussions is genuinely valuable — when you're not there, we end up revisiting topics later anyway. If we can count on your attendance going forward, it would make our meetings far more productive for everyone.",
    },
    {
        "blunt": "Why are you not responding to my emails? I've sent three already.",
        "friendly":    "Hi! I hope everything is going well on your end. I just wanted to follow up since I've sent a few emails and haven't heard back. I know you're probably swamped! Whenever you get a moment, I'd love to connect on this — no rush at all.",
        "assertive":   "I have sent three emails without a response. I require a reply within 24 hours. If email is not the best channel for you, let me know your preferred method of communication.",
        "apologetic":  "I'm sorry to keep reaching out — I know you're likely very busy and I don't want to be a bother. I've sent a few emails and just wanted to make sure they landed in the right place. I completely understand if now isn't a good time. Whenever you're free, I'd truly appreciate any response you can offer.",
        "persuasive":  "I wanted to follow up once more on my previous emails. I know everyone's inbox is overwhelming, but a quick reply would help me move forward on a project that affects our shared timeline. Even a brief acknowledgment would go a long way — I promise to keep my follow-up short.",
    },
    {
        "blunt": "Your report is full of errors. Did you even proofread it?",
        "friendly":    "Hi! I had a chance to review the report and noticed a few things that might need a second look. It's a good start! If you have a chance, could you take another pass at it? Happy to go through it together if that would help.",
        "assertive":   "The report contains significant errors and cannot be submitted as-is. Review and correct all figures, grammar, and formatting by Thursday. Do not send client-facing documents without proofreading them first.",
        "apologetic":  "I'm so sorry to bring this up, and I want to say upfront that I really appreciate all the work you put into this. I noticed a few potential errors in the report that I wanted to flag. I apologize if my initial guidance wasn't clear enough — would you be able to take another look when you have time?",
        "persuasive":  "I reviewed the report and noticed several errors that should be addressed before it goes out. Submitting an accurate, polished report reflects well on the entire team and builds client trust. A quick round of revisions now will save us from a much harder conversation later — it's worth the effort.",
    },
    {
        "blunt": "You still haven't finished the task I gave you two weeks ago.",
        "friendly":    "Hey! I just wanted to check in on the task we discussed a couple of weeks back. How's it coming along? If you've hit any roadblocks, I'm totally happy to help reprioritize or assist where I can — just let me know!",
        "assertive":   "The task assigned two weeks ago remains incomplete. I need a status update today and a firm completion date. If there are blockers, I expect to hear about them immediately — not after the fact.",
        "apologetic":  "I'm sorry to follow up on this again — I know you have a lot on your plate and I feel bad adding to it. The task from a couple of weeks ago is still open, and I'm sorry if I didn't check in sooner. Would you be able to share where things stand? I really appreciate everything you do.",
        "persuasive":  "I wanted to circle back on the task from two weeks ago. Completing this is an important piece of a larger project, and wrapping it up this week would allow the rest of the team to move forward without interruption. If there's anything I can do to help unblock you, I'm here.",
    },
    {
        "blunt": "Stop interrupting people during meetings.",
        "friendly":    "Hey! I just wanted to share a small piece of feedback — I've noticed that sometimes people don't get to finish their thoughts during our meetings. It might help to let everyone wrap up their points before jumping in. I think it would make our discussions even more productive!",
        "assertive":   "In our meetings, you are interrupting colleagues before they finish speaking. This needs to stop. Let people complete their thoughts before you respond.",
        "apologetic":  "I'm a bit hesitant to bring this up because I really value your enthusiasm and contributions in meetings. I noticed some team members may not always get to finish their points. I apologize if this feedback is unwelcome — please know it comes from a good place.",
        "persuasive":  "I wanted to share some feedback about meeting dynamics. When everyone gets to finish their thoughts before responses come in, it leads to better ideas and a more comfortable space for people to contribute. It's a small shift that tends to have a big positive impact on the whole team.",
    },
    {
        "blunt": "This presentation was embarrassing. You weren't prepared.",
        "friendly":    "Hey, thanks for putting yourself out there today! I have some thoughts that might help make the next one even stronger. It felt like a few more practice runs could really help with the flow. Want to grab some time to prep together before the next one?",
        "assertive":   "Today's presentation was not up to the required standard. You were visibly unprepared and it reflected poorly on the team. For all future client presentations, a mandatory dry run is required the day before. No exceptions.",
        "apologetic":  "Thank you so much for presenting today — I know presentations can be stressful. I wanted to share some gentle feedback, and I'm sorry if this feels critical. I think a bit more preparation time might help things flow more smoothly next time. I also apologize if I didn't give you enough lead time to get ready.",
        "persuasive":  "I wanted to follow up on today's presentation. The content is strong, and I think with a bit more preparation and rehearsal it could land really powerfully with clients. Investing an hour or two into dry runs before the next one would give us a much stronger impression — it's time well spent.",
    },
    {
        "blunt": "You ignored all the feedback I gave you.",
        "friendly":    "Hi! I was reviewing the latest version and noticed some of the earlier feedback might not have made it in. Totally possible things got mixed up! Could we take a quick look together and make sure all the comments are addressed? I think it'll make the final product even better.",
        "assertive":   "The feedback I provided was not incorporated into the revised version. Review my comments and address every point. Resubmit by Friday.",
        "apologetic":  "I'm sorry to flag this, and I want to be clear that I really appreciate your effort on this. I noticed some of my earlier feedback may not have made it into the revision. I apologize if my notes weren't clear or easy to follow — would you be willing to take another pass? I'm happy to clarify anything.",
        "persuasive":  "I noticed the revision didn't include the earlier feedback. Taking that feedback on board would really strengthen the final output and show stakeholders that we're responsive to input — which builds a lot of trust. It would be worth the extra pass to make sure everything is addressed.",
    },
    {
        "blunt": "This feature is broken in production. Why didn't you test it?",
        "friendly":    "Hey! Heads-up — it looks like the new feature is running into some issues in production. These things happen! Could you take a look and let us know what you're seeing on your end? Happy to help investigate together if that's useful.",
        "assertive":   "A feature released to production is broken and impacting users. This requires immediate attention. Going forward, all releases must pass full QA before deployment. This is a non-negotiable process.",
        "apologetic":  "I'm so sorry to flag this urgently — I know this isn't what you want to hear after all your hard work on this. It looks like there may be an issue in production. I apologize if the testing requirements weren't communicated clearly on our end. Would you be able to look into it when you get a chance?",
        "persuasive":  "I wanted to flag that the recent feature release appears to have issues in production. Addressing this quickly will protect the user experience and prevent a rise in support tickets. A fast fix now will significantly limit the impact — I think it's worth making this the immediate priority.",
    },
    {
        "blunt": "You went over budget and didn't tell anyone.",
        "friendly":    "Hi! I was reviewing the project budget and noticed we may have gone a bit over the allocated amount. No worries — let's sort it out together! Could you share some context on what drove the overage? That will help us plan better going forward.",
        "assertive":   "The project has exceeded budget and I was not notified. Going forward, you are required to flag any budget variance of 10% or more immediately. Schedule a call today to walk me through what happened.",
        "apologetic":  "I'm sorry to bring this up — I know budgets can be stressful to track. I noticed the project may have gone over the original estimate. I apologize if I didn't check in enough during the project to help manage this. Would you be able to share an overview of where things stand financially?",
        "persuasive":  "I wanted to discuss the project budget. Being transparent about variances early helps us adjust before they become larger problems and protects everyone on the team. Going forward, early communication here makes a significant difference in how we manage costs across the portfolio.",
    },
    {
        "blunt": "You sent the wrong file to the client. This is a huge mistake.",
        "friendly":    "Hey! I think there might have been a mix-up with the file that went to the client — it looks like the wrong version was attached. These things happen! Could you reach out to them to clarify and resend the correct one? Let me know if you need any help sorting it out.",
        "assertive":   "The wrong file was sent to the client. Contact them immediately, apologize, and send the correct version. In the future, double-check all attachments before sending any client communication. This cannot happen again.",
        "apologetic":  "I'm so sorry to flag this — I know mistakes like this are stressful and I don't want to add to that. It looks like the wrong file may have gone to the client. I apologize if there was any confusion about which version to send. Would you be able to follow up with them? I'm happy to help draft the message.",
        "persuasive":  "I wanted to flag a file mix-up in the recent client email. Getting the correct version to them quickly is important — clients notice responsiveness, and handling this promptly actually turns a mistake into a trust-building moment. A fast, professional follow-up from you would go a long way here.",
    },
    {
        "blunt": "You didn't update the documentation. Now everyone is confused.",
        "friendly":    "Hey! It looks like the documentation might be a bit behind the latest changes. No big deal — could you take some time to bring it up to date? It'll save a lot of back-and-forth for the team and make everyone's lives easier. Thanks so much!",
        "assertive":   "The documentation has not been updated to reflect recent changes and is causing confusion across the team. Update all relevant documentation by end of week. Documentation is part of every deliverable — not optional.",
        "apologetic":  "I'm sorry to mention this — I know documentation can be easy to overlook when you're in the middle of shipping. I noticed the docs may not reflect the latest changes, and the team has been a bit confused as a result. I apologize for not flagging this sooner. Would you be able to find time to update it this week?",
        "persuasive":  "I wanted to flag that the documentation hasn't been updated after the recent changes, and it's causing confusion for teammates trying to use it. Keeping docs current is one of those investments that saves a lot of time downstream — ten minutes of updating now prevents hours of confusion for others.",
    },
    {
        "blunt": "Stop making last-minute changes to the scope.",
        "friendly":    "Hey! I've noticed we've been getting some scope changes pretty close to deadlines recently. I totally understand things evolve — could we try to get those changes flagged a bit earlier next time? It would really help the team plan and deliver the best work possible!",
        "assertive":   "Last-minute scope changes are disrupting delivery timelines. Effective immediately, all scope changes must be submitted at least five business days before a deadline and require written sign-off. This is now a formal process.",
        "apologetic":  "I wanted to gently raise something I hope doesn't come across as critical — I've noticed some scope changes have been coming in close to deadlines, and it's been a bit challenging for the team to absorb them. I'm sorry if I haven't communicated capacity constraints clearly enough. Would it be possible to try surfacing changes a bit earlier going forward?",
        "persuasive":  "I wanted to discuss the pattern of late-breaking scope changes. Getting those changes in earlier gives the team time to do their best work rather than rushing. Earlier visibility leads to better quality delivery and better outcomes for stakeholders — it's a process improvement worth making.",
    },
    {
        "blunt": "Your standup updates are useless. Nobody knows what you're working on.",
        "friendly":    "Hey! I wanted to share some friendly feedback about standup updates. It would be really helpful for the team to know what you're working on each day and if anything is blocking you. Even just two or three sentences makes a big difference! Happy to chat about a good format if that helps.",
        "assertive":   "Your standup updates lack the detail needed for the team to track progress and blockers. Going forward, each update must include: what you completed yesterday, what you are working on today, and any blockers. This format is mandatory.",
        "apologetic":  "I'm a little hesitant to bring this up because I know standups can feel like a lot, and I appreciate you participating. I just wanted to share that some of us have been having trouble following what you're working on. I'm sorry if the expectations weren't clear — could we find a format that works better for you?",
        "persuasive":  "I wanted to share some feedback about our standup updates. When everyone has clear visibility into what others are working on, it makes it much easier to offer help, avoid duplicate work, and keep the project moving. A slightly more detailed update each day has a real multiplying effect on the team's coordination.",
    },
    {
        "blunt": "You keep missing sprint planning.",
        "friendly":    "Hey! I noticed you haven't been able to make sprint planning recently. We miss having your input! If the timing doesn't work for you, let me know and we can see if there's a way to adjust. Your perspective really helps us prioritize well.",
        "assertive":   "You have missed sprint planning multiple times this quarter. This is a required meeting. Your attendance is non-negotiable going forward. If you have a conflict, notify the team lead 24 hours in advance.",
        "apologetic":  "I'm sorry to bring this up — I know you're juggling a lot. I noticed you haven't been able to attend sprint planning recently. I apologize if the scheduling has been difficult. Would it be possible to make it to the next one? Your input really does make a difference.",
        "persuasive":  "I wanted to flag that sprint planning works significantly better when the whole team is involved. Your perspective on technical complexity is valuable when we're estimating and prioritizing. Having you at the next sprint planning would help us commit to a more realistic and achievable sprint for everyone.",
    },
    {
        "blunt": "This is the third time you've been late with your timesheet.",
        "friendly":    "Hey! Just a quick reminder about timesheets — it looks like the last few may have come in a bit late. No big deal at all! If the deadline is hard to hit or the process is unclear, let me know and I'll help sort it out. Thanks so much!",
        "assertive":   "This is the third consecutive timesheet submitted late. Timesheets are due every Friday by 5 PM — this deadline is firm. Late submissions delay payroll for the entire team and will not be tolerated.",
        "apologetic":  "I'm sorry to keep following up about timesheets — I know it can feel like a lot of admin. I noticed the last few have come in past the deadline. I apologize if the deadline or process wasn't communicated well. Would you be able to try to get it in on time going forward? I really appreciate your help with this.",
        "persuasive":  "I wanted to touch base about timesheet submissions. On-time submissions make a real difference — they allow payroll to run smoothly and prevent extra work for the finance team. Getting it in by Friday each week is a small effort that has a meaningful impact on others.",
    },
    {
        "blunt": "You promised this would be done by today. It's not.",
        "friendly":    "Hey! I was expecting to have the deliverable today and it looks like it might still be in progress. Totally understand if something came up! Could you give me a quick update on timing? Just want to make sure I'm planning around the right date.",
        "assertive":   "You committed to delivering this today and it has not been delivered. I need a revised deadline from you today — and I expect that one to be kept. Going forward, do not commit to dates you cannot meet.",
        "apologetic":  "I'm sorry to follow up on this — I know you've been working hard and I don't want to add pressure. I was expecting the deliverable today and noticed it may not be quite ready yet. I apologize if my timeline created unnecessary stress. Whenever it's ready, please send it over — I really appreciate your effort.",
        "persuasive":  "I wanted to follow up on the deliverable that was due today. Commitments to timelines help the whole team plan effectively — and if the date needs to change, communicating that early gives everyone a chance to adjust. A quick update on the revised timing would help me keep things on track on my end.",
    },
    {
        "blunt": "Your feedback was way too harsh and it upset the team.",
        "friendly":    "Hey! I just wanted to share something I noticed — it seems like some of the recent feedback may have landed a bit harder than intended, and a few team members seemed down after. I know you have high standards and that's a great thing! Maybe we could chat about framing it in a way that still gets the message across but feels more supportive?",
        "assertive":   "Feedback delivered in the recent session was unnecessarily harsh and negatively affected team morale. Constructive feedback must be specific, solution-oriented, and respectful in tone. This is a professional expectation, not a suggestion.",
        "apologetic":  "I'm a bit nervous to raise this, and I want to say upfront that I know your intentions are good and your standards are high. Some team members felt the recent feedback was quite difficult to receive. I'm sorry if raising this creates any friction — I just wanted you to have that context in case it's helpful.",
        "persuasive":  "I wanted to share some context about the team's reaction to recent feedback. Feedback lands best when it feels like it's coming from a place of support — people are more receptive and more likely to act on it. A small shift toward acknowledging what's working alongside the critique tends to lead to much better outcomes.",
    },
    {
        "blunt": "Why is this taking so long? This should have been done days ago.",
        "friendly":    "Hey! I wanted to check in on this one — it's been a few days and I haven't seen it come through yet. I know things get busy! Is there anything holding it up? Happy to help clear any blockers if that would move things along.",
        "assertive":   "This task is overdue. I need a status update and a firm completion date by end of day. If you are blocked, you are required to escalate immediately — not silently.",
        "apologetic":  "I'm sorry to keep following up on this — I know you have a lot on your plate and I don't want to add stress. I noticed this task has been taking a bit longer than expected. I apologize if my original deadline wasn't realistic. Whenever it's ready, please send it over — I appreciate your patience with me as well.",
        "persuasive":  "I wanted to check in on this task. I know complex work takes time and I don't want to rush quality. That said, other team members are waiting on this, and even a partial update or an expected completion date would help us plan around it and reduce the downstream bottleneck.",
    },
]

tones = ["friendly", "assertive", "apologetic", "persuasive"]

out_filename = "tone_emails.jsonl"
count = 0
with open(out_filename, "w") as f:
    for entry in data:
        for tone in tones:
            record = {
                "instruction": f"Rewrite in a {tone} tone: {entry['blunt']}",
                "output": entry[tone],
            }
            f.write(json.dumps(record) + "\n")
            count += 1

print(f"Generated {count} examples ({len(data)} emails x {len(tones)} tones) in {out_filename}")
