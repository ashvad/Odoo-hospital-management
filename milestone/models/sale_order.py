from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project')
    sub_task_ids = fields.Many2many('project.task')
    state = fields.Selection(selection_add=[('project', 'project'), ("sent",)])

    def action_sale_create_project(self):
        """ creating project through sale order """
        self.write({'state': 'project'})
        project = self.env['project.project'].create({
            'name': self.name,
            'partner_id': self.partner_id.id
        })
        self.project_id = project.id
        milestone = self.order_line.mapped('milestone')
        for mile in list(set(milestone)):
            task = self.env['project.task'].create({
                'name': "Milestone - " + str(mile),
                'project_id': project.id
            })

            rec_ids = 0
            rec_ids = self.order_line.filtered(lambda m: m.milestone == mile)
            for rec in rec_ids:
                sub_task = self.env['project.task'].create({
                    'name': "Milestone - " + str(mile) + " - " + rec.product_template_id.name,
                    'parent_id': task.id
                })
                self.sub_task_ids = [fields.Command.link(sub_task.id)]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'view_mode': 'form',
            'res_model': 'project.project',
            'context': "{'create':'False'}",
            'res_id': project.id
        }

    def action_sale_update_project(self):
        """ adding an update button for updating order line """
        list_order_line = [line for line in self.order_line]
        for task in self.sub_task_ids:
            task_name = task.name.split('-')
            if task_name[2].strip() not in list_order_line:
                task.unlink()
                self.sub_task_ids = [fields.Command.unlink(task.id)]

        for task in self.project_id.tasks:
            if len(task.parent_id) == 0:
                if len(task.child_ids) == 0:
                    task.unlink()

        for update_line in self.order_line:
            if len(self.project_id.tasks) == 0:
                task_parent = self.env['project.task'].create({
                    'name': "Milestone - " + str(update_line.milestone),
                    'project_id': self.project_id.id
                })
                update_store_sub_task = "Milestone - " + str(
                    update_line.milestone) + " - " + update_line.product_template_id.name
                sub_task = self.env['project.task'].create({
                    'name': update_store_sub_task,
                    'parent_id': task_parent.id
                })
                self.sub_task_ids = [fields.Command.link(sub_task.id)]
            for update_parent_task in self.project_id.tasks:
                if len(update_parent_task.parent_id) == 0:
                    update_store = "Milestone - " + str(update_line.milestone)
                    if update_parent_task.name == update_store:
                        list_map = update_parent_task.child_ids.mapped("name")
                        update_sub_store = "Milestone - " + str(
                            update_line.milestone) + " - " + update_line.product_template_id.name
                        if update_sub_store not in list_map:
                            create_sub_task = self.env['project.task'].create({
                                'name': update_sub_store,
                                'parent_id': update_parent_task.id
                            })
                            self.sub_task_ids = [fields.Command.link(create_sub_task.id)]
                    else:
                        list_mile = self.project_id.tasks.mapped('name')
                        if update_store not in list_mile:
                            create_parent_task = self.env['project.task'].create({
                                'name': update_store,
                                'project_id': self.project_id.id
                            })
                            update_sub2_store = "Milestone - " + str(
                                update_line.milestone) + " - " + update_line.product_template_id.name
                            create_sub_task = self.env['project.task'].create({
                                'name': update_sub2_store,
                                'parent_id': create_parent_task.id
                            })
                            self.sub_task_ids = [fields.Command.link(create_sub_task.id)]

    def action_get_project(self):
        """ creating smart tab in sales """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project',
            'view_mode': 'form',
            'res_model': 'project.project',
            'context': "{'create':'False'}",
            'res_id': self.project_id.id
        }
