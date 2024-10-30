from flask import g


class SiteSettingRepository:
    @staticmethod
    def set_org_name(name):
        org_name = g.session.scalar(SiteSetting.select().where(SiteSetting.key == 'org_name')) or SiteSetting()
        org_name.key = 'org_name'
        org_name.value = name.encode('utf-8')
        org_name.save()

    @staticmethod
    def get_org_name():
        name = g.session.scalar(SiteSetting.select().where(SiteSetting.key == 'org_name'))
        if name:
            return name.value.decode('utf-8')
        return "Szervezet neve"

    @staticmethod
    def delete(site_setting):
        g.session.delete(site_setting)
        g.session.commit()

    @staticmethod
    def save(site_setting):
        g.session.add(site_setting)
        g.session.commit()


from persistence.model.site_setting import SiteSetting
