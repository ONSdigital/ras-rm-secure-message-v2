def test_mark_thread_for_deletion(test_client, mocker):
    mocker.patch("secure_message_v2.views.batch_requests.marked_for_deletion_by_closed_at_date")
    response = test_client.patch("batch/mark_thread_for_deletion", auth=("admin", "secret"))

    assert 204 == response.status_code


def test_delete_threads_marked_for_deletion(test_client, mocker):
    mocker.patch("secure_message_v2.views.batch_requests.delete_threads_marked_for_deletion")
    response = test_client.delete("batch/threads", auth=("admin", "secret"))

    assert 204 == response.status_code
