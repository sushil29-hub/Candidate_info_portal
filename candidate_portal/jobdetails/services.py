from functools import reduce
from django.db.models import Q
import jinja2

from jobdetails import s3_connection
from .models import CandidateInfo


class CandidateInfoService:

    @staticmethod
    def filter_candidate_info(city=None, tech_skills=None, page=1, per_page=10):
        candidate_info = CandidateInfo.objects
        if city:
            candidate_info = candidate_info.filter(city=city)

        if tech_skills:
            tech_skill_query = reduce(lambda x, y: x | y, [Q(tech_skills__icontains=tech_skill) for tech_skill in tech_skills])
            candidate_info = candidate_info.filter(tech_skill_query)

        return candidate_info.all()[(page-1)*per_page: (page-1)*per_page + per_page]

    @staticmethod
    def get_candidate_info(candidate_id):
        if not candidate_id:
            return None
        try:
            return CandidateInfo.objects.get(id=candidate_id)
        except:
            return None

    @staticmethod
    def get_template_args_resume_data(candidate_data):
        template_args = dict(
            name=candidate_data.name,
            number=candidate_data.number,
            city=candidate_data.city,
            email=candidate_data.email,
            address=candidate_data.address,
            tech_skills=candidate_data.tech_skills
        )
        pdf_key = '{}/{}.pdf'.format(candidate_data.id, candidate_data.name)
        return template_args, pdf_key

    @staticmethod
    def generate_pdf_resume(template_args, pdf_key):
        loader = jinja2.FileSystemLoader(searchpath="./")
        jenv = jinja2.Environment(loader=loader)
        template = jenv.get_template('jobdetails/templates/resume.html')
        html = template.render(data=template_args)

        #Need to convert HTML to PDF content before put S3 object

        s3_connection.client('s3').put_object(Body=html, ContentType='application/pdf',
                                 Bucket='candidate-resumes', Key=pdf_key)

    @staticmethod
    def get_candidate_resume(bucket, key):
        s3 = s3_connection.resource('s3')
        obj = s3.Object(bucket, key)
        return obj.get()['Body'].read()