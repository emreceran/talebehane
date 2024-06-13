# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_profile.controllers.main import WebsiteProfile


class CustomWebsiteProfile(WebsiteProfile):

    @http.route('/profile/edit', type='http', auth="user", website=True)
    def view_user_profile_edition(self, **kwargs):
        user_id = int(kwargs.get('user_id', 0))
        countries = request.env['res.country'].search([])
        ils = request.env['talebehane.il'].sudo().search([])

        if user_id and request.env.user.id != user_id and request.env.user._is_admin():
            user = request.env['res.users'].browse(user_id)
            values = self._prepare_user_values(searches=kwargs, user=user, is_public_user=False)
        else:
            values = self._prepare_user_values(searches=kwargs)

        values.update({
            'email_required': kwargs.get('email_required'),
            'countries': countries,
            'ils': ils,
            'url_param': kwargs.get('url_param'),
        })

        return request.render("website_profile.user_profile_edit_main", values)

    def _profile_edition_preprocess_values(self, user, **kwargs):
        values = {
            'name': kwargs.get('name'),
            'website': kwargs.get('website'),
            'email': kwargs.get('email'),
            'twitter_account': kwargs.get('twitter_account'),
            'il_id': int(kwargs.get('il_id')) if kwargs.get('il_id') else False,
            'ilce_id': int(kwargs.get('ilce_id')) if kwargs.get('ilce_id') else False,
            'lise_id': int(kwargs.get('lise_id')) if kwargs.get('lise_id') else False,
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
        if 'lise_id' in values:
            whitelisted_values['lise_id'] = values['lise_id']
        if 'twitter_account' in values:
            whitelisted_values['twitter_account'] = values['twitter_account']

        user.write(whitelisted_values)

        if kwargs.get('url_param'):
            return request.redirect("/profile/user/%d?%s" % (user.id, kwargs['url_param']))
        else:
            return request.redirect("/profile/user/%d" % user.id)
