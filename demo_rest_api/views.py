from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):
      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    """
    GET: Obtiene un elemento por ID.
    PUT: Reemplaza completamente un elemento (menos el ID).
    PATCH: Actualiza parcialmente un elemento por ID.
    DELETE: Inactiva (elimina lógicamente) un elemento por ID.
    """

    def find_item_by_id(self, item_id):
        return next((item for item in data_list if item['id'] == item_id), None)

    def get(self, request, id):
        item = self.find_item_by_id(id)
        if not item:
            return Response({'message': f'Elemento con id {id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Elemento encontrado.', 'data': item}, status=status.HTTP_200_OK)

    def put(self, request, id):
        item = self.find_item_by_id(id)
        if not item:
            return Response({'message': f'Elemento con id {id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'message': 'Faltan campos requeridos: "name" y "email".'}, status=status.HTTP_400_BAD_REQUEST)

        item.update({
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True)
        })

        return Response({'message': 'Elemento actualizado completamente.', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, id):
        item = self.find_item_by_id(id)
        if not item:
            return Response({'message': f'Elemento con id {id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        campos_actualizados = []

        for field in ['name', 'email', 'is_active']:
            if field in data:
                item[field] = data[field]
                campos_actualizados.append(field)

        if not campos_actualizados:
            return Response({'message': 'No se proporcionaron campos válidos para actualizar.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f'Campos actualizados: {", ".join(campos_actualizados)}.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        item = self.find_item_by_id(id)
        if not item:
            return Response({'message': f'Elemento con id {id} no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not item.get('is_active', True):
            return Response({'message': 'El elemento ya estaba inactivo.'}, status=status.HTTP_200_OK)

        item['is_active'] = False
        return Response({'message': f'Elemento con id {id} eliminado lógicamente.'}, status=status.HTTP_200_OK)