from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Article(models.Model):
    APPROVE = 1
    REJECT = 2
    STATUS = (
        (APPROVE, _('APPROVE')),
        (REJECT, _('REJECT')),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=REJECT,
        null=True,
        blank=True
    )

    # Foreign Keys
    written_by = models.ForeignKey('writer.Writer', on_delete=models.CASCADE, related_name="writer" , null=True, blank=True)
    edited_by = models.ForeignKey('writer.Writer', on_delete=models.CASCADE, related_name="editor" , null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
