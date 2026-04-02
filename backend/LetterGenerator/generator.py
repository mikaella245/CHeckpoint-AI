from LetterGenerator.schemas import LetterRequest
from LetterGenerator.templates import render_letter
from LetterGenerator.llm_service import polish_details


def right_block(text: str, indent: int = 40) -> str:
    lines = text.split("\n")
    return "\n".join((" " * indent) + line for line in lines)


def generate_letter(data: LetterRequest) -> str:
    details_paragraph = polish_details(data.letter_type, data.additional_details or "")

    if data.letter_type == "rent-increase":
        return render_letter(
            tenant_name=data.tenant_name,
            address=data.address,
            landlord_name=data.landlord_name,
            landlord_address=data.landlord_address,
            subject="Objet : Contestation de la hausse de loyer",
            opening=(
                "Madame, Monsieur,\n\n"
                "Par la présente, je conteste la hausse de loyer qui m'a été communiquée."
            ),
            details_paragraph=details_paragraph,
            legal_paragraph=(
                "Conformément aux articles 269, 269a et 270 du Code des obligations (CO), "
                "je vous prie de bien vouloir justifier cette augmentation et m'en communiquer les bases."
            ),
            closing=(
                "Dans l'attente de votre réponse, je vous prie d'agréer, Madame, Monsieur, "
                "mes salutations distinguées."
            ),
        )

    if data.letter_type == "rent-decrease":
        return render_letter(
            tenant_name=data.tenant_name,
            address=data.address,
            landlord_name=data.landlord_name,
            landlord_address=data.landlord_address,
            subject="Objet : Demande de baisse de loyer",
            opening=(
                "Madame, Monsieur,\n\n"
                "Par la présente, je sollicite une diminution de mon loyer."
            ),
            details_paragraph=details_paragraph,
            legal_paragraph=(
                "Conformément à l'article 270a du Code des obligations (CO), "
                "je vous prie de bien vouloir réexaminer mon loyer et me communiquer le montant ajusté."
            ),
            closing=(
                "Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, "
                "mes salutations distinguées."
            ),
        )

    if data.letter_type == "guarantee-return":
        return render_letter(
            tenant_name=data.tenant_name,
            address=data.address,
            landlord_name=data.landlord_name,
            landlord_address=data.landlord_address,
            subject="Objet : Demande de libération de la garantie de loyer",
            opening=(
                "Madame, Monsieur,\n\n"
                "Par la présente, je vous demande de bien vouloir procéder à la libération de ma garantie de loyer."
            ),
            details_paragraph=details_paragraph,
            legal_paragraph=(
                "Conformément à l'article 257e du Code des obligations (CO), "
                "je vous prie de prendre les mesures nécessaires pour permettre la restitution de ce montant."
            ),
            closing=(
                "Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées."
            ),
        )

    if data.letter_type == "fault-repair":
        return render_letter(
            tenant_name=data.tenant_name,
            address=data.address,
            landlord_name=data.landlord_name,
            landlord_address=data.landlord_address,
            subject="Objet : Signalement d'un défaut et demande de réparation",
            opening=(
                "Madame, Monsieur,\n\n"
                "Par la présente, je vous informe d'un défaut affectant le logement que j'occupe "
                "et vous demande d'y remédier dans les meilleurs délais."
            ),
            details_paragraph=details_paragraph,
            legal_paragraph=(
                "Conformément aux articles 256 et 259a à 259b du Code des obligations (CO), "
                "le bailleur est tenu d'entretenir la chose dans un état approprié à l'usage convenu."
            ),
            closing=(
                "Dans l'attente de votre intervention rapide, je vous prie d'agréer, Madame, Monsieur, "
                "mes salutations distinguées."
            ),
        )

    if data.letter_type == "conciliation":
        return render_letter(
            tenant_name=data.tenant_name,
            address=data.address,
            landlord_name=data.landlord_name,
            landlord_address=data.landlord_address,
            subject="Objet : Requête en conciliation",
            opening=(
                "Madame, Monsieur,\n\n"
                "Par la présente, je soumets une requête en conciliation concernant un litige locatif."
            ),
            details_paragraph=details_paragraph,
            legal_paragraph=(
                "Conformément à l'article 274a du Code des obligations (CO), "
                "je sollicite l'intervention de l'autorité de conciliation compétente."
            ),
            closing=(
                "Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées."
            ),
        )

    if data.letter_type == "resiliation":
        if data.preavis_type == "outside":
            return render_letter(
                tenant_name=data.tenant_name,
                address=data.address,
                landlord_name=data.landlord_name,
                landlord_address=data.landlord_address,
                subject="Objet : Résiliation anticipée du bail",
                opening=(
                    "Madame, Monsieur,\n\n"
                    "Par la présente, je vous informe de mon souhait de résilier le contrat de bail "
                    "me liant à vous avant l'échéance ordinaire."
                ),
                details_paragraph=details_paragraph,
                legal_paragraph=(
                    "Conformément à l'article 264 du Code des obligations (CO), "
                    "je reste disposé(e) à collaborer dans le cadre d'une éventuelle reprise de bail."
                ),
                closing=(
                    "Dans l'attente de votre réponse, je vous prie d'agréer, Madame, Monsieur, "
                    "mes salutations distinguées."
                ),
            )

        return render_letter(
            tenant_name=data.tenant_name,
            address=data.address,
            landlord_name=data.landlord_name,
            landlord_address=data.landlord_address,
            subject="Objet : Résiliation du bail",
            opening=(
                "Madame, Monsieur,\n\n"
                "Par la présente, je vous informe de ma décision de résilier le contrat de bail "
                "me liant à vous, dans le respect du délai de préavis applicable."
            ),
            details_paragraph=details_paragraph,
            legal_paragraph=(
                "Conformément aux articles 266a et suivants du Code des obligations (CO), "
                "je vous prie de bien vouloir prendre acte de cette résiliation."
            ),
            closing=(
                "Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées."
            ),
        )

    raise ValueError("Unsupported letter type")