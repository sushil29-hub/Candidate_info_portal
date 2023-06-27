from .models import CandidateInfo
from rest_framework import serializers
from .services import CandidateInfoService

class CandiateInfoSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        candidate_info = super(CandiateInfoSerializer, self).create(validated_data)

        pdf_key = None
        # Generate Candidate Resume and storing to S3
        try:
            template_args, pdf_key = CandidateInfoService.get_template_args_resume_data(candidate_info)
            CandidateInfoService.generate_pdf_resume(template_args, pdf_key)
        except:
            pass

        candidate_info.resume_url = pdf_key
        candidate_info.save()

        return candidate_info

    class Meta:
        model = CandidateInfo
        fields = "__all__"