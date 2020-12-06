# Secret Santa Selection System

Looking for something that will choose your gift exchange's Secret Santas and contact them for you? Ho ho ho, you've found it!


## Getting Started

To get the sleigh moving...

1. You'll need Python 3.6+ installed on your computer, Internet access (for sending emails), and should feel comfortable running scripts from a command prompt.

2. Copy `SecretSanta_CONFIG.txt.example` to `SecretSanta_CONFIG.txt` and update it with your own settings.

3. Copy `SecretSanta_FAMILY.txt.example` to `SecretSanta_FAMILY.txt` and provide your family's/office's details.

4. Run `python SecretSantaSelectionSystem_Pick.py` to select Secret Santas. Who it picked will be kept under wraps... unless you peek at the `SecretSanta20XX_From*.txt` files it generates.

5. Run `python SecretSantaSelectionSystem_Send.py SecretSanta20XX_FromALL.txt go` (replacing *XX* with the current year) and follow the prompts to send out emails! If there are any issues along the way, check and correct your `SecretSanta_CONFIG.txt` and `SecretSanta_FAMILY.txt` files accordingly.

A few things to note:
* This is all command-line; there is no graphical interface.
* Names are picked at random but someone won't end up "drawing their own name" (or anyone else you've set up as "ineligible" for them).
* The send script is written to communicate with an email server that supports STARTTLS (typically port 587).


## ~~Too Many~~ More Details

Want to know a bit more? Keep reading!

### Prologue (Overview)

The selection system consists of two command-line tools written in Python: one that randomly picks names from the list of participants you provide and one that sends out emails to notify everyone.

Why two tools instead of one? Splitting the process allows the picking of names to be done once and for emails to be sent at a later time, for an email to be re-sent if needed, etc.

### SecretSanta_FAMILY.txt

Add each person participating in the gift exchange to this file, one person per row. Be sure to use a regular/plain text editor like Notepad, not a word processor like Word.

Each person row has four parts separated by commas:

```
key name,common name,email address,ineligible list (of key names)
```

*key name* uniquely identifies each person. You can just use first names here unless you need to differentiate two (or more) people that have the same name. In that case add a last initial, name, etc. This key name is also used in emails to identify the gift recipient so keep that in mind when deciding on a key name! Also, it's recommended that you only use letters, digits, and spaces in the key name.

*common name* can specify an alternate name for the "to" and greeting in emails. This is just a friendlier way of addressing someone if you couldn't just use their first name as the key name. For instance, if there's a Jennifer A and a Jennifer B, you can just specify Jennifer here so their emails say "Hi Jennifer!" instead of "Hi Jennifer A!" If this is left blank then key name will be used for common name.

*email address* is, well, the address a "You are the Secret Santa for..." email will be sent to.

*ineligible list (of key names)* is a "do not select" list of key names that should *not* be picked for this person. This prevents someone from getting a significant other, for example. If there are multiple people who are "ineligible", separate them with vertical bars: `Person A|Person B|Person C`. Remember to use key names here, not common names! If there's no one to add here be sure the row ends with a comma!

Do not add a header row to this file, just people rows.

#### Example

Let's say the contents of `SecretSanta_FAMILY.txt` are as follows:

```
John,,john@example.com,Jane A
Jane A,Jane,jane_a@example.com,John
Jane B,Jane,jane_b@example.com,Joe
Joe,,joe@example.com,Jane B
Jeff,,jeff@example.com,
```

When picking a name for John, Jane A will not be selected (nor will John since the system is aware that someone should not be buying for themselves). Notice that Jeff's row ends with a comma since he doesn't have anyone one his "ineligible" list.

#### Sample Email

John has volunteered to send out emails. Let's say Jane A is the Secret Santa for Jane B. Her notification email would look something like this:

> From: John \<john@example.com\>\
> To: Jane \<jane_a@example.com\>\
> Subject: Jane, Your 202X Family Secret Santa Info
> 
> Hi Jane!
> 
> This year you are the Secret Santa for...
> 
> ***  Jane B  ***
> 
> Merry Christmas!

Even though she's in the file as "Jane A", she's addressed in the email with the specified common name of "Jane". To more clearly identify the gift recipient, key name is always used, "Jane B" in this case.

The message body template can be modified in `SecretSantaSelectionSystem_Send.py` as desired.

#### Troubleshooting

If you get a `not enough values to unpack (expected 4, got 3)` error you may be missing a comma at the end of the row for someone who doesn't have any "ineligible" key names. Similarly, check your commas if the `too many values to unpack (expected 4)` error occurs.

#### Resending an email for one person.

The name picker will create a file with all picks, `SecretSanta20XX_FromALL.txt` (where XX is the current year), as well as one per person where `ALL` is replaced with their key name minus any spaces. Step 5 in the Getting Started section above describes how to send out all emails at once. However, you can swap out the `ALL` file with one of the individual files to only send to that person. If you need to send to a different email address, just update it in `SecretSanta_FAMILY.txt` and re-send to that person!

### SecretSanta_CONFIG.txt

The settings in this file are fairly straightforward. However, it's worth reiterating that the email sender is coded to talk to an SMTP server that supports the STARTTLS protocol (commonly port 587). You will need to modify the code to support an email server that requires a non-STARTTLS protocol.

To streamline the sending process, especially if you are planning to send multiple separate emails, you can provide your email password in this file. Leaving it blank will cause the send tool to prompt you at runtime.

### Quick Developer Note

I'm in the process of learning Python so the code here may not be the best or most Pythonic way to accomplish something.

### Epilogue

This code is provided "as is" and for entertainment purposes only. There is no support and no warranties or guarantees, express or implied, to its operation, outcomes, consequences, eggnog consumption, or anything else.

Thanks for stopping by -- I hope you find the *Secret Santa Selection System* useful.

**Enjoy and Merry Christmas!**
