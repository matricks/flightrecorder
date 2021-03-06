import os.path
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flightrecorder.waypoint import Waypoint
import flightrecorder.waypoint as waypoint


class TestWaypointSet(unittest.TestCase):

    def test_compegps(self):
        lines = [
            'G  WGS 84',
            'U  1',
            'W  Punto_7 A 36.7545386335\xc2N 5.3576058812\xc2W 27-MAR-62 00:00:00 762.000000',
            'w Crossed Square,0,-1.0,16777215,255,1,7,,0.0,']
        ws = waypoint.load(StringIO('\n'.join(lines)))
        self.assertEqual(len(ws), 1)
        w = ws[0]
        self.assertEqual(w.id, 'Punto_7')
        self.assertEqual(w.name, '')
        self.assertAlmostEqual(w.lon, -5.3576058812)
        self.assertAlmostEqual(w.lat, 36.7545386335)
        self.assertEqual(w.alt, 762.0)
        self.assertEqual(w.color, '#ff0000')
        self.assertEqual(w.radius, 0.0)

    def test_compegps_roundtrip(self):
        w = Waypoint('B01100', 45.0, 5.0, 1000)
        s = StringIO()
        waypoint.dump([w], s, format='compegps')
        v = waypoint.load(StringIO(s.getvalue().decode('iso-8859-1')))[0]
        self.assertEqual(w.id, v.id)
        self.assertEqual(w.name, v.name)
        self.assertAlmostEqual(w.lat, v.lat)
        self.assertAlmostEqual(w.lon, v.lon)
        self.assertAlmostEqual(w.alt, v.alt)

    def test_formatgeo(self):
        lines = [
            '$FormatGEO',
            'A01095    N 42 42 46.98    W 006 26 10.68   954  A01095']
        ws = waypoint.load(StringIO('\n'.join(lines)))
        self.assertEqual(len(ws), 1)
        w = ws[0]
        self.assertEqual(w.id, 'A01')
        self.assertEqual(w.name, '')
        self.assertAlmostEqual(w.lat, 42.7130500)
        self.assertAlmostEqual(w.lon, -6.4363000)
        self.assertEqual(w.alt, 954.0)
        self.assertEqual(w.color, None)
        self.assertEqual(w.radius, None)

    def test_formatgeo_roundtrip(self):
        w = Waypoint('B01100', 45.0, 5.0, 1000)
        s = StringIO()
        waypoint.dump([w], s, format='formatgeo')
        v = waypoint.load(StringIO(s.getvalue()))[0]
        self.assertEqual(w.id, v.id)
        self.assertEqual(w.name, v.name)
        self.assertAlmostEqual(w.lat, v.lat)
        self.assertAlmostEqual(w.lon, v.lon)
        self.assertAlmostEqual(w.alt, v.alt)

    def test_seeyou(self):
        lines = [
            'Title,Code,Country,Latitude,Longitude,Elevation,Style,Direction,Length,Frequency,Description',
            '"T01",T01068,,4606.633N,01343.667E,680.0m,1,,,,']
        ws = waypoint.load(StringIO('\n'.join(lines)))
        self.assertEqual(len(ws), 1)
        w = ws[0]
        self.assertEqual(w.id, 'T01')
        self.assertEqual(w.name, '')
        self.assertAlmostEqual(w.lat, 46.1105500)
        self.assertAlmostEqual(w.lon, 13.7277833)
        self.assertEqual(w.alt, 680.0)
        self.assertEqual(w.color, None)
        self.assertEqual(w.radius, None)

    def test_seeyou_roundtrip(self):
        w = Waypoint('B01100', 45.0, 5.0, 1000)
        s = StringIO()
        waypoint.dump([w], s, format='seeyou')
        v = waypoint.load(StringIO(s.getvalue()))[0]
        self.assertEqual(w.id, v.id)
        self.assertEqual(w.name, v.name)
        self.assertAlmostEqual(w.lat, v.lat)
        self.assertAlmostEqual(w.lon, v.lon)
        self.assertAlmostEqual(w.alt, v.alt)

    def test_oziexplorer(self):
        lines = [
            'OziExplorer Waypoint File Version 1.0',
            'WGS 84',
            'Reserved 2',
            'Reserved 3',
            '   1,A01062        ,  46.131761,   6.522414,36674.82502, 0, 1, 3, 0, 65535,ATTERO MIEUSSY                          , 0, 0, 0 , 2027',
            ' 185,TMA607 ,  47.900000,   6.416667,37404.69450,  0, 1, 3, 0, 16711680,BALE TMA6  NO    , 0, 0, 0, -777, 6, 0,17']
        ws = waypoint.load(StringIO('\n'.join(lines)))
        self.assertEqual(len(ws), 2)
        w = ws[0]
        self.assertEqual(w.id, 'A01')
        self.assertEqual(w.name, 'ATTERO MIEUSSY')
        self.assertAlmostEqual(w.lat, 46.131761)
        self.assertAlmostEqual(w.lon, 6.522414)
        self.assertEqual(w.alt, 0.3048 * 2027)
        self.assertEqual(w.color, '#ffff00')
        self.assertEqual(w.radius, None)
        w = ws[1]
        self.assertEqual(w.id, 'TMA607')
        self.assertEqual(w.name, 'BALE TMA6  NO')
        self.assertAlmostEqual(w.lat, 47.900000)
        self.assertAlmostEqual(w.lon, 6.416667)
        self.assertEqual(w.alt, None)
        self.assertEqual(w.color, '#0000ff')
        self.assertEqual(w.radius, None)

    def test_oziexplorer_roundtrip(self):
        w = Waypoint('B01100', 45.0, 5.0, 1000)
        s = StringIO()
        waypoint.dump([w], s, format='oziexplorer')
        v = waypoint.load(StringIO(s.getvalue()))[0]
        self.assertEqual(w.id, v.id)
        self.assertEqual(w.name, v.name)
        self.assertAlmostEqual(w.lat, v.lat)
        self.assertAlmostEqual(w.lon, v.lon)
        self.assertAlmostEqual(w.alt, v.alt)


if __name__ == '__main__':
    unittest.main()
