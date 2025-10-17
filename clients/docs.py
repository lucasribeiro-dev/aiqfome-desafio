from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from clients.serializers import ClientSerializer

client_docs = extend_schema_view(
    create=extend_schema(
        summary="Criar um novo usuário",
        description=(
            "Cria um novo usuário no sistema. "
            "Endpoint público."
        ),
        auth=[],
    ),
    list=extend_schema(
        summary="Listar todos os usuários",
        description=(
            "Retorna a lista completa de usuários. "
            "Apenas administradores têm acesso."
        ),
    ),
    retrieve=extend_schema(
        summary="Obter detalhes de um usuário",
        description=(
            "Obtém os dados do próprio usuário autenticado. "
            "Administradores podem visualizar outros usuários."
        ),
    ),
    partial_update=extend_schema(
        summary="Atualização parcial de dados do usuário",
        description=(
            "Atualiza parcialmente os dados do usuário autenticado, exceto o e-mail."
        ),
    ),
    destroy=extend_schema(
        summary="Excluir usuário",
        description=(
            "Remove a conta do usuário autenticado. "
            "Administradores podem excluir qualquer usuário."
        ),
    ),
)

me_docs = extend_schema(
    summary="Visualizar ou atualizar o próprio perfil",
    description=(
        "Permite que o usuário autenticado visualize ou atualize suas próprias informações de perfil.\n\n"
        "GET - retorna os dados do usuário autenticado.\n"
        "PATCH - atualiza campos parciais do perfil, como nome ou senha."
    ),
    request=ClientSerializer,
    responses={
        200: OpenApiResponse(
            response=ClientSerializer,
            description="Perfil atualizado ou retornado com sucesso.",
            examples=[
                OpenApiExample(
                    "Exemplo de resposta GET/PATCH",
                    value={
                        "id": 1,
                        "name": "Fulano ",
                        "email": "fulano@example.com",
                    },
                )
            ],
        ),
    },
)
