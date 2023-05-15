# -*- coding: utf-8 -*-


import io
import json

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class PatientReport(models.TransientModel):
    """ creating a wizard to get the report of the patients """
    _name = 'patient.report'
    _description = 'patient report wizard'

    patient_name_id = fields.Many2one('res.partner', string="Patient Name")
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string='To Date')
    disease_id = fields.Many2one('patient.disease', string="Disease")
    department_id = fields.Many2one('hr.department', string="Department")

    @api.constrains('date_from', 'date_to')
    def validation_error(self):
        """ set validation error for date"""
        if (self.date_from and self.date_to) and self.date_from > self.date_to:
            raise ValidationError('Sorry, End Date Must be greater Than Start Date...')

    def action_print_report(self):
        """ adding print button for report """
        seq = []
        if self.patient_name_id:
            seq = self.env['patient.card'].search([('patient_name_id', "=", self.patient_name_id.id)]).mapped(
                'patient')

        record_table = """
                    select hr_employee.name AS doctor,
                    patient_op.token_no, patient_op.date,
                    res_partner.name AS patient_name,
                    hr_department.name AS dept_name,
    				patient_disease.disease
    				
    				from patient_op
                    inner join hr_employee on patient_op.doctor_id = hr_employee.id
                    inner join res_partner on patient_op.patient_name_id = res_partner.id
                    inner join hr_department on patient_op.department_id = hr_department.id
    				inner join patient_consultation on patient_op.id=patient_consultation.op_id
    				inner join patient_disease on patient_consultation.disease_id=patient_disease.id
                    where 1=1
                    """

        if self.patient_name_id:
            record_table += """ and res_partner.name=  '""" + self.patient_name_id.name + """'"""

        if self.doctor_id:
            record_table += """ and hr_employee.name = '""" + self.doctor_id.name + """'"""

        if self.department_id:
            record_table += """ and hr_department.name = '""" + self.department_id.name + """'"""

        if self.date_from:
            record_table += """ and patient_op.date >= '""" + str(self.date_from) + """'"""

        if self.date_to:
            record_table += """ and patient_op.date <= '""" + str(self.date_to) + """'"""

        if self.disease_id:
            record_table += """ and patient_disease.disease= '""" + self.disease_id.disease + """'"""

        self.env.cr.execute(record_table)
        table = self.env.cr.dictfetchall()

        data = {
            'patient_name_id': self.patient_name_id.name,
            'doctor_id': self.doctor_id.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'disease_id': self.disease_id.id,
            'department': self.department_id.id,
            'seq': seq,
            'table_data': table,
        }
        return self.env.ref('hospital_management.action_patient_report').report_action(self, data=data)

    def action_print_xls(self):
        """ adding XLSX button for report """
        sequence = []
        if self.patient_name_id:
            sequence = self.env['patient.card'].search([('patient_name_id', '=', self.patient_name_id.id)]).mapped(
                'patient')

        xl_table = """
                   select hr_employee.name AS doctor,
                    patient_op.token_no, patient_op.date,
                    res_partner.name AS patient_name,
                    hr_department.name AS dept_name,
    				patient_disease.disease
    				
    				from patient_op
                    inner join hr_employee on patient_op.doctor_id = hr_employee.id
                    inner join res_partner on patient_op.patient_name_id = res_partner.id
                    inner join hr_department on patient_op.department_id = hr_department.id
    				inner join patient_consultation on patient_op.id=patient_consultation.op_id
    				inner join patient_disease on patient_consultation.disease_id=patient_disease.id
                 """

        if self.patient_name_id:
            xl_table += """ and res_partner.name=  '""" + self.patient_name_id.name + """'"""

        if self.doctor_id:
            xl_table += """ and hr_employee.name = '""" + self.doctor_id.name + """'"""

        if self.department_id:
            xl_table += """ and hr_department.name = '""" + self.department_id.name + """'"""

        if self.date_from:
            xl_table += """ and patient_op.date >= '""" + str(self.date_from) + """'"""

        if self.date_to:
            xl_table += """ and patient_op.date <= '""" + str(self.date_to) + """'"""

        if self.disease_id:
            xl_table += """ and patient_disease.disease= '""" + self.disease_id.disease + """'"""

        self.env.cr.execute(xl_table)
        table_xl = self.env.cr.dictfetchall()

        data = {
            'patient_name': self.patient_name_id.name,
            'doctor': self.doctor_id.name,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'disease': self.disease_id.id,
            'department': self.department_id.id,
            'seq': sequence,
            'xl_table': table_xl

        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'patient.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """ datas passing to xls """

        if len(data['seq']) == 1:
            sub = str(data['seq']) + ' - ' + data['patient_name']
            sub = sub.replace(']', "")
            sub = sub.replace('[', "")
        else:
            sub = data['patient_name']

        patient_name = data['patient_name']
        doctor = data['doctor']
        date_from = data['date_from']
        date_to = data['date_to']
        table = data['xl_table']
        head_sub = sub

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '25px', 'bg_color': '#CCCCCC'})

        sub_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px'})

        doctor_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '12px'})

        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})

        date_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '12px'})

        bold = workbook.add_format({'bold': True, 'font_size': '12px', 'bg_color': '#CCCCCC', 'align': 'center'})

        sheet.merge_range('C2:K3', 'Medical Report', head)

        if patient_name:
            sheet.merge_range('E5:I6', head_sub, sub_head)
        else:
            sheet.merge_range('D5:J6', '', sub_head)

        if doctor:
            sheet.merge_range('F9:H9', doctor, doctor_head)
        else:
            sheet.merge_range('F9:H9', '', doctor_head)

        if date_from:
            sheet.merge_range('C12:F12', 'From Date  :  ' + date_from, date_head)

        if date_to:
            sheet.merge_range('H12:K12', 'To Date  :  ' + date_to, date_head)

        sheet.write('A16', 'Sl_no', bold)

        sheet.merge_range('B16:C16', 'OP', bold)

        sheet.merge_range('D16:F16', 'Patient_Name', bold)

        sheet.write('G16', 'Date', bold)

        sheet.merge_range('H16:I16', 'Doctor', bold)

        sheet.merge_range('J16:L16', 'Department', bold)

        sheet.merge_range('M16:N16', 'Disease', bold)

        row = 17
        sl_no = 1

        for rec in table:

            sheet.write('A' + str(row + 2), sl_no, txt)

            sheet.merge_range('B' + str(row + 2) + ':C' + str(row + 2), rec['token_no'], txt)

            sheet.merge_range('D' + str(row + 2) + ':F' + str(row + 2), rec['patient_name'], txt)

            sheet.write('G' + str(row + 2), rec['date'], txt)

            sheet.merge_range('H' + str(row + 2) + ':I' + str(row + 2), rec['doctor'], txt)

            sheet.merge_range('J' + str(row + 2) + ':L' + str(row + 2), rec['dept_name'], txt)

            sheet.merge_range('M' + str(row + 2) + ':N' + str(row + 2), rec['disease'], txt)

            row += 2
            sl_no += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


