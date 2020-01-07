from __future__ import absolute_import

from sentry import eventstore
from sentry.tasks.base import instrumented_task, retry


@instrumented_task(
    name="sentry.tasks.update_user_report",
    queue="update",
    default_retry_delay=60 * 5,
    max_retries=5,
)
@retry()
def update_user_report(user_report, **kwargs):
    event = eventstore.get_event_by_id(user_report.project.id, user_report.event_id)
    if not event:
        raise ValueError

    user_report.update(group=event.group, environment=event.get_environment())
