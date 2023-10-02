from rest_framework import serializers
from .models import Announcement,Reaction
from user.serializers import UserSerializer
from academic.models import Course
from academic.serializers import CourseSerializer

class AnnouncementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    owner = UserSerializer()
    like_count = serializers.IntegerField(default = 0)
    dislike_count = serializers.IntegerField(default=0)
    user_reaction = serializers.ChoiceField(Reaction.Type,allow_null=True)
    is_saved = serializers.BooleanField(default=False)
    image = serializers.ImageField(allow_null = True)
    course = CourseSerializer()
    created_at = serializers.DateTimeField()


    

    
class CreateAnnouncmentSerilizer(serializers.Serializer):
    text = serializers.CharField(min_length = 20,max_length = 1000)
    image = serializers.ImageField(allow_null = True)
    course_code = serializers.CharField()

    # def validate_image(self,image):
    #     if image == None:
    #         return;
    #     max_size = 10 * 1024 * 1024
    #     if image.size > max_size:
    #         raise serializers.ValidationError(f"Max file size allowed is {max_size} bytes.")
        
    def save(self,user):
        text = self.validated_data.get("text")
        image = self.validated_data.get("image")
        course_code = self.validated_data.get("course_code")
        course = Course.objects.get(code = course_code)
        announcement = user.announcement_set.create(course = course, text = text, image = image)
        print(announcement.image)
        return announcement

