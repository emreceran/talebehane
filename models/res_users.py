from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    il_id = fields.Many2one('talebehane.il', string='Province')
    ilce_id = fields.Many2one('talebehane.ilce', string='District')
    lise_id = fields.Many2one('talebehane.lise', string='School')

    adres = fields.Char(string="adres")
    birth_date = fields.Date(string="Doğum Günü")
    birth_place = fields.Char(string="Doğum Yeri")
    school_email = fields.Char(string="Okul Email")
    twitter_account = fields.Char(string="Twitter")
    facebook_account = fields.Char(string="Facebook")
    instagram_account = fields.Char(string="Instagram")
    linkedin_account = fields.Char(string="LinkedIn")

    uni_id = fields.Many2one('talebehane.uni', string='Üniversite')
    fak_id = fields.Many2one('talebehane.fak', string='Fakülte')
    bolum_id = fields.Many2one('talebehane.bolum', string='Bölüm')


    managed_il_ids = fields.One2many('talebehane.il', 'manager_id', string='Yönettiği İller')
    managed_ilce_ids = fields.One2many('talebehane.ilce', 'manager_id', string='Yönettiği İlçeler')
    managed_lise_ids = fields.One2many('talebehane.lise', 'manager_id', string='Yönettiği Liseler')

    nationality_id = fields.Many2one('res.country', string='Uyruk')
    tc_kimlik_no = fields.Char(string="Tc Kimlik No")
    gender = fields.Selection([
        ('male', 'Erkek'),
        ('female', 'Kadın'),
    ], string='Cinsiyet')

    @api.constrains('tc_kimlik_no')
    def _check_tc_kimlik_no(self):
        for record in self:
            if record.tc_kimlik_no:
                if not record.tc_kimlik_no.isdigit():
                    raise ValidationError('TC Kimlik No sadece rakamlardan oluşmalıdır.')
                if len(record.tc_kimlik_no) != 11:
                    raise ValidationError('TC Kimlik No 11 haneli olmalıdır.')

    def action_grant_karma(self):
        self.ensure_one()
        self.karma += 10  # Örneğin, 10 karma puanı ekleyin


