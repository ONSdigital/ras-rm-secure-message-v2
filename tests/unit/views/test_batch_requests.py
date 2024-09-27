def test_batch_mark_thread_for_deletion(test_client, mocker):
    mocker.patch("secure_message_v2.views.batch_requests.marked_for_deletion_by_closed_at_date")
    response = test_client.patch("batch/mark_thread_for_deletion", auth=("admin", "secret"))

    assert 204 == response.status_code
