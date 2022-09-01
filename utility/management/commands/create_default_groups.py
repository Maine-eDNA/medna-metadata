from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
import logging

GROUPS = {
    'admin-permissions': {
        # general permissions
        'log entry': ['add', 'delete', 'change', 'view'],
        'email address': ['add', 'delete', 'change', 'view'],
        'email confirmation': ['add', 'delete', 'change', 'view'],
        'group': ['add', 'delete', 'change', 'view'],
        'permission': ['add', 'delete', 'change', 'view'],
        'Token': ['add', 'delete', 'change', 'view'],
        'token': ['add', 'delete', 'change', 'view'],
        'social account': ['add', 'delete', 'change', 'view'],
        'social application': ['add', 'delete', 'change', 'view'],
        'social application token': ['add', 'delete', 'change', 'view'],
        'user': ['add', 'delete', 'change', 'view'],
        'content type': ['add', 'delete', 'change', 'view'],
        'session': ['add', 'delete', 'change', 'view'],

        # django app model specific permissions
        # field_site
        'ENVO Biome 1st Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Biome 2nd Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Biome 3rd Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Biome 4th Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Biome 5th Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 1st Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 2nd Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 3rd Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 4th Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 5th Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 6th Tier': ['add', 'delete', 'change', 'view'],
        'ENVO Feature 7th Tier': ['add', 'delete', 'change', 'view'],
        'System': ['add', 'change', 'view'],
        'Watershed': ['change', 'view'],
        'Field Site': ['add', 'change', 'view'],
        'World Border': ['change', 'view'],

        # sample_label
        'Sample Type': ['add', 'change', 'view'],
        'SampleLabelRequest': ['add', 'change', 'view'],
        'SampleBarcode': ['view'],

        # utility
        'Fund': ['add', 'change', 'view'],
        'Project': ['add', 'delete', 'change', 'view'],
        'Publication': ['add', 'delete', 'change', 'view'],
        'Process Location': ['add', 'delete', 'change', 'view'],
        'Standard Operating Procedure': ['add', 'delete', 'change', 'view'],
        'Metadata Template File': ['add', 'delete', 'change', 'view'],
        'Defined Term': ['add', 'delete', 'change', 'view'],
        'Contact Us': ['add', 'delete', 'change', 'view'],
        'Default Site CSS': ['add', 'delete', 'change', 'view'],
        'Custom User CSS': ['add', 'delete', 'change', 'view'],
        'Periodic Task Run': ['view'],

        # field_survey
        'Field Survey': ['view'],
        'Field Crew': ['view'],
        'Env Measure Type': ['view'],
        'Env Measurement': ['view'],
        'Field Collection': ['view'],
        'Water Collection': ['view'],
        'Sediment Collection': ['view'],
        'Field Sample': ['view'],
        'Filter Sample': ['view'],
        'SubCore Sample': ['view'],
        'FieldSurveyETL': ['view'],
        'EnvMeasurementETL': ['view'],
        'FieldCollectionETL': ['view'],
        'SampleFilterETL': ['view'],

        # wet_lab
        'Primer Pair': ['add', 'delete', 'change', 'view'],
        'Index Pair': ['add', 'delete', 'change', 'view'],
        'Index Removal Method': ['add', 'delete', 'change', 'view'],
        'Size Selection Method': ['add', 'delete', 'change', 'view'],
        'Quantification Method': ['add', 'delete', 'change', 'view'],
        'Extraction Method': ['add', 'delete', 'change', 'view'],
        'Extraction': ['add', 'delete', 'change', 'view'],
        'PCR Replicate': ['add', 'delete', 'change', 'view'],
        'PCR': ['add', 'delete', 'change', 'view'],
        'Library Prep': ['add', 'delete', 'change', 'view'],
        'Pooled Library': ['add', 'delete', 'change', 'view'],
        'Run Prep': ['add', 'delete', 'change', 'view'],
        'Run Result': ['add', 'delete', 'change', 'view'],
        'Fastq File': ['add', 'delete', 'change', 'view'],
        'WetLabDocumentationFile': ['add', 'delete', 'change', 'view'],

        # freezer_inventory
        'Return Action': ['add', 'delete', 'change', 'view'],
        'Freezer': ['add', 'delete', 'change', 'view'],
        'Freezer Rack': ['add', 'delete', 'change', 'view'],
        'Freezer Box': ['add', 'delete', 'change', 'view'],
        'Freezer Inventory': ['add', 'delete', 'change', 'view'],
        'Inventory Log': ['add', 'delete', 'change', 'view'],
        'Inventory Return Metadata': ['add', 'delete', 'change', 'view'],

        # bioinformatics
        'Quality Metadata': ['add', 'delete', 'change', 'view'],
        'DenoiseCluster Method': ['add', 'delete', 'change', 'view'],
        'DenoiseCluster Metadata': ['add', 'delete', 'change', 'view'],
        'Feature Output': ['add', 'delete', 'change', 'view'],
        'Feature Read': ['add', 'delete', 'change', 'view'],
        'Reference Database': ['add', 'delete', 'change', 'view'],
        'Taxon Domain': ['add', 'delete', 'change', 'view'],
        'Taxon Kingdom': ['add', 'delete', 'change', 'view'],
        'Taxon Supergroup': ['add', 'delete', 'change', 'view'],
        'Taxon Phylum/Division': ['add', 'delete', 'change', 'view'],
        'Taxon Class': ['add', 'delete', 'change', 'view'],
        'Taxon Order': ['add', 'delete', 'change', 'view'],
        'Taxon Family': ['add', 'delete', 'change', 'view'],
        'Taxon Genus': ['add', 'delete', 'change', 'view'],
        'Taxon Species': ['add', 'delete', 'change', 'view'],
        'Annotation Method': ['add', 'delete', 'change', 'view'],
        'Annotation Metadata': ['add', 'delete', 'change', 'view'],
        'Taxonomic Annotation': ['add', 'delete', 'change', 'view'],
    },

    'gradstudent-permissions': {
        # general permissions
        'log entry': ['view'],
        'email address': ['view'],
        'email confirmation': ['view'],
        'group': ['view'],
        'permission': ['view'],
        'Token': ['view'],
        'token': ['view'],
        'social account': ['view'],
        'social application': ['view'],
        'social application token': ['view'],
        'user': ['view'],
        'content type': ['view'],
        'session': ['view'],

        # django app model specific permissions
        # field_site
        'ENVO Biome 1st Tier': ['add', 'change', 'view'],
        'ENVO Biome 2nd Tier': ['add', 'change', 'view'],
        'ENVO Biome 3rd Tier': ['add', 'change', 'view'],
        'ENVO Biome 4th Tier': ['add', 'change', 'view'],
        'ENVO Biome 5th Tier': ['add', 'change', 'view'],
        'ENVO Feature 1st Tier': ['add', 'change', 'view'],
        'ENVO Feature 2nd Tier': ['add', 'change', 'view'],
        'ENVO Feature 3rd Tier': ['add', 'change', 'view'],
        'ENVO Feature 4th Tier': ['add', 'change', 'view'],
        'ENVO Feature 5th Tier': ['add', 'change', 'view'],
        'ENVO Feature 6th Tier': ['add', 'change', 'view'],
        'ENVO Feature 7th Tier': ['add', 'change', 'view'],
        'System': ['view'],
        'Watershed': ['view'],
        'Field Site': ['view'],
        'World Border': ['view'],

        # sample_label
        'Sample Type': ['view'],
        'SampleLabelRequest': ['view'],
        'SampleBarcode': ['view'],

        # utility
        'Fund': ['view'],
        'Project': ['add', 'change', 'view'],
        'Publication': ['add', 'change', 'view'],
        'Process Location': ['add', 'change', 'view'],
        'Standard Operating Procedure': ['add', 'change', 'view'],
        'Metadata Template File': ['add', 'change', 'view'],
        'Defined Term': ['add', 'change', 'view'],
        'Contact Us': ['add', 'view'],
        'Default Site CSS': ['add', 'change', 'view'],
        'Custom User CSS': ['add', 'change', 'view'],
        'Periodic Task Run': ['view'],

        # field_survey
        'Field Survey': ['view'],
        'Field Crew': ['view'],
        'Env Measure Type': ['view'],
        'Env Measurement': ['view'],
        'Field Collection': ['view'],
        'Water Collection': ['view'],
        'Sediment Collection': ['view'],
        'Field Sample': ['view'],
        'Filter Sample': ['view'],
        'SubCore Sample': ['view'],
        'FieldSurveyETL': ['view'],
        'EnvMeasurementETL': ['view'],
        'FieldCollectionETL': ['view'],
        'SampleFilterETL': ['view'],

        # wet_lab
        'Primer Pair': ['add', 'change', 'view'],
        'Index Pair': ['add', 'change', 'view'],
        'Index Removal Method': ['add', 'change', 'view'],
        'Size Selection Method': ['add', 'change', 'view'],
        'Quantification Method': ['add', 'change', 'view'],
        'Extraction Method': ['add', 'change', 'view'],
        'Extraction': ['add', 'change', 'view'],
        'PCR Replicate': ['add', 'change', 'view'],
        'PCR': ['add', 'change', 'view'],
        'Library Prep': ['add', 'change', 'view'],
        'Pooled Library': ['add', 'change', 'view'],
        'Run Prep': ['add', 'change', 'view'],
        'Run Result': ['view'],
        'Fastq File': ['view'],
        'WetLabDocumentationFile': ['view'],

        # freezer_inventory
        'Return Action': ['add', 'change', 'view'],
        'Freezer': ['add', 'change', 'view'],
        'Freezer Rack': ['add', 'change', 'view'],
        'Freezer Box': ['add', 'change', 'view'],
        'Freezer Inventory': ['add', 'change', 'view'],
        'Inventory Log': ['add', 'change', 'view'],
        'Inventory Return Metadata': ['add', 'change', 'view'],

        # bioinformatics
        'Quality Metadata': ['add', 'change', 'view'],
        'DenoiseCluster Method': ['add', 'change', 'view'],
        'DenoiseCluster Metadata': ['add', 'change', 'view'],
        'Feature Output': ['view'],
        'Feature Read': ['view'],
        'Reference Database': ['add', 'change', 'view'],
        'Taxon Domain': ['add', 'change', 'view'],
        'Taxon Kingdom': ['add', 'change', 'view'],
        'Taxon Supergroup': ['add', 'change', 'view'],
        'Taxon Phylum/Division': ['add', 'change', 'view'],
        'Taxon Class': ['add', 'change', 'view'],
        'Taxon Order': ['add', 'change', 'view'],
        'Taxon Family': ['add', 'change', 'view'],
        'Taxon Genus': ['add', 'change', 'view'],
        'Taxon Species': ['add', 'change', 'view'],
        'Annotation Method': ['add', 'change', 'view'],
        'Annotation Metadata': ['add', 'change', 'view'],
        'Taxonomic Annotation': ['add', 'change', 'view'],
    },

    'internstudent-permissions': {
        # django app model specific permissions
        # field_site
        'ENVO Biome 1st Tier': ['view'],
        'ENVO Biome 2nd Tier': ['view'],
        'ENVO Biome 3rd Tier': ['view'],
        'ENVO Biome 4th Tier': ['view'],
        'ENVO Biome 5th Tier': ['view'],
        'ENVO Feature 1st Tier': ['view'],
        'ENVO Feature 2nd Tier': ['view'],
        'ENVO Feature 3rd Tier': ['view'],
        'ENVO Feature 4th Tier': ['view'],
        'ENVO Feature 5th Tier': ['view'],
        'ENVO Feature 6th Tier': ['view'],
        'ENVO Feature 7th Tier': ['view'],
        'System': ['view'],
        'Watershed': ['view'],
        'Field Site': ['view'],
        'World Border': ['view'],

        # sample_label
        'Sample Type': ['view'],
        'SampleLabelRequest': ['view'],
        'SampleBarcode': ['view'],

        # utility
        'Fund': ['view'],
        'Project': ['view'],
        'Publication': ['view'],
        'Process Location': ['view'],
        'Standard Operating Procedure': ['view'],
        'Metadata Template File': ['view'],
        'Defined Term': ['view'],
        'Contact Us': ['add', 'view'],
        'Default Site CSS': ['view'],
        'Custom User CSS': ['view'],
        'Periodic Task Run': ['view'],

        # field_survey
        'Field Survey': ['view'],
        'Field Crew': ['view'],
        'Env Measure Type': ['view'],
        'Env Measurement': ['view'],
        'Field Collection': ['view'],
        'Water Collection': ['view'],
        'Sediment Collection': ['view'],
        'Field Sample': ['view'],
        'Filter Sample': ['view'],
        'SubCore Sample': ['view'],
        'FieldSurveyETL': ['view'],
        'EnvMeasurementETL': ['view'],
        'FieldCollectionETL': ['view'],
        'SampleFilterETL': ['view'],

        # wet_lab
        'Primer Pair': ['view'],
        'Index Pair': ['view'],
        'Index Removal Method': ['view'],
        'Size Selection Method': ['view'],
        'Quantification Method': ['view'],
        'Extraction Method': ['view'],
        'Extraction': ['add', 'change', 'view'],
        'PCR Replicate': ['add', 'change', 'view'],
        'PCR': ['add', 'change', 'view'],
        'Library Prep': ['add', 'change', 'view'],
        'Pooled Library': ['add', 'change', 'view'],
        'Run Prep': ['add', 'change', 'view'],
        'Run Result': ['view'],
        'Fastq File': ['view'],
        'WetLabDocumentationFile': ['view'],

        # freezer_inventory
        'Return Action': ['view'],
        'Freezer': ['view'],
        'Freezer Rack': ['view'],
        'Freezer Box': ['view'],
        'Freezer Inventory': ['add', 'change', 'view'],
        'Inventory Log': ['add', 'change', 'view'],
        'Inventory Return Metadata': ['change', 'view'],

        # bioinformatics
        'Quality Metadata': ['view'],
        'DenoiseCluster Method': ['view'],
        'DenoiseCluster Metadata': ['view'],
        'Feature Output': ['view'],
        'Feature Read': ['view'],
        'Reference Database': ['view'],
        'Taxon Domain': ['view'],
        'Taxon Kingdom': ['view'],
        'Taxon Supergroup': ['view'],
        'Taxon Phylum/Division': ['view'],
        'Taxon Class': ['view'],
        'Taxon Order': ['view'],
        'Taxon Family': ['view'],
        'Taxon Genus': ['view'],
        'Taxon Species': ['view'],
        'Annotation Method': ['view'],
        'Annotation Metadata': ['view'],
        'Taxonomic Annotation': ['view'],
    },
}


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)
            # Loop models in group
            for app_model in GROUPS[group_name]:
                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:
                    # Generate permission name as Django would generate it
                    name = 'Can {} {}'.format(permission_name, app_model)
                    print('Creating {}'.format(name))
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning('Permission not found with name "{}".'.format(name))
                        continue
                    new_group.permissions.add(model_add_perm)
