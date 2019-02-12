import csv
import datetime
from optparse import make_option
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from ginvest.apps.tesouro.models import TesouroDireto
from ginvest.apps.indicadores.models import SELIC, IGPM, IPCA


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option("--dir", "-d",
            dest="directory",
            action="store",
            default=None,
            help="The directory containing the data files"),
    )

    def _populate_selic(self, directory):

        with open(directory + "/selic.csv", "rU") as csvfile:

                    r = csv.reader(csvfile)

                    for line in r:

                        try:
                            obj = SELIC.objects.get(maturity=int(line[0]))

                        except SELIC.DoesNotExist:
                            obj = SELIC(maturity=int(line[0]))

                        obj.rate = float(line[1].strip().replace(",", "."))
                        obj.updated = datetime.datetime.today()

                        if settings.DEBUG:
                            print("Saving {}".format(obj))

                        obj.save()

    def _populate_ipca(self, directory):

        with open(directory + "/ipca.csv", "rU") as csvfile:

                    r = csv.reader(csvfile)

                    for line in r:

                        try:
                            obj = IPCA.objects.get(maturity=int(line[0]))

                        except IPCA.DoesNotExist:
                            obj = IPCA(maturity=int(line[0]))

                        obj.rate = float(line[1].strip().replace(",", "."))
                        obj.updated = datetime.datetime.today()

                        if settings.DEBUG:
                            print("Saving {}".format(obj))

                        obj.save()

    def _populate_igpm(self, directory):

        with open(directory + "/igpm.csv", "rU") as csvfile:

                    r = csv.reader(csvfile)

                    for line in r:

                        try:
                            obj = IGPM.objects.get(maturity=int(line[0]))

                        except IGPM.DoesNotExist:
                            obj = IGPM(maturity=int(line[0]))

                        obj.rate = float(line[1].strip().replace(",", "."))
                        obj.updated = datetime.datetime.today()

                        if settings.DEBUG:
                            print("Saving {}".format(obj))

                        obj.save()

    def _populate_tesouro_direto(self, directory):

        with open(directory + "/tesouro.csv", "rU") as csvfile:

            r = csv.reader(csvfile)

            for line in r:

                try:

                    maturity = datetime.datetime.strptime(line[2].strip().strip("\""), "%d/%m/%Y")
                    obj = TesouroDireto.objects.get(name=line[0].strip(), maturity=maturity)

                except TesouroDireto.DoesNotExist:

                    obj = TesouroDireto(name=line[0].strip(), maturity=maturity)

                obj.description = line[1].strip().strip("\"")
                obj.rate = float(line[3].strip().strip("\""))

                index = line[4].rstrip("\n").strip().strip("\"")

                print("[{}]".format(index))

                if index == "IPCA":
                    obj.indexedby = TesouroDireto.INDEX_IPCA
                elif index == "IGP-M":
                    obj.indexedby = TesouroDireto.INDEX_IGPM
                elif index == "SELIC":
                    obj.indexedby = TesouroDireto.INDEX_SELIC
                else:
                    obj.indexedby = TesouroDireto.NOINDEX

                if settings.DEBUG:
                    print("Saving {}".format(obj))

                obj.updated = datetime.datetime.today()

                obj.save()

    def handle(self, *args, **options):

        self.stdout.write("Populating database with indexes")

        if options["directory"] is None:
            raise CommandError("You must pass the directory containing the data files")

        else:
            call_command("clean_pyc", interactive=False)
            call_command("reset_db", router="default", interactive=False)
            call_command("syncdb", interactive=False)

            try:
                self.stdout.write("Populating SELIC Indexes")
                self._populate_selic(options["directory"])

                self.stdout.write("Populating IPCA Indexes")
                self._populate_ipca(options["directory"])

                self.stdout.write("Populating IPG-M Indexes")
                self._populate_igpm(options["directory"])

                self.stdout.write("Populating Tesouro Direto bonds")
                self._populate_tesouro_direto(options["directory"])

            except BaseException, message:
                raise CommandError(message)
