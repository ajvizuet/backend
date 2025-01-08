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
    
class LandingAPIDetail(APIView):
    name = 'Landing Detail API'

    collection_name = 'collection'

    def get(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')

        item = ref.get()
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response("Item not found", status.HTTP_404_NOT_FOUND)

    
    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')

        if request.data:
            current_time = datetime.now()
            custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
            request.data.update({"saved": custom_format})

            if ref.get():
                update = ref.update(request.data)

                return Response("Item updated", status=status.HTTP_200_OK)
            else:
                return Response("Item not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Missing data", status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')

        if ref.get():
            ref.delete()
            return Response("Item deleted", status=status.HTTP_204_NO_CONTENT)

        return Response("Item not found", status=status.HTTP_404_NOT_FOUND)