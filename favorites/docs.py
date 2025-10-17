from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)
from favorites.serializers import FavoriteSerializer

favorite_docs = extend_schema_view(
    create=extend_schema(
        summary="Adicionar produto aos favoritos",
        description=(
            "Adiciona um produto à lista de favoritos do usuário autenticado.\n\n"
            "**Requer autenticação.** O campo `product_id` deve ser informado no corpo da requisição."
        ),
        request=FavoriteSerializer,
        responses={
            201: OpenApiResponse(
                response=FavoriteSerializer,
                description="Produto adicionado com sucesso aos favoritos.",
                examples=[
                    OpenApiExample(
                        "Exemplo de resposta bem-sucedida",
                        value={
                            "id": 1,
                            "product_id": 123,
                            "product_snapshot": {"title": "Produto Exemplo", "price": 99.90, "description": "Descrição exemplo"},
                            "created_at": "2025-10-17T05:30:00Z"
                        },
                    )
                ],
            ),
            404: OpenApiResponse(
                description="Produto não encontrado.",
                examples=[
                    OpenApiExample(
                        "Produto não encontrado",
                        value={"error": "Produto não encontrado."},
                    )
                ],
            ),
        },
    ),

    list=extend_schema(
        summary="Listar produtos favoritos",
        description="Retorna todos os produtos marcados como favoritos pelo usuário autenticado.\n\n**Requer autenticação.**",
        responses={200: OpenApiResponse(response=FavoriteSerializer(many=True))},
    ),

    retrieve=extend_schema(
        summary="Obter favorito específico",
        description="Obtém os detalhes de um produto favorito específico com base no seu ID (`pk`).\n\n**Requer autenticação.**",
        parameters=[
            OpenApiParameter(name='pk', description='ID do favorito', required=True, type=int, location=OpenApiParameter.PATH),
        ],
        responses={
            200: OpenApiResponse(response=FavoriteSerializer),
            404: OpenApiResponse(description="Favorito não encontrado."),
        },
    ),

    destroy=extend_schema(
        summary="Remover produto dos favoritos",
        description="Remove um produto específico da lista de favoritos com base no ID (`pk`).\n\n**Requer autenticação.**",
        parameters=[
            OpenApiParameter(name='pk', description='ID do favorito', required=True, type=int, location=OpenApiParameter.PATH),
        ],
        responses={
            204: OpenApiResponse(description="Favorito removido com sucesso."),
            404: OpenApiResponse(description="Favorito não encontrado."),
        },
    ),
)
