from django.db import models


class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)  # type: ignore
    url_or_path = models.CharField(max_length=2048)  # type: ignore
    new_tab = models.BooleanField(default=False)  # type: ignore

    site_setup = models.ForeignKey(  # type: ignore
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True,
        default=None
    )

    def __str__(self) -> str:
        return self.text


class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)  # type: ignore
    description = models.CharField(max_length=255)  # type: ignore

    show_header = models.BooleanField(default=True)  # type: ignore
    show_search = models.BooleanField(default=True)  # type: ignore
    show_menu = models.BooleanField(default=True)  # type: ignore
    show_description = models.BooleanField(default=True)  # type: ignore
    show_pagination = models.BooleanField(default=True)  # type: ignore
    show_footer = models.BooleanField(default=True)  # type: ignore

    def __str__(self) -> str:
        return self.title
