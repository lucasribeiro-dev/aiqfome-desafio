from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework import status

@extend_schema(
    summary="Health Check",
    description="Verifica se o servidor está em execução e responde com status OK.",
    responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}},
)
class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
