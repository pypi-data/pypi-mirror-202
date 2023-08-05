import re
import unittest
from datetime import datetime

from codicefiscale import codicefiscale
from codicefiscale.metadata import (
    __author__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
)


class CodiceFiscaleTestCase(unittest.TestCase):
    def test_encode_lastname(self):
        data = [
            {
                "input": "",
                "result": "XXX",
            },
            {
                "input": "Caccamo",
                "result": "CCC",
            },
            {
                "input": "Fò",
                "result": "FOX",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(codicefiscale.encode_lastname(obj["input"]), obj["result"])

    def test_encode_firstname(self):
        data = [
            {
                "input": "",
                "result": "XXX",
            },
            {
                "input": "Alessandro",
                "result": "LSN",
            },
            {
                "input": "Dario",
                "result": "DRA",
            },
            {
                "input": "Fabio",
                "result": "FBA",
            },
            {
                "input": "Giovanni",
                "result": "GNN",
            },
            {
                "input": "Hu",
                "result": "HUX",
            },
            {
                "input": "Maria",
                "result": "MRA",
            },
            {
                "input": "Michele",
                "result": "MHL",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_firstname(obj["input"]), obj["result"]
            )

    def test_encode_birthdate_formats(self):
        data = [
            {
                "input": datetime(1985, 4, 3),
                "result": "85D03",
            },
            {
                "input": "03 04 1985",
                "result": "85D03",
            },
            {
                "input": "03/04/1985",
                "result": "85D03",
            },
            {
                "input": "03-04-1985",
                "result": "85D03",
            },
            {
                "input": "03.04.1985",
                "result": "85D03",
            },
            {
                "input": "3/4/1985",
                "result": "85D03",
            },
            {
                "input": "3-4-1985",
                "result": "85D03",
            },
            {
                "input": "3.4.1985",
                "result": "85D03",
            },
            {
                "input": "1985 04 03",
                "result": "85D03",
            },
            {
                "input": "1985/04/03",
                "result": "85D03",
            },
            {
                "input": "1985-04-03",
                "result": "85D03",
            },
            {
                "input": "1985.04.03",
                "result": "85D03",
            },
            {
                "input": "1985/4/3",
                "result": "85D03",
            },
            {
                "input": "1985-4-3",
                "result": "85D03",
            },
            {
                "input": "1985.4.3",
                "result": "85D03",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthdate(obj["input"], "M"), obj["result"]
            )

    def test_encode_birthdate_invalid_arguments(self):
        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate(None, "M")

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate("03/04/1985", None)

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate("03/04/1985", "X")

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthdate("1985/1985/1985", "M")

    def test_encode_birthdate_gender(self):
        data = [
            {
                "input": ["03/04/1985", "M"],
                "result": "85D03",
            },
            {
                "input": ["03/04/1985", "F"],
                "result": "85D43",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthdate(*obj["input"]), obj["result"]
            )

    def test_encode_birthplace_italy(self):
        data = [
            {
                "input": "Torino, Italy",
                "result": "L219",
            },
            {
                "input": "Torino (TO), Italy",
                "result": "L219",
            },
            {
                "input": "Torino (TO)",
                "result": "L219",
            },
            {
                "input": "Torino",
                "result": "L219",
            },
            {
                "input": "L219",
                "result": "L219",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthplace(obj["input"]), obj["result"]
            )

    def test_encode_birthplace_foreign_country(self):
        data = [
            {
                "input": "Lettonia",
                "result": "Z145",
            },
            {
                "input": "Giappone",
                "result": "Z219",
            },
            {
                "input": "Marocco",
                "result": "Z330",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(
                codicefiscale.encode_birthplace(obj["input"]), obj["result"]
            )

    def test_encode_birthplace_invalid_arguments(self):
        with self.assertRaises(ValueError):
            codicefiscale.encode_birthplace(None)

        with self.assertRaises(ValueError):
            codicefiscale.encode_birthplace("Area 51")

    def test_encode_birthplace_invalid_birthdate(self):
        with self.assertRaises(ValueError):
            codicefiscale.encode_birthplace("Torino", "01/01/1888")

    def test_encode_cin(self):
        data = [
            {
                "input": "CCCFBA85D03L219",
                "result": "P",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            self.assertEqual(codicefiscale.encode_cin(obj["input"]), obj["result"])

    def test_encode_cin_invalid_arguments(self):
        with self.assertRaises(ValueError):
            codicefiscale.encode_cin(None)

        with self.assertRaises(ValueError):
            codicefiscale.encode_cin("CCCFBA85D03")

    def test_encode(self):
        data = [
            {
                "input": {
                    "lastname": "Ait Hadda",
                    "firstname": "Saad",
                    "gender": "M",
                    "birthdate": "08/09/1995",
                    "birthplace": "Marocco",
                },
                "result": "THDSDA95P08Z330H",
            },
            {
                "input": {
                    "lastname": "Belousovs",
                    "firstname": "Olegs",
                    "gender": "M",
                    "birthdate": "22/03/1984",
                    "birthplace": "Lettonia",
                },
                "result": "BLSLGS84C22Z145O",
            },
            {
                "input": {
                    "lastname": "Bruno",
                    "firstname": "Giovanni",
                    "gender": "M",
                    "birthdate": "26/02/1971",
                    "birthplace": "Torino",
                },
                "result": "BRNGNN71B26L219T",
            },
            {
                "input": {
                    "lastname": "Caccamo",
                    "firstname": "Fabio",
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
                "result": "CCCFBA85D03L219P",
            },
            {
                "input": {
                    "lastname": "Gomba",
                    "firstname": "Alessandro",
                    "gender": "M",
                    "birthdate": "05/01/1984",
                    "birthplace": "Pinerolo",
                },
                "result": "GMBLSN84A05G674H",
            },
            {
                "input": {
                    "lastname": "Martini",
                    "firstname": "Maria",
                    "gender": "F",
                    "birthdate": "16/12/1983",
                    "birthplace": "Anagni",
                },
                "result": "MRTMRA83T56A269B",
            },
            {
                "input": {
                    "lastname": "Panella",
                    "firstname": "Michele",
                    "gender": "M",
                    "birthdate": "27/10/1979",
                    "birthplace": "San Severo (FG)",
                },
                "result": "PNLMHL79R27I158P",
            },
            {
                "input": {
                    "lastname": "Quatrini",
                    "firstname": "Dario",
                    "gender": "M",
                    "birthdate": "13/09/1971",
                    "birthplace": "Pavia",
                },
                "result": "QTRDRA71P13G388J",
            },
            {
                "input": {
                    "lastname": "Takakura",
                    "firstname": "Yuuki",
                    "gender": "F",
                    "birthdate": "28/02/1987",
                    "birthplace": "Torino",
                },
                "result": "TKKYKU87B68L219F",
            },
            {
                "input": {
                    "lastname": "Rossi",
                    "firstname": "Mario",
                    "gender": "M",
                    "birthdate": "17/02/1950",
                    "birthplace": "Porretta Terme",
                },
                "result": "RSSMRA50B17A558W",
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            code = codicefiscale.encode(**obj["input"])
            self.assertEqual(code, obj["result"])

    def test_decode(self):
        data = [
            {
                "input": "THDSDA95P08Z330H",
                "result": {
                    "gender": "M",
                    "birthdate": "08/09/1995",
                    "birthplace": "Marocco",
                },
            },
            {
                "input": "BLSLGS84C22Z145O",
                "result": {
                    "gender": "M",
                    "birthdate": "22/03/1984",
                    "birthplace": "Lettonia",
                },
            },
            {
                "input": "BRNGNN71B26L219T",
                "result": {
                    "gender": "M",
                    "birthdate": "26/02/1971",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA85D03L219P",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "GMBLSN84A05G674H",
                "result": {
                    "gender": "M",
                    "birthdate": "05/01/1984",
                    "birthplace": "Pinerolo",
                },
            },
            {
                "input": "MRTMRA83T56A269B",
                "result": {
                    "gender": "F",
                    "birthdate": "16/12/1983",
                    "birthplace": "Anagni",
                },
            },
            {
                "input": "PNLMHL79R27I158P",
                "result": {
                    "gender": "M",
                    "birthdate": "27/10/1979",
                    "birthplace": "San Severo",
                },
            },
            {
                "input": "QTRDRA71P13G388J",
                "result": {
                    "gender": "M",
                    "birthdate": "13/09/1971",
                    "birthplace": "Pavia",
                },
            },
            {
                "input": "TKKYKU87B68L219F",
                "result": {
                    "gender": "F",
                    "birthdate": "28/02/1987",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "RSSMRA68A01H501Y",
                "result": {
                    "gender": "M",
                    "birthdate": "01/01/1968",
                    "birthplace": "Roma",
                },
            },
            {
                "input": "RSSMRA50B17A558W",
                "result": {
                    "gender": "M",
                    "birthdate": "17/02/1950",
                    "birthplace": "Porretta Terme",
                },
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):
            result = obj["result"]
            obj_decoded = codicefiscale.decode(obj["input"])
            #  print(obj_decoded)
            gender = obj_decoded.get("gender")
            self.assertFalse(gender is None)
            self.assertEqual(gender, result["gender"])

            birthdate = obj_decoded.get("birthdate")
            self.assertFalse(birthdate is None)
            self.assertEqual(
                birthdate, datetime.strptime(result["birthdate"], "%d/%m/%Y")
            )

            birthplace = obj_decoded.get("birthplace")
            self.assertFalse(birthplace is None)
            self.assertEqual(birthplace["name"].upper(), result["birthplace"].upper())

    def test_decode_invalid_syntax(self):
        # invalid lastname
        with self.assertRaises(ValueError):
            codicefiscale.decode("CC0FBA85X03L219P")

        # invalid firstname
        with self.assertRaises(ValueError):
            codicefiscale.decode("CCCFB085X03L219P")

        # invalid date-year
        with self.assertRaises(ValueError):
            codicefiscale.decode("CCCFBA8XD03L219S")

        # invalid date-month
        with self.assertRaises(ValueError):
            codicefiscale.decode("CCCFBA85X03L219P")

        # invalid date-day
        with self.assertRaises(ValueError):
            codicefiscale.decode("CCCFBA85D00L219P")

    def test_decode_omocodia(self):
        data = [
            {
                "input": "CCCFBA85D03L219P",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA85D03L21VE",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA85D03L2MVP",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA85D03LNMVE",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA85D0PLNMVA",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA85DLPLNMVL",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBA8RDLPLNMVX",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
            {
                "input": "CCCFBAURDLPLNMVU",
                "result": {
                    "gender": "M",
                    "birthdate": "03/04/1985",
                    "birthplace": "Torino",
                },
            },
        ]

        for obj in data:
            # with self.subTest(obj=obj):

            code = obj["input"]
            result = obj["result"]
            obj_decoded = codicefiscale.decode(code)

            gender = obj_decoded.get("gender")
            self.assertFalse(gender is None)
            self.assertEqual(gender, result["gender"])

            birthdate = obj_decoded.get("birthdate")
            self.assertFalse(birthdate is None)
            self.assertEqual(
                birthdate, datetime.strptime(result["birthdate"], "%d/%m/%Y")
            )

            birthplace = obj_decoded.get("birthplace")
            self.assertFalse(birthplace is None)
            self.assertEqual(birthplace["name"].upper(), result["birthplace"].upper())

            omocodes = obj_decoded.get("omocodes", [])
            self.assertEqual(128, len(omocodes))

    def test_decode_omocodes(self):
        code = "CCCFBA85D03L219P"
        decoded = codicefiscale.decode(code)
        expected_omocodes = [
            "CCCFBA85D03L219P",
            "CCCFBA85D03L21VE",
            "CCCFBA85D03L2M9A",
            "CCCFBA85D03LN19E",
            "CCCFBA85D0PL219L",
            "CCCFBA85DL3L219A",
            "CCCFBA8RD03L219B",
            "CCCFBAU5D03L219M",
            "CCCFBA85D03L2MVP",
            "CCCFBA85D03LN1VT",
            "CCCFBA85D0PL21VA",
            "CCCFBA85DL3L21VP",
            "CCCFBA8RD03L21VQ",
            "CCCFBAU5D03L21VB",
            "CCCFBA85D03LNM9P",
            "CCCFBA85D0PL2M9W",
            "CCCFBA85DL3L2M9L",
            "CCCFBA8RD03L2M9M",
            "CCCFBAU5D03L2M9X",
            "CCCFBA85D0PLN19A",
            "CCCFBA85DL3LN19P",
            "CCCFBA8RD03LN19Q",
            "CCCFBAU5D03LN19B",
            "CCCFBA85DLPL219W",
            "CCCFBA8RD0PL219X",
            "CCCFBAU5D0PL219I",
            "CCCFBA8RDL3L219M",
            "CCCFBAU5DL3L219X",
            "CCCFBAURD03L219Y",
            "CCCFBA85D03LNMVE",
            "CCCFBA85D0PL2MVL",
            "CCCFBA85DL3L2MVA",
            "CCCFBA8RD03L2MVB",
            "CCCFBAU5D03L2MVM",
            "CCCFBA85D0PLN1VP",
            "CCCFBA85DL3LN1VE",
            "CCCFBA8RD03LN1VF",
            "CCCFBAU5D03LN1VQ",
            "CCCFBA85DLPL21VL",
            "CCCFBA8RD0PL21VM",
            "CCCFBAU5D0PL21VX",
            "CCCFBA8RDL3L21VB",
            "CCCFBAU5DL3L21VM",
            "CCCFBAURD03L21VN",
            "CCCFBA85D0PLNM9L",
            "CCCFBA85DL3LNM9A",
            "CCCFBA8RD03LNM9B",
            "CCCFBAU5D03LNM9M",
            "CCCFBA85DLPL2M9H",
            "CCCFBA8RD0PL2M9I",
            "CCCFBAU5D0PL2M9T",
            "CCCFBA8RDL3L2M9X",
            "CCCFBAU5DL3L2M9I",
            "CCCFBAURD03L2M9J",
            "CCCFBA85DLPLN19L",
            "CCCFBA8RD0PLN19M",
            "CCCFBAU5D0PLN19X",
            "CCCFBA8RDL3LN19B",
            "CCCFBAU5DL3LN19M",
            "CCCFBAURD03LN19N",
            "CCCFBA8RDLPL219I",
            "CCCFBAU5DLPL219T",
            "CCCFBAURD0PL219U",
            "CCCFBAURDL3L219J",
            "CCCFBA85D0PLNMVA",
            "CCCFBA85DL3LNMVP",
            "CCCFBA8RD03LNMVQ",
            "CCCFBAU5D03LNMVB",
            "CCCFBA85DLPL2MVW",
            "CCCFBA8RD0PL2MVX",
            "CCCFBAU5D0PL2MVI",
            "CCCFBA8RDL3L2MVM",
            "CCCFBAU5DL3L2MVX",
            "CCCFBAURD03L2MVY",
            "CCCFBA85DLPLN1VA",
            "CCCFBA8RD0PLN1VB",
            "CCCFBAU5D0PLN1VM",
            "CCCFBA8RDL3LN1VQ",
            "CCCFBAU5DL3LN1VB",
            "CCCFBAURD03LN1VC",
            "CCCFBA8RDLPL21VX",
            "CCCFBAU5DLPL21VI",
            "CCCFBAURD0PL21VJ",
            "CCCFBAURDL3L21VY",
            "CCCFBA85DLPLNM9W",
            "CCCFBA8RD0PLNM9X",
            "CCCFBAU5D0PLNM9I",
            "CCCFBA8RDL3LNM9M",
            "CCCFBAU5DL3LNM9X",
            "CCCFBAURD03LNM9Y",
            "CCCFBA8RDLPL2M9T",
            "CCCFBAU5DLPL2M9E",
            "CCCFBAURD0PL2M9F",
            "CCCFBAURDL3L2M9U",
            "CCCFBA8RDLPLN19X",
            "CCCFBAU5DLPLN19I",
            "CCCFBAURD0PLN19J",
            "CCCFBAURDL3LN19Y",
            "CCCFBAURDLPL219F",
            "CCCFBA85DLPLNMVL",
            "CCCFBA8RD0PLNMVM",
            "CCCFBAU5D0PLNMVX",
            "CCCFBA8RDL3LNMVB",
            "CCCFBAU5DL3LNMVM",
            "CCCFBAURD03LNMVN",
            "CCCFBA8RDLPL2MVI",
            "CCCFBAU5DLPL2MVT",
            "CCCFBAURD0PL2MVU",
            "CCCFBAURDL3L2MVJ",
            "CCCFBA8RDLPLN1VM",
            "CCCFBAU5DLPLN1VX",
            "CCCFBAURD0PLN1VY",
            "CCCFBAURDL3LN1VN",
            "CCCFBAURDLPL21VU",
            "CCCFBA8RDLPLNM9I",
            "CCCFBAU5DLPLNM9T",
            "CCCFBAURD0PLNM9U",
            "CCCFBAURDL3LNM9J",
            "CCCFBAURDLPL2M9Q",
            "CCCFBAURDLPLN19U",
            "CCCFBA8RDLPLNMVX",
            "CCCFBAU5DLPLNMVI",
            "CCCFBAURD0PLNMVJ",
            "CCCFBAURDL3LNMVY",
            "CCCFBAURDLPL2MVF",
            "CCCFBAURDLPLN1VJ",
            "CCCFBAURDLPLNM9F",
            "CCCFBAURDLPLNMVU",
        ]
        self.assertEqual(len(decoded["omocodes"]), 128)
        self.assertEqual(decoded["omocodes"], expected_omocodes)

    def test_decode_with_invalid_birthplace(self):
        code = "FRTMXM74L15D354A"
        valid = codicefiscale.is_valid(code)
        self.assertFalse(valid)

    def test_is_omocode(self):
        self.assertFalse(codicefiscale.is_omocode("CCCFBA85D03L219P"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBA85D03L21VE"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBA85D03L2MVP"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBA85D03LNMVE"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBA85D0PLNMVA"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBA85DLPLNMVL"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBA8RDLPLNMVX"))
        self.assertTrue(codicefiscale.is_omocode("CCCFBAURDLPLNMVU"))

    def test_is_valid(self):
        self.assertTrue(codicefiscale.is_valid("CCCFBA85D03L219P"))
        self.assertTrue(codicefiscale.is_valid("CCC FBA 85 D03 L219 P"))
        self.assertTrue(codicefiscale.is_valid("CCC-FBA-85-D03-L219-P"))

        self.assertFalse(codicefiscale.is_valid("CCCFBA85D03L219PP"))  # too long
        self.assertFalse(codicefiscale.is_valid("CCCFBA85D03L219B"))  # wrong CIN
        self.assertFalse(codicefiscale.is_valid("CCCFBA85D03L219"))  # too short
        self.assertFalse(
            codicefiscale.is_valid("CCCFBA85D00L219")
        )  # wrong birthdate day
        self.assertFalse(
            codicefiscale.is_valid("CCCFBA85D99L219")
        )  # wrong birthdate day

    def test_metadata(self):
        self.assertTrue(
            all(
                [
                    __author__,
                    __copyright__,
                    __description__,
                    __license__,
                    __title__,
                    __version__,
                ]
            )
        )

    def test_version(self):
        version_pattern = re.compile(r"^(([\d]+)\.([\d]+)\.([\d]+))$")
        self.assertTrue(version_pattern.match(__version__))
