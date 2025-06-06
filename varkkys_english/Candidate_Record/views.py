from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Candidate,CandidateAudioRecord,VlmModel
from .serializers import CandidateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)  # Checks hashed password

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_candidates(request):
    user = request.user
    if user.is_superuser:
        candidates = Candidate.objects.all()
    else:
        candidates = Candidate.objects.filter(assigned_to=user)

    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # for form-data with files
def candidate_detail(request, phone):
    try:
        candidate = Candidate.objects.get(phone=phone)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if not user.is_superuser and candidate.assigned_to != user:
        return Response({'error': 'Unauthorized Access'}, status=status.HTTP_403_FORBIDDEN)

    # Handle audio file uploads
    audio_files = request.FILES.getlist('audio_record')

    for audio_file in audio_files:
        if CandidateAudioRecord.objects.filter(candidate=candidate, original_filename=audio_file.name).exists():
            continue  # skip duplicate by original filename

        CandidateAudioRecord.objects.create(
            candidate=candidate,
            audio_file=audio_file,
            original_filename=audio_file.name
        )

    # Update candidate fields
    serializer = CandidateSerializer(candidate, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_version(request):
    token_version = request.query_params.get('version_no')

    if not token_version:
        return Response({'status': 'fail', 'message': 'No version provided'}, status=400)

    try:
        token_version = int(token_version)
    except ValueError:
        return Response({'status': 'fail', 'message': 'Invalid version format'}, status=400)

    # Get latest version by updated_at
    latest = VlmModel.objects.order_by('-updated_at').first()

    if not latest:
        return Response({'status': 'fail', 'message': 'No version in backend'}, status=500)

    if token_version == latest.version_no:
        return Response({'status': 'success', 'match': True})
    else:
        return Response({'status': 'fail', 'match': False, 'latest_version': latest.version_no})

# @api_view(['PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def candidate_update(request, phone):
#     try:
#         candidate = Candidate.objects.get(phone=phone)
#     except Candidate.DoesNotExist:
#         return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     serializer = CandidateSerializer(candidate, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def upload_audio_record(request, phone):
#     try:
#         candidate = Candidate.objects.get(phone=phone)
#     except Candidate.DoesNotExist:
#         return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
#     if not request.FILES.get('audio_file'):
#         return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)
#
#     audio_record = CandidateAudioRecord(candidate=candidate, audio_file=request.FILES['audio_file'])
#     audio_record.save()
#
#     return Response({'message': 'Audio uploaded successfully'}, status=status.HTTP_201_CREATED)

