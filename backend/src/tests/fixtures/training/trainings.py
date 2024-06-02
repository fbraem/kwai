"""Module for defining factory fixtures for trainings."""

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.modules.training.coaches.coach import CoachEntity
from kwai.modules.training.trainings.training import TrainingEntity
from kwai.modules.training.trainings.training_db_repository import TrainingDbRepository
from kwai.modules.training.trainings.value_objects import TrainingCoach


@pytest.fixture
def make_text(
    *,
    locale: Locale | None = None,
    format_: DocumentFormat | None = None,
    title: str = "Training Test",
    content: str = "This is a test training",
    summary: str = "Test",
    owner: Owner,
):
    """A factory fixture for a text."""

    def _make_text() -> LocaleText:
        return LocaleText(
            title=title,
            content=content,
            summary=summary,
            locale=locale or Locale.NL,
            format=format_ or DocumentFormat.MARKDOWN,
            author=owner,
        )

    return _make_text


@pytest.fixture
def make_training_coach(make_coach, owner: Owner):
    """A factory fixture for a training coach."""

    def _make_training_coach(coach: CoachEntity | None = None) -> TrainingCoach:
        if coach is None:
            # make_coach returns a coach entity from the club module, so we need
            # to convert it to one for the training module.
            club_coach = make_coach()
            coach = CoachEntity(
                id_=club_coach.id, name=club_coach.name, active=club_coach.is_active
            )
        return TrainingCoach(coach=coach, owner=owner)

    return _make_training_coach


@pytest.fixture
def make_training(make_text, make_training_coach):
    """A factory fixture for a training."""

    def _make_training(
        text: LocaleText | None = None,
        coach: TrainingCoach | None = None,
        period: Period | None = None,
    ) -> TrainingEntity:
        coach = coach or make_training_coach()
        text = text or make_text()
        period = period or Period.create_from_delta(hours=2)
        return TrainingEntity(texts=[text], coaches=[coach], season=None, period=period)

    return _make_training


@pytest.fixture
def make_training_in_db(request, event_loop, database: Database, make_training):
    """A factory fixture for a training in the database."""

    async def _make_training_in_db(
        training: TrainingEntity | None = None,
    ) -> TrainingEntity:
        training = training or make_training()
        repo = TrainingDbRepository(database)
        async with UnitOfWork(database):
            training = await repo.create(training)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(training)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return training

    return _make_training_in_db
