# -*- coding: utf-8 -*-
from odoo import models, api


class PatientReport(models.AbstractModel):
    _name = 'report.hospital_management.patient_report_temp'

    @api.model
    def _get_report_values(self, docids, data=None):
        if len(data['seq']) == 1:
            sub = str(data['seq']) + ' - ' + data['patient_name_id']
            sub = sub.replace('[', " ")
            sub = sub.replace(']', " ")
        else:
            sub = data['patient_name_id']
        return {
            'doc_ids': docids,
            'doc_model': "patient.report",
            'sub_head': sub,
            'doctor': data['doctor_id'],
            'data': data,
            'table': data['table_data'],
        }
