from odoo import http
from odoo.http import request
from odoo.addons.website_profile.controllers.main import WebsiteProfile
import base64


class CustomWebsiteProfile(WebsiteProfile):

    @http.route('/profile/edit', type='http', auth="user", website=True)
    def view_user_profile_edition(self, **kwargs):
        user_id = int(kwargs.get('user_id', 0))
        countries = request.env['res.country'].search([])
        country_tr = request.env['res.country'].search([('code', '=', 'TR')], limit=1)
        ils = request.env['talebehane.il'].sudo().search([])
        unis = request.env['talebehane.uni'].sudo().search([])

        if user_id and request.env.user.id != user_id and request.env.user._is_admin():
            user = request.env['res.users'].browse(user_id)
            values = self._prepare_user_values(searches=kwargs, user=user, is_public_user=False)
        else:
            user = request.env.user
            values = self._prepare_user_values(searches=kwargs)

        ilces = request.env['talebehane.ilce'].sudo().search([('il_id', '=', user.il_id.id)]) if user.il_id else []
        faks = request.env['talebehane.fak'].sudo().search([('uni_id', '=', user.uni_id.id)]) if user.uni_id else []
        liseler = request.env['talebehane.lise'].sudo().search([('ilce_id', '=', user.ilce_id.id)]) if user.ilce_id else []
        bolumler = request.env['talebehane.bolum'].sudo().search([('fak_id', '=', user.fak_id.id)]) if user.fak_id else []

        values.update({
            'email_required': kwargs.get('email_required'),
            'countries': countries,
            'country_tr': country_tr,
            'ils': ils,
            'unis': unis,
            'ilces': ilces,
            'faks': faks,
            'liseler': liseler,
            'bolumler': bolumler,
            'user': user,
            'url_param': kwargs.get('url_param'),
        })

        return request.render("website_profile.user_profile_edit_main", values)

    def _profile_edition_preprocess_values(self, user, **kwargs):
        values = {
            'name': kwargs.get('name'),
            'website': kwargs.get('website'),
            'email': kwargs.get('email'),
            'twitter_account': kwargs.get('twitter_account'),
            'facebook_account': kwargs.get('facebook_account'),
            'instagram_account': kwargs.get('instagram_account'),
            'linkedin_account': kwargs.get('linkedin_account'),
            'tc_kimlik_no': kwargs.get('tc_kimlik_no'),
            'gender': kwargs.get('gender'),
            'birth_date': kwargs.get('birth_date'),
            'school_email': kwargs.get('school_email'),
            'adres': kwargs.get('adres'),
            'phone': kwargs.get('phone'),

            'birth_place': int(kwargs.get('birth_place')) if kwargs.get('birth_place') else False,
            'il_id': int(kwargs.get('il_id')) if kwargs.get('il_id') else False,
            'ilce_id': int(kwargs.get('ilce_id')) if kwargs.get('ilce_id') else False,
            # 'lise_id': int(kwargs.get('lise_id')) if kwargs.get('lise_id') else False,
            'uni_id': int(kwargs.get('uni_id')) if kwargs.get('uni_id') else False,
            'fak_id': int(kwargs.get('fak_id')) if kwargs.get('fak_id') else False,
            'bolum_id': int(kwargs.get('bolum_id')) if kwargs.get('bolum_id') else False,
            'website_description': kwargs.get('description'),
        }

        if 'clear_image' in kwargs:
            values['image_1920'] = False
        elif kwargs.get('ufile'):
            image = kwargs.get('ufile').read()
            values['image_1920'] = base64.b64encode(image)

        if request.uid == user.id:  # the controller allows to edit only its own privacy settings; use partner management for other cases
            values['website_published'] = kwargs.get('website_published') == 'True'

        return values

    @http.route('/profile/user/save', type='http', auth="user", methods=['POST'], website=True)
    def save_edited_profile(self, **kwargs):
        user_id = int(kwargs.get('user_id', 0))
        if user_id and request.env.user.id != user_id and request.env.user._is_admin():
            user = request.env['res.users'].browse(user_id)
        else:
            user = request.env.user

        values = self._profile_edition_preprocess_values(user, **kwargs)
        whitelisted_values = {key: values[key] for key in user.SELF_WRITEABLE_FIELDS if key in values}

        # Eklenen alanları kontrol edelim ve whitelist'e ekleyelim
        if 'il_id' in values:
            whitelisted_values['il_id'] = values['il_id']
        if 'ilce_id' in values:
            whitelisted_values['ilce_id'] = values['ilce_id']
        # if 'lise_id' in values:
        #     whitelisted_values['lise_id'] = values['lise_id']
        if 'uni_id' in values:
            whitelisted_values['uni_id'] = values['uni_id']
        if 'fak_id' in values:
            whitelisted_values['fak_id'] = values['fak_id']
        if 'bolum_id' in values:
            whitelisted_values['bolum_id'] = values['bolum_id']
        if 'twitter_account' in values:
            whitelisted_values['twitter_account'] = values['twitter_account']
        if 'facebook_account' in values:
            whitelisted_values['facebook_account'] = values['facebook_account']
        if 'instagram_account' in values:
            whitelisted_values['instagram_account'] = values['instagram_account']
        if 'linkedin_account' in values:
            whitelisted_values['linkedin_account'] = values['linkedin_account']
        if 'tc_kimlik_no' in values:
            whitelisted_values['tc_kimlik_no'] = values['tc_kimlik_no']
        if 'gender' in values:
            whitelisted_values['gender'] = values['gender']
        if 'birth_date' in values:
            whitelisted_values['birth_date'] = values['birth_date']
        if 'birth_place' in values:
            whitelisted_values['birth_place'] = values['birth_place']
        if 'school_email' in values:
            whitelisted_values['school_email'] = values['school_email']
        if 'adres' in values:
            whitelisted_values['adres'] = values['adres']
        if 'phone' in values:
            whitelisted_values['phone'] = values['phone']



        user.write(whitelisted_values)

        if kwargs.get('url_param'):
            return request.redirect("/profile/user/%d?%s" % (user.id, kwargs['url_param']))
        else:
            return request.redirect("/profile/user/%d" % user.id)

    @http.route('/get_ilce', type='json', auth='user', methods=['POST'], website=True)
    def get_ilce(self, il_id):
        try:
            il_id = int(il_id)
        except (ValueError, TypeError):
            return []

        ilceler = request.env['talebehane.ilce'].sudo().search([('il_id', '=', il_id)])
        return [{'id': ilce.id, 'name': ilce.name} for ilce in ilceler]

    # @http.route('/get_lise', type='json', auth='user', methods=['POST'], website=True)
    # def get_lise(self, ilce_id):
    #     liseler = request.env['talebehane.lise'].sudo().search([('ilce_id', '=', int(ilce_id))])
    #     return [{'id': lise.id, 'name': lise.name} for lise in liseler]


    @http.route('/get_fak', type='json', auth='user', methods=['POST'], website=True)
    def get_fak(self, uni_id):
        fakulteler = request.env['talebehane.fak'].sudo().search([('uni_id', '=', int(uni_id))])
        return [{'id': fak.id, 'name': fak.name} for fak in fakulteler]

    @http.route('/get_bolum', type='json', auth='user', methods=['POST'], website=True)
    def get_bolum(self, fak_id):
        bolumler = request.env['talebehane.bolum'].sudo().search([('fak_id', '=', int(fak_id))])
        return [{'id': bolum.id, 'name': bolum.name} for bolum in bolumler]