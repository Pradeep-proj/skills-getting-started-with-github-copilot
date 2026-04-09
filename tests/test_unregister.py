from urllib.parse import quote


def test_unregister_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "Missing Club"
    email = "student@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_signed_up_returns_400(client):
    # Arrange
    activity = "Soccer Team"
    email = "unknown@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
