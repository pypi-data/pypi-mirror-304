from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializer import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import OperationalError
from rest_framework.renderers import JSONRenderer
from rest_framework import status


class ContactFormView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny,]


class EmailSubcriptionView(generics.CreateAPIView):
    queryset = EmailSubcription.objects.all()
    serializer_class = EmailSubcriptionSerializer
    permission_classes = [AllowAny,]


class OurClientView(generics.ListAPIView):
    serializer_class = OurClientSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        query = OurClient.objects.all()
        return query


class ServiceView(APIView):
    permission_classes = [AllowAny,]
    # renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)
        except OperationalError:
            # Handle the exception or return an appropriate response
            return Response({"message": "An error occurred while accessing the database."}, status=500)


class ServiceDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [AllowAny,]


class TestimonialView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        testimonials = Testimonial.objects.all()
        serializer = TestimonialSerializer(testimonials, many=True)
        return Response(serializer.data)


class OurTeamView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        our_team = OurTeam.objects.all()
        serializer = OurTeamSerializer(our_team, many=True)
        return Response(serializer.data)


class CompanyInfoView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [AllowAny,]


class CoeValueView(generics.ListAPIView):
    serializer_class = CoreValueSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        query = CoreValue.objects.all()
        return query