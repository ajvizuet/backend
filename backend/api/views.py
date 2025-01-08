from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
	    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'collection'

    def get(self, request):
        ref = db.reference(f'{self.collection_name}')

        data = ref.get()

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        ref = db.reference(f'{self.collection_name}')

        current_time = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format})

        new_resource = ref.push(request.data)

        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)