from flask import g
from werkzeug.datastructures import FileStorage


class SiteSettingRepository:
    @staticmethod
    def find_by_key(key):
        return g.session.scalar(SiteSetting.select().where(SiteSetting.key == key))

    @staticmethod
    def set_org_name(name):
        org_name = SiteSettingRepository.find_by_key('org_name') or SiteSetting()
        org_name.key = 'org_name'
        org_name.value = name.encode('utf-8')
        org_name.save()

    @staticmethod
    def get_org_name():
        name = SiteSettingRepository.find_by_key('org_name')
        if name:
            return name.value.decode('utf-8')
        return "Szervezet neve"

    @staticmethod
    def set_favicon(file):
        favicon = SiteSettingRepository.find_by_key('favicon') or SiteSetting()
        favicon.key = 'favicon'
        favicon.value = file.read()
        favicon.save()

    @staticmethod
    def get_favicon():
        favicon = SiteSettingRepository.find_by_key('favicon')
        if favicon:
            file: FileStorage = favicon.value
            return file
        return None

    @staticmethod
    def delete(site_setting):
        g.session.delete(site_setting)
        g.session.commit()

    @staticmethod
    def save(site_setting):
        g.session.add(site_setting)
        g.session.commit()

    @staticmethod
    def get_by_key(key):
        return g.session.scalar(SiteSetting.select().where(SiteSetting.key == key))

    @staticmethod
    def get_by_id(id):
        return g.session.scalar(SiteSetting.select().where(SiteSetting.id == id))

from persistence.model.site_setting import SiteSetting
