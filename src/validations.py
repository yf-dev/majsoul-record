def validate(data):
    errors = []

    if "error" in data:
        errors.append(
            {"code": "cannot-get-log", "message": "Cannot get game log data."}
        )
        return False, errors

    head = data["head"]

    accounts = head["accounts"]

    if len(accounts) != 4:
        errors.append(
            {
                "code": "invalid-player-count",
                "message": f"Invalid player count: {len(accounts)}. It should be 4.",
                "data": len(accounts),
            }
        )

    if "roomId" not in head["config"]["meta"]:
        errors.append({"code": "missing-room-id", "message": "roomId is missing."})

    if head["config"]["category"] != 1:
        errors.append(
            {
                "code": "invalid-category",
                "message": f'Invalid category: {head["config"]["category"]}. It should be Friendly Match(1)',
                "data": head["config"]["category"],
            }
        )

    if head["config"]["mode"]["mode"] != 2:
        errors.append(
            {
                "code": "invalid-mode",
                "message": f'Invalid mode: {head["config"]["mode"]["mode"]}. It should be 4-Player Two-Wind Match Mode(2).',
                "data": head["config"]["mode"]["mode"],
            }
        )

    rule = head["config"]["mode"]["detailRule"]

    if "bianjietishi" in rule and rule["bianjietishi"] != True:
        errors.append(
            {
                "code": "invalid-tips",
                "message": f'Invalid tips: {rule["bianjietishi"]}. It should be True.',
                "data": rule["bianjietishi"],
            }
        )

    if "doraCount" in rule and rule["doraCount"] != 3:
        errors.append(
            {
                "code": "invalid-red-dora",
                "message": f'Invalid red dora: {rule["doraCount"]}. It should be 3.',
                "data": rule["doraCount"],
            }
        )

    if "fandian" in rule and rule["fandian"] != 30000:
        errors.append(
            {
                "code": "invalid-min-points-to-win",
                "message": f'Invalid min points to win: {rule["fandian"]}. It should be 30000.',
                "data": rule["fandian"],
            }
        )

    if "fanfu" in rule and rule["fanfu"] != 1:
        errors.append(
            {
                "code": "invalid-min-han",
                "message": f'Invalid min han: {rule["fanfu"]}. It should be 1.',
                "data": rule["fanfu"],
            }
        )

    if "initPoint" in rule and rule["initPoint"] != 25000:
        errors.append(
            {
                "code": "invalid-starting-points",
                "message": f'Invalid starting points: {rule["initPoint"]}. It should be 25000.',
                "data": rule["initPoint"],
            }
        )

    if "shiduan" in rule and rule["shiduan"] != 1:
        errors.append(
            {
                "code": "invalid-open-tanyao",
                "message": f'Invalid open tanyao: {rule["shiduan"]}. It should be 1.',
                "data": rule["shiduan"],
            }
        )

    if "guyiMode" in rule and rule["guyiMode"] != 1:
        errors.append(
            {
                "code": "invalid-local-yaku",
                "message": f'Invalid local yaku: {rule["guyiMode"]}. It should be 0.',
                "data": rule["guyiMode"],
            }
        )

    if "openHand" in rule and rule["openHand"] != 0:
        errors.append(
            {
                "code": "invalid-open-hand",
                "message": f'Invalid open hand: {rule["openHand"]}. It should be 0.',
                "data": rule["openHand"],
            }
        )

    if "timeAdd" in rule and rule["timeAdd"] != 20:
        errors.append(
            {
                "code": "invalid-thinking-time-add",
                "message": f'Invalid thinking time(add): {rule["timeAdd"]}. It should be 20.',
                "data": rule["timeAdd"],
            }
        )

    if "timeFixed" in rule and rule["timeFixed"] != 5:
        errors.append(
            {
                "code": "invalid-thinking-time-fixed",
                "message": f'Invalid thinking time(fixed): {rule["timeFixed"]}. It should be 5.',
                "data": rule["timeFixed"],
            }
        )

    return not bool(errors), errors
