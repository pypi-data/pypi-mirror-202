"""These tests will only run if you have set up an Pretalx Account"""
import os
from datetime import date

import pytest

EVENT_SLUG = "pyconde-pydata-berlin-2023"


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_me_endpoint(pretalx_client):
    me = pretalx_client.me()
    assert me.name == "Florian Wilhelm"


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_events_endpoint(pretalx_client):
    count, all_events = pretalx_client.events()
    assert count == len(list(all_events))


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_event_endpoint(pretalx_client):
    event = pretalx_client.event(EVENT_SLUG)
    assert event.date_from == date.fromisoformat('2023-04-17')


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_submissions_endpoint(pretalx_client):
    count, subs = pretalx_client.submissions(EVENT_SLUG)
    assert count == len(list(subs))


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_submission_endpoint(pretalx_client):
    sub = pretalx_client.submission(EVENT_SLUG, 'MD9SLQ')
    assert sub.submission_type.en == 'Talk'


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_talks_endpoint(pretalx_client):
    count, talks = pretalx_client.talks(EVENT_SLUG)
    assert count == len(list(talks))


# ToDo: Add check for single speaker too


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_speakers_endpoint(pretalx_client):
    count, speakers = pretalx_client.speakers(EVENT_SLUG)
    assert count == len(list(speakers))


# ToDo: Add check for single speaker too


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_reviews_endpoint(pretalx_client):
    count, reviews = pretalx_client.reviews(EVENT_SLUG)
    assert count == len(list(reviews))


# ToDo: Add check for single review too


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_rooms_endpoint(pretalx_client):
    count, rooms = pretalx_client.rooms(EVENT_SLUG)
    assert count == len(list(rooms))


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_room_endpoint(pretalx_client):
    room = pretalx_client.room(EVENT_SLUG, 1882)
    assert room.name.en == 'B09'


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_questions_endpoint(pretalx_client):
    count, questions = pretalx_client.questions(EVENT_SLUG)
    assert count == len(list(questions))


# ToDo: Add check for single question too


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_answers_endpoint(pretalx_client):
    count, answers = pretalx_client.answers(EVENT_SLUG)
    assert count == len(list(answers))


# ToDo: Add check for single answer too


@pytest.mark.skipif(os.getenv('GITHUB'), reason="on Github")
def test_tags_endpoint(pretalx_client):
    count, tags = pretalx_client.tags(EVENT_SLUG)
    assert count == len(list(tags))


# ToDo: Add check for single tag too
