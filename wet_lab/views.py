from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PrimerPairSerializer, IndexPairSerializer, IndexRemovalMethodSerializer, \
    SizeSelectionMethodSerializer, QuantificationMethodSerializer, ExtractionMethodSerializer, \
    ExtractionSerializer, DdpcrSerializer, QpcrSerializer, LibraryPrepSerializer, PooledLibrarySerializer, \
    FinalPooledLibrarySerializer, RunPrepSerializer, RunResultSerializer, FastqFileSerializer
from .models import PrimerPair, IndexPair, IndexRemovalMethod, \
    SizeSelectionMethod, QuantificationMethod, ExtractionMethod, \
    Extraction, Ddpcr, Qpcr, LibraryPrep, PooledLibrary, \
    FinalPooledLibrary, RunPrep, RunResult, FastqFile


# Create your views here.
class PrimerPairViewSet(viewsets.ModelViewSet):
    serializer_class = PrimerPairSerializer
    queryset = PrimerPair.objects.all()


class IndexPairViewSet(viewsets.ModelViewSet):
    serializer_class = IndexPairSerializer
    queryset = IndexPair.objects.all()


class IndexRemovalMethodViewSet(viewsets.ModelViewSet):
    serializer_class = IndexRemovalMethodSerializer
    queryset = IndexRemovalMethod.objects.all()


class SizeSelectionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = SizeSelectionMethodSerializer
    queryset = SizeSelectionMethod.objects.all()


class QuantificationMethodViewSet(viewsets.ModelViewSet):
    serializer_class = QuantificationMethodSerializer
    queryset = QuantificationMethod.objects.all()


class ExtractionMethodViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionMethodSerializer
    queryset = ExtractionMethod.objects.all()


class ExtractionViewSet(viewsets.ModelViewSet):
    serializer_class = ExtractionSerializer
    queryset = Extraction.objects.all()


class DdpcrViewSet(viewsets.ModelViewSet):
    serializer_class = DdpcrSerializer
    queryset = Ddpcr.objects.all()


class QpcrViewSet(viewsets.ModelViewSet):
    serializer_class = QpcrSerializer
    queryset = Qpcr.objects.all()


class LibraryPrepViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryPrepSerializer
    queryset = LibraryPrep.objects.all()


class PooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = PooledLibrarySerializer
    queryset = PooledLibrary.objects.all()


class FinalPooledLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = FinalPooledLibrarySerializer
    queryset = FinalPooledLibrary.objects.all()


class RunPrepViewSet(viewsets.ModelViewSet):
    serializer_class = RunPrepSerializer
    queryset = RunPrep.objects.all()


class RunResultViewSet(viewsets.ModelViewSet):
    serializer_class = RunResultSerializer
    queryset = RunResult.objects.all()


class FastqFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastqFileSerializer
    queryset = FastqFile.objects.all()
