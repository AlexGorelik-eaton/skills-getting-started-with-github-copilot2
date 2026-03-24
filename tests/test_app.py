import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities dict to its original state after each test."""
    yield
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

def test_get_activities_returns_200():
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Robotics Club",
    ]

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    for name in expected_activities:
        assert name in data


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404():
    # Arrange
    activity_name = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_signup_duplicate_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # already a participant in seed data

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/unregister
# ---------------------------------------------------------------------------

def test_unregister_success():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # existing participant in seed data

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404():
    # Arrange
    activity_name = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_not_registered_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "notaparticipant@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
