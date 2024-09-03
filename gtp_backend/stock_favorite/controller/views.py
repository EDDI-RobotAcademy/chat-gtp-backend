from rest_framework import viewsets, status
from rest_framework.response import Response
from stock_favorite.service.stock_favorite_service_impl import FavoriteStocksServiceImpl
from django.http import JsonResponse

class FavoriteStocksView(viewsets.ViewSet):
    favoriteStocksService = FavoriteStocksServiceImpl.getInstance()


    def addFavorite(self, request):
        try:
            email = request.data.get('email')
            ticker = request.data.get('ticker')

            if email is None or ticker is None:
                return Response({'error': 'Email and Ticker are required'}, status=status.HTTP_400_BAD_REQUEST)

            favorite = self.favoriteStocksService.addFavorite(email, ticker)
            return Response({'status': 'success', 'favorite': favorite.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def getFavorites(self, request):
        try:
            data = request.data
            userToken = data.get('userToken')
            accountId = self.redisService.getValueByKey(userToken)

            if not accountId:
                raise ValueError('Invalid User Token')

            favorites = self.favoriteStocksService.getFavorites(accountId)
            return Response(favorites.values(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_favorite_stocks(self, request):
        email = request.data.get('email')
        print("email: ", email)
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        favorite_stocks = self.favoriteStocksService.get_favorite_stocks(email)
        print("Favorite stocks: ", favorite_stocks)
        return JsonResponse({'stocks': favorite_stocks})


    def removeFavorite(self, request):
        try:
            email = request.data.get('email')
            ticker = request.data.get('ticker')

            if email is None or ticker is None:
                return Response({'error': 'Email and Ticker are required'}, status=status.HTTP_400_BAD_REQUEST)

            self.favoriteStocksService.removeFavorite(email, ticker)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)