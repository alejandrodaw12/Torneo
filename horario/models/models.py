# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class horario(models.Model):
#     _name = 'horario.horario'
#     _description = 'horario.horario'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions


class itinerario(models.Model):
    _name = 'horario.itinerario'
    _description = 'Define los atributos del itinerario'

    # Atributos
    nombreItinerario = fields.Char(string='Nombre', required=True)
    inicioTorneo = fields.Selection(string='Inicio del Torneo', selection=[('f','9:00'),('b','16:00'), ('c','20:00')], help='Itinerario del Torneo' )

    inicioPrimerEncuentro = fields.Selection(string='1 Inicio', selection='_get_valid_hours', default='8.5', required=True)
    finalPrimerEncuentro = fields.Selection(string='1 Fin', selection='_get_valid_hours', default='15', required=True)

    inicioSegundoEncuentro = fields.Selection(string='2 Inicio', selection='_get_valid_hours',default='8.5', required=True)
    finalSegundoEncuentro = fields.Selection(string='2 Fin', selection='_get_valid_hours',default='15', required=True)

    inicioTerceroEncuentro = fields.Selection(string='3 Inicio', selection='_get_valid_hours',default='8.5', required=True)
    finalTerceroEncuentro = fields.Selection(string='3 Fin', selection='_get_valid_hours',default='15', required=True)

    inicioCuartoEncuentro = fields.Selection(string='4 Inicio', selection='_get_valid_hours',default='8.5', required=True)
    finalCuartoEncuentro = fields.Selection(string='4 Fin', selection='_get_valid_hours',default='15', required=True)

    #Relacion entre clases
    arbitros_ids = fields.Many2one('horario.arbitros', string='Arbitros')
    reglas_ids = fields.Many2many('horario.reglas', string='Reglas')

    # Relacion entre modulos
    competidores_id = fields.Many2one('torneo.competidores', string='Competidores')


    def name_get(self):
        listaItinerario = []
        for itinerario in self:
            listaItinerario.append((itinerario.id, itinerario.nombreItinerario))
        return listaItinerario

    @api.model
    def _get_valid_hours(self):
        selection = [
            ('8', '8:00'), ('8.5', '8:30'),
            ('9', '9:00'), ('9.5', '9:30'),
            ('10', '10:00'), ('10.5', '10:30'),
            ('11', '11:00'), ('11.5', '11:30'),
            ('12', '12:00'), ('12.5', '12:30'),
            ('13', '13:00'), ('13.5', '13:30'),
            ('14', '14:00'), ('14.5', '14:30'),
            ('15', '15:00'), ('15.5', '15:30'),
            ('16', '16:00'), ('16.5', '16:30'),
            ('17', '17:00'), ('17.5', '17:30'),
            ('18', '18:00')
        ]
        return selection

    @api.constrains('inicioPrimerEncuentro', 'inicioTorneo')
    def change_data_field(self):
        he = float(self.inicioPrimerEncuentro)
        hs = float(self.finalPrimerEncuentro)
        if (he > hs):
            raise exceptions.ValidationError("La hora de finalizar el encuentro no puede ser menos que la del inicio")

        he = float(self.inicioPrimerEncuentro)
        ti = float(self.inicioTorneo)
        if(ti > he):
            raise exceptions.ValidationError("La hora de del primer encuentro no puede menor que el inicio del torneo")

        he = float(self.inicioSegundoEncuentro)
        hs = float(self.finalSegundoEncuentro)
        if (he > hs):
            raise exceptions.ValidationError("La hora de finalizar el encuentro no puede ser menos que la del inicio")

        he = float(self.inicioTerceroEncuentro)
        hs = float(self.finalTerceroEncuentro)
        if (he > hs):
            raise exceptions.ValidationError("La hora de finalizar el encuentro no puede ser menos que la del inicio")

        he = float(self.inicioCuartoEncuentro)
        hs = float(self.finalCuartoEncuentro)
        if (he > hs):
            raise exceptions.ValidationError("La hora de finalizar el encuentro no puede ser menos que la del inicio")



class arbitros(models.Model):
    _name = 'horario.arbitros'
    _description = 'Define los atributos del arbitro del partido'

    dniArbitro = fields.Char(string='DNI Arbitro', required=True)
    nombreArbitro = fields.Char(string='Nombre Arbitro', required=True)
    fechaNacimiento = fields.Date(string='Fecha Nacimiento', required=True, default=fields.date.today())
    edad =  fields.Integer('Edad', compute='_getEdad')
    añosArbitrando = fields.Char(string='Años arbitrando',required=True)

    @api.depends('fechaNacimiento')
    def _getEdad(self):
        hoy = date.today()
        for arbitros in self:
            arbitros.edad = relativedelta(hoy, arbitros.fechaNacimiento).years

    @api.constrains('fechaNacimiento')
    def _checkEdad(self):
        for arbitros in self:
            if (arbitros.edad < 18):
                raise exceptions.ValidationError("El competidor no puede ser menor de edad")

    @api.constrains('dniArbitro')
    def _checkDNI(self):
        for arbitros in self:
            if (len(arbitros.dniArbitro) > 9):
                raise exceptions.ValidationError("El DNI no puede tener mas 9 caracteres")
            if (len(arbitros.dniArbitro) < 9):
                raise exceptions.ValidationError("El DNI no puede tener menos 9 caracteres")

    def name_get(self):
        listaArbitro = []
        for arbitros in self:
            listaArbitro.append((arbitros.id, arbitros.nombreArbitro))
        return listaArbitro

    #Relacion entre clases
    itinerario_ids = fields.Many2one('horario.itinerario', string='Itinerario')
    reglas_ids = fields.Many2many('horario.reglas', string='Reglas')

    #Relacion entre modulos
    competicion_ids = fields.Many2many('torneo.competicion', string='Competicion')


class reglas(models.Model):
    _name = 'horario.reglas'
    _description = 'Define las reglas para cada torneo'

    numeroRegla = fields.Char('Id Regla', required=True)
    nombreRegla = fields.Char('Nombre', required=True)
    descripcionRegla = fields.Text('Description', required=True)

    def name_get(self):
        listaReglas = []
        for reglas in self:
            listaReglas.append((reglas.id, reglas.nombreRegla))
        return listaReglas

    # Relacion entre clases
    arbitros_ids = fields.Many2one('horario.arbitros', string='Arbitros')

    # Relacion entre modulos
    competicion_ids = fields.Many2one('torneo.competicion', string='Competicion')
