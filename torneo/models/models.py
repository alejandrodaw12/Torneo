# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class torneo(models.Model):
#     _name = 'torneo.torneo'
#     _description = 'torneo.torneo'

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

from odoo import models, fields, exceptions, api


class competidores(models.Model):
    _name = 'torneo.competidores'
    _description = 'Define los atributos del competidor'

    # Atributos
    dniCompetidor = fields.Char(string='DNI', required=True)
    nombreCompetidor = fields.Char(string='Nombre y apellidos', required=True)
    fechaNacimiento = fields.Date(string='Fecha Nacimiento', required=True, default=fields.date.today())
    nombrePokemon = fields.Char(string='Pokemon')
    edad = fields.Integer('Edad', compute='_getEdad')

    # Relacion de tablas
    competicion_id = fields.Many2one('torneo.competicion', string='Competicion')



    def name_get(self):
        listaCompetidores = []
        for competidores in self:
            listaCompetidores.append((competidores.id, competidores.nombreCompetidor))
        return listaCompetidores

    @api.depends('fechaNacimiento')
    def _getEdad(self):
        hoy = date.today()
        for competidores in self:
            competidores.edad = relativedelta(hoy, competidores.fechaNacimiento).years

    @api.constrains('fechaNacimiento')
    def _checkEdad(self):
        for competidores in self:
            if (competidores.edad < 18):
                raise exceptions.ValidationError("El competidor no puede ser menor de edad")

    @api.constrains('dniCompetidor')
    def _checkDNI(self):
        for competidores in self:
            if (len(competidores.dniCompetidor) > 9):
                raise exceptions.ValidationError("El DNI no puede tener mas 9 caracteres")
            if (len(competidores.dniCompetidor) < 9):
                raise exceptions.ValidationError("El DNI no puede tener menos 9 caracteres")

class competicion(models.Model):
    _name = 'torneo.competicion'
    _description = 'Define los atributos de la competicion'

    # Atributos
    idCompeticion = fields.Integer(string='id', required=True)
    nombreCompeticion = fields.Char(string='Nombre Competicion', required=True)
    fechaCompeticion = fields.Date(string='Fecha Competicion', required=True, default=fields.date.today())
    lugarCompeticion = fields.Selection(string='Lugar de la Competicion', selection=[('f','Madrid'),('b','Barcelona'), ('c','Sevilla')], help='Lugar para hacer la Competicion' )


    #Relacion entre tablas
    competidores_id = fields.Many2many('torneo.competidores', string='Competidores')

    # Relacion entre modulos
    itinerario_id = fields.Many2many('horario.itinerario', string="Itinerario")
    arbitro_id = fields.Many2many('horario.arbitros', string="Arbitro")
    reglas_id = fields.Many2many('horario.reglas', string="Reglas")


    def name_get(self):
        listaCompetiones = []
        for competicion in self:
            listaCompetiones.append((competicion.id, competicion.nombreCompeticion))
        return listaCompetiones

