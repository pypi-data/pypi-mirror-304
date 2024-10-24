# copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-eac unit tests for dataimport"""

import datetime
from io import BytesIO
from itertools import count
from os.path import join, dirname
import sys
import unittest

from cubicweb import NoResultError
from cubicweb.dataimport.importer import ExtEntity, SimpleImportLog
from cubicweb_web.devtools.testlib import WebCWTC

from cubicweb_eac import dataimport, testutils


def mock_(string):
    return string


def extentities2dict(entities):
    edict = {}
    for extentity in entities:
        edict.setdefault(extentity.etype, {})[extentity.extid] = extentity.values
    return edict


def mk_extid_generator():
    """Predicate extid_generator."""
    gen = map(str, count())
    return gen.__next__


class EACXMLParserTC(unittest.TestCase):
    if sys.version_info < (3, 2):
        assertCountEqual = unittest.TestCase.assertItemsEqual

    @classmethod
    def datapath(cls, *fname):
        """joins the object's datadir and `fname`"""
        return join(dirname(__file__), "data", *fname)

    def file_extentities(self, fname):
        fpath = self.datapath(fname)
        import_log = SimpleImportLog(fpath)
        importer = dataimport.EACCPFImporter(
            fpath, import_log, mock_, extid_generator=mk_extid_generator()
        )
        return importer.external_entities()

    def test_parse_FRAD033_EAC_00001(self):
        _gen_extid = map(str, (x for x in count() if x != 2)).__next__
        expected = [
            (
                "AuthorityRecord",
                "FRAD033_EAC_00001",
                {
                    "isni": {"22330001300016"},
                    "start_date": {datetime.date(1800, 1, 1)},
                    "end_date": {datetime.date(2099, 1, 1)},
                    "agent_kind": {"agentkind/authority"},
                    "record_id": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "EACOtherRecordId",
                _gen_extid(),
                {
                    "eac_other_record_id_of": {"FRAD033_EAC_00001"},
                    "value": {"1234"},
                },
            ),
            (
                "EACOtherRecordId",
                _gen_extid(),
                {
                    "eac_other_record_id_of": {"FRAD033_EAC_00001"},
                    "value": {"ABCD"},
                    "local_type": {"letters"},
                },
            ),
            (
                "EACSource",
                _gen_extid(),
                {
                    "source_agent": {"FRAD033_EAC_00001"},
                    "title": {"1. Ouvrages imprimés..."},
                    "description": {"des bouquins"},
                    "description_format": {"text/plain"},
                },
            ),
            (
                "EACSource",
                _gen_extid(),
                {
                    "source_agent": {"FRAD033_EAC_00001"},
                    "url": {"http://archives.gironde.fr"},
                    "title": {"Site des Archives départementales de la Gironde"},
                },
            ),
            (
                "Activity",
                _gen_extid(),
                {
                    "type": {"create"},
                    "generated": {"FRAD033_EAC_00001"},
                    "start": {
                        datetime.datetime(
                            2013, 4, 24, 5, 34, 41, tzinfo=datetime.timezone.utc
                        )
                    },
                    "end": {
                        datetime.datetime(
                            2013, 4, 24, 5, 34, 41, tzinfo=datetime.timezone.utc
                        )
                    },
                    "description": {"bla bla"},
                    "description_format": {"text/plain"},
                },
            ),
            (
                "Activity",
                _gen_extid(),
                {
                    "generated": {"FRAD033_EAC_00001"},
                    "type": {"modify"},
                    "start": {
                        datetime.datetime(
                            2015, 1, 15, 7, 16, 33, tzinfo=datetime.timezone.utc
                        )
                    },
                    "end": {
                        datetime.datetime(
                            2015, 1, 15, 7, 16, 33, tzinfo=datetime.timezone.utc
                        )
                    },
                    "agent": {"Delphine Jamet"},
                },
            ),
            (
                "AgentKind",
                "agentkind/authority",
                {"name": {"authority"}},
            ),
            (
                "NameEntry",
                _gen_extid(),
                {
                    "parts": {"Gironde, Conseil général"},
                    "form_variant": {"authorized"},
                    "name_entry_for": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "NameEntry",
                _gen_extid(),
                {
                    "parts": {"CG33"},
                    "form_variant": {"alternative"},
                    "name_entry_for": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "PostalAddress",
                _gen_extid(),
                {
                    "street": {"1 Esplanade Charles de Gaulle"},
                    "postalcode": {"33074"},
                    "city": {" Bordeaux Cedex"},
                },
            ),
            (
                "AgentPlace",
                _gen_extid(),
                {
                    "name": {"Bordeaux (Gironde, France)"},
                    "role": {"siege"},
                    "place_agent": {"FRAD033_EAC_00001"},
                    "place_address": {"9"},
                    "equivalent_concept": {
                        "http://catalogue.bnf.fr/ark:/12148/cb152418385"
                    },
                },
            ),
            (
                "AgentPlace",
                _gen_extid(),
                {
                    "name": {"Toulouse (France)"},
                    "place_agent": {"FRAD033_EAC_00001"},
                    "role": {"domicile"},
                },
            ),
            (
                "AgentPlace",
                _gen_extid(),
                {
                    "name": {"Lit"},
                    "place_agent": {"FRAD033_EAC_00001"},
                    "role": {"dodo"},
                },
            ),
            (
                "LegalStatus",
                _gen_extid(),
                {
                    "term": {"Collectivité territoriale"},
                    "start_date": {datetime.date(1234, 1, 1)},
                    "end_date": {datetime.date(3000, 1, 1)},
                    "description": {"Description du statut"},
                    "description_format": {"text/plain"},
                    "legal_status_agent": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "Mandate",
                _gen_extid(),
                {
                    "term": {"1. Constitutions françaises"},
                    "description": {"Description du mandat"},
                    "description_format": {"text/plain"},
                    "mandate_agent": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "History",
                _gen_extid(),
                {
                    "text": {
                        "\n".join(
                            (
                                '<p xmlns="urn:isbn:1-931666-33-4" '
                                'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                                'xmlns:xlink="http://www.w3.org/1999/xlink">{}</p>'
                            ).format(text)
                            for text in [
                                "La loi du 22 décembre 1789, en divisant ...",
                                "L'inspecteur Canardo",
                            ]
                        )
                    },
                    "text_format": {"text/html"},
                    "history_agent": {"FRAD033_EAC_00001"},
                    "has_citation": {"16", "17"},
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "uri": {
                        "http://www.assemblee-nationale.fr/histoire/images-decentralisation/decentralisation/loi-du-22-decembre-1789-.pdf"  # noqa
                    }
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {"uri": {"http://pifgadget"}, "note": {"Voir aussi pifgadget"}},
            ),
            (
                "Structure",
                _gen_extid(),
                {
                    "description": {
                        '<p xmlns="urn:isbn:1-931666-33-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">Pour accomplir ses missions ...</p>'  # noqa
                    },
                    "description_format": {"text/html"},
                    "structure_agent": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "AgentFunction",
                _gen_extid(),
                {
                    "description": {
                        '<p xmlns="urn:isbn:1-931666-33-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">Quatre grands domaines de compétence...</p>'  # noqa
                    },
                    "description_format": {"text/html"},
                    "function_agent": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "AgentFunction",
                _gen_extid(),
                {
                    "name": {"action sociale"},
                    "function_agent": {"FRAD033_EAC_00001"},
                    "description": {
                        '<p xmlns="urn:isbn:1-931666-33-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">1. Solidarité\n'  # noqa
                        "            blablabla.</p>"
                    },
                    "description_format": {"text/html"},
                    "equivalent_concept": {
                        "http://data.culture.fr/thesaurus/page/ark:/67717/T1-200"
                    },
                },
            ),
            (
                "AgentFunction",
                _gen_extid(),
                {
                    "name": {"environnement"},
                    "function_agent": {"FRAD033_EAC_00001"},
                    "equivalent_concept": {
                        "http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074"
                    },
                },
            ),
            (
                "Occupation",
                _gen_extid(),
                {
                    "term": {"Réunioniste"},
                    "start_date": {datetime.date(1987, 1, 1)},
                    "end_date": {datetime.date(2099, 1, 1)},
                    "description": {"Organisation des réunions ..."},
                    "description_format": {"text/plain"},
                    "occupation_agent": {"FRAD033_EAC_00001"},
                    "has_citation": {"23"},
                    "equivalent_concept": {"http://pifgadget.com"},
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "note": {"la bible"},
                },
            ),
            (
                "GeneralContext",
                _gen_extid(),
                {
                    "content": {
                        '<p xmlns="urn:isbn:1-931666-33-4" '
                        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                        'xmlns:xlink="http://www.w3.org/1999/xlink">very famous</p>'
                    },
                    "content_format": {"text/html"},
                    "has_citation": {"25"},
                    "general_context_of": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "Citation",
                _gen_extid(),
                {
                    "note": {"it's well known"},
                },
            ),
            (
                "ExternalUri",
                "CG33-DIRADSJ",
                {
                    "uri": {"CG33-DIRADSJ"},
                    "cwuri": {"CG33-DIRADSJ"},
                },
            ),
            (
                "HierarchicalRelation",
                _gen_extid(),
                {
                    "start_date": {datetime.date(2008, 1, 1)},
                    "end_date": {datetime.date(2099, 1, 1)},
                    "entry": {
                        "Gironde. Conseil général. Direction de l'administration et de "
                        "la sécurité juridique"
                    },
                    "description": {"Coucou"},
                    "description_format": {"text/plain"},
                    "hierarchical_parent": {"CG33-DIRADSJ"},
                    "hierarchical_child": {"FRAD033_EAC_00001"},
                },
            ),
            (
                "ExternalUri",
                "whatever",
                {
                    "uri": {"whatever"},
                    "cwuri": {"whatever"},
                },
            ),
            (
                "ExternalUri",
                "/dev/null",
                {
                    "uri": {"/dev/null"},
                    "cwuri": {"/dev/null"},
                },
            ),
            (
                "ChronologicalRelation",
                _gen_extid(),
                {
                    "chronological_predecessor": {"whatever"},
                    "chronological_successor": {"FRAD033_EAC_00001"},
                    "start_date": {datetime.date(1917, 1, 1)},
                    "end_date": {datetime.date(2009, 1, 1)},
                    "entry": {"CG32"},
                },
            ),
            (
                "ChronologicalRelation",
                _gen_extid(),
                {
                    "chronological_predecessor": {"FRAD033_EAC_00001"},
                    "chronological_successor": {"/dev/null"},
                    "start_date": {datetime.date(2042, 1, 1)},
                    "xml_wrap": {
                        b'<gloups xmlns="urn:isbn:1-931666-33-4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">hips</gloups>'  # noqa
                    },
                    "entry": {"Trash"},
                },
            ),
            (
                "AssociationRelation",
                _gen_extid(),
                {
                    "association_from": {"FRAD033_EAC_00001"},
                    "association_to": {"agent-x"},
                },
            ),
            (
                "EACResourceRelation",
                _gen_extid(),
                {
                    "agent_role": {"creatorOf"},
                    "resource_role": {"Fonds d'archives"},
                    "resource_relation_resource": {
                        "http://gael.gironde.fr/ead.html?id=FRAD033_IR_N"
                    },
                    "resource_relation_agent": {"FRAD033_EAC_00001"},
                    "start_date": {datetime.date(1673, 1, 1)},
                    "end_date": {datetime.date(1963, 1, 1)},
                    "xml_wrap": {
                        b'<he xmlns="urn:isbn:1-931666-33-4" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">joe</he>'  # noqa
                    },
                },
            ),
            (
                "ExternalUri",
                "http://gael.gironde.fr/ead.html?id=FRAD033_IR_N",
                {
                    "uri": {"http://gael.gironde.fr/ead.html?id=FRAD033_IR_N"},
                    "cwuri": {"http://gael.gironde.fr/ead.html?id=FRAD033_IR_N"},
                },
            ),
            (
                "ExternalUri",
                "agent-x",
                {"uri": {"agent-x"}, "cwuri": {"agent-x"}},
            ),
            (
                "ExternalUri",
                "http://data.culture.fr/thesaurus/page/ark:/67717/T1-200",
                {
                    "uri": {"http://data.culture.fr/thesaurus/page/ark:/67717/T1-200"},
                    "cwuri": {
                        "http://data.culture.fr/thesaurus/page/ark:/67717/T1-200"
                    },
                },
            ),
            (
                "ExternalUri",
                "http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074",
                {
                    "uri": {"http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074"},
                    "cwuri": {
                        "http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074"
                    },
                },
            ),
            (
                "ExternalUri",
                "http://catalogue.bnf.fr/ark:/12148/cb152418385",
                {
                    "uri": {"http://catalogue.bnf.fr/ark:/12148/cb152418385"},
                    "cwuri": {"http://catalogue.bnf.fr/ark:/12148/cb152418385"},
                },
            ),
            (
                "ExternalUri",
                "http://pifgadget.com",
                {"uri": {"http://pifgadget.com"}, "cwuri": {"http://pifgadget.com"}},
            ),
        ]
        expected = [ExtEntity(*vals) for vals in expected]
        fpath = self.datapath("FRAD033_EAC_00001_simplified.xml")
        import_log = SimpleImportLog(fpath)
        importer = dataimport.EACCPFImporter(
            fpath, import_log, mock_, extid_generator=mk_extid_generator()
        )
        entities = list(importer.external_entities())
        self.check_external_entities(entities, expected)
        visited = set()
        for x in importer._visited.values():
            visited.update(x)
        self.assertCountEqual(visited, [x.extid for x in expected])
        # Gather not-visited tag by name and group source lines.
        not_visited = {}
        for tagname, sourceline in importer.not_visited():
            not_visited.setdefault(tagname, set()).add(sourceline)
        self.assertEqual(
            not_visited,
            {
                "maintenanceStatus": {12},
                "publicationStatus": {14},
                "maintenanceAgency": {16},
                "languageDeclaration": {21},
                "conventionDeclaration": {25, 35, 44},
                "localControl": {54},
                "source": {76},  # empty.
                "structureOrGenealogy": {189},  # empty.
                "biogHist": {204},  # empty.
            },
        )

    def test_mandate_under_mandates(self):
        """In FRAD033_EAC_00003.xml, <mandate> element are within <mandates>."""
        entities = list(self.file_extentities("FRAD033_EAC_00003.xml"))
        expected_terms = [
            "Code du patrimoine, Livre II",
            "Loi du 5 brumaire an V [26 octobre 1796]",
            (
                "Loi du 3 janvier 1979 sur les archives, accompagnée de ses décrets\n"
                "                        d’application datant du 3 décembre."
            ),
            "Loi sur les archives du 15 juillet 2008",
        ]
        self.assertCountEqual(
            [
                next(iter(x.values["term"]))
                for x in entities
                if x.etype == "Mandate" and "term" in x.values
            ],
            expected_terms,
        )
        mandate_with_link = next(
            x
            for x in entities
            if x.etype == "Mandate"
            and "Code du patrimoine, Livre II" in x.values["term"]
        )
        extid = next(iter(mandate_with_link.values["has_citation"]))
        url = (
            "http://www.legifrance.gouv.fr/affichCode.do?idArticle=LEGIARTI000019202816"
        )
        citation = next(
            x for x in entities if x.etype == "Citation" and url in x.values["uri"]
        )
        self.assertEqual(extid, citation.extid)

    def test_agentfunction_within_functions_tag(self):
        """In FRAD033_EAC_00003.xml, <function> element are within <functions>
        not <description>.
        """
        entities = self.file_extentities("FRAD033_EAC_00003.xml")
        self.assertCountEqual(
            [
                x.values["name"].pop()
                for x in entities
                if x.etype == "AgentFunction" and "name" in x.values
            ],
            ["contr\xf4le", "collecte", "classement", "restauration", "promotion"],
        )

    def test_no_nameentry_authorizedform(self):
        entities = self.file_extentities(
            "Service de l'administration generale et des assemblees.xml"
        )
        expected = (
            "Gironde. Conseil général. Service de l'administration "
            "générale et des assemblées"
        )
        self.assertIn(
            expected,
            [x.values["parts"].pop() for x in entities if x.etype == "NameEntry"],
        )

    def ctx_assert(self, method, actual, expected, ctx, msg=None):
        """Wrap assertion method with a context message"""
        try:
            getattr(self, method)(actual, expected, msg=msg)
        except AssertionError as exc:
            msg = str(exc)
            if ctx:
                msg = ("[%s] " % ctx) + msg
            raise AssertionError(msg).with_traceback(sys.exc_info()[-1])

    def check_external_entities(self, entities, expected):
        entities = extentities2dict(entities)
        expected = extentities2dict(expected)
        etypes, expected_etypes = list(entities), list(expected)
        self.ctx_assert("assertCountEqual", etypes, expected_etypes, ctx="etypes")

        def safe_int(value):
            try:
                return int(value)
            except ValueError:
                return 9999

        ordered_etypes = [
            x[1]
            for x in sorted(
                (min(safe_int(extid) for extid in edict), etype)
                for etype, edict in expected.items()
            )
        ]
        for etype in ordered_etypes:
            edict = expected[etype]
            entities_etype = entities[etype]
            extids, expected_extids = list(entities_etype), list(edict)
            self.ctx_assert(
                "assertCountEqual", extids, expected_extids, ctx="%s/extids" % etype
            )
            for extid, values in edict.items():
                self.ctx_assert(
                    "assertEqual",
                    entities_etype[extid],
                    values,
                    ctx=f"{etype}/{extid}/values",
                )

    def test_errors(self):
        log = SimpleImportLog("<dummy>")
        with self.assertRaises(dataimport.InvalidXML):
            importer = dataimport.EACCPFImporter(BytesIO(b"no xml"), log, mock_)
            list(importer.external_entities())
        with self.assertRaises(dataimport.MissingTag):
            importer = dataimport.EACCPFImporter(BytesIO(b"<xml/>"), log, mock_)
            list(importer.external_entities())


class EACDataImportTC(WebCWTC):
    def test_FRAD033_EAC_00001(self):
        fpath = self.datapath("FRAD033_EAC_00001_simplified.xml")
        with self.admin_access.repo_cnx() as cnx:
            # create a skos concept to ensure it's used instead of a ExternalUri
            scheme = cnx.create_entity("ConceptScheme")
            scheme.add_concept(
                "environnement",
                cwuri="http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074",
            )
            cnx.commit()
            created, updated = testutils.eac_import(cnx, fpath)
            self.assertEqual(len(created), 39)
            self.assertEqual(updated, set())
            rset = cnx.find("AuthorityRecord", isni="22330001300016")
            self.assertEqual(len(rset), 1)
            record = rset.one()
            self.assertEqual(record.kind, "authority")
            self.assertEqual(
                record.start_date,
                datetime.date(1800, 1, 1),
            )
            self.assertEqual(record.end_date, datetime.date(2099, 1, 1))
            self.assertEqual(
                record.other_record_ids, [(None, "1234"), ("letters", "ABCD")]
            )
            address = record.postal_address[0]
            self.assertEqual(address.street, "1 Esplanade Charles de Gaulle")
            self.assertEqual(address.postalcode, "33074")
            self.assertEqual(address.city, " Bordeaux Cedex")
            rset = cnx.execute(
                "Any R,N WHERE P place_agent A, A eid %(eid)s, P role R, P name N",
                {"eid": record.eid},
            )
            self.assertCountEqual(
                rset.rows,
                [
                    ["siege", "Bordeaux (Gironde, France)"],
                    ["domicile", "Toulouse (France)"],
                    ["dodo", "Lit"],
                ],
            )
            self.assertEqual(len(record.reverse_function_agent), 3)
            for related in (
                "structure",
                "history",
                "mandate",
                "occupation",
                "generalcontext",
                "legal_status",
                "eac_relations",
                "equivalent_concept",
                "control",
            ):
                with self.subTest(related=related):
                    checker = getattr(self, "_check_" + related)
                    checker(cnx, record)

    def _check_structure(self, cnx, record):
        rset = cnx.find("Structure", structure_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("description", format="text/plain").strip(),
            "Pour accomplir ses missions ...",
        )

    def _check_history(self, cnx, record):
        rset = cnx.find("History", history_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("text", format="text/plain").strip(),
            "La loi du 22 décembre 1789, en divisant ...\n\nL'inspecteur Canardo",
        )

    def _check_mandate(self, cnx, record):
        rset = cnx.find("Mandate", mandate_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("description", format="text/plain").strip(),
            "Description du mandat",
        )

    def _check_occupation(self, cnx, record):
        occupation = cnx.find("Occupation", occupation_agent=record).one()
        self.assertEqual(occupation.term, "Réunioniste")
        citation = occupation.has_citation[0]
        self.assertEqual(citation.note, "la bible")
        voc = occupation.equivalent_concept[0]
        self.assertEqual(voc.uri, "http://pifgadget.com")

    def _check_generalcontext(self, cnx, record):
        occupation = cnx.find("GeneralContext", general_context_of=record).one()
        self.assertIn("very famous", occupation.content)
        self.assertEqual(occupation.content_format, "text/html")
        citation = occupation.has_citation[0]
        self.assertEqual(citation.note, "it's well known")

    def _check_legal_status(self, cnx, record):
        rset = cnx.find("LegalStatus", legal_status_agent=record)
        self.assertEqual(len(rset), 1)
        self.assertEqual(
            rset.one().printable_value("description", format="text/plain").strip(),
            "Description du statut",
        )

    def _check_eac_relations(self, cnx, record):
        relation = cnx.find("HierarchicalRelation").one()
        self.assertEqual(
            relation.entry,
            "Gironde. Conseil général. Direction de "
            "l'administration et de la sécurité juridique",
        )
        self.assertEqual(
            relation.printable_value("description", format="text/plain"), "Coucou"
        )
        other_record = cnx.find("ExternalUri", uri="CG33-DIRADSJ").one()
        self.assertEqual(relation.hierarchical_parent[0], other_record)
        relation = cnx.find("AssociationRelation").one()
        self.assertEqual(relation.association_from[0], record)
        other_record = cnx.find("ExternalUri", uri="agent-x").one()
        self.assertEqual(other_record.cwuri, "agent-x")
        self.assertEqual(relation.association_to[0], other_record)
        rset = cnx.find("EACResourceRelation", agent_role="creatorOf")
        self.assertEqual(len(rset), 1)
        rrelation = rset.one()
        self.assertEqual(rrelation.resource_relation_agent[0], record)
        exturi = rrelation.resource_relation_resource[0]
        self.assertEqual(exturi.uri, "http://gael.gironde.fr/ead.html?id=FRAD033_IR_N")
        self.assertEqual(
            rrelation.xml_wrap.getvalue(),
            b'<he xmlns="urn:isbn:1-931666-33-4" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">joe</he>',  # noqa
        )

    def _check_equivalent_concept(self, cnx, record):
        functions = {f.name: f for f in record.reverse_function_agent}
        self.assertEqual(
            functions["action sociale"].equivalent_concept[0].cwuri,
            "http://data.culture.fr/thesaurus/page/ark:/67717/T1-200",
        )
        self.assertEqual(
            functions["action sociale"].equivalent_concept[0].cw_etype, "ExternalUri"
        )
        self.assertEqual(
            functions["environnement"].equivalent_concept[0].cwuri,
            "http://data.culture.fr/thesaurus/page/ark:/67717/T1-1074",
        )
        self.assertEqual(
            functions["environnement"].equivalent_concept[0].cw_etype, "Concept"
        )
        self.assertEqual(
            functions["environnement"].vocabulary_source[0].eid,
            functions["environnement"].equivalent_concept[0].scheme.eid,
        )
        place = cnx.find("AgentPlace", role="siege").one()
        self.assertEqual(
            place.equivalent_concept[0].cwuri,
            "http://catalogue.bnf.fr/ark:/12148/cb152418385",
        )

    def _check_control(self, cnx, record):
        rset = cnx.find("EACSource")
        self.assertEqual(len(rset), 2)
        rset = cnx.execute("Any A WHERE A generated X, X eid %(x)s", {"x": record.eid})
        self.assertEqual(len(rset), 2)
        rset = cnx.execute('Any A WHERE A agent "Delphine Jamet"')
        self.assertEqual(len(rset), 1)

    def test_multiple_imports(self):
        def count_entity(cnx, etype):
            return cnx.execute("Any COUNT(X) WHERE X is %s" % etype)[0][0]

        with self.admin_access.repo_cnx() as cnx:
            nb_records_before = count_entity(cnx, "AuthorityRecord")
            for fname in (
                "FRAD033_EAC_00001.xml",
                "FRAD033_EAC_00003.xml",
                "FRAD033_EAC_00071.xml",
            ):
                fpath = self.datapath(fname)
                created, updated = testutils.eac_import(cnx, fpath)
            nb_records_after = count_entity(cnx, "AuthorityRecord")
            self.assertEqual(nb_records_after - nb_records_before, 3)

    def test_unknown_kind(self):
        with self.admin_access.repo_cnx() as cnx:
            testutils.eac_import(cnx, self.datapath("custom_kind.xml"))
            self.assertRaises(
                NoResultError, cnx.find("AgentKind", name="a custom kind").one
            )
            self.assertEqual(
                cnx.find("AuthorityRecord").one().agent_kind[0].name,
                "unknown-agent-kind",
            )

    def test_no_name_entry(self):
        with self.admin_access.repo_cnx() as cnx:
            with self.assertRaises(dataimport.MissingTag) as cm:
                testutils.eac_import(cnx, self.datapath("no_name_entry.xml"))
            self.assertEqual(cm.exception.tag, "nameEntry")
            self.assertEqual(cm.exception.tag_parent, "identity")

    def test_no_name_entry_part(self):
        with self.admin_access.repo_cnx() as cnx:
            with self.assertRaises(dataimport.MissingTag) as cm:
                testutils.eac_import(cnx, self.datapath("no_name_entry_part.xml"))
            self.assertEqual(cm.exception.tag, "part")
            self.assertEqual(cm.exception.tag_parent, "nameEntry")


if __name__ == "__main__":
    unittest.main()
