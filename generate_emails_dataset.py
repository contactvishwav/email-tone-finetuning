import json

data = [
    ("Send me the report today. You missed it yesterday.", "Could you please share the report today? I noticed it was delayed yesterday."),
    ("I hate this design. Do it again.", "I believe we can improve this design. Could we explore some alternatives?"),
    ("Fix this bug immediately.", "Could you please prioritize fixing this bug as soon as possible?"),
    ("I'm not doing this task. It's stupid.", "I have some concerns about this task. Can we discuss its purpose?"),
    ("Give me the slides by noon.", "Please send over the slides by noon if possible."),
    ("Your code is garbage and broke the build.", "It seems the recent code commit broke the build. Can we review it together?"),
    ("Stop emailing me about this.", "I would appreciate it if we could pause the email updates on this topic."),
    ("The client is super annoying.", "The client has been quite demanding recently."),
    ("Why did you do it this way? It makes no sense.", "Could you help me understand the reasoning behind this approach?"),
    ("Tell John he is wrong about the budget.", "Please let John know that there might be an oversight regarding the budget figures."),
    ("This meeting was a waste of time.", "I think we could structure our meetings more efficiently in the future."),
    ("You completely ignored my email.", "Did you get a chance to review my previous email?"),
    ("I don't care what they say, we are doing it my way.", "Let's consider their feedback, but I still recommend we proceed with the current plan."),
    ("You're late again.", "I noticed you've been arriving late recently. Is everything okay?"),
    ("This is the worst idea I've ever heard.", "I have some reservations about this idea. Let's explore other options."),
    ("Fix the spelling mistake right now.", "Could you please correct the spelling typo when you have a moment?"),
    ("I am too busy for this nonsense.", "My schedule is currently full, so I won't be able to take this on."),
    ("You clearly didn't read my instructions.", "It seems there might have been a misunderstanding regarding my instructions."),
    ("Do not interrupt me when I am speaking.", "I would appreciate it if you could let me finish my thought."),
    ("You messed up the presentation.", "There are a few areas in the presentation that we need to improve."),
    ("This code is a disaster.", "This code could benefit from some refactoring."),
    ("I expect this done by tomorrow, no excuses.", "Please aim to have this completed by tomorrow."),
    ("Your performance has been terrible.", "We need to discuss some areas for improvement in your recent performance."),
    ("I'm done dealing with this client.", "I feel it might be best if someone else handles this client moving forward."),
    ("Why is this taking so long?", "Could you provide an update on the timeline for this?"),
    ("You need to learn how to communicate.", "I think active communication would greatly benefit our teamwork."),
    ("Don't ask me for help again.", "I'm currently stretched thin and may not be available for further assistance."),
    ("I refuse to work with him.", "I find it challenging to collaborate with him and would prefer to work independently."),
    ("Your report is full of lies.", "I noticed some inaccuracies in the report that we need to address."),
    ("This project is a complete joke.", "I have serious concerns about the viability of this project."),
    ("You need to stop being so lazy.", "I would appreciate it if we could see more consistent effort on these tasks."),
    ("I don't want to hear your excuses.", "Let's focus on finding a solution rather than focusing on the delays."),
    ("I told you so.", "This aligns with the concerns I raised earlier."),
    ("You're not paid to think.", "Please focus on executing the established process for now."),
    ("This is not my problem.", "This matter falls outside my current responsibilities."),
    ("You are wrong.", "My understanding of the situation is slightly different."),
    ("I'm muting this chat.", "I will be adjusting my notifications for this chat to minimize distractions."),
    ("Do whatever you want, I don't care.", "I defer to your judgment on this matter."),
    ("You clearly have no idea what you're doing.", "It seems you might need some additional support with this task."),
    ("This is a hard no.", "Unfortunately, I cannot approve this request."),
    ("I'm logging off early because this is useless.", "I'm concluding my day now as I've reached a roadblock here."),
    ("Learn how to use Git properly.", "Could we review some best practices for version control?"),
    ("This is above your pay grade.", "This decision requires input from management."),
    ("I already answered this. Read the thread.", "As mentioned earlier in the thread...")
]

out_filename = "emails.jsonl"
with open(out_filename, "w") as f:
    for blunt, prof in data:
        record = {
            "instruction": f"Rewrite professionally: {blunt}",
            "output": prof
        }
        f.write(json.dumps(record) + "\n")

print(f"Generated {len(data)} examples in {out_filename}")
