#     category_field = "cat"
#     json_path = "members.json"

#     with open(json_path) as members_file:
#         members = json.load(members_file)

#     pair = secret_santa(members)

#     emoji = "🔔🎉🎅🎁🎄🧦🌟"
#     for m in pair:
#         print(f"{random.choice(emoji)} {m[0]['name'].capitalize()} est le secret santa de {m[1]['name'].capitalize()}.")
