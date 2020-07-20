from drf_writable_nested import WritableNestedModelSerializer
from crm.views.contractors.postformats.post_format_list_serializer import PostFormatListSerializer
from ...models import Contractor, PostFormatList
from ...library.validators import check_positive_numbers


class ContractorSerializer(WritableNestedModelSerializer):
    postformatlist_set = PostFormatListSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Contractor
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1

    def create(self, validated_data):
        new_contractor = self.__create_contractor(validated_data)
        new_contractor.save()
        return new_contractor

    def __create_contractor(self, validated_data):
        return Contractor.objects.create_contractor(**validated_data)
