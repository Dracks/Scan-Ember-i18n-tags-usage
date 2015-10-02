import unittest
import gen_locales
import StringIO
import json

class JsonOutputTests(unittest.TestCase):
    def test_save_without_base(self):
        file_output=StringIO.StringIO()
        output=gen_locales.JsonOutput(file_output)
        d={
            "hello": "world",
            "pingpong": {
                "ping": "pong",
                "number": 1
            }
        }
        output.save(d)
        self.assertEquals(json.loads(file_output.getvalue()), d)
        
    def test_save(self):
        file_output = StringIO.StringIO()
        output = gen_locales.JsonOutput(file_output, {
            "hello": "Muerte!",
            "pingpong": {
                "ping": "otra"
            }
        })
        d={
            "hello": "world",
            "pingpong": {
                "ping": "pong",
                "number": 1
            }
        };
        output.save(d)
        d['hello']="Muerte!"
        d['pingpong']["ping"]="otra"
        self.assertEquals(json.loads(file_output.getvalue()), d)
         


if __name__=='__main__':
    unittest.main()