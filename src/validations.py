import typing as t

ValidationError = t.NewType("ValidationError", t.Dict[str, t.Any])


def make_validation_error(
    code: str, message: str, data: t.Any = None
) -> ValidationError:
    """Make error object for validation

    Args:
        code (str): error code
        message (str): error message
        data (Any): invalid data

    Returns:
        ValidationError: new error object
    """
    return ValidationError(
        {
            "code": code,
            "message": message,
            "data": data,
        }
    )


def make_invalid_value_error(
    code: str,
    name: str,
    value: t.Any,
    expected_value: t.Any,
    expected_value_hint: str = None,
) -> ValidationError:
    """Make error object for invalid value

    Args:
        code (str): error code
        name (str): name of value
        value (Any): invalid value itself
        expected_value (Any): expected value
        expected_value_hint (str, optional): hint of expected value

    Returns:
        ValidationError: new error object
    """
    if expected_value_hint:
        expected_value_str = f"{expected_value_hint}({str(expected_value)})"
    else:
        expected_value_str = str(expected_value)
    return make_validation_error(
        code=code,
        message=f"Invalid {name}: {str(value)}. It should be {expected_value_str}.",
        data=value,
    )


def validate_value(
    errors: t.List[ValidationError],
    code: str,
    name: str,
    value: t.Any,
    expected_value: t.Any,
    expected_value_hint: str = None,
) -> None:
    """Validate value

    If value is invalid, error object will be added to errors.

    Args:
        errors (List[ValidationError]): list to add new error object
        code (str): error code for error object
        name (str): name of value
        value (Any): value to validate
        expected_value (Any): expected value to validate
        expected_value_hint (str, optional): hint of expected value
    """
    if value != expected_value:
        errors.append(
            make_invalid_value_error(
                code=code,
                name=name,
                value=value,
                expected_value=expected_value,
                expected_value_hint=expected_value_hint,
            )
        )


def validate_log(data: t.Dict) -> t.Tuple[bool, t.List[ValidationError]]:
    """Validate log data

    Args:
        data (Dict): [description]

    Returns:
        List[ValidationError]: [description]
    """
    errors = []

    if "error" in data:
        errors.append(
            make_validation_error(
                code="cannot-get-log", message="Cannot get game log data."
            )
        )
        return False, errors

    head = data["head"]

    accounts = head["accounts"]

    validate_value(
        errors=errors,
        code="invalid-player-count",
        name="player count",
        value=len(accounts),
        expected_value=4,
    )

    if "roomId" not in head["config"]["meta"]:
        errors.append(
            make_validation_error(code="missing-room-id", message="roomId is missing.")
        )
        return False, errors

    validate_value(
        errors=errors,
        code="invalid-category",
        name="category",
        value=head["config"]["category"],
        expected_value=1,
        expected_value_hint="Friendly Match",
    )

    validate_value(
        errors=errors,
        code="invalid-mode",
        name="mode",
        value=head["config"]["mode"]["mode"],
        expected_value=2,
        expected_value_hint="4-Player Two-Wind Match Mode",
    )

    rule = head["config"]["mode"]["detailRule"]

    if "bianjietishi" in rule:
        validate_value(
            errors=errors,
            code="invalid-tips",
            name="tips",
            value=rule["bianjietishi"],
            expected_value=True,
        )

    if "doraCount" in rule:
        validate_value(
            errors=errors,
            code="invalid-red-dora",
            name="red dora",
            value=rule["doraCount"],
            expected_value=3,
        )

    if "fandian" in rule:
        validate_value(
            errors=errors,
            code="invalid-min-points-to-win",
            name="min points to win",
            value=rule["fandian"],
            expected_value=30000,
        )

    if "fanfu" in rule:
        validate_value(
            errors=errors,
            code="invalid-min-han",
            name="min han",
            value=rule["fanfu"],
            expected_value=1,
        )

    if "initPoint" in rule:
        validate_value(
            errors=errors,
            code="invalid-starting-points",
            name="starting points",
            value=rule["initPoint"],
            expected_value=25000,
        )

    if "shiduan" in rule:
        validate_value(
            errors=errors,
            code="invalid-open-tanyao",
            name="open tanyao",
            value=rule["shiduan"],
            expected_value=1,
        )

    if "guyiMode" in rule:
        validate_value(
            errors=errors,
            code="invalid-local-yaku",
            name="local yaku",
            value=rule["guyiMode"],
            expected_value=0,
        )

    if "openHand" in rule:
        validate_value(
            errors=errors,
            code="invalid-open-hand",
            name="open hand",
            value=rule["openHand"],
            expected_value=0,
        )

    if "timeAdd" in rule:
        validate_value(
            errors=errors,
            code="invalid-thinking-time-add",
            name="thinking time(add)",
            value=rule["timeAdd"],
            expected_value=20,
        )

    if "timeFixed" in rule:
        validate_value(
            errors=errors,
            code="invalid-thinking-time-fixed",
            name="thinking time(fixed)",
            value=rule["timeFixed"],
            expected_value=5,
        )

    return not bool(errors), errors
