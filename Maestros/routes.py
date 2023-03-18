from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Blueprint
import forms
from db import get_connection

blueprint = Blueprint('blueprint',__name__)

maestros = Blueprint('maestros',__name__)

@maestros.route('/maestros', methods = ['GET', 'POST'])
def obtener_maestros():
    frm_maestros = forms.MaesForm(request.form)
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call obtener_maestros()')
            resulset = cursor.fetchall()
            return render_template('maestros.html', form = frm_maestros, resulset = resulset)
    
    except Exception as ex:
        print(ex)
        flash("No fue posible obtener los registros: " + str(ex))

    return render_template('maestros.html', form = frm_maestros)

@maestros.route('/addMaestro', methods = ['GET', 'POST'])
def insert_maestro():

    frm_maestros = forms.MaesForm(request.form)

    if request.method == 'POST':
        nombre = frm_maestros.nombre.data
        apellidos = frm_maestros.apellidos.data
        materia = frm_maestros.materia.data
        email = frm_maestros.email.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call insertar_maestro(%s, %s, %s, %s)', (nombre, apellidos, materia, email))
                connection.commit()
                connection.close()
                flash("Registro ALMACENADO satisfactoriamente")
        except Exception as ex:
            flash("No fue posible insertar el registro: " + str(ex))
        return redirect(url_for('maestros.obtener_maestros'))
    
    return render_template('reggistrarMaestro.html', form = frm_maestros)

@maestros.route('/updateMaestro', methods = ['GET', 'POST'])
def update_maestro():

    frm_maestro = forms.MaesForm(request.form)

    if request.method == 'GET':

        id = request.args.get('id')

        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute('call obtener_maestro(%s)', (id))

            resulset = cursor.fetchall()
        
            return render_template('updateMaestros.html', form = frm_maestro, resulset = resulset)


    if request.method == 'POST':
        id = frm_maestro.id.data
        nombre = frm_maestro.nombre.data
        apellidos = frm_maestro.apellidos.data
        materia = frm_maestro.materia.data
        email = frm_maestro.email.data

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call actualizar_maestro(%s, %s, %s, %s, %s)', (id, nombre,apellidos, materia, email))
                connection.commit()
                connection.close()
                flash("Registro ATUALIZADO satisfactoriamente")
        except Exception as ex:
            flash("No fue posible actualizar el registro: " + str(ex))
        return redirect(url_for('maestros.obtener_maestros'))
    
    return render_template('updateMaestros.html', form = frm_maestro)

@maestros.route('/deleteMaestro', methods = ['GET'])
def delete_maestro():

    frm_maestro = forms.MaesForm(request.form)

    id = request.args.get('id')

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call eliminar_maestro(%s)', (id))
            connection.commit()
            connection.close()

            flash("Registro ELIMINADO satisfactoriamente")
    except Exception as ex:
        flash("No fue posible eliminar el registro: " + str(ex))
    return redirect(url_for('maestros.obtener_maestros', form = frm_maestro))

@maestros.route('/searchMaestro', methods = ['GET'])
def search_maestro():

    frm_maestros = forms.MaesForm(request.form)

    buscar = request.args.get('buscar')

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute('call buscar_maestro(%s)',(buscar,))
            resulset = cursor.fetchall()
            print(resulset)
            print(buscar)
            return render_template('maestros.html', form = frm_maestros, resulset = resulset)
    except Exception as ex:
        flash("No fue posible encotrar el registro: " + str(ex))