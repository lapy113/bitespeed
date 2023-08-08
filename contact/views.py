from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contact.serializers import ContactSerializer
from .models import Contact
from django.db.models import Q
from datetime import datetime, timezone

# Create your views here.
class ContactView(APIView):
    def create_new(self,request, link_precedence = "primary",linkedId = None):
        
        
        serializer = ContactSerializer(data=request.data)
        serializer.initial_data['linkPrecedence'] = link_precedence
        serializer.initial_data['linkedId'] = linkedId
        if serializer.is_valid():
            serializer.save()
            return 1
        return -1
    
    def find_entries(self,request,link_precedence = "primary"):
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')
    
        if not email and not phone_number:
            return None,0
        
        # for searching primary records only
        if link_precedence == "all":
            if not email :
                queryset = Contact.objects.filter((Q(phoneNumber=phone_number)) )
                return queryset,1 
            if not phone_number :
                queryset = Contact.objects.filter((Q(email=email)) )
                return queryset,1
            queryset = Contact.objects.filter((Q(email=email) | Q(phoneNumber=phone_number)))
            return queryset,1
        
        # for seacching all records
        if link_precedence == "primary":
            if not email :
                queryset = Contact.objects.filter((Q(phoneNumber=phone_number)) & Q(linkPrecedence=link_precedence))
                return queryset,1 
            if not phone_number :
                queryset = Contact.objects.filter((Q(email=email)) & Q(linkPrecedence=link_precedence))
                return queryset,1
            queryset = Contact.objects.filter((Q(email=email) | Q(phoneNumber=phone_number)) & Q(linkPrecedence=link_precedence))
            return queryset,1
        # for searching duplicate in secondary
        
        if link_precedence == "secondary":
            queryset = Contact.objects.filter((Q(email=email) | Q(phoneNumber=phone_number)) & Q(linkPrecedence=link_precedence))
            return queryset,1
        
        
        
    
    def result(self,request):
        queryset,status = self.find_entries(request,"all")
        primary_id = None
        emails = []
        phone_numbers = []
        secondary_ids = []
        
        for i in range(len(queryset)):
            if queryset[i].linkPrecedence == "primary":
               primary_id = queryset[i].id
               emails.insert(0,queryset[i].email)
               phone_numbers.insert(0,queryset[i].phoneNumber)
            else :
               emails.append(queryset[i].email)
               phone_numbers.append(queryset[i].phoneNumber)
               secondary_ids.append(queryset[i].id)
               
        data = {
            "contact":{
                "primaryContatctId": primary_id,
                "emails": emails,
                "phoneNumbers": phone_numbers,
                "secondaryContactIds": secondary_ids
            }
        }
        
        return Response(data, status=200)
    
    def post(self,request):
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')
        
        queryset,status = self.find_entries(request)
        #error handling for missing email and phonenumber
        if status == 0:
            return Response({"error": "Please provide an email or phone number."}, status=400)
        
        count = queryset.count()
        # The record is missing in db, create a new one
        if count == 0:
            # create a new entry for contact
            create_res = self.create_new(request)
            if create_res == 1:
            # After creating return the response
                return self.result(request)
                
            if create_res == -1:
                return Response("Invalid Email")

        if count == 1:
            #TODO handle case if the email/phone is missing in primary
            # means, there is a matching single primary record for query
            email_ = queryset[0].email
            phone_number_ = queryset[0].phoneNumber
            linked_id_ = queryset[0].id
            
            #if email is none or phone is none or both match just show response
            if not email or not phone_number or (email==email_ and phone_number==phone_number_):
                return self.result(request)
            # Create Seconday contact
            #check for duplicate secondary contact
            queryset,status = self.find_entries(request,"secondary")
            count = queryset.count()
            if count == 0:
                create_res = self.create_new(request,"secondary",linked_id_)
                if create_res == 1:
                # After create return the reponse
                    return self.result(request)
                    
                if create_res == -1:
                    return Response("Invalid Email")
            return self.result(request)
        
        if count == 2:

            id_1 = queryset[0].id
            createdAt_1 = queryset[0].createdAt
           
            cur_time =datetime.now(timezone.utc)
            
            id_2 = queryset[1].id
            createdAt_2 = queryset[0].createdAt
            
            if createdAt_1 < createdAt_2:
                Contact.objects.filter(id=id_2).update(linkedId = id_1,updatedAt = cur_time,linkPrecedence = "secondary")
            else :
                Contact.objects.filter(id=id_1).update(linkedId = id_2,updatedAt = cur_time,linkPrecedence = "secondary")
            return self.result(request)
        #default
        return self.result(request)