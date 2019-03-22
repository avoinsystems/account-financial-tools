# Copyright 2019 Avoin.Systems
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class BankAccount(models.Model):
    _inherit = 'res.partner.bank'
    _sql_constraints = [('unique_number',
                         'CHECK(1=1)',
                         'Check 1=1 should never fail.')]

    override_uniqueness = fields.Boolean(
        "Override Uniqueness",
        help="Overrides bank account number uniqueness constraint",
    )

    @api.constrains('company_id',
                    'sanitized_acc_number',
                    'override_uniqueness')
    def _check_account_uniqueness(self):
        records = self.filtered(lambda x: not x.override_uniqueness)
        errors = []

        for r in records:
            duplicate_count = r.search_count([
                ('company_id', '=', r.company_id.id),
                ('sanitized_acc_number', '=', r.sanitized_acc_number),
                ('id', '!=', r.id),
                ('override_uniqueness', '=', False)])

            if duplicate_count:
                errors.append(r.sanitized_acc_number)

        if errors:
            raise models.ValidationError(
                'Account number must be unique. '
                'The following accounts have duplicates: {}'
                .format(", ".join(errors)))