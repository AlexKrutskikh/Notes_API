from django.shortcuts import render

class AddMessageView(APIView):

    def post(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        is_user = Profile.objects.get(user_id=user_id).is_user
        text = request.data.get('text')

        message = Message.objects.create(
            text=text,
            is_user=is_user,
            question_id=pk,
            user_id=user_id
        )

        files = request.FILES.getlist('files')
        for file in files:
            MessageFile.objects.create(message=message, file=file)

        serializer = MessageSerializer(message, context={'request': request})
        return JsonResponse(serializer.data, status=201)


class AllMessagesView(APIView):
    def get(self, request, pk):

        messages = Message.objects.filter(question_id=pk).order_by('created_at')
        serializer = MessageSerializer(messages, many=True, context={'request': request})

        return JsonResponse(serializer.data, safe=False, status=200)
