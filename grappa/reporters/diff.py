# -*- coding: utf-8 -*-
import os
import difflib

from .base import BaseReporter


class DiffReporter(BaseReporter):
    """
    Outputs the comparison differences result between the
    subject/expected objects.
    """

    title = 'Difference comparison'

    def run(self, error):
        # Ensure operator enables diff reporter, otherwise just exit
        show_diff = any([
            self.ctx.show_diff,
            self.from_operator('show_diff', False)
        ])
        if not show_diff:
            return

        # Match if the given operator implements a custom differ
        differ = self.from_operator('differ', None)
        if differ:
            return error.operator.differ()

        # Obtain subject/expected values
        subject = str(self.from_operator('subject', self.ctx.subject))
        expected = str(self.from_operator('expected', self.ctx.expected))

        # Expected results
        if isinstance(expected, tuple) and len(expected) == 1:
            expected = expected[0]

        if isinstance(subject, str):
            subject = subject.splitlines(1)
        else:
            subject = [subject]

        if isinstance(expected, str):
            expected = expected.splitlines(1)
        else:
            expected = [expected]

        # Diff subject and expected values
        data = list(difflib.ndiff(subject, expected))

        # Remove trailing line feed
        data[-1] = data[-1].replace(os.linesep, '')

        # Normalize line separator with proper indent level
        data = [i.replace(os.linesep, '') for i in data]

        return data
