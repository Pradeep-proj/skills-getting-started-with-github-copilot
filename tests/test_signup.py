from urllib.parse import quote


def test_signup_for_activity_success(client):
    # Arrange
    activity = "Soccer Team"
    email = "newstudent@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate_fails(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    encoded_activity = quote(activity, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
