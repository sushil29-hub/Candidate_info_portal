from django.http import HttpResponse
from rest_framework import status

from rest_framework.views import APIView
from .serializer import CandiateInfoSerializer
from rest_framework.response import Response
from .services import CandidateInfoService


class CandidateView(APIView):

    def get(self, request):
        city = request.GET.get('city', None)
        tech_skills = request.GET.getlist('tech_skills')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))

        if page <= 0:
            return Response({"message": "page should be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        if per_page < 0:
            return Response({"message": "per_page should be greater than or epual to 0"}, status=status.HTTP_400_BAD_REQUEST)

        candidate_info = CandidateInfoService.filter_candidate_info(city, tech_skills, page, per_page)

        serializer = CandiateInfoSerializer(candidate_info, many=True)
        page_data = dict(
            page=page,
            per_page=per_page,
            count=candidate_info.count()
        )
        return Response({"page_data": page_data, "candidate_infos": serializer.data})

    def post(self, request):
        if isinstance(request.data, list):
            serializer = CandiateInfoSerializer(data=request.data, many=True)
        else:
            serializer = CandiateInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, candidate_info_id, *args, **kwargs):
        candidate_info = CandidateInfoService.get_candidate_info(candidate_info_id)
        if not candidate_info:
            return Response({"message": "CandidateInfo does not found for candidiate_info_id: {}".format(candidate_info_id)},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CandiateInfoSerializer(data=request.data, instance=candidate_info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GETResumeFile(APIView):

    def get(self, request, candidate_info_id):
        candidate_info = CandidateInfoService.get_candidate_info(candidate_info_id)
        try:
            file = CandidateInfoService.get_candidate_resume("candidate-resumes", candidate_info.resume_url)

            response = HttpResponse(file)
            response['Content-Disposition'] = "attachment; filename={}".format(candidate_info.resume_url)
            response['mimetype'] = "application/pdf"
            return response
        except Exception as e:
            return Response({"message": "Unable to fetch resume data Error: {}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)