import linkedin

g = linkedin(consumer_key='86cb2r2cajpbnp', consumer_secret='8n9rTyfPv6nJDbmD')

for repo in g.get_user().get_skills():
    print(i.skill.name)