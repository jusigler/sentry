from __future__ import absolute_import

from sentry.models import UserReport
from sentry.tasks.update_user_reports import update_user_report
from sentry.testutils import TestCase


class UpdateUserReportTest(TestCase):
    def test_task_persistent_name(self):
        assert update_user_report.name == "sentry.tasks.update_user_report"

    def test_simple(self):
        project = self.create_project()
        event = self.store_event(data={}, project_id=project.id)

        report = UserReport.objects.create(project=project, event_id=event.event_id)

        update_user_report(user_report=report)

        report = UserReport.objects.get(project=project, event_id=event.id)
        assert report.group == event.group
        assert report.environment == event.get_environment()
