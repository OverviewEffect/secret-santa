import os, random, secrets, re, csv, datetime

print("*** Secret Santa Selection System: Pick ***")
print()

year = datetime.datetime.now().year

# --------------------------------------------------------------------------------

class Picker:
    def __init__(self, family):
        self.redo = False
        self.recipients = family[:]
        self.santas = family[:]
        self.pairs = []

    def _pick(self):
        santa = self.santas[0]
        santaName = santa["name"]
        eligibleRecipients = [r for r in self.recipients if r["name"] != santaName and r["name"] not in santa["nope"]]
        if len(eligibleRecipients) == 0:
            #print(f"** STALEMATE; SIGNALING REDO (santa: {santaName}, remaining: {', '.join([r['name'] for r in self.recipients])}) **")
            self.redo = True
            return
        recipient = secrets.choice(eligibleRecipients)
        recipientName = recipient["name"]
        self.santas.remove(santa)
        self.recipients.remove(recipient)
        self.pairs.append((santaName, recipientName))

    def go(self):
        # just use random (instead of secrets) for a quick shuffle
        random.shuffle(self.santas)
        while not self.redo and (len(self.santas) > 0 or len(self.recipients) > 0):
            self._pick()
        return not self.redo

# --------------------------------------------------------------------------------

def get_santa_filename(name):
    return f"SecretSanta{year}_From{name.replace(' ', '')}.txt"

def check_for_existing_all_file():
    from_all_filename = get_santa_filename("ALL")
    if os.path.exists(from_all_filename):
        print(f"! {from_all_filename} already exists - halting to prevent overwrite!")
        exit()
    return from_all_filename

def get_family_info(family_filename):
    family = []
    print("Participating:")
    with open(family_filename, "r") as family_file:
        reader = csv.reader(family_file)
        unique_names = set()
        for key_name, _, _, nopes in reader:
            key_name = key_name.strip()
            if key_name == "":
                print(" ! empty (key) name found in list")
                exit()
            elif key_name.lower() in unique_names:
                print(f" ! duplicate (key) name found in list: {key_name}")
                exit()
            unique_names.add(key_name.lower())
            nope_list = [nope.strip() for nope in nopes.split("|")] if nopes.strip() != "" else []
            family.append({"name": key_name, "nope": nope_list})
            print(f" * {key_name} (nope: {(', '.join(nope_list) if len(nope_list) > 0 else '<none>')})")
            if os.path.exists(get_santa_filename(key_name)):
                print(f" ! {get_santa_filename(key_name)} already exists - halting to prevent overwrite!")
                exit()
    print()
    return family

def participation_validator(family):
    memberNames = [member["name"] for member in family]
    errors = []
    for member in family:
        unknowns = list(set(member["nope"]) - set(memberNames))
        [errors.append(f"Unknown Nope: '{u}' on {member['name']}") for u in unknowns]
    if len(errors) > 0:
        [print(f"!! ERROR: {error}") for error in errors]
        exit()

def run(family_filename):
    from_all_filename = check_for_existing_all_file()
    family = get_family_info(family_filename)
    participation_validator(family)
    tries = 0
    redosLeft = 500
    successful = False
    while redosLeft > 0:
        tries += 1
        p = Picker(family)
        if p.go():
            with open(from_all_filename, "w") as big_file:
                for pair in p.pairs:
                    santa_name = pair[0]
                    recv_name = pair[1]
                    out_line = f"{santa_name},buying for,{recv_name}"
                    big_file.write(f"{out_line}\n")
                    with open(get_santa_filename(santa_name), "w") as santa_file:
                        santa_file.write(f"{out_line}\n")
            successful = True
            break
        else:
            redosLeft -= 1
    if successful:
        print(f"Names picked, done (in {tries} tr{('ies' if tries != 1 else 'y')}).")
    else:
        print("!! TOO MANY REDOS, POSSIBLE IMPOSSIBLE COMBINATION? HALTING.")

# --------------------------------------------------------------------------------

run("SecretSanta_FAMILY.txt")
