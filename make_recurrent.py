
with open ("input.ics", "r") as myfile:
    input_data = myfile.read().splitlines()

output = ""

for line in input_data:
    output += (line + "\n")
    if line[:11] == "DTEND;VALUE":
        output += ("RRULE:FREQ=YEARLY\n")

with open('output.ics', "w") as myfile:
    myfile.write(output)