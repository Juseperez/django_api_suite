from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"

    def get(self, request):
        """
        Obtener todos los elementos de la colección desde Firebase Realtime Database
        """
        try:
            # Referencia a la colección
            ref = db.reference(self.collection_name)

            # Obtener todos los datos
            data = ref.get()

            # Si no hay datos, devolver una lista vacía
            if not data:
                return Response([], status=status.HTTP_200_OK)

            # Convertir diccionario a lista de objetos con su ID
            #result = [{"id": key, **value} for key, value in data.items()]

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Obtener datos del cuerpo de la solicitud
            data = request.data

            # Obtener referencia a la colección en Firebase
            ref = db.reference(self.collection_name)

            # Obtener fecha y hora actual del servidor
            now = datetime.now()

            
            # Formatear fecha con notación española y minúsculas
            timestamp = now.strftime("%d/%m/%Y, %I:%M:%S %p").lower() \
                .replace("am", "a. m.") \
                .replace("pm", "p. m.")

            # Añadir el timestamp al objeto recibido
            data["timestamp"] = timestamp

            # Guardar el objeto en Firebase con push
            new_ref = ref.push(data)

            # Devolver el ID generado y código 201 Created
            return Response({"id": new_ref.key}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)