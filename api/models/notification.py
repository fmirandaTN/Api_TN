from datetime import datetime, date, timedelta
from django.db import models
from api.models.project import Project
from api.models.user import User
from api.models.request import Request

types_of_notification = {'project': {1 : "Haz recibido una nueva postulación en tu projecto {}.",
                                    2 : "Haz recibido una nueva negociacion en la postulacion de {}.",
                                    3 : "Alguien hizo un pregunta en tu projecto {}.",
                                    4 : "Se termino el proceso de postulación en tu projecto {}, revisa las postulaciones.",
                                    5 : "Se llego a un acuerdo en la negociación con {}.",
                                    6 : "Recuerda realizar el pago para poder dar inicio al proyecto {}."},
                        'request-collaborator': {1 : "Tu postulación al proyecto {} fue rechazada :(",
                                    2 : "El proyecto al que postulaste paso a estado de selección",
                                    3 : "Tienes una nueva negociación en tu postulación a {}.",
                                    4 : "Se ha llegado a un acuerdo de negociación en tu postulación a {}.",
                                    5 : "El proyecto al que postulaste fue editado, resvisalo nuevamente.",
                                    6 : "¡Tu postulacion fue aceptada! Revisa el proyecto.",
                                    7 : "El pago del proyecto {} fue realizado por parte del cliente !Empieza a trabajar!.",
                                    8 : "Tu pregunta en el proyecto {}, fue contestada."},
                        'service': {1: "Haz recibido una invitacion a un proyecto a travez de un servicio. Revisa el proyecto."}}

class Notification(models.Model):
    text_type_choices = [
        ('project', 'project'),
        ('request-collaborator', 'request-collaborator'),
        ('service', 'service')]
    class_type_choices = [
        ('project', 'project'),
        ('request', 'request'),
        ('service', 'service'),
        ('user','user'),
        ('none', 'none')]

    owner = models.ForeignKey(
        'api.User', related_name="notification", on_delete=models.CASCADE, null=True)
    text_type =  models.CharField(max_length=50, choices=text_type_choices)
    text_number = models.IntegerField()
    class_type = models.CharField(max_length=50, choices=class_type_choices)
    class_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def text_template(self):
        out_text = types_of_notification[self.text_type][self.text_number]
        if self.text_type == 'project':
            if self.text_number in [1,3,4,6]:
                # out_text = out_text.format('<b>' + Project.objects.get(id=self.class_id).title +'</b>')
                out_text = out_text.format(Project.objects.get(id=self.class_id).title)
            elif self.text_number in [2,5]:
                user = Request.objects.get(id=self.class_id).emitter
                # out_text = out_text.format('<b>' + user.first_name + ' ' + user.last_name +'</b>')
                out_text = out_text.format(user.first_name + ' ' + user.last_name)
        elif self.text_type == 'request-collaborator':
            if self.text_number in [1,3,4,7,8]:
                print(self.class_id)
                # out_text = out_text.format('<b>' + Project.objects.get(id=self.class_id).title +'</b>')
                out_text = out_text.format(Project.objects.get(id=self.class_id).title)
        return out_text
