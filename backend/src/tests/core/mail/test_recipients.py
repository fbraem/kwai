from kwai.core.domain.value_objects import EmailAddress
from kwai.core.mail.recipient import Recipients, Recipient


def test_recipients_add_cc():
    recipients = Recipients(
        Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")
    )
    recipients = recipients.add_cc(
        Recipient(email=EmailAddress("kyuzo.mifune@kwai.com"), name="Kyuzo Mifune")
    ).add_cc(
        Recipient(
            email=EmailAddress("kunisaburo.iizuka@kwai.com"), name="Kunisaburo Iizuka"
        )
    )

    assert len(recipients.cc) == 2, "There should be 2 cc recipients."


def test_recipients_with_cc():
    recipients = Recipients(
        Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")
    )
    recipients = recipients.with_cc(
        Recipient(email=EmailAddress("kyuzo.mifune@kwai.com"), name="Kyuzo Mifune"),
        Recipient(
            email=EmailAddress("kunisaburo.iizuka@kwai.com"), name="Kunisaburo Iizuka"
        ),
    )

    assert len(recipients.cc) == 2, "There should be 2 cc recipients."


def test_recipients_add_to():
    recipients = Recipients(
        Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")
    )
    recipients = recipients.add_to(
        Recipient(email=EmailAddress("kyuzo.mifune@kwai.com"), name="Kyuzo Mifune")
    ).add_to(
        Recipient(
            email=EmailAddress("kunisaburo.iizuka@kwai.com"), name="Kunisaburo Iizuka"
        )
    )

    assert len(recipients.to) == 2, "There should be 2 to recipients."


def test_recipients_with_to():
    recipients = Recipients(
        Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")
    )
    recipients = recipients.with_to(
        Recipient(email=EmailAddress("kyuzo.mifune@kwai.com"), name="Kyuzo Mifune"),
        Recipient(
            email=EmailAddress("kunisaburo.iizuka@kwai.com"), name="Kunisaburo Iizuka"
        ),
    )

    assert len(recipients.to) == 2, "There should be 2 to recipients."


def test_recipients_add_bcc():
    recipients = Recipients(
        Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")
    )
    recipients = recipients.add_bcc(
        Recipient(email=EmailAddress("kyuzo.mifune@kwai.com"), name="Kyuzo Mifune")
    ).add_bcc(
        Recipient(
            email=EmailAddress("kunisaburo.iizuka@kwai.com"), name="Kunisaburo Iizuka"
        )
    )

    assert len(recipients.bcc) == 2, "There should be 2 bcc recipients."


def test_recipients_with_bcc():
    recipients = Recipients(
        Recipient(email=EmailAddress("jigoro.kano@kwai.com"), name="Jigoro Kano")
    )
    recipients = recipients.with_bcc(
        Recipient(email=EmailAddress("kyuzo.mifune@kwai.com"), name="Kyuzo Mifune"),
        Recipient(
            email=EmailAddress("kunisaburo.iizuka@kwai.com"), name="Kunisaburo Iizuka"
        ),
    )

    assert len(recipients.bcc) == 2, "There should be 2 cc recipients."
