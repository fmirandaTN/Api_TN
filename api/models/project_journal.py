from datetime import datetime, date, timedelta
from django.db import models

journal_entry_types = {1 : "Se completo la etapa {}.",
                        2: "Se libero el pago asociado a la etapa {}.",
                        3: "El pago fue completado, se inicio el proyecto."}


class ProjectJournal(models.Model):
    project = models.ForeignKey(
        'api.Project', related_name="journal", on_delete=models.CASCADE)
    entry = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def text_template(self):
        return journal_entry_types[self.entry]