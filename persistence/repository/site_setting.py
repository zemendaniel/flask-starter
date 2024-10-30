from flask import g


class SiteSettingRepository:
    @staticmethod
    def set_org_name(name):
        org_name = g.session.scalar(SiteSetting.select().where(SiteSetting.key == 'org_name')) or SiteSetting()
        org_name.key = 'org_name'
        org_name.value = name
        org_name.save()

    @staticmethod
    def get_org_name():
        name = g.session.scalar(SiteSetting.select().where(SiteSetting.key == 'org_name'))
        if name:
            return name.value
        return "Szervezet neve"

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
