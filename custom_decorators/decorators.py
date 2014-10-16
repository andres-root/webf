# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage
import json as simplejson
from django.http import HttpResponseNotAllowed,\
    HttpResponseForbidden, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import redirect

SIZE = getattr(settings, "OBJECTS_PAGE", 8)
DEBUG = getattr(settings, "DEBUG")
MAX_SIZE = getattr(settings, "MAX_OBJECTS_PAGE", 12)


def redirect_if_admin(func):
    """
    Redirecciona al menu del administrador si el usuario logeado es un administrador
    """
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.type is not None:
            return func(request, *args, **kwargs)
        elif request.user.is_authenticated():
            return redirect('admin:index')
        else:
            return func(request, *args, **kwargs)

    return decorator


def requires_ceelat_ally(func):
    """
    Redirecciona al menu del administrador si el usuario logeado es un administrador
    """
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated() and not request.user.is_ceelat_ally():
            return redirect('dashboard')
        else:
            return func(request, *args, **kwargs)
    return decorator


def requires_company_user(func):
    """
    Redirecciona al menu del administrador si el usuario logeado es un administrador
    """
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated() and not request.user.is_company_user():
            return redirect('dashboard')
        else:
            return func(request, *args, **kwargs)
    return decorator


def requires_entrepreneur(func):
    """
    Redirecciona al dashboard si el usuario logeado no es
    """
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated() and not request.user.is_entrepreneur():
            return redirect('dashboard')
        else:
            return func(request, *args, **kwargs)
    return decorator


def requires_post(func):
    """
    Retorna un error 405 si el request.method no es POST
    """
    def decorator(request, *args, **kwargs):
        if DEBUG or request.method == 'POST':
            return func(request, *args, **kwargs)
        return HttpResponseNotAllowed(['POST'])
    return decorator


def requires_get(func):
    """
    Retorna un error 405 si el request.method no es GET
    """
    def decorator(request, *args, **kwargs):
        if DEBUG or request.method == 'GET':
            return func(request, *args, **kwargs)
        return HttpResponseNotAllowed(['GET'])
    return decorator


def requires_login(func):
    """
    Retorna un error 403 si el usuario no esta logueado
    """
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        return HttpResponseForbidden()
    return decorator


def json_response(func):
    """
    Convierte la respuesta de la funcion en json usando
    la libreria simplejson.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = simplejson.dumps(objects)
            if 'callback' in request.GET:
                data = '%s(%s);' % (request.GET['callback'], data)
        except:
            data = simplejson.dumps(str(objects))
        if 'just_the_json_plz' in kwargs:
            return data
        if 'just_the_data_plz' in kwargs:
            return objects
        if 'callback' in request.GET or 'callback' in request.POST:
            #jsonp
            return HttpResponse(data, "text/javascript")
        else:
            #json
            return HttpResponse(data, "application/json")
    return decorator


def paginator(func):
    """
    Este metodo decora una funcion que retorne algo iterable
    y lo pagina por la variable POST page. Retorna la pagina,
    si no existe la variable page, retorna la primera pagina,
    el parametro paginate_by determina el numero de elementos por pagina.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        try:
            if request.method == "POST":
                page = int(request.POST['page'] or 1)
            else:
                page = int(request.GET['page'] or 1)
        except Exception:
            page = 1
        try:
            if request.method == "POST":
                size = int(request.POST['size'] or SIZE)
            else:
                size = int(request.GET['size'] or SIZE)
        except Exception:
            size = SIZE
        if size > MAX_SIZE:
            size = MAX_SIZE
        paginatorr = Paginator(objects, size, orphans=0, allow_empty_first_page=True)
        try:
            page_obj = paginatorr.page(page)
        except InvalidPage:
            raise Http404
        return page_obj
    return decorator


def paginated_for_json_response(func):
    """
    Este metodo decora una funcion que retorna, y utiliza el metodo
    to_json_dict para obtener el diccionario de cada objeto.
    El resultado del json va de la siguiente manera:
    {
        total_number:int,
        page_number:int,
        next:boolean,
        previous:boolean,
        objects:[object]
    }
    """
    def decorator(request, *args, **kwargs):
        page = func(request, *args, **kwargs)
        data = {}
        data['total_number'] = page.paginator.count
        data['page_number'] = page.number
        data['total_pages'] = page.paginator.num_pages
        data['next'] = page.has_next()
        data['previous'] = page.has_previous()
        objects = []
        for o in page.object_list:
            if hasattr(o, 'to_json_dict'):
                try:
                    objects.append(o.to_json_dict())
                except Exception, args:
                    pass
            else:
                try:
                    objects.append(o)
                except Exception, args:
                    pass
        if not objects:
            objects = serializers.serialize("python", [o for o in page.object_list])
        data['objects'] = objects
        return data
    return decorator


def paginated_search_for_json_response(func):
    """
    Este metodo decora una funcion que retorna, y utiliza el metodo
    to_json_dict para obtener el diccionario de cada objeto.
    El resultado del json va de la siguiente manera:
    {
        total_number:int,
        page_number:int,
        next:boolean,
        previous:boolean,
        objects:[object]
    }
    """
    def decorator(request, *args, **kwargs):
        page = func(request, *args, **kwargs)
        data = {}
        data['total_number'] = page.paginator.count
        data['page_number'] = page.number
        data['total_pages'] = page.paginator.num_pages
        data['next'] = page.has_next()
        data['previous'] = page.has_previous()
        try:
            data['objects'] = [(a.object.to_json_dict(request)) for a in page.object_list]
        except Exception, args:

            try:
                data['objects'] = [(a.object.to_json_dict()) for a in page.object_list]
            except Exception, args:
                data['objects'] = serializers.serialize("python", [a.object for a in page.object_list])
        return data
    return decorator


def paginated_json_response(func):
    """
    Combina los decoradores paginator, paginated_for_json_response y
    json_response para devolver una json de elementos iterables paginados.
    """
    @json_response
    @paginated_for_json_response
    @paginator
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        return objects
    return decorator


def paginated_search_json_response(func):
    """
    Combina los decoradores paginator, paginated_for_json_response y
    json_response para devolver una json de elementos iterables paginados.
    """
    @json_response
    @paginated_search_for_json_response
    @paginator
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        return objects
    return decorator


def http_var_required(parameter_name):
    """
    Verifica que exista el parametro post con nombre parameter_name
    y si no, retorna HttpResponseBadRequest
    """
    def wrap(func):
        def decorator(request, *args, **kwargs):
            if not (parameter_name in request.POST or parameter_name in request.GET):
                return HttpResponseBadRequest('Please define GET or POST parameter '+parameter_name)
            return func(request, *args, **kwargs)
        return decorator
    return wrap


def add_http_var(parameter_name, required=True):
    """
    Pasa la variable a la funcion, extrayendola del POST o GET,
    lanzando una excepcion si no existe esta y no ha sido explicitamente
    declarado opcional en True.
    """
    def wrap(func):
        def decorator(request, *args, **kwargs):
            if parameter_name in request.POST:
                kwargs[parameter_name] = request.POST[parameter_name]
            elif parameter_name in request.GET:
                kwargs[parameter_name] = request.GET[parameter_name]
            elif required:
                return HttpResponseBadRequest('Please define GET or POST parameter '+parameter_name)
            else:
                pass
            return func(request, *args, **kwargs)
        return decorator
    return wrap
