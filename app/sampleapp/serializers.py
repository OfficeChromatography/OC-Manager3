from rest_framework import serializers
from .models import *
from finecontrol.serializers import *


class BandComponentsSerializer(serializers.ModelSerializer):
    id_band_component = serializers.IntegerField(read_only=True)
    sample_application = serializers.PrimaryKeyRelatedField(many=False,
                                                            read_only=False,
                                                            queryset=SampleApplication_Db.objects.all())

    class Meta:
        model = BandsComponents_Db
        fields = ['id_band_component', 'sample_application']


class BandSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandSettings_Db
        exclude = ('id',)


class ApplicationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationSettings_Db
        exclude = ('id',)


class StepSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepSettings_Db
        exclude = ('id',)

class SampleAppSerializer(serializers.ModelSerializer):
    zero_position = ZeroPositionSerializer(many=False, read_only=False)
    offset = OffsetSerializer(many=False, read_only=False)
    plate_size = PlateSizesSerializer(many=False, read_only=False)
    band_settings = BandSettingsSerializer(many=False, read_only=False)
    application_settings = ApplicationSettingsSerializer(many=False,
                                                         read_only=False)
    step_settings = StepSettingsSerializer(many=False, read_only=False)
    band_components = BandComponentsSerializer(many=True, read_only=False)

    class Meta:
        model = SampleApplication_Db
        fields = ['id', 'filename', 'method', 'offset', 'plate_size',
                  'zero_position', 'step_settings', 'band_settings',
                  'application_settings', 'band_components']

    def create(self, validated_data):
        print(validated_data)
        validated_data['zero_position'] = ZeroPosition_Db.objects.create(
            **validated_data['zero_position'])
        validated_data['plate_size'] = PlateSizeSettings_Db.objects.create(
            **validated_data['plate_size'])
        validated_data['offset'] = OffsetSettings_Db.objects.create(
            **validated_data['offset'])
        validated_data['band_settings'] = BandSettings_Db.objects.create(
            **validated_data['band_settings'])
        validated_data[
            'application_settings'] = ApplicationSettings_Db.objects.create(
            **validated_data['application_settings'])
        validated_data['step_settings'] = StepSettings_Db.objects.create(
            **validated_data['step_settings'])

        band_components=validated_data.pop('band_components')

        print(f"VALIDATED_DATA: {validated_data}")
        print(band_components)
        sample = SampleApplication_Db.objects.create(**validated_data)

#         band_components_serializer = BandComponentsSerializer(data=band_components, many=True)
#         if band_components_serializer.is_valid():
#             print('valido')
#         else:
#             print('no valido')
#             print(band_components_serializer.errors)


        return sample

    def update(self, instance, validated_data):
        instance.zero_position.__dict__.update(
            **validated_data.pop('zero_position', instance.zero_position))
        instance.zero_position.save()

        instance.plate_size.__dict__.update(
            **validated_data.pop('plate_size', instance.plate_size))
        instance.plate_size.save()

        instance.offset.__dict__.update(
            **validated_data.pop('offset', instance.offset))
        instance.offset.save()

        instance.band_settings.__dict__.update(
            **validated_data.pop('band_settings', instance.band_settings))
        instance.band_settings.save()

        instance.application_settings.__dict__.update(
            **validated_data.pop('application_settings',
                                 instance.application_settings))
        instance.application_settings.save()

        instance.step_settings.__dict__.update(
            **validated_data.pop('step_settings', instance.step_settings))
        instance.step_settings.save()

        instance.method = validated_data.pop('method', instance.method)
        instance.filename = validated_data.pop('filename', instance.filename)
        instance.save()
        return instance
