from datetime import datetime

LEGAL_BASIS = {
    "rent-increase": "Art. 269, 269a, 270 CO",
    "rent-decrease": "Art. 270a CO",
    "guarantee-return": "Art. 257e CO",
    "fault-repair": "Art. 256, 259a-259b CO",
    "conciliation": "Art. 274a CO",
    "resiliation-within": "Art. 266a-266o CO",
    "resiliation-outside": "Art. 264 CO",
}

MONTHS_FR = {
    1: "janvier",
    2: "février",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "août",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "décembre",
}


def today_formal_fr() -> str:
    now = datetime.now()
    return f"{now.day} {MONTHS_FR[now.month]} {now.year}"


def right_align(text: str, width: int = 80) -> str:
    lines = text.split("\n")
    return "\n".join(line.rjust(width) for line in lines)


def render_letter(
    tenant_name: str,
    address: str,
    landlord_name: str,
    landlord_address: str,
    subject: str,
    opening: str,
    details_paragraph: str,
    legal_paragraph: str,
    closing: str,
) -> str:
    details_block = f"\n\n{details_paragraph}" if details_paragraph.strip() else ""

    recipient_block = right_align(f"{landlord_name}\n{landlord_address}")
    date_block = right_align(today_formal_fr())

    return f"""{tenant_name}
{address}

{recipient_block}

{date_block}

{subject}

{opening}{details_block}

{legal_paragraph}

{closing}

{tenant_name}"""