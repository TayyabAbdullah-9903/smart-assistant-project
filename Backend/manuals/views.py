from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import Manual
from .serializers import ManualSerializer
from parser.service import parse_manual_file

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_manual(request):
    file = request.FILES.get("file")
    uploaded_by_type = request.data.get("uploaded_by_type","user")
    if not file:
        return Response({"error":"file required"}, status=400)
    manual = Manual.objects.create(file=file, filename=file.name, uploaded_by_type=uploaded_by_type)
    
    parse_manual_file(manual)
    serializer = ManualSerializer(manual)
    return Response(serializer.data, status=201)
