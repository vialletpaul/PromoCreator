import json


def export_chan(ctx):
    category = []
    c = None
    for chan in ctx.guild.categories:
        print(chan.name)
        if not chan.category:
            if c:
                category.append(c)
            tmp = __export_chan_permissions(chan)
            c = dict(name=chan.name, permissions=tmp, channels=[])
            for tmp in chan.channels:
                t = "Text Channel"
                if hasattr(tmp, "bitrate"):
                    t = "Voice Channel"
                c["channels"].append(dict(name=tmp.name, type=t, permissions=__export_chan_permissions(tmp)))

    category.append(c)

    print(json.dumps(category, ensure_ascii=False))
    return category


def __export_chan_permissions(chan):
    permissions = []
    for role in chan.overwrites:
        role = role[0]
        tmp = dict(role=role.name, permissions={})
        if not hasattr(role, "permissions"):
            continue
        for permission, value in role.permissions:
            tmp["permissions"][permission] = value
        permissions.append(tmp)

    return permissions


def export_roles(ctx):
    roles = dict(roles=[])
    for role in ctx.guild.role_hierarchy:
        roles["roles"].append(dict(name=role.name, color=str(role.colour), mentionable=str(role.mentionable),
                                   hoist=str(role.hoist), permissions=str(role.permissions.value)))
    print(json.dumps(roles, ensure_ascii=False))
    return roles
