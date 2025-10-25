from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from models import db, Region, Comuna, AvisoAdopcion, Foto, ContactarPor, Comentario
from config import Config
from utils.validations import *
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Portada con los últimos 5 avisos"""
    ultimos_avisos = AvisoAdopcion.query.order_by(
        AvisoAdopcion.fecha_ingreso.desc()
    ).limit(5).all()
    return render_template('index.html', avisos=ultimos_avisos)

@app.route('/agregar-aviso')
def agregar_aviso():
    """Muestra formulario de agregar aviso"""
    return render_template('agregar-aviso.html')

@app.route('/api/regiones')
def get_regiones():
    """API para obtener regiones"""
    regiones = Region.query.all()
    return jsonify([{'id': r.id, 'nombre': r.nombre} for r in regiones])

@app.route('/api/comunas/<int:region_id>')
def get_comunas(region_id):
    """API para obtener comunas de una región"""
    comunas = Comuna.query.filter_by(region_id=region_id).all()
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])

@app.route('/agregar-aviso', methods=['POST'])
def procesar_aviso():
    """Procesa el formulario de agregar aviso con validaciones del lado del servidor"""
    errores = {}
    
    # Validar región
    region_id = request.form.get('region', '').strip()
    if not region_id:
        errores['region'] = "Debe seleccionar una región"
    else:
        try:
            region_id = int(region_id)
            region = Region.query.get(region_id)
            if not region:
                errores['region'] = "La región seleccionada no es válida"
        except (ValueError, TypeError):
            errores['region'] = "ID de región inválido"
    
    # Validar comuna (debe pertenecer a la región)
    comuna_id = request.form.get('comuna', '').strip()
    if not comuna_id:
        errores['comuna'] = "Debe seleccionar una comuna"
    else:
        try:
            comuna_id = int(comuna_id)
            comuna = Comuna.query.get(comuna_id)
            if not comuna:
                errores['comuna'] = "La comuna seleccionada no es válida"
            elif 'region' not in errores and comuna.region_id != region_id:
                errores['comuna'] = "La comuna no pertenece a la región seleccionada"
        except (ValueError, TypeError):
            errores['comuna'] = "ID de comuna inválido"
    
    # Validar sector (opcional)
    sector = request.form.get('sector', '').strip()
    if sector and len(sector) > 100:
        errores['sector'] = "El sector no puede tener más de 100 caracteres"
    if sector and ('<' in sector or '>' in sector):
        errores['sector'] = "El sector contiene caracteres no permitidos"
    
    # Validar nombre
    nombre = request.form.get('nombre', '').strip()
    valid, error = validar_nombre(nombre)
    if not valid:
        errores['nombre'] = error
    elif '<' in nombre or '>' in nombre:
        errores['nombre'] = "El nombre contiene caracteres no permitidos"
    
    # Validar email
    email = request.form.get('email', '').strip()
    valid, error = validar_email(email)
    if not valid:
        errores['email'] = error
    
    # Validar celular (opcional)
    celular = request.form.get('celular', '').strip()
    valid, error = validar_celular(celular)
    if not valid:
        errores['celular'] = error
    
    # Validar contactar por (si se proporciona, el identificador es obligatorio)
    contactar_por = request.form.get('contactar-por', '').strip()
    contacto_info = request.form.get('contacto-info', '').strip()
    
    if contactar_por:
        valores_validos = ['whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra']
        if contactar_por not in valores_validos:
            errores['contactar-por'] = "Opción de contacto no válida"
        
        if not contacto_info:
            errores['contacto-info'] = "Debe ingresar el identificador de contacto"
        elif len(contacto_info) < 4:
            errores['contacto-info'] = "El identificador debe tener al menos 4 caracteres"
        elif len(contacto_info) > 150:
            errores['contacto-info'] = "El identificador no puede tener más de 150 caracteres"
        elif '<' in contacto_info or '>' in contacto_info:
            errores['contacto-info'] = "El identificador contiene caracteres no permitidos"
    elif contacto_info:
        errores['contactar-por'] = "Debe seleccionar una opción de contacto"
    
    # Validar tipo de mascota
    tipo = request.form.get('tipo', '').strip()
    if not tipo:
        errores['tipo'] = "Debe seleccionar el tipo de mascota"
    elif tipo not in ['gato', 'perro']:
        errores['tipo'] = "El tipo de mascota no es válido"
    
    # Validar cantidad
    cantidad = request.form.get('cantidad', '').strip()
    if not cantidad:
        errores['cantidad'] = "La cantidad es obligatoria"
    else:
        try:
            cantidad = int(cantidad)
            if cantidad < 1:
                errores['cantidad'] = "La cantidad debe ser al menos 1"
            elif cantidad > 99:
                errores['cantidad'] = "La cantidad no puede ser mayor a 99"
        except (ValueError, TypeError):
            errores['cantidad'] = "La cantidad debe ser un número válido"
    
    # Validar edad
    edad = request.form.get('edad', '').strip()
    if not edad:
        errores['edad'] = "La edad es obligatoria"
    else:
        try:
            edad = int(edad)
            if edad < 1:
                errores['edad'] = "La edad debe ser al menos 1"
            elif edad > 100:
                errores['edad'] = "La edad es demasiado alta"
        except (ValueError, TypeError):
            errores['edad'] = "La edad debe ser un número válido"
    
    # Validar unidad de medida
    unidad_edad = request.form.get('unidad-edad', '').strip()
    if not unidad_edad:
        errores['unidad-edad'] = "Debe seleccionar la unidad de medida"
    elif unidad_edad not in ['meses', 'anos']:
        errores['unidad-edad'] = "La unidad de medida no es válida"
    
    # Validar fecha de entrega (debe ser futura)
    fecha_entrega_str = request.form.get('fecha-entrega', '').strip()
    if not fecha_entrega_str:
        errores['fecha-entrega'] = "La fecha de entrega es obligatoria"
    else:
        valid, error = validar_fecha_entrega(fecha_entrega_str)
        if not valid:
            errores['fecha-entrega'] = error
        else:
            try:
                fecha_entrega = datetime.fromisoformat(fecha_entrega_str)
            except:
                errores['fecha-entrega'] = "Formato de fecha inválido"
    
    # Validar descripción (opcional)
    descripcion = request.form.get('descripcion', '').strip()
    if descripcion:
        if len(descripcion) > 500:
            errores['descripcion'] = "La descripción no puede tener más de 500 caracteres"
        if '<script' in descripcion.lower() or '<iframe' in descripcion.lower():
            errores['descripcion'] = "La descripción contiene contenido no permitido"
    
    # Validar fotos (mínimo 1, máximo 5)
    fotos = request.files.getlist('foto')
    fotos_validas = []
    fotos_con_contenido = [f for f in fotos if f and f.filename]
    
    if len(fotos_con_contenido) < 1:
        errores['fotos'] = "Debe subir al menos 1 foto"
    elif len(fotos_con_contenido) > 5:
        errores['fotos'] = "No puede subir más de 5 fotos"
    else:
        for i, foto in enumerate(fotos_con_contenido):
            valid, error = validar_archivo(foto)
            if not valid:
                errores[f'foto-{i}'] = f"Foto {i+1}: {error}"
            else:
                foto.seek(0, 2)
                tamaño = foto.tell()
                foto.seek(0)
                
                if tamaño > 5 * 1024 * 1024:
                    errores[f'foto-{i}'] = f"Foto {i+1}: El archivo es muy grande (máximo 5MB)"
                else:
                    fotos_validas.append(foto)
        
        if any(key.startswith('foto-') for key in errores):
            errores['fotos'] = "Hay errores en las fotos subidas"
    
    # Si hay errores, devolver al formulario
    if errores:
        return render_template('agregar-aviso.html', 
                             errores=errores, 
                             form_data=request.form)
    
    # Guardar en la base de datos
    try:
        nuevo_aviso = AvisoAdopcion(
            comuna_id=comuna_id,
            sector=sector if sector else None,
            nombre=nombre,
            email=email,
            celular=celular if celular else None,
            tipo=tipo,
            cantidad=cantidad,
            edad=edad,
            unidad_medida='a' if unidad_edad == 'anos' else 'm',
            fecha_entrega=fecha_entrega,
            descripcion=descripcion if descripcion else None,
            fecha_ingreso=datetime.now()
        )
        
        db.session.add(nuevo_aviso)
        db.session.flush()
        
        # Guardar fotos
        for foto in fotos_validas:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_original = secure_filename(foto.filename)
            filename = f"{nuevo_aviso.id}_{timestamp}_{filename_original}"
            ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            foto.save(ruta_completa)
            
            nueva_foto = Foto(
                ruta_archivo=f"uploads/{filename}",
                nombre_archivo=filename,
                actividad_id=nuevo_aviso.id
            )
            db.session.add(nueva_foto)
        
        # Guardar contacto adicional (opcional)
        if contactar_por and contacto_info:
            contacto = ContactarPor(
                nombre=contactar_por,
                identificador=contacto_info,
                actividad_id=nuevo_aviso.id
            )
            db.session.add(contacto)
        
        db.session.commit()
        flash('¡Aviso de adopción agregado exitosamente!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar el aviso: {str(e)}', 'error')
        return render_template('agregar-aviso.html', 
                             form_data=request.form,
                             errores={'general': 'Hubo un error al procesar el formulario. Intente nuevamente.'})

@app.route('/ver-listado')
def ver_listado():
    """Muestra listado de avisos con paginación"""
    page = request.args.get('page', 1, type=int)
    avisos_paginados = AvisoAdopcion.query.order_by(
        AvisoAdopcion.fecha_ingreso.desc()
    ).paginate(page=page, per_page=15, error_out=False)
    
    return render_template('ver-listado.html', 
                         avisos=avisos_paginados.items,
                         pagination=avisos_paginados)

@app.route('/api/aviso/<int:aviso_id>')
def get_aviso_detalle(aviso_id):
    """API para obtener detalles de un aviso"""
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    return jsonify({
        'id': aviso.id,
        'nombre': aviso.nombre,
        'email': aviso.email,
        'celular': aviso.celular,
        'tipo': aviso.tipo,
        'cantidad': aviso.cantidad,
        'edad': aviso.edad,
        'unidad_medida': aviso.unidad_medida,
        'descripcion': aviso.descripcion,
        'comuna': aviso.comuna.nombre,
        'region': aviso.comuna.region.nombre,
        'sector': aviso.sector,
        'fecha_entrega': aviso.fecha_entrega.isoformat(),
        'fotos': [{'ruta_archivo': f.ruta_archivo, 'nombre_archivo': f.nombre_archivo} for f in aviso.fotos],
        'contactos': [{'tipo': c.nombre, 'id': c.identificador} for c in aviso.contactos]
    })

@app.route('/api/aviso/<int:aviso_id>/comentario', methods=['POST'])
def agregar_comentario(aviso_id):
    """API para agregar un comentario a un aviso"""
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        texto = data.get('texto', '').strip()
        
        errores = {}
        
        if not nombre:
            errores['nombre'] = 'El nombre es obligatorio'
        elif len(nombre) < 3:
            errores['nombre'] = 'El nombre debe tener al menos 3 caracteres'
        elif len(nombre) > 80:
            errores['nombre'] = 'El nombre no puede superar 80 caracteres'
        
        if not texto:
            errores['texto'] = 'El comentario es obligatorio'
        elif len(texto) < 5:
            errores['texto'] = 'El comentario debe tener al menos 5 caracteres'
        
        aviso = AvisoAdopcion.query.get(aviso_id)
        if not aviso:
            return jsonify({'success': False, 'error': 'Aviso no encontrado'}), 404
        
        if errores:
            return jsonify({'success': False, 'errores': errores}), 400
        
        nuevo_comentario = Comentario(
            nombre=nombre,
            texto=texto,
            fecha=datetime.now(),
            aviso_id=aviso_id
        )
        
        db.session.add(nuevo_comentario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'mensaje': 'Comentario agregado exitosamente',
            'comentario': {
                'id': nuevo_comentario.id,
                'nombre': nuevo_comentario.nombre,
                'texto': nuevo_comentario.texto,
                'fecha': nuevo_comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/aviso/<int:aviso_id>/comentarios', methods=['GET'])
def obtener_comentarios(aviso_id):
    """API para obtener todos los comentarios de un aviso"""
    try:
        aviso = AvisoAdopcion.query.get(aviso_id)
        if not aviso:
            return jsonify({'error': 'Aviso no encontrado'}), 404
        
        comentarios = Comentario.query.filter_by(aviso_id=aviso_id)\
                                       .order_by(Comentario.fecha.desc())\
                                       .all()
        
        comentarios_json = []
        for c in comentarios:
            comentarios_json.append({
                'id': c.id,
                'nombre': c.nombre,
                'texto': c.texto,
                'fecha': c.fecha.strftime('%d/%m/%Y %H:%M')
            })
        
        return jsonify(comentarios_json), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/aviso/<int:aviso_id>')
def ver_aviso(aviso_id):
    """Muestra el detalle completo de un aviso con comentarios"""
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    comuna = Comuna.query.get(aviso.comuna_id)
    region = Region.query.get(comuna.region_id) if comuna else None
    
    return render_template('ver-aviso.html', 
                          aviso=aviso, 
                          comuna=comuna, 
                          region=region)

@app.route('/estadisticas')
def estadisticas():
    """Muestra la página de estadísticas con gráficos"""
    return render_template('estats.html')

@app.route('/api/estadisticas/avisos-por-dia')
def get_avisos_por_dia():
    """API que retorna cantidad de avisos agrupados por día"""
    from sqlalchemy import func
    
    try:
        resultados = db.session.query(
            func.date(AvisoAdopcion.fecha_ingreso).label('fecha'),
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(
            func.date(AvisoAdopcion.fecha_ingreso)
        ).order_by('fecha').all()
        
        datos = []
        for fecha, cantidad in resultados:
            datos.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'cantidad': cantidad
            })
        
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas/avisos-por-tipo')
def get_avisos_por_tipo():
    """API que retorna cantidad de avisos por tipo de mascota (gato/perro)"""
    from sqlalchemy import func
    
    try:
        resultados = db.session.query(
            AvisoAdopcion.tipo,
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(AvisoAdopcion.tipo).all()
        
        datos = []
        for tipo, cantidad in resultados:
            datos.append({
                'tipo': tipo,
                'cantidad': cantidad
            })
        
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas/avisos-por-mes-tipo')
def get_avisos_por_mes_tipo():
    """API que retorna avisos agrupados por mes y tipo de mascota"""
    from sqlalchemy import func
    
    try:
        avisos = AvisoAdopcion.query.all()
        datos_por_mes = {}
        
        for aviso in avisos:
            mes = aviso.fecha_ingreso.strftime('%Y-%m')
            
            if mes not in datos_por_mes:
                datos_por_mes[mes] = {'mes': mes, 'perros': 0, 'gatos': 0}
            
            if aviso.tipo == 'perro':
                datos_por_mes[mes]['perros'] += 1
            else:
                datos_por_mes[mes]['gatos'] += 1
        
        datos = sorted(datos_por_mes.values(), key=lambda x: x['mes'])
        
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
