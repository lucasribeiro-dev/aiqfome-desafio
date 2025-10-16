from rest_framework.views import APIView
from rest_framework.response import Response

class VersionView(APIView):
    schema = None
    def get(self, request):
        return Response({
            "api_version": "v1.0",
            "docs_url": "/api/schema/swagger-ui/",
            "status": "running"
        })
